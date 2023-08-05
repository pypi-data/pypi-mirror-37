import numpy as np
from scipy.stats import linregress
import rainflow

from .StorageComponent import StorageComponent

# ignore numpy errors
np.seterr(divide='ignore', invalid='ignore')


class VRBEnergy(StorageComponent):
    """Vanadium redox flow battery (VRB) plant module.
    This module models only the energy [kWh] of the VRB. A VRBPower module
    should also be initialized to model the power [kW].

    Parameters
    ----------
    pow_module : VRBPower
        The corresponding power module for the VRB.
    eff_c : float
        Charging efficiency.
    eff_dc : float
        Discharging efficiency.
    dod_min : float
        Minimum depth of discharge (DOD).
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
    size_nom : float
        Size [kWh] per battery.
    num_ser : float
        Number of VRB cells in series in a stack.
    volt_eq : float
        Equilibrium voltage [V] of the VRB redox reaction.
    soc_corr : float
        SOC correction factor.
    temp : float
        Operating temperature [K].
    res_int : float
        Internal resistance [ohm] in the equivalent circuit.
    vsc : float
        Electrolye viscosity [Pa-s].
    stk_l : float
        Length [m] of a single cell in the stack.
    stk_w : float
        Width [m] of a single cell in the stack.
    stk_d : float
        Thickness [m] of a single cell in the stack.
    perm : float
        Permeability [m^2] of porous electrode.
    vol_flow : float
        Volumetric flow rate [m^3/s] of electrolyte per stack.
    pump_eff : float
        Pump efficiency.
    diff_rat : float
        Diffusion ratio of the membrane.

    References
    ----------
    ..[1] Zhang, Y. et. al., "A comprehensive equivalent circuit model of
        all-vanadium redox flow battery for power system analysis," Journal
        of Power Soures, 2015.

    """

    def __init__(
        self, pow_module, eff_c=0.86, eff_dc=0.86,
        dod_min=0.1, dod_max=0.9, capex=600.0, opex_fix=0.0,
        opex_var=0.0, life=10.0, **kwargs
    ):
        """Initializes the base class."""

        # base class parameters
        settings = {
            'name_solid': 'VRB',  # label for power output
            'color_solid': '#0000CC',  # color for power output in powerflow
            'name_line': 'VRB SOC',  # label for SOC
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

        # get power module
        self.pow_module = pow_module

        # adjustable battery plant parameters
        self.eff_c = eff_c  # charging efficiency
        self.eff_dc = eff_dc  # discharging efficiency
        self.dod_min = dod_min  # minimum DOD
        self.dod_max = dod_max  # maximum DOD
        self.volt_nom = kwargs.pop('volt_nom', 60.0)  # nominal voltage [V]
        self.num_cell = kwargs.pop('num_cell', 15)  # number of cells per stack
        self.volt_eq = kwargs.pop('volt_eq', 1.39)  # eq volt [V] of cell
        self.soc_corr = kwargs.pop('soc_corr', 1.4)  # SOC correction factor
        self.temp = kwargs.pop('temp', 316)  # operating temp [K]
        self.res_int = kwargs.pop('res_int', 0.02)  # res int [ohm] of stack
        self.vsc = kwargs.pop('vsc', 6e-3)  # viscosity [Pa-s] of electrolyte
        self.stk_l = kwargs.pop('stk_l', 0.3)  # length [m] of stack
        self.stk_w = kwargs.pop('stk_w', 0.26)  # width [m] of stack
        self.stk_d = kwargs.pop('stk_d', 3e-3)  # thickness [m] of stack
        self.perm = kwargs.pop('perm', 1.685e-10)  # permeability [m^2]
        self.vol_flow = kwargs.pop('vol_flow', 6.67e-5)  # v fl [m^3/s] of stk
        self.pump_eff = kwargs.pop('pump_eff', 0.5)  # pump efficiency
        self.diff_rat = kwargs.pop('diff_rat', 0.05)  # diffusion ratio

        # derivable battery plant parameters
        self.num_stk = self.volt_nom/(  # num of stacks
            self.num_cell*self.volt_eq
        )

        # initialize battery plant parameters
        self.pow_pump = np.array([])  # pumping power
        self.num_cycyr = np.array([])  # number of cycles per year

        # initialize electrical parameters
        self.curr = np.array([])  # current [A] at time t
        self.volt = np.array([])  # voltage of EMF element [V] at time t
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

        # determine power [kW] going in or out of each module
        pow_in = (
            pow_rec*(pow_rec < 0)*self.eff_c*self.num_stk /
            self.pow_module.size
        )
        pow_out = (
            pow_rec*(pow_rec > 0)*self.num_stk /
            (self.eff_dc*self.pow_module.size)
        )

        # solve for current [A] and voltage [V] at EMF element for module
        # put nan_to_num to avoid error when size is zero
        self._update_iv(np.nan_to_num(pow_in+pow_out), hr)

        # update battery SOC
        self._update_soc(hr)  # updates self.soc[hr+1, :]

        # update OCV
        self._update_ocv(hr)  # updates self.ocv

        # update max powers
        self._update_max_pow(hr)  # updates self.powmaxc, self.powmaxdc

    @staticmethod
    def exp_curve(yr, yr_0=2020, **kwargs):
        """Experience curve for VRB.
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
        a = kwargs.pop('a', 920)
        b = kwargs.pop('b', 0.168)

        # calculate cost [USD/kWh]
        cap = a_sat/(1+(a_sat-a_base)/a_base*np.exp(-r*(yr+(yr_0-2011))))
        cost = a*cap**(-b)

        return cost

    def _config(self):
        """Updates other parameters once essential parameters are complete."""

        # update battery plant parameters
        self.soc = (1-self.dod_min)*np.ones(self.num_case)  # SOC array
        self.is_full = np.ones(self.num_case, dtype=bool)  # True if full
        self._pow_pump()  # pump power [kW] of a 1 kW VRB stack
        self.num_cycyr = np.zeros(self.num_case)  # number of cycles per year

        # update electrical parameters
        self.curr = np.zeros(self.num_case)  # current [A] at t
        self.volt = self.volt_nom*np.ones(self.num_case)  # volt [V] at t
        self.ocv = self.volt_nom*np.ones(self.num_case)  # OCV [V] at t

        # update max powers
        self.pow_maxc = np.zeros(self.num_case)  # max charging power [kW]
        self.pow_maxdc = self.size*self.dod_max  # max discharging power [kW]
        self._update_max_pow(-1)  # recalculate max powers

    def _pow_pump(self):
        """Calculates the pump power [kW] for each VRB module."""

        # calculate hydraulic resistance [Pa-s/m^3] of a 1 kW stack
        res_hyd = self.vsc*self.stk_l/(self.perm*self.stk_w*self.stk_d)

        # calculate pressure drop [Pa] of stack of a 1 kW stack
        p_stk = self.vol_flow*res_hyd/(0.7*15.0)  # 15 cells in 1 kW stack

        # calculate power of pump [kW] for the module
        self.pow_pump = self.num_stk*p_stk*self.vol_flow*1e-3/self.pump_eff

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
        ..[1] Zhang, Y. et. al., "A comprehensive equivalent circuit model of
          all-vanadium redox flow battery for power system analysis," Journal
          of Power Soures, 2015.

        """
        # check if power used pump exceeds charging power
        # in this case, do nothing to avoid losing power
        is_dc = np.logical_and.reduce([  # cases where pow pump > pow charge
            pow_dc < 0, pow_dc+self.pow_pump > 0
        ])
        pow_dc[is_dc] = 0  # replace cases with zero (don't charge)

        # add pump power [kW] if battery is discharged
        pow_dc = pow_dc+self.pow_pump*(pow_dc != 0)

        # solve for terminal
        curr_term = (  # terminal current [A]
            (-self.ocv+np.sqrt(self.ocv**2+4*self.res_int*pow_dc*1e3)) /
            (2*self.res_int)
        )

        # solve for diffusion current [A]
        curr_diff = self.diff_rat*curr_term/(2-self.diff_rat)

        # solve for current [A] and voltage [V] at EMF element
        # nan_to_num removes nan values which appear when no power is used
        self.curr = curr_term-curr_diff  # current [A]
        self.volt = pow_dc*1e3/curr_term  # EMF voltage [V]

    def _update_ocv(self, hr):
        """Updates the open circuit voltage [V] of the battery.

        Parameters
        ----------
        hr : int
            Time [h] in the simulation.

        """
        # prevent hr+1 from going beyond array size
        if hr != 8759:

            # calculate OCV
            ln_socrat = np.log((self.soc)/(1-self.soc))
            ln_socrat[np.isposinf(ln_socrat)] = 0  # if starting SOC is 1
            self.ocv = self.num_stk*self.num_cell*(
                self.volt_eq+2*self.soc_corr*8.314*self.temp/96485*ln_socrat
            )

    def _update_soc(self, hr):
        """Updates the state of charge of the battery.

        Parameters
        ----------
        hr : int
            Time [h] in the simulation.

        """
        # prevent hr+1 from going beyond array size
        if hr != 8759:

            # solve for power [kW] into the battery module
            pow_eff = self.curr*self.ocv*self.pow_module.size/(
                1e3*self.num_stk
            )

            # update SOC
            # put nan_to_num to avoid error when size is zero
            soc_new = np.minimum(
                np.nan_to_num(self.soc-pow_eff/self.size),
                1-self.dod_min  # maximum SOC
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
            self.is_full = self.soc >= 1-self.dod_min

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
                self.size*(1-self.dod_min-self.soc) +
                self.pow_pump*self.pow_module.size/self.num_stk,
                0  # prevents negative answers
            )
            maxc_stk = self.pow_module.size  # max c due to max power
            self.pow_maxc = np.minimum(maxc_cap, maxc_stk)

            # calculate maximum discharge [kW]
            maxdc_cap = np.maximum(  # max dc due to SOC
                self.size*(self.soc-(1-self.dod_max)) -
                self.pow_pump*self.pow_module.size/self.num_stk,
                0  # prevents negative answers
            )
            maxdc_stk = self.pow_module.size  # max dc due to max power
            self.pow_maxdc = np.minimum(maxdc_cap, maxdc_stk)
