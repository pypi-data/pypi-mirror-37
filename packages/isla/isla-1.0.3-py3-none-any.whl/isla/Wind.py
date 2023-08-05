import numpy as np
from scipy.stats import weibull_min
from scipy.interpolate import InterpolatedUnivariateSpline

from .FixedComponent import FixedComponent

# ignore numpy errors
np.seterr(divide='ignore', invalid='ignore')


class Wind(FixedComponent):
    """Wind power plant module.

    Parameters
    ----------
    data : dict
        Dataset. Pass a dict with 'wd_spd' as the key for the wind speed [m/s]
        and 'wd_dir' for the wind direction [deg] (optional). A tracker will
        be assumed to be present if no wind direction data is present. If only
        an ndarray is given, it will be assumed to be the the wind speed.
    dir : float
        Direction faced by the wind turbine [deg]. Set to 'auto' if the
        turbine has a tracker.
    z_anem : float
        Anemometer height [m] for dataset.
    capex : float or callable
        Capital expenses [USD/kW]. Depends on size. Can be a callable
        function that returns capital cost starting from year zero to end of
        project lifetime.
    opex_fix : float or callable
        Fixed yearly operating expenses [USD/kW-yr]. Depends on size. Can be
        a callable function that returns the fixed operating cost starting
        from year zero to end of project lifetime.
    opex_var : float or callable
        Variable yearly operating expenses [USD/kWh-yr]. Depends on energy
        produced. Can be a callable function that returns the variable
        operating cost starting from year zero to end of project lifetime.
    life : float
        Maximum life [yr] before the component is replaced.

    Other Parameters
    ----------------
    repex : float
        Replacement costs [USD/kW]. Depends on size. Equal to CapEx by
        default.
    fail_prob : float
        Probability of failure of the component.
    name_solid : str
        Label for the power output. This will be used in generated graphs and
        files.
    color_solid : str
        Hex code (e.g. '#33CC33') of the color for the power output. This will
        be used in generated graphs.
    num_case : int
        Number of scenarios to simultaneously simulate. This is set by the
        Control module.
    size : int
        Size of the component [kW]. This is set by the Control module.
    z_hub : float
        Hub height [m].
    z_rough : float
        Surface roughness [m]. Depends on terrain.
    pow_x : ndarray
        The wind speed [m/s] in a set of power output [kW] vs wind speed [m/s]
        data.
    pow_y : ndarray
        The power output [kW] in a set of power output [kW] vs wind speed [m/s]
        data.
    stat_data : dict, str, or None
        Statistical data used for load variance. Set to None to remove load
        variability. Set to 'auto' to automatically make noise based on
        dataset. Pass a dict with 'beta' as key and beta parameter for a
        Weibull distribution as values to manually adjust noise.

    References
    ----------
    ..[1] Ozbay, A. et. al., "Interference of wind turbines with different
        yaw angles of the upstream wind turbine," 42nd AIAA Fluid Dynamics\
        Conference and Exhibit, 2012.

    """

    def __init__(
        self, data, dir='auto', z_anem=10.0, capex=2000.0,
        opex_fix=20.0, opex_var=0.0, life=20.0, **kwargs
    ):
        """Initializes the base class."""

        # base class parameters
        settings = {
            'name_solid': 'Wind',  # label for power output
            'color_solid': '#66CCFF',  # color for power output in powerflow
            'capex': capex,  # CapEx [USD/kW]
            'opex_fix': opex_fix,  # size-dependent OpEx [USD/kW-yr]
            'opex_var': opex_var,  # output-dependent OpEx [USD/kWh-yr]
            'life': life,  # maximum life [yr]
            'data': data,  # dataset
            'is_re': True  # renewable
        }
        settings.update(kwargs)  # replace default settings with input settings

        # initialize base class
        super().__init__(**settings)

        # extract dataset
        if isinstance(self.data, dict):  # pass dict
            self.wd_spd = self.data['wd_spd']  # wind speed [m/s]
            self.wd_dir = self.data.pop('wd_dir', None)  # wind dir [deg]
        elif isinstance(self.data, np.ndarray):  # pass ndarray
            self.wd_spd = self.data
            self.wd_dir = None

        # convert dataset to 1D array
        self.wd_spd = np.ravel(self.wd_spd)
        if self.wd_dir is not None:
            self.wd_dir = np.ravel(self.wd_dir)

        # initialize wind plant parameters
        self.pow_unit = np.array([])

        # adjustable wind plant parameters
        self.dir = dir  # direction of plant [deg]
        self.z_anem = z_anem  # anemometer height [m]
        self.z_hub = kwargs.pop('z_hub', 80)  # hub height [m]
        self.z_rough = kwargs.pop('z_rough', 0.0005)  # surface roughness [m]
        self.pow_x = kwargs.pop('pow_x', np.arange(4, 25))  # wind speed [m/s]
        self.pow_y = kwargs.pop(  # corresponding power [kW]
            'pow_y',
            np.array([
                66.3, 152, 280, 457, 690, 978,
                1296, 1598, 1818, 1935, 1980,
                1995, 1999, 2000, 2000, 2000,
                2000, 2000, 2000, 2000, 2000
            ])
        )

        # derivable wind plant parameters
        self.pow_func = InterpolatedUnivariateSpline(
            self.pow_x, self.pow_y, k=1, ext='zeros'  # pow vs speed
        )

        # adjustable reliability parameters
        self.stat_data = kwargs.pop('stat_data', None)

        # initalize reliability parameters
        self.stat_beta = 0.0

        # update initialized parameters if essential data is complete
        self._update_config()

    def get_pow(self, hr):
        """Returns the power output [kW] at the specified time [h].

        Parameters
        ----------
        hr : int
            Time [h] in the simulation.

        """
        # check if noise has to be simulated
        if self.stat_data is None:
            noise = 1
        elif self.stat_data == 'auto':
            noise = np.random.weibull(
                self.stat_beta[hr % 24], self.num_case
            )
        else:
            noise = np.random.weibull(
                self.stat_beta, self.num_case
            )

        # calculate PV power [kW] for timestep
        self.pow = self.size*self.pow_unit[hr]*np.ones(self.num_case)*noise

        # add to total energy [kWh]
        self.enr_tot += self.pow

        # get power [kW] at timestep
        return self.pow

    def cost_calc(self, yr_proj, infl):
        """Calculates the cost of the component.

        Parameters
        ----------
        yr_proj : float
            Project lifetime [yr].
        infl : float
            Inflation rate.

        """
        def ann_func(i):
            """Annunity factor"""
            return 1/(1+infl)**i

        # capital costs [USD], size [kW] based
        if callable(self.capex):  # if experience curve is given
            self.cost_c = np.atleast_1d(self.capex(0)*self.size)
        else:  # if fixed value is given
            self.cost_c = self.capex*self.size

        # fixed operating costs [USD], size [kW] based
        if callable(self.opex_fix):
            opex_fix = self.size*np.sum(
                self.opex_fix(i)*ann_func(i)
                for i in np.arange(1, yr_proj+1)
            )
        else:
            opex_fix = self.opex_fix*self.size*np.sum(
               1/(1+infl)**np.arange(1, yr_proj+1)
            )

        # variable operating costs [USD], output [kWh] based
        if callable(self.opex_var):
            opex_var = self.enr_tot*np.sum(
                self.opex_var(i)*ann_func(i)
                for i in np.arange(1, yr_proj+1)
            )
        else:
            opex_var = self.opex_var*self.enr_tot*np.sum(
               1/(1+infl)**np.arange(1, yr_proj+1)
            )

        # total operating costs [USD]
        self.cost_o = opex_fix+opex_var

        # calculate replacement frequency [yr]
        rep_freq = self.life*np.ones(self.num_case)  # replace due to max life

        # replace nan's in rep_freq to prevent errors with arange
        rep_freq[np.isnan(rep_freq)] = yr_proj+1  # no replacement

        # replacement costs [USD], size [kW] based
        if callable(self.repex):
            repex = np.zeros(self.num_case)  # initialize replacement costs
            for i in range(0, self.num_case):
                repex[i] = np.sum(  # output [kWh] based
                    self.repex(j)*ann_func(j)
                    for j in np.arange(0, yr_proj, rep_freq[i])
                )-self.repex(0)*ann_func(0)  # no replacement at time zero
        else:
            disc_rep = np.zeros(self.num_case)  # initialize sum of ann factors
            for i in range(0, self.num_case):
                disc_rep[i] = np.sum(
                    1/(1+infl) **
                    np.arange(0, yr_proj, rep_freq[i])[1:]  # remove yr 0
                )
            repex = disc_rep*self.repex
        self.cost_r = self.size*repex

        # total cost [USD]
        self.cost = self.cost_c+self.cost_o+self.cost_r

    def _config(self):
        """Updates other parameters once essential parameters are complete."""

        # adjust wind speed [m/s] for altitude
        spd_adj = (
            self.wd_spd *
            np.log(self.z_hub/self.z_rough) /
            np.log(self.z_anem/self.z_rough)
        )

        # check if direction effects are included
        dir_fc = 1  # direction factor
        if not (self.wd_dir is None or self.dir == 'auto'):

            # power proportional to cos(difference)^3
            dir_fc = np.abs(np.cos(np.deg2rad(
                self.wd_dir-self.dir
            ))**3)

        # calculate power output [kW] per unit size
        self.pow_unit = self.pow_func(spd_adj)*dir_fc/np.max(self.pow_y)

        # update reliability parameters
        if isinstance(self.stat_data, dict):
            self.stat_beta = self.stat_data['beta']
        elif self.stat_data == 'auto':
            self.stat_beta = self._stat_solve()

    @staticmethod
    def exp_curve(yr, yr_0=2016, **kwargs):
        """Experience curve for Solar PV.
        Returns the cost [USD/kW] at the given year

        Parameters
        ----------
        yr : int
            Index of the year.
        yr_0 : int
            Year where index is set to zero.

        """
        # get regression parameters
        a_sat = kwargs.pop('a_sat', 75)
        a_base = kwargs.pop('a_base', 1.5)
        r = kwargs.pop('r', 0.201)
        a = kwargs.pop('a', 96.22)
        b = kwargs.pop('b', 0.344)

        # calculate cost [USD/kWh]
        cap = a_sat/(1+(a_sat-a_base)/a_base*np.exp(-r*(yr+(yr_0-1990))))
        cost = a*cap**(-b)

        return cost

    def _stat_solve(self):
        """Solves for parameters for reliability calculations."""

        # solve for beta parameter in Weibull distribution
        beta_list = []  # list of beta parameters
        norm_arr = self.wd_spd/np.max(self.wd_spd)  # normalize
        for i in range(24):
            b_i, loc_i, scl_i = weibull_min.fit(norm_arr[i::24])  # beta
            beta_list.append(b_i)  # append variance

        return np.array(beta_list)
