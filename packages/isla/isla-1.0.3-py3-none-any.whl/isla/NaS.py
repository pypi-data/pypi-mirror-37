import numpy as np
from scipy.stats import linregress
from scipy.interpolate import InterpolatedUnivariateSpline
import rainflow

from .StorageComponent import StorageComponent

# ignore numpy errors
np.seterr(divide='ignore', invalid='ignore')


class NaS(StorageComponent):
    """Sodium sulfur (NaS) battery plant module.

    Parameters
    ----------
    eff_c : float
        Charging efficiency.
    eff_dc : float
        Discharging efficiency.
    dod_max : float
        Maximum depth of discharge (DOD).
    c_rate : float
        C-rate of the battery.
    capex : float or callable
        Capital expenses [USD/kWh]. Depends on size. Can be a callable
        function that returns capital cost starting from year zero to end of
        project lifetime.
    opex_fix : float or callable
        Fixed yearly operating expenses [USD/kWh-yr]. Depends on size. Can be
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
        Replacement costs [USD/kWh]. Depends on size. Equal to CapEx by
        default. Can be a callable function that returns replacement costs
        starting from year zero to end of project lifetime.
    fail_prob : float
        Probability of failure of the component
    name_solid : str
        Label for the power output. This will be used in generated graphs and
        files.
    color_solid : str
        Hex code (e.g. '#33CC33') of the color for the power output. This will
        be used in generated graphs.
    name_line : str
        Label for the state of charge. This will be used in generated graphs
        and files.
    color_line : str
        Hex code (e.g. '#33CC33') of the color for the state of charge. This
        will be used in generated graphs.
    num_case : int
        Number of scenarios to simultaneously simulate. This is set by the
        Control module.
    size : int
        Size of the component [kWh]. This is set by the Control module.
    data : ndarray
        Dataset. No dataset is required for this component.
    size_nom : float
        Size [kWh] per battery.
    c_rate : float
        C-rate [kW/kWh] of the battery.
    c_x : ndarray
        The SOC in a set of internal resistance while charging vs SOC data.
    c_y : ndarray
        The internal resistance [ohm] in a set of internal resistance while
        charging vs SOC data.
    dc_x : ndarray
        The SOC in a set of internal resistance while discharging vs SOC data.
    dc_y : ndarray
        The internal resistance [ohm] in a set of internal resistance while
        discharging vs SOC data.
    ocv_x : ndarray
        The DOD in a set of OCV vs DOD data.
    ocv_y : ndarray
        The OCV [V] in a set of OCV vs DOD data.

    References
    ----------
    ..[1] Sarasua, A.E. et. al., "Dynamic model of sodium sulfur battery
        for application in microgrids," HYFUSEN, 2011.
    ..[2] Siam, F.M. et. al., "Modeling of sodium sulfur battery for power
        system applications," ResearchGate, 2007.
    ..[3] Sparacino, A. et. al., "Survey of battery energy storage systems
        and modeling techniques," IEEE, 2012.

    """

    def __init__(
        self, eff_c=0.9, eff_dc=0.9, dod_max=0.8, c_rate=0.125,
        capex=500.0, opex_fix=5.0, opex_var=0.0,
        life=10.0, **kwargs
    ):
        """Initializes the base class.

        """
        # base class parameters
        settings = {
            'name_solid': 'NaS',  # label for power output
            'color_solid': '#0000CC',  # color for power output in powerflow
            'name_line': 'NaS SOC',  # label for SOC
            'color_line': '#FF0000',  # color for SOC in powerflow
            'capex': capex,  # CapEx [USD/kWh]
            'opex_fix': opex_fix,  # size-dependent OpEx [USD/kWh-yr]
            'opex_var': opex_var,  # output-dependent OpEx [USD/kWh-yr]
            'life': life,  # maximum battery life [yr]
            'fail_prob': 0.011,  # probability of failure
            'data': 0,  # no datasets were used
            'is_re': True  # renewable
        }
        settings.update(kwargs)  # replace default settings with input settings

        # initialize base class
        super().__init__(**settings)

        # adjustable battery plant parameters
        self.eff_c = eff_c  # charging efficiency
        self.eff_dc = eff_dc  # discharging efficiency
        self.dod_max = dod_max  # maximum DOD
        self.c_rate = c_rate  # C-rate [kW/kWh]
        self.size_nom = kwargs.pop('size_nom', 70.5)  # size per batt [kWh]

        # adjustable electrical parameters
        self.c_x = kwargs.pop(  # SOC
            'c_x',
            np.array([
                0, 0.07, 0.14, 0.15, 0.43, 0.47, 0.84, 0.95, 1
            ])
        )
        self.c_y = kwargs.pop(  # internal resistance [ohm] when charging
            'c_y',
            np.array([
                0.1385, 0.1385, 0.09059, 0.09405, 0.08193,
                0.08193, 0.07905, 0.09924, 0.07732
            ])
        )
        self.dc_x = kwargs.pop(  # SOC
            'dc_x',
            np.array([
                0, 0.07, 0.08, 0.15, 0.17, 0.33, 0.46, 0.64, 0.83, 1
            ])
        )
        self.dc_y = kwargs.pop(  # internal resistance [ohm] when discharging
            'dc_y',
            np.array([
                0.08865, 0.08865, 0.07905, 0.07790,
                0.07790, 0.07963, 0.08193, 0.09001,
                0.1137, 0.1039
            ])
        )
        self.ocv_x = kwargs.pop('ocv_x', np.array([0, 0.56, 1.1]))  # DOD
        self.ocv_y = kwargs.pop(  # OCV
            'ocv_y', np.array([120.0, 120.0, 100.6])
        )

        # derivable electrical parameters
        self.resc_func = InterpolatedUnivariateSpline(
            self.c_x, self.c_y, k=1  # internal res vs SOC (charging)
        )
        self.resdc_func = InterpolatedUnivariateSpline(
            self.dc_x, self.dc_y, k=1  # internal res vs SOC (discharging)
        )
        self.ocv_func = InterpolatedUnivariateSpline(
            self.ocv_x, self.ocv_y, k=1  # OCV vs DOD
        )

        # initialize electrical parameters
        self.curr = np.array([])  # current [A] at time t
        self.volt = np.array([])  # voltage [V] at time t
        self.ocv = np.array([])  # OCV [V] at time t

        # update initialized parameters if essential data is complete
        self._update_config()

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

        # capital costs [USD], size [kWh] based
        if callable(self.capex):  # if experience curve is given
            self.cost_c = np.atleast_1d(self.capex(0)*self.size)
        else:  # if fixed value is given
            self.cost_c = self.capex*self.size

        # fixed operating costs [USD], size [kWh] based
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
        rep_freq = self.life*np.ones(self.num_case)  # due to max life [yr]

        # replace nan's in rep_freq to prevent errors with arange
        rep_freq[np.isnan(rep_freq)] = yr_proj+1  # no replacement

        # replacement costs [USD], size [kWh] based
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

    def rec_pow(self, pow_rec, hr):
        """Records the power at a specified time step.

        Parameters
        ----------
        pow_rec : ndarray
            Power [kW] sto be recorded into self.pow.
        hr : int
            Time [h] in the simulation.

        Notes
        -----
        Negative values indicate charging.
        All inputs are assumed to be valid (does not go beyond maximum).

        """
        # record power [kW]
        self.pow = pow_rec*(pow_rec > 0)  # instantaneous power [kW]
        self.enr_tot += self.pow  # total energy [kWh]

        # determine power [kW] going in or out of each battery
        pow_in = pow_rec*(pow_rec < 0)*self.eff_c*self.size_nom/self.size
        pow_out = pow_rec*(pow_rec > 0)*self.size_nom/(self.eff_dc*self.size)

        # solve for current [A] and terminal voltage [V]
        # put nan_to_num to avoid error when size is zero
        self._update_iv(np.nan_to_num(pow_in+pow_out), hr)

        # solve for the SOC
        self._update_soc(hr)  # updates self.soc[hr+1, :]

        # solve for the OCV [V]
        self._update_ocv(hr)  # updates self.ocv

        # update max powers [kW]
        self._update_max_pow(hr)  # updates self.powmaxc, self.powmaxdc

    @staticmethod
    def exp_curve(yr, yr_0=2020, **kwargs):
        """Experience curve for NaS.
        Returns the cost [USD/kWh] at the given year

        Parameters
        ----------
        yr : int
            Index of the year.
        yr_0 : int
            Year where index is set to zero.

        """
        # get regression parameters
        a_sat = kwargs.pop('a_sat', 96)
        a_base = kwargs.pop('a_base', 0.21)
        r = kwargs.pop('r', 0.326)
        a = kwargs.pop('a', 476)
        b = kwargs.pop('b', 0.0948)

        # calculate cost [USD/kWh]
        cap = a_sat/(1+(a_sat-a_base)/a_base*np.exp(-r*(yr+(yr_0-2011))))
        cost = a*cap**(-b)

        return cost

    def _config(self):
        """Updates other parameters once essential parameters are complete."""

        # update battery plant parameters
        self.is_full = np.ones(self.num_case, dtype=bool)  # True if batt full
        self.num_cycyr = np.zeros(self.num_case)  # number of cycles per year

        # update electrical parameters
        self.curr = np.zeros(self.num_case)  # current [A] at t
        self.volt = np.zeros(self.num_case)  # volt [V] at t
        self.ocv = self.ocv_func(1-self.soc)  # solve for OCV

        # update max powers
        self.pow_maxc = np.zeros(self.num_case)  # max charging power [kW]
        self.pow_maxdc = self.size*self.dod_max  # max discharging power [kW]
        self._update_max_pow(-1)  # recalculate max powers

    def _update_iv(self, pow_dc, hr):
        """Updates the current [A] and terminal voltage [V].

        Parameters
        ----------
        pow_dc : ndarray
            Power [kW] drawn from the battery.
        hr : int
            Time [h] in the simulation.

        References
        ----------
        ..[1] Siam, F.M. et. al., "Modeling of sodium sulfur battery for power
          system applications," ResearchGate, 2007.
        ..[2] Sparacino, A. et. al., "Survey of battery energy storage systems
          and modeling techniques," IEEE, 2012.

        """
        # solve for current when discharging
        a = -self.resdc_func(1-self.soc)
        b = self.ocv
        c = -pow_dc*1e3
        curr_dc = (-b+np.sqrt(np.abs(b**2-4*a*c)))/(2*a)

        # solve for current when charging
        a = -self.resc_func(1-self.soc)
        curr_c = -(-b+np.sqrt(np.abs(b**2-4*a*c)))/(2*a)

        # update current and voltage
        # nan_to_num removes nan values which appear when no power is used
        self.curr = -curr_c*(pow_dc < 0)+curr_dc*(pow_dc > 0)  # current [A]
        self.volt = np.nan_to_num(pow_dc*1e3/self.curr)  # terminal voltage [V]

    def _update_soc(self, hr):
        """Updates the state of charge of the battery.

        Parameters
        ----------
        hr : int
            Time [h] in the simulation.

        """
        # prevent hr+1 from going beyond array size
        if hr != 8759:

            # solve for power [kW] into the battery
            pow_eff = self.curr*self.ocv*self.size/(1e3*self.size_nom)

            # update SOC
            # put nan_to_num to avoid error when size is zero
            soc_new = np.minimum(
                np.nan_to_num(self.soc-pow_eff/self.size),
                1  # maximum SOC
            )

            # check for cases where battery is about to go below min SOC
            is_trn = np.logical_and(
                soc_new <= 1-self.dod_max,  # new SOC is below min SOC and
                self.soc > 1-self.dod_max  # previous SOC is above min
            )

            # set these cases to min SOC
            soc_new[is_trn] = 1-self.dod_max
            self.soc = soc_new

            # check if full
            self.is_full = self.soc >= 1

    def _update_max_pow(self, hr):
        """Updates the maximum charge and discharge power [kW].

        Parameters
        ----------
        hr : int
            Time [h] in the simulation.

        """
        # prevent hr+1 from going beyond array size
        if hr != 8759:

            # calculate maximum charge [kW]
            maxc_cap = np.maximum(  # max c due to SOC
                self.size*(1-self.soc),
                0
            )
            maxc_crate = self.c_rate*self.size  # max c due to C-rate
            self.pow_maxc = np.minimum(maxc_cap, maxc_crate)

            # maximum discharge power [kW] depends on SOC only
            self.pow_maxdc = np.maximum(
                self.size *
                (self.soc-(1-self.dod_max)),
                0
            )

    def _update_ocv(self, hr):
        """Updates the open circuit voltage [V] of the battery.

        Parameters
        ----------
        hr : int
            Time [h] in the simulation.

        """
        # prevent hr+1 from going beyond array size
        if hr != 8759:

            # update OCV [V]
            self.ocv = self.ocv_func(1-self.soc)
