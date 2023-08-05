import numpy as np
from scipy.stats import linregress
from scipy.interpolate import InterpolatedUnivariateSpline

from .StorageComponent import StorageComponent

# ignore numpy errors
np.seterr(divide='ignore', invalid='ignore')


class H2Storage(StorageComponent):
    """Hydrogen storage module.

    Parameters
    ----------
    fc_module : HydrogenPower
        The corresponding fuel cell module for the hydrogen module.
    el_module : HydrogenPower
        The corresponding electrolyzer module for the hydrogen module.
    eff_c : float
        Charging efficiency.
    eff_dc : float
        Discharging efficiency.
    dod_max : float
        Maximum depth of discharge (DOD).
    capex : float
        Capital expenses [USD/kWh]. Depends on size.
    opex_fix : float
        Fixed yearly operating expenses [USD/kWh-yr]. Depends on size.
    opex_var : float
        Variable yearly operating expenses [USD/kWh-yr]. Depends on energy
        produced.
    fl_cost : float or None
        Initial cost of fuel (hydrogen) [USD/kWh]. If the module should not
        import hydrogen fuel, set this to None.
    life : float
        Maximum life [yr] before the component is replaced

    Other Parameters
    ----------------
    repex : float
        Replacement costs [USD/kWh]. Depends on size. Equal to CapEx by
        default.
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
    size : int
        Size of the component [kWh]. This is set by the Control module.
    data : ndarray
        Dataset. No dataset is required for this component.

    Notes
    -----
    This module models only the energy [kWh] of the hydrogen system. A
    H2FuelCell and H2Electrolyzer module should also be initialized to model
    the power [kW].

    """

    def __init__(
        self, fc_module, el_module, eff_c=0.95, eff_dc=0.95, dod_max=0.9,
        capex=500.0, opex_fix=5.0, opex_var=0.0, fl_cost=None,
        life=10.0, **kwargs
    ):
        """Initializes the base class.

        """
        # base class parameters
        settings = {
            'name_solid': 'H2 Storage',  # label for power output
            'color_solid': '#0000CC',  # color for power output in powerflow
            'name_line': 'Hydrogen SOC',  # label for SOC
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

        # get fuel cell and electrolyzer module
        self.fc_module = fc_module
        self.el_module = el_module

        # initialize battery plant parameters
        self.fl_tot = np.array([])  # if more H2 is needed

        # adjustable battery plant parameters
        self.eff_c = eff_c  # charging efficiency
        self.eff_dc = eff_dc  # discharging efficiency
        self.dod_max = dod_max  # maximum DOD

        # adjustable economic parameters
        self.fl_cost = fl_cost  # initial fuel cost [USD/L]

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
        # capital costs [USD]
        self.cost_c = self.capex*self.size  # size [kWh] based

        # operating costs [USD]
        opex_fix = self.opex_fix*self.size  # size [kWh] based
        opex_var = self.opex_var*self.enr_tot  # output [kWh] based
        self.cost_o = (opex_fix+opex_var)*(
            np.sum(1/(1+infl)**np.arange(1, yr_proj+1))  # annualize
        )

        # calculate replacement frequency [yr]
        rep_freq = self.life*np.ones(self.num_case)  # replace due to max life

        # replace nan's in rep_freq to prevent errors with arange
        rep_freq[np.isnan(rep_freq)] = yr_proj+1  # no replacement

        # replacement costs [USD], size [kWh] based
        disc_rep = np.zeros(self.num_case)  # initialize sum of annuity factors
        for i in range(0, self.num_case):
            disc_rep[i] = np.sum(
                1/(1+infl) **
                np.arange(0, yr_proj, rep_freq[i])[1:]  # remove year 0
            )
        self.cost_r = self.size*self.repex*disc_rep  # size [kWh] based

        # fuel costs [USD]
        if self.fl_cost is not None:
            self.cost_f = (
                self.fl_tot*self.fl_cost *  # fuel cons [L]
                np.sum(  # sum of annuity factors
                    1/(1+infl) **
                    np.arange(1, yr_proj+1)
                )
            )
        else:
            self.cost_f = np.zeros(self.num_case)

        # total cost [USD]
        self.cost = self.cost_c+self.cost_o+self.cost_r+self.cost_f

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
        self.pow = pow_rec*(pow_rec > 0)  # positive power (discharge only)
        self.enr_tot += self.pow

        # determine power [kW] going in or out of each battery
        pow_in = pow_rec*(pow_rec < 0)*self.eff_c
        pow_out = pow_rec*(pow_rec > 0)/self.eff_dc

        # solve for the SOC
        self._update_soc(pow_out+pow_in, hr)  # updates self.soc[hr+1, :]

        # update max powers [kW]
        self._update_max_pow(hr)  # updates self.powmaxc, self.powmaxdc

    def _config(self):
        """Updates other parameters once essential parameters are complete.

        """
        # update battery plant parameters
        self.is_full = np.ones(self.num_case, dtype=bool)  # True if batt full
        self.fl_tot = np.zeros(self.num_case)  # extra H2 if need more

        # update max powers
        self.pow_maxc = np.zeros(self.num_case)  # max charging power [kW]
        self.pow_maxdc = self.size*self.dod_max  # max discharging power [kW]
        self._update_max_pow(-1)  # recalculate max powers

    def _update_soc(self, pow_dc, hr):
        """Updates the state of charge of the battery.

        Parameters
        ----------
        pow_dc : ndarray
            Power [kW] drawn from the battery.
        hr : int
            Time [h] in the simulation.

        """
        # prevent hr+1 from going beyond array size
        if hr != 8759:

            # update SOC
            # put nan_to_num to avoid error when size is zero
            soc_new = np.minimum(
                np.nan_to_num(self.soc-pow_dc/self.size),
                1  # maximum SOC
            )

            # check for cases where battery is about to go below min SOC
            is_trn = soc_new < 1-self.dod_max

            # import additional fuel [kWh] if needed
            self.fl_tot += is_trn*(1-self.dod_max-soc_new)*self.size

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

            # maximum charge power [kW] depends on power rating
            maxc_cap = np.maximum(  # max c due to SOC
                self.size*(1-self.soc),
                0
            )
            maxc_pow = self.el_module.size  # max c due to el
            self.pow_maxc = np.minimum(maxc_cap, maxc_pow)

            # calculate maximum discharge [kW]
            if self.fl_cost is not None:  # import hydrogen fuel

                # maximum discharge power [kW] depends on fuel cell
                self.pow_maxdc = self.fc_module.size

            else:  # do not import hydrogen

                # maximum discharge power [kW] depends on power rating
                maxdc_cap = np.maximum(  # max dc due to SOC
                    self.size *
                    (self.soc-(1-self.dod_max)),
                    0
                )
                maxdc_pow = self.fc_module.size  # max dc due to fc
                self.pow_maxdc = np.minimum(maxdc_cap, maxdc_pow)
