import copy

import numpy as np
import scipy as sp
from scipy.stats import linregress
from scipy.interpolate import InterpolatedUnivariateSpline
from scipy.integrate import simps
from scipy.optimize import curve_fit

from .StorageComponent import StorageComponent

# ignore numpy errors
np.seterr(divide='ignore', invalid='ignore')


class LiIon(StorageComponent):
    """Lithium-ion (Li-ion) battery plant module.

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
        Probability of failure of the component.
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
    cap_nom : float
        Capacity [Ah] per battery.
    volt_nom : float
        Voltage [V] per battery.
    c_rate : float
        C-rate [kW/kWh] of the battery.
    res1 : float
        Resistor [ohm] in series with the battery in the equivalent circuit.
        Uses Thevenin model.
    res2 : float
        Resistor [ohm] in the RC component in the equivalent circuit.
    capac : float
        Capacitor [F] in the RC component in the equivalent circuit.
    ocv_x : ndarray
        The DOD in a set of OCV vs DOD data.
    ocv_y : ndarray
        The OCV [V] in a set of OCV vs DOD data.
    rate_x : ndarray
        The current [A] in a set of rate factor vs current data.
    rate_y : ndarray
        The rate factor in a set of rate factor vs current data. The rate
        factor accounts for changes in capacity with various currents.

    References
    ----------
    ..[1] Smith, K. et. al., "Comparison of plug-in hybrid electric vehicle
        battery life across geographies and drive cycles," National Renewable
        Energy Laboratory, 2012.
    ..[2] He, H. et. al., "Evaluation of lithium-ion battery equivalent
        circuit models for state of charge estimation by an experimental
        approach," Energies, 2011.
    ..[3] Weng, C. et. al., "An open-circuit-voltage model of lithium-ion
        batteries for effective incremental capacity analysis," 2013.
    ..[4] Gao, L., Liu, S., "Dynamic lithium-ion battery model for system
        simulation," IEEE Transactions on Components and Packaging
        Technologies, vol. 25, no. 3, 2002.

    """

    def __init__(
        self, eff_c=0.95, eff_dc=0.95, dod_max=0.8, c_rate=1.0,
        capex=300.0, opex_fix=3.0, opex_var=0.0,
        life=10.0, **kwargs
    ):
        """Initializes the base class."""

        # base class parameters
        settings = {
            'name_solid': 'Li-ion',  # label for power output
            'color_solid': '#0000CC',  # color for power output in powerflow
            'name_line': 'Li-ion SOC',  # label for SOC
            'color_line': '#FF0000',  # color for SOC in powerflow
            'capex': capex,  # CapEx [USD/kWh]
            'opex_fix': opex_fix,  # size-dependent OpEx [USD/kWh-yr]
            'opex_var': opex_var,  # output-dependent OpEx [USD/kWh-yr]
            'life': life,  # maximum battery life [yr]
            'fail_prob': 0.01,  # probability of failure
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
        self.cap_nom = kwargs.pop('cap_nom', 100.0)  # cap per batt [Ah]
        self.volt_nom = kwargs.pop('volt_nom', 48.0)  # volt per batt [V]

        # derivable battery plant parameters
        self.size_nom = self.cap_nom*self.volt_nom/1e3  # size per batt [kWh]

        # initialize battery plant parameters
        self.is_full = np.array([])  # True if battery is full
        self.num_batt = np.array([])  # number of batteries
        self.num_cycyr = np.array([])  # number of cycles per year

        # adjustable electrical parameters
        self.res1 = kwargs.pop('res1', 0.44)  # R1 in equivalent circuit [ohm]
        self.res2 = kwargs.pop('res2', 0.16)  # R2 in equivalent circuit [ohm]
        self.capac = kwargs.pop('capac', 16)  # C in equivalent circuit [F]
        self.ocv_x = kwargs.pop(  # depth of discharge
            'ocv_x',
            np.array([
                0.0667, 0.1333, 0.2000, 0.2667,
                0.3333, 0.4000, 0.4667, 0.5333,
                0.6000, 0.6667, 0.7333, 0.8000,
                0.8667, 0.9333, 1.0000
            ])
        )
        self.ocv_y = kwargs.pop(  # corresponding OCV [V]
            'ocv_y',
            np.array([
                51.32, 51.20, 51.16, 51.12,
                51.08, 50.96, 50.88, 50.72,
                50.64, 50.40, 50.20, 50.00,
                49.72, 49.16, 48.24
            ])
        )
        self.rate_x = kwargs.pop(  # current [A]
            'rate_x', np.array([0.6, 1.4, 2.8, 5.6])
        )
        self.rate_y = kwargs.pop(  # corresponding rate factor
            'rate_y', np.array([0.96, 1, 1.01, 1.05])
        )

        # derivable electrical parameters
        ocv_param, err = curve_fit(  # curve fit of OCV vs DOD
            self._ocv_curve, 1-self.ocv_x, self.ocv_y
        )
        self.ocv_func = lambda v: self._ocv_curve(  # OCV as fxn of DOD
            v, ocv_param[0], ocv_param[1], ocv_param[2], ocv_param[3],
            ocv_param[4], ocv_param[5], ocv_param[6], ocv_param[7],
            ocv_param[8], ocv_param[9], ocv_param[10], ocv_param[11]
        )
        self.rate_func = InterpolatedUnivariateSpline(  # RF as fxn of curr
            self.rate_x, self.rate_y, ext='const'
        )

        # intialize electrical parameters
        self.volt = np.array([])  # voltage [V] at time t
        self.ocv1 = np.array([])  # OCV [V] at time t+1
        self.ocv = np.array([])  # OCV [V] at time t
        self.curr = np.array([])  # current [A] at time t
        self.volt_th = np.array([])  # voltage at RC circuit [V]

        # initialize maximum charge and discharge current
        self.pow_maxc = 0  # maximum charging power [kW]
        self.pow_maxdc = 0  # maximum discharging power [kW]

        # update initialized parameters if essential data is complete
        self._update_config()

    def rec_pow(self, pow_rec, hr):
        """Records the power at a specified time step.

        Parameters
        ----------
        pow_rec : ndarray
            Power [kW] sto be recorded into self.pow[hr, :]
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
        pow_in = -pow_rec*(pow_rec < 0)*self.eff_c/self.num_batt
        pow_out = pow_rec*(pow_rec > 0)/(self.eff_dc*self.num_batt)

        # solve for current [A] and terminal voltage [V]
        # put nan_to_num to avoid error when size is zero
        self._update_iv(np.nan_to_num(pow_out-pow_in))

        # solve for the SOC
        self._update_soc(hr)  # updates self.soc[hr+1, :]

        # solve for the OCV [V]
        self._update_ocv(hr)  # updates self.ocv, self.ocv1

        # update max powers [kW]
        self._update_max_pow(hr)  # updates self.powmaxc, self.powmaxd

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
        rep_freq = self.life*np.ones(self.num_case)

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

    def _ocv_curve(self, soc, k0, k1, k2, k3, k4, k5, a1, a2, a3, a4, b1, b2):
        """Empirical equation of OCV vs SOC.

        Parameters
        ----------
        soc : ndarray
            State of charge of battery.
        k0, k1, k2, k3, k4, k5, a1, a2, a3, a4, b1, b2 : float
            Empirical constants.

        Returns
        -------
        ndarray
            OCV [V] of battery.

        References
        ----------
        ..[1] Weng, C. et. al., "An open-circuit-voltage model of lithium-ion
          batteries for effective incremental capacity analysis," 2013.

        """
        # calculate terms
        term1 = k1/(1+np.exp(a1*(soc-b1)))
        term2 = k2/(1+np.exp(a2*(soc-b2)))
        term3 = k3/(1+np.exp(a3*(soc-1)))
        term4 = k4/(1+np.exp(a4*soc))

        return term1+term2+term3+term4+k0+k5*soc

    def _config(self):
        """Updates other parameters once essential parameters are complete."""

        # update battery plant parameters
        self.is_full = np.ones(self.num_case, dtype=bool)  # True if batt full
        self.num_batt = self.size/self.size_nom  # number of batteries
        self.num_cycyr = np.zeros(self.num_case)  # number of cycles per year

        # update electrical parameters
        self.volt = self.ocv_func(1)*np.ones(self.num_case)  # volt [V] at t
        self.ocv1 = copy.deepcopy(self.volt)  # OCV [V] at t-1
        self.ocv = copy.deepcopy(self.volt)  # OCV [V] at t
        self.curr = np.zeros(self.num_case)  # current [A] at t
        self.volt_th = np.zeros(self.num_case)  # voltage at the RC circuit [V]

        # update max powers
        self.pow_maxc = np.zeros(self.num_case)  # max charging power [kW]
        self.pow_maxdc = self.size*self.dod_max  # max discharging power [kW]
        self._update_max_pow(-1)  # recalculate max powers

    def _update_iv(self, pow_dc):
        """Updates the current [A] and terminal voltage [V].

        Parameters
        ----------
        pow_dc : ndarray
            Power [kW] drawn from the battery.

        References
        ----------
        ..[1] He, H. et. al., "Evaluation of lithium-ion battery equivalent
          circuit models for state of charge estimation by an experimental
          approach," Energies, 2011.

        """
        # solve for current and terminal voltage
        self.volt_th = (self.curr-self.volt_th/self.res2)/self.capac
        self.volt = self.ocv-self.volt_th-self.curr*self.res1
        self.curr = np.nan_to_num(pow_dc*1e3/self.volt)  # terminal voltage [V]

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
                0  # prevents negative answers
            )
            maxc_crate = self.c_rate*self.size  # max c due to C-rate
            self.pow_maxc = np.minimum(maxc_cap, maxc_crate)

            # calculate maximum discharge [kW]
            self.pow_maxdc = np.maximum(  # max dc due to SOC
                self.size*(self.soc-(1-self.dod_max)),
                0  # prevents negative answers
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
            self.ocv1 = copy.deepcopy(self.ocv)  # pass by value
            self.ocv = self.ocv_func(self.soc)  # calculate new OCV

    def _update_soc(self, hr):
        """Updates the state of charge of the battery.

        Parameters
        ----------
        hr : int
            Time [h] in the simulation.

        References
        ----------
        ..[1] Gao, L., Liu, S., "Dynamic lithium-ion battery model for system
          simulation," IEEE Transactions on Components and Packaging
          Technologies, vol. 25, no. 3, 2002.

        """
        # prevent hr+1 from going beyond array size
        if hr != 8759:

            # update SOC
            delta_soc = self.curr*self.ocv*self.rate_func(self.curr)/(
                self.cap_nom*self.volt_nom
            )
            soc_new = np.minimum(self.soc-delta_soc, 1)  # new SOC

            # check for cases where battery is about to go below min SOC
            is_trn = np.logical_and(
                soc_new <= 1-self.dod_max,  # new SOC is below min SOC and
                self.soc > 1-self.dod_max  # previous SOC is above min
            )

            # set these cases to min SOC
            soc_new[is_trn] = 1-self.dod_max

            # record new SOC
            self.soc = soc_new

            # check if battery is full
            self.is_full = self.soc >= 1

    def fail_calc(self):
        """Calculates the probability of failure of the component."""

        # calculate number of cycles per year
        num_cycyr = np.zeros(self.num_case)
        for i in range(0, self.num_case):
            cyc_yr = 0
            for val, cyc in rainflow.count_cycles(self.soc[:, i]):
                if cyc == 1:
                    cyc_yr += 1
            self.num_cycyr[i] = cyc_yr

        # calculate replacement frequency
        life_freq = self.life*np.ones(self.num_case)
        thr_freq = self.thr_life/self.thr
        rep_freq = np.minimum.reduce([life_freq, thr_freq, deg_freq])

        # calculate number of cycles throughout lifetime
        num_cyc = rep_freq*num_cycyr

        # calculate ccycles to 5% failure
        cyc_life = self.life*num_cycyr-82

        # Weibull distribution
        self.fail = 1-np.exp(-((num_cyc-cyc_life)/300)**2.3)

    @staticmethod
    def exp_curve(yr, yr_0=2020, **kwargs):
        """Experience curve for Li-ion.
        Returns the cost [USD/kWh] at the given year

        Parameters
        ----------
        yr : int
            Index of the year.
        yr_0 : int
            Year where index is set to zero.

        """
        # get regression parameters
        a_sat = kwargs.pop('a_sat', 2600)
        a_base = kwargs.pop('a_base', 1)
        r = kwargs.pop('r', 0.348)
        a = kwargs.pop('a', 868)
        b = kwargs.pop('b', 0.251)

        # calculate cost [USD/kWh]
        cap = a_sat/(1+(a_sat-a_base)/a_base*np.exp(-r*(yr+(yr_0-2011))))
        cost = a*cap**(-b)

        return cost
