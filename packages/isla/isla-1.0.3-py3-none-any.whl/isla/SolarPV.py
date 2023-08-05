import numpy as np
from scipy.stats import norm

from .FixedComponent import FixedComponent

# ignore numpy errors
np.seterr(divide='ignore', invalid='ignore')


class SolarPV(FixedComponent):
    """Photovoltaic (PV) solar plant module.

    Parameters
    ----------
    data : dict or ndarray
        Dataset. Pass a dict with 'ghi' as the key for the hourly GHI [kW/m^2]
        and 'temp' for the hourly ambient temperature [K] (optional).
        Temperature effects will be neglected if no temperature data is given.
        If only an ndarray is given, it will be assumed to be the the hourly
        GHI.
    lat : float
        Latitude [deg] of the location of the PV plant.
    track : int
        Indicates tracking. Set to '0' for no tracking (fixed axis) or '1' for
        horizontal axis tracking.
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
    repex : float or callable
        Replacement costs [USD/kW]. Depends on size. Equal to CapEx by
        default. Can be a callable function that returns replacement costs
        starting from year zero to end of project lifetime.
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
    infl : float
        Inflation rate. This is set by the Control module.
    rad_stc : float
        Radiance [kW/m^2] on the PV panel under standard test conditons (STC).
        Equal to 1 kW/m^2.
    derat : float
        Derating factor. Accounts for dust and other inefficiencies on the PV
        panels.
    temp_stc : float
        Temperature [K] at STC. Equal to 25 deg C.
    temp_cf : float
        Temperature coefficient of performance [/K].
    temp_noct : float
        Nominal operating cell temperature (NOCT) [K]. Equal to 47 deg C.
    temp_nocta : float
        Ambient temperature at NOCT [K]. Equal to 20 deg C.
    rad_noct : float
        Radiance [kW/m^2] at NOCT. Equal to 0.8 kW/m^2.
    mp_stc : float
        Maximum power point efficiency at STC.
    trabs : float
        Product of solar transmittance and solar absorptance.
    tol : float
        Tolerance.
    stat_data : dict, str, or None
        Statistical data used for load variance. Set to None to remove load
        variability. Set to 'auto' to automatically make noise based on
        dataset. Pass a dict with 'alpha' and 'beta' as keys and alpha and beta
        parameters respectively for a beta distribution as values to manually
        adjust noise.

    References
    ----------
    ..[1] Jager, K. et. al., "Solar energy: fundamentals, technology,
        systems," Delft University of Technology, 2014.
    ..[2] HOMER, "How HOMER calculates the PV cell temperature," n.d.

    """

    def __init__(
        self, data, lat, track=0, capex=1200.0, opex_fix=25.0,
        opex_var=0.0, life=20.0, **kwargs
    ):
        """Initializes the base class."""

        # base class parameters
        settings = {
            'name_solid': 'Solar',  # label for power output
            'color_solid': '#FFCC00',  # color for power output in powerflow
            'capex': capex,  # CapEx [USD/kW]
            'opex_fix': opex_fix,  # size-dependent OpEx [USD/kW-yr]
            'opex_var': opex_var,  # output-dependent OpEx [USD/kWh-yr]
            'life': life,  # maximum life [yr]
            'fail_prob': 0.0083,  # probability of failure
            'data': data,  # dataset
            'is_re': True  # renewable
        }
        settings.update(kwargs)  # replace default settings with input settings

        # initialize base class
        super().__init__(**settings)

        # extract dataset
        if isinstance(self.data, dict):  # pass dict
            self.ghi = self.data['ghi']  # GHI [kW/m^2]
            self.temp_amb = self.data.pop('temp', None)  # temp [K]
        elif isinstance(self.data, np.ndarray):  # pass ndarray
            self.ghi = self.data
            self.temp_amb = None

        # convert dataset to 1D array
        self.ghi = np.ravel(self.ghi)
        if self.temp_amb is not None:
            self.temp_amb = np.ravel(self.temp_amb)

        # adjustable PV plant parameters
        self.lat = lat
        self.track = track
        self.rad_stc = kwargs.pop('rad_stc', 1)
        self.derat = kwargs.pop('derat', 0.8)
        self.temp_stc = kwargs.pop('temp_stc', 298.15)
        self.temp_cf = kwargs.pop('temp_cf', -5e-3)
        self.temp_noct = kwargs.pop('temp_noct', 320.15)
        self.temp_nocta = kwargs.pop('temp_nocta', 293.15)
        self.rad_noct = kwargs.pop('rad_noct', 0.8)
        self.mp_stc = kwargs.pop('mp_stc', 0.13)
        self.trabs = kwargs.pop('trabs', 0.9)
        self.albedo = kwargs.pop('albedo', 0.07)
        self.tol = kwargs.pop('tol', 1e-5)

        # initialize PV plant parameters
        self.rad_tilt = np.array([])
        self.temp_cell = np.array([])
        self.pow_unit = np.array([])

        # adjustable reliability parameters
        self.stat_data = kwargs.pop('stat_data', None)

        # initalize reliability parameters
        self.stat_var = 0.0

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
            noise = 1+np.random.normal(
                0.0, self.stat_var[hr % 24], self.num_case
            )
        else:
            noise = 1+np.random.normal(
                0.0, self.stat_var, self.num_case
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
        rep_freq = self.life*np.ones(self.num_case)  # due to max life

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

    @staticmethod
    def exp_curve(yr, yr_0=2020, **kwargs):
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
        a_sat = kwargs.pop('a_sat', 200)
        a_base = kwargs.pop('a_base', 1)
        r = kwargs.pop('r', 0.328)
        a = kwargs.pop('a', 5282)
        b = kwargs.pop('b', 0.376)

        # calculate cost [USD/kWh]
        cap = a_sat/(1+(a_sat-a_base)/a_base*np.exp(-r*(yr+(yr_0-2004))))
        cost = a*cap**(-b)

        return cost

    def _config(self):
        """Updates other parameters once essential parameters are complete."""

        # calculate irradiance [kW/m^2] on tilted surface
        self._irrad_calc(self.ghi)

        # check if temperature effects are to be considered
        temp_fc = 1  # temperature factor
        if self.temp_amb is not None:  # use temp effects

            # calculate temperature [K] of PV cells
            self._temp_calc()

            # redefine temperature factor
            temp_fc = 1+self.temp_cf*(self.temp_cell-self.temp_stc)

        # calcualate power per kW size over a year
        self.pow_unit = self.derat*(self.rad_tilt/self.rad_stc)*temp_fc

        # update reliability parameters
        if isinstance(self.stat_data, dict):
            self.stat_var = self.stat_data['var']
        elif self.stat_data == 'auto':
            self.stat_var = self._stat_solve()

    def _irrad_calc(self, ghi):
        """Calculates the irradiation on a tilted surface.

        Parameters
        ----------
        ghi : ndarray
            Global horizontal irradiance [kW/m^2] on the PV plant.

        """
        # convert to radians
        lat = np.deg2rad(self.lat)

        # generate list of days
        days = np.repeat(np.arange(1, 366), 24)

        # calculate declination
        dec = np.deg2rad(23.45*np.sin(2*np.pi*(284+days)/365))

        # generate list of solar times
        sol_time = np.tile(np.arange(0, 24), 365)

        # generate hour angle
        hang = np.deg2rad(15*(sol_time-12))

        # determine PV slope
        if self.track == 1:
            slp = np.arctan(
                (
                    -np.sin(dec)*np.cos(lat) +
                    np.cos(dec)*np.sin(lat)*np.cos(hang)
                ) /
                (np.sin(dec)*np.sin(lat)+np.cos(dec)*np.cos(lat)*np.cos(hang))
            )
        else:
            slp = lat

        # calculate cosine of angle of incidence
        cos_inc = np.cos(np.arccos(
            np.sin(dec)*np.sin(lat)*np.cos(slp) -
            np.sin(dec)*np.cos(lat)*np.sin(slp) +
            np.cos(dec)*np.cos(lat)*np.cos(slp)*np.cos(hang) +
            np.cos(dec)*np.sin(lat)*np.sin(slp)*np.cos(hang) - self.tol
        ))

        # calculate zenith angle
        cos_zen = np.cos(lat)*np.cos(dec)*np.cos(hang)+np.sin(lat)*np.sin(dec)

        # calculate extraterrestrial radiation
        g_on = 1.367*(1+0.033*np.cos(2*np.pi*days/365))
        g_o = g_on*cos_zen

        # calculate average ET radiation
        hang_shift = np.append(hang[1:], hang[0])
        rad_et = 12/np.pi*g_on*(
            np.cos(lat)*np.cos(dec)*(np.sin(hang_shift)-np.sin(hang)) +
            (hang_shift-hang)*np.sin(lat)*np.sin(dec)
        )

        # clearness index
        k = self.ghi/rad_et

        # get ratio between diffuse and total GHI
        def diff_ratio(k):

            # classify as low, med, high
            low = k <= 0.22
            high = k > 0.8
            med = np.logical_not(np.logical_or(low, high))

            # calc diffusion ratio
            dr = (
                (1-0.09*k)*low +
                0.165*high +
                (0.9511-0.1604*k+4.388*k**2-16.638*k**3+12.336*k**4)*med
            )

            return dr

        # get diffuse and beam components
        rad_diff = self.ghi*diff_ratio(k)
        rad_beam = self.ghi-rad_diff

        # calculate ratio of beam on tilted to horizontal
        r = cos_inc/cos_zen

        # calculate anisotropy index
        a = rad_beam/rad_et

        # calculate cloudiness
        f = np.sqrt(rad_beam/self.ghi)

        # calculate irradiance on tilted surface
        rad_surf = (
            (rad_beam+rad_diff*a)*r +
            rad_diff*(1-a)*(1+np.cos(slp))/2*(1+f*np.sin(slp/2)**3) +
            self.ghi*self.albedo*(1-np.cos(slp))/2
        )

        # remove negative answers
        rad_surf[rad_surf < 0] = 0

        # convert nans to zero
        self.rad_tilt = np.nan_to_num(rad_surf)

    def _temp_calc(self):
        """Calculates the cell temperature [K]."""

        # calculate the cell temperature [K]
        a = (self.temp_noct-self.temp_nocta)*(self.rad_tilt/self.rad_noct)
        b = 1-self.mp_stc*(1-self.temp_cf*self.temp_stc)/self.trabs
        c = self.temp_cf*self.mp_stc/self.trabs

        # calculate cell temperature [K]
        self.temp_cell = (self.temp_amb+a*b)/(1+a*c)

    def _stat_solve(self):
        """Solves for parameters for reliability calculations."""

        # solve for variance between hours per day
        var_list = []  # list of variances
        norm_arr = self.ghi/np.max(self.ghi)  # normalize
        for i in range(24):
            loc_i, var_i = norm.fit(norm_arr[i::24])  # variance per hour
            var_list.append(var_i)  # append variance

        return np.array(var_list)
