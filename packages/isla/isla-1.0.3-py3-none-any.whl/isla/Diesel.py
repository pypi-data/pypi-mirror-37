import numpy as np

from .AdjustComponent import AdjustComponent

# ignore numpy errors
np.seterr(divide='ignore', invalid='ignore')


class Diesel(AdjustComponent):
    """Diesel plant module.

    Parameters
    ----------
    th_module : ThermalLoad object
        Thermal load module.
    capex : float or callable
        Capital expenses [USD/kW]. Depends on size. Can be a callable function
        that returns capital cost starting from year zero to end of project
        lifetime.
    opex_fix : float or callable
        Fixed yearly operating expenses [USD/kW-yr]. Depends on size. Can be a
        callable function that returns the fixed operating cost starting from
        year zero to end of project lifetime.
    opex_var : float or callable
        Variable yearly operating expenses [USD/kWh-yr]. Depends on energy
        produced. Can be a callable function that returns the variable
        operating cost starting from year zero to end of project lifetime.
    fl_cost : float
        Initial cost of fuel [USD/L].
    fl_infl : float
        Inflation rate of fuel.
    life : float
        Maximum life [yr] before the component is replaced.

    Other Parameters
    ----------------
    repex : float or callable
        Replacement costs [USD/kW]. Depends on size. Equal to CapEx by default.
        Can be a callable function that returns replacement costs starting
        from year zero to end of project lifetime.
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
    data : ndarray
        Dataset. No dataset is required for this component.
    fl_int : ndarray
        y-intercept [L/kWh] of the fuel consumption line.
    fl_slp : ndarray
        Slope [L/kWh] of the fuel consumption line.
    fl_den : float
        Density of the fuel [kg/m^3].
    fl_lhv : float
        Lower heating value of the fuel [MJ/kg].
    min_ratio : ndarray
        Ratio of minimum power output [kW] to the load in the current time
        step.

    References
    ----------
    ..[1] HOMER, "How HOMER calculates the generator efficiency curve,"
        n.d.

    Notes
    -----
    Fuel consumption is given by (fuel consumption [L/h]) =
    (intercept [L/kWh])*(size [kW])+(slope [L/kWh])*(power output [kW])

    """

    def __init__(
        self, th_module=None, capex=500.0, opex_fix=5.0, opex_var=0.0,
        opex_hr=0.0, fl_cost=0.9, fl_infl=0.03, life=10.0, life_hr=0.0,
        **kwargs
    ):
        """Initializes the base class."""

        # base class parameters
        settings = {
            'name_solid': 'Diesel',  # label for power output
            'color_solid': '#000000',  # color for power output in powerflow
            'capex': capex,  # CapEx [USD/kW]
            'opex_fix': opex_fix,  # size-dependent OpEx [USD/kW-yr]
            'opex_var': opex_var,  # output-dependent OpEx [USD/kWh-yr]
            'life': life,  # maximum life [yr]
            'fail_prob': 0.014,  # probability of failure
            'data': 0,  # no datasets were used
            'is_re': False  # nonrenewable
        }
        settings.update(kwargs)  # replace default settings with input settings

        # initialize base class
        super().__init__(**settings)

        # get thermal load module
        self.th_module = th_module

        # adjustable diesel plant parameters
        self.life_hr = life_hr  # hours of operation before replacement [h]
        self.fl_int = kwargs.pop('fl_int', 0.08)  # intercept [L/kWh]
        self.fl_slp = kwargs.pop('fl_slp', 0.25)  # slope [L/kWh]
        self.fl_den = kwargs.pop('fl_den', 820)  # density [kg/m^3]
        self.fl_lhv = kwargs.pop('fl_lhv', 43.2)  # lower heating value [MJ/kg]
        self.min_ratio = kwargs.pop('min_ratio', 0.1)  # ratio of min pow to ld

        # adjustable economic parameters
        self.opex_hr = opex_hr  # hourly opex [USD/hr]
        self.fl_cost = fl_cost  # initial fuel cost [USD/L]
        self.fl_infl = fl_infl  # inflation rate of fuel

        # update initialized parameters if essential data is complete
        self._update_config()

    def calc_pow(self, pow_req, hr):
        """Returns the power output [kW] of the component given the minimum
        required power [kW] and timestep.

        Parameters
        ----------
        pow_req : ndarray
            Minimum required power [kW].
        hr : int
            Time [h] in the simulation.

        Returns
        -------
        ndarray
            The power output [kW] of the component.

        """
        # calculate generated power [kW]
        pow_gen = np.minimum(  # cannot generate higher than size
            np.maximum(  # cannot generate lower than minimum loading
                pow_req,
                self.min_ratio*self.size
            ),
            self.size
        )

        return pow_gen

    def rec_pow(self, pow_rec, hr):
        """Records the power at a specified time step.

        Parameters
        ----------
        pow_rec : ndarray
            Power [kW] sto be recorded into self.pow.
        hr : int
            Time [h] in the simulation.

        """
        # calculate fuel consumption [L/h]
        self.fl_tot += (  # total fuel consumption [L]
            self.fl_int*self.size*(pow_rec != 0) +
            self.fl_slp*pow_rec
        )

        # record power generated [kW]
        self.pow = pow_rec  # instantaneous power [kW]
        self.enr_tot += pow_rec  # total energy [kWh]

        # record diesel use
        self.use_tot += pow_rec != 0  # +1 if fuel was used in timestep

        # update thermal load
        self._update_th_module(pow_rec, hr)

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

        def annfl_func(i):
            """Annunity factor for fuel"""
            return ((1+self.fl_infl)/(1+infl))**i

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

        # variable operating costs [USD], time [h] based
        if callable(self.opex_hr):
            opex_hr = self.use_tot*np.sum(
                self.opex_hr(i)*ann_func(i)
                for i in np.arange(1, yr_proj+1)
            )
        else:
            opex_hr = self.opex_hr*self.use_tot*np.sum(
                1/(1+infl)**np.arange(1, yr_proj+1)
            )

        # total operating costs [USD]
        self.cost_o = opex_fix+opex_var+opex_hr

        # calculate replacement frequency [yr]
        if self.life == 0 or self.life is None:  # do not consider yearly life
            rep_life = np.inf*np.ones(self.num_case)
        else:
            rep_life = self.life*np.ones(self.num_case)
        if self.life_hr == 0 or self.life_hr is None:  # dont consider hr life
            rep_hr = np.inf*np.ones(self.num_case)
        else:
            rep_hr = self.life_hr/np.sum(self.pow > 0, axis=0)
        rep_freq = np.minimum(rep_life, rep_hr)  # replace due to max life

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

        # fuel costs [USD]
        if callable(self.fl_cost):
            self.cost_f = self.fl_tot*np.sum(
                self.fl_cost(i)*annfl_func(i)
                for i in np.arange(1, yr_proj+1)
            )
        else:
            self.cost_f = self.fl_tot*self.fl_cost*np.sum(
                    ((1+self.fl_infl)/(1+infl)) **
                    np.arange(1, yr_proj+1)
                )

        # total cost [USD]
        self.cost = self.cost_c+self.cost_o+self.cost_r+self.cost_f

    def _update_th_module(self, pow_ds, hr):
        """Updates the thermal module

        Parameters
        ----------
        pow_ds : ndarray
            Power generated by this component.
        hr : int
            Time [h] in the simulation.

        """
        # check if module exists and does not go beyond array size
        if self.th_module is not None and hr != 8759:

            # calculate efficiency
            ds_eff = 3600*pow_ds/(
                self.fl_den*self.fl_lhv *
                (self.fl_int*self.size+self.fl_slp*pow_ds)
            )

            # calculate thermal energy produced
            pow_th = np.nan_to_num(  # turn nans to zeros
                pow_ds*(1-ds_eff)*self.th_module.rec_ratio/ds_eff
            )

            # lower thermal load
            self.th_module.pow_red = np.maximum(
                self.th_module.pow_ld[hr+1]-pow_th,
                0  # cannot go lower than zero
            )
