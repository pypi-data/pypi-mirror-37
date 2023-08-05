import copy

import numpy as np
from scipy.stats import linregress
from scipy.interpolate import InterpolatedUnivariateSpline
import rainflow

from .StorageComponent import StorageComponent

# ignore numpy errors
np.seterr(divide='ignore', invalid='ignore')


class PbAcid(StorageComponent):
    """Lead acid battery plant module.

    Parameters
    ----------
    eff_c : float
        Charging efficiency.
    eff_dc : float
        Discharging efficiency.
    dod_max : float
        Maximum depth of discharge (DOD).
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
        Label for the power output. This will be used in generated graphs
        and files.
    color_solid : str
        Hex code (e.g. '#33CC33') of the color for the power output. This
        will be used in generated graphs.
    name_line : str
        Label for the state of charge. This will be used in generated
        graphs and files.
    color_line : str
        Hex code (e.g. '#33CC33') of the color for the state of charge.
        This will be used in generated graphs.
    num_case : int
        Number of scenarios to simultaneously simulate. This is set by the
        Control module
    yr_proj : int
        Project lifetime [yr]. This is set by the Control module.
    size : int
        Size of the component [kWh]. This is set by the Control module.
    infl : float
        Inflation rate. This is set by the Control module.
    data : ndarray
        Dataset. No dataset is required for this component.
    size_nom : float
        Size [kWh] per battery.
    cap_ratio : float
        Capacity ratio of the battery. Uses the kinetic battery model
    rate_const : float
        Rate constant [/hr] of the battery. Uses the kinetic battery model.
    res_int : float
        Internal resistance [ohm] of the battery. Uses the Rint model.
    c_rate : float
        C-rate [kW/kWh] of the battery.
    curr_max : float
        Maximum charing current [A] into the battery.
    deg_life : float
        Battery life [yr] if battery is repeatedly cycled to its maximum
        DOD.
    deg_max : float
        Maximum amount of degradation. Default value is 0.2.
    deg_x : ndarray
        The DOD in a set of number of cycles vs DOD data.
    deg_y : ndarray
        The number of cycles before replacement in a set of number of
        cycles vs DOD data.
    ocv_x : ndarray
        The DOD in a set of OCV vs DOD data.
    ocv_y : ndarray
        The OCV [V] in a set of OCV vs DOD data.

    References
    ----------
    ..[1] DiOrio, N. et. al., "Technoeconomic modelling of battery energy
        storage in SAM," National Renewable Energy Laboratory," n.d.
    ..[2] He, H. et. al., "Evaluation of lithium-ion battery equivalent
        circuit models for state of charge estimation by an experimental
        approach," Energies, 2011.

    """

    def __init__(
        self, eff_c=0.8, eff_dc=0.8, dod_max=0.6,
        capex=500.0, opex_fix=5.0, opex_var=0.0,
        life=5.0, **kwargs
    ):
        """Initializes the base class.

        """
        # base class parameters
        settings = {
            'name_solid': 'Pb Acid',  # label for power output
            'color_solid': '#0000CC',  # color for power output in powerflow
            'name_line': 'Pb Acid SOC',  # label for SOC
            'color_line': '#FF0000',  # color for SOC in powerflow
            'capex': capex,  # CapEx [USD/kWh]
            'opex_fix': opex_fix,  # size-dependent OpEx [USD/kWh-yr]
            'opex_var': opex_var,  # output-dependent OpEx [USD/kWh-yr]
            'life': life,  # maximum battery life [yr]
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
        self.size_nom = kwargs.pop('size_nom', 0.06)  # size per batt [kWh]
        self.cap_ratio = kwargs.pop('cap_ratio', 0.308)  # capacity ratio
        self.rate_const = kwargs.pop('rate_const', 2.86)  # rate constant [/hr]
        self.c_rate = kwargs.pop('c_rate', 1)  # C-rate [kW/kWh]

        # initialize battery plant parameters
        self.enr_av = np.array([])  # available energy [kWh] at time t
        self.enr_bd = np.array([])  # bounded energy [kWh] at time t
        self.enr_tot = np.array([])  # total energy [kWh] at time t
        self.num_cycyr = np.array([])  # number of cycles per year

        # adjustable battery life parameters
        self.thr_life = kwargs.pop('thr_life', 20.2)  # max enrgy fr batt [kWh]
        self.deg_life = kwargs.pop('deg_life', 3)  # max DOD cycling life [yr]
        self.deg_max = kwargs.pop('deg_max', 0.2)  # maximum degradation
        self.deg_x = kwargs.pop(  # depth of discharge
            'deg_x', np.array([0.3, 0.5, 1])
        )
        self.deg_y = kwargs.pop(  # corresponding number of cycles
            'deg_y', np.array([1360, 575, 260])
        )

        # derivable battery life parameters
        # fit deg_x and deg_y into deg_y = a(deg_x)^b
        ln_x = np.log(np.array(self.deg_x))
        ln_y = -np.log(np.array(self.deg_y))
        slope, intercept, r_value, p_value, std_err = linregress(ln_x, ln_y)
        self.deg_b = slope
        self.deg_a = self.deg_max/(365*self.deg_life*self.dod_max**slope)

        # adjustable electrical parameters
        self.curr_max = kwargs.pop('curr_max', 4)
        self.res_int = kwargs.pop('res_int', 5e-3)
        self.ocv_x = kwargs.pop(  # depth of discharge
            'ocv_x', np.array([0, 0.1, 0.52, 0.77, 1])
        )
        self.ocv_y = kwargs.pop(  # corresponding number of cycles
            'ocv_y', np.array([6.1, 6, 5.75, 5.5, 5.4])
        )

        # derivable electrical parameters
        self.ocv_func = InterpolatedUnivariateSpline(
            self.ocv_x, self.ocv_y, k=1  # OCV vs DOD
        )

        # initialize electrical parameters
        self.curr = np.array([])  # current [A] at time t
        self.volt = np.array([])  # voltage [V] at time t
        self.ocv = np.array([])  # OCV [V] at time t

        # update initialized parameters if essential data is complete
        self._update_config()

    def cost_calc(self):
        """Calculates the cost of the component.

        """
        def ann_func(i):
            """Annunity factor"""
            return 1/(1+self.infl)**i

        # capital costs [USD], size [kWh] based
        if callable(self.capex):  # if experience curve is given
            self.cost_c = np.atleast_1d(self.capex(0)*self.size)
        else:  # if fixed value is given
            self.cost_c = self.capex*self.size

        # fixed operating costs [USD], size [kWh] based
        if callable(self.opex_fix):
            opex_fix = self.size*np.sum(
                self.opex_fix(i)*ann_func(i)
                for i in np.arange(1, self.yr_proj+1)
            )
        else:
            opex_fix = self.opex_fix*self.size*np.sum(
               1/(1+self.infl)**np.arange(1, self.yr_proj+1)
            )

        # variable operating costs [USD], output [kWh] based
        if callable(self.opex_var):
            opex_var = np.sum(self.pow, axis=0)*np.sum(
                self.opex_var(i)*ann_func(i)
                for i in np.arange(1, self.yr_proj+1)
            )
        else:
            opex_var = self.opex_var*np.sum(self.pow, axis=0)*np.sum(
               1/(1+self.infl)**np.arange(1, self.yr_proj+1)
            )

        # total operating costs [USD]
        self.cost_o = opex_fix+opex_var

        # calculate replacement frequency [yr]
        life_freq = self.life*np.ones(self.num_case)  # due to max life [yr]
        thr_freq = self.thr_life*self.size*self.eff_dc/(  
            self.size_nom*np.sum(self.pow, axis=0)  # due to max thr [kWh]
        )
        deg_freq = self._deg_calc()  # due to cycling degradation
        rep_freq = np.minimum.reduce([life_freq, thr_freq, deg_freq])

        # replace nan's in rep_freq to prevent errors with arange
        rep_freq[np.isnan(rep_freq)] = self.yr_proj+1  # no replacement

        # replacement costs [USD], size [kWh] based
        if callable(self.repex):
            repex = np.zeros(self.num_case)  # initialize replacement costs
            for i in range(0, self.num_case):
                repex[i] = np.sum(  # output [kWh] based
                    self.repex(j)*ann_func(j)
                    for j in np.arange(0, self.yr_proj, rep_freq[i])
                )-self.repex(0)*ann_func(0)  # no replacement at time zero
        else:
            disc_rep = np.zeros(self.num_case)  # initialize sum of ann factors
            for i in range(0, self.num_case):
                disc_rep[i] = np.sum(
                    1/(1+self.infl) **
                    np.arange(0, self.yr_proj, rep_freq[i])[1:]  # remove yr 0
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
            Power [kW] sto be recorded into self.pow[hr, :]
        hr : int
            Time [h] in the simulation.

        Notes
        -----
        Negative values indicate charging.
        All inputs are assumed to be valid (does not go beyond maximum).

        """
        # record power [kW] discharge
        self.pow[hr, :] = pow_rec*(pow_rec > 0)

        # determine power [kW] going in or out of each battery
        pow_in = pow_rec*(pow_rec < 0)*self.eff_c*self.size_nom/self.size
        pow_out = pow_rec*(pow_rec > 0)*self.size_nom/(self.eff_dc*self.size)

        # solve for current [A] and terminal voltage [V]
        # put nan_to_num to avoid error when size is zero
        self._update_iv(np.nan_to_num(pow_in+pow_out), hr)

        # solve for the SOC
        self._update_soc(hr)  # updates self.soc[hr+1, :]

        # solve for available and bounded energies [kWh]
        self._update_av()  # updates self.enr_av, self.enr_bd

        # solve for the OCV [V]
        self._update_ocv(hr)  # updates self.ocv

        # update max powers [kW]
        self._update_max_pow(hr)  # updates self.powmaxc, self.powmaxdc

    def _config(self):
        """Updates other parameters once essential parameters are complete.

        """
        # update battery plant parameters
        self.is_full = np.ones(self.num_case, dtype=bool)  # True if batt full
        self.enr_av = self.cap_ratio*self.size  # available energy [kWh] at t
        self.enr_bd = (1-self.cap_ratio)*self.size  # bounded energy [kWh] at t
        self.enr_tot = copy.deepcopy(self.size)  # total energy [kWh] at time t
        self.num_cycyr = np.zeros(self.num_case)  # number of cycles per year

        # update electrical parameters
        self.curr = np.zeros(self.num_case)  # current [A] at time t
        self.volt = np.zeros(self.num_case)  # voltage [V] at time t
        self.ocv = self.ocv_func(1-self.soc[0, :])  # solve for OCV

        # update max powers
        self.pow_maxc = np.zeros(self.num_case)  # max charging power [kW]
        self.pow_maxdc = self.size*self.dod_max  # max discharging power [kW]
        self._update_max_pow(-1)  # recalculate max powers

    def _deg_calc(self):
        """Calculates frequency of replacement due to degradation.

        Returns
        -------
        ndarray
            Replacement frequency [yr] due to degradation.

        """
        # initialize array with sum of degradation
        deg_arr = np.zeros(self.num_case)

        # calculate degradation per case
        for i in range(0, self.num_case):
            soc_cyc = []
            for val, cyc in rainflow.count_cycles(self.soc[:, i]):
                if cyc == 1:
                    soc_cyc.append(val)
            soc_cyc = np.array(soc_cyc)
            deg_arr[i] = self.deg_a*np.sum(soc_cyc**self.deg_b)  # add deg
            self.num_cycyr[i] = np.size(soc_cyc)

        # calculate replacement frequency [yr] due to cycling degradation
        deg_freq = self.deg_max/deg_arr

        return deg_freq

    def _update_av(self):
        """Updates available and bounded energies [kWh].

        References
        ----------
        ..[1] DiOrio, N. et. al., "Technoeconomic modelling of battery energy
          storage in SAM," National Renewable Energy Laboratory, n.d.

        """
        # solve for power [kW] into the battery
        pow_eff = -self.curr*self.ocv*self.size/(1e3*self.size_nom)

        # copy required variables
        k = self.rate_const   # rate constant [/hr]
        c = self.cap_ratio  # capacity ratio
        ekt = np.exp(-k)  # exp(-kdt)
        p_av = self.enr_av  # available energy [kWh] at time t
        p_bd = self.enr_bd  # bounded energy [kWh] at time t
        p_tot = self.enr_tot  # total energy [kWh] at time t

        # update available energy [kWh]
        self.enr_av = (
            p_av*ekt +
            (p_tot*k*c+pow_eff)*(1-ekt)/k +
            pow_eff*c*(k-1+ekt)/k
        )

        # update bounded energy [kWh]
        self.enr_bd = (
            p_bd*ekt +
            p_tot*(1-c)*(1-ekt) +
            pow_eff*(1-c)*(k-1+ekt)/k
        )

        # update total energy [kWh]
        self.enr_tot = self.enr_av+self.enr_bd

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
        ..[1] He, H. et. al., "Evaluation of lithium-ion battery equivalent
          circuit models for state of charge estimation by an experimental
          approach," Energies, 2011.

        """
        # solve for current when discharging
        a = -self.res_int
        b = self.ocv
        c = -pow_dc*1e3
        
        # update current and voltage
        self.curr = np.nan_to_num((-b+np.sqrt(b**2-4*a*c))/(2*a))
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
                np.nan_to_num(self.soc[hr, :]-pow_eff/self.size),
                1  # maximum SOC
            )

            # check for cases where battery is about to go below min SOC
            is_trn = np.logical_and(
                soc_new <= 1-self.dod_max,  # new SOC is below min SOC and
                self.soc[hr, :] > 1-self.dod_max  # previous SOC is above min
            )

            # set these cases to min SOC
            soc_new[is_trn] = 1-self.dod_max
            self.soc[hr+1, :] = soc_new

            # check if full
            self.is_full = self.soc[hr+1, :] >= 1

    def _update_max_pow(self, hr):
        """Updates the maximum charge and discharge power [kW].

        Parameters
        ----------
        hr : int
            Time [h] in the simulation.

        """
        # prevent hr+1 from going beyond array size
        if hr != 8759:

            # copy required variables
            k = self.rate_const   # rate constant [/hr]
            c = self.cap_ratio  # capacity ratio
            ekt = np.exp(-k)  # exp(-kdt)
            p_av = self.enr_av  # available energy [kWh] at time t
            p_tot = self.enr_tot  # total energy [kWh] at time t
            p_max = self.size  # size of battery [kWh]

            # calculate maximum charge [kW]
            maxc_kibam = (  # max c due to kinetics
                -(-k*c*p_max+k*p_av*ekt+p_tot*k*c*(1-ekt)) /
                (1-ekt+c*(k-1+ekt))
            )
            maxc_cap = np.maximum(  # max c due to SOC
                self.size*(1-self.soc[hr+1, :]),
                0  # prevents negative answers
            )
            maxc_crate = (  # max c due to C-rate
                (1-np.exp(-self.c_rate)) *
                (p_max-p_tot)
            )
            maxc_curr = (  # max c due to max current
                self.size*self.curr_max*self.ocv /
                (1e3*self.size_nom)
            )
            self.pow_maxc = np.minimum.reduce([
                maxc_kibam, maxc_cap, maxc_crate, maxc_curr
            ])

            # calculate maximum discharge [kW]
            maxdc_kibam = (  # max dc due to kinetics
                (k*p_av*ekt+p_tot*k*c*(1-ekt)) /
                (1-ekt+c*(k-1+ekt))
            )
            maxdc_cap = np.maximum(  # max dc due to SOC
                self.size *
                (self.soc[hr+1, :]-(1-self.dod_max)),
                0  # prevents negative answers
            )
            self.pow_maxdc = np.minimum(maxdc_kibam, maxdc_cap)

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
            self.ocv = self.ocv_func(1-self.soc[hr+1, :])  # calculate new OCV
