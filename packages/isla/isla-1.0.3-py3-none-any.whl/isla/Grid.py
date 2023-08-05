import numpy as np

from .GridComponent import GridComponent

# ignore numpy errors
np.seterr(divide='ignore', invalid='ignore')


class Grid(GridComponent):
    """Grid module.

    Parameters
    ----------
    capex : float
        Capital expenses [USD].
    opex_fix : float
        Fixed yearly operating expenses [USD/yr].
    rate_use : float
        Price [USD/kWh] of drawing power from the grid.
    rate_nmt : float
        Sellback rate [USD/kWh] for giving power to the grid.
    life : float
        Maximum life [yr] before the component is replaced.

    Other Parameters
    ----------------
    repex : float
        Replacement costs [USD]. Equal to CapEx by default.
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
        Size of the component [kWh]. This is set by the Control module.
    data : ndarray
        Dataset. No dataset is required for this component.

    """

    def __init__(
        self, capex=0.0, opex_fix=0.0, rate_use=0.4,
        rate_nmt=0.1, life=20.0, **kwargs
    ):
        """Initializes the base class.

        """
        # base class parameters
        settings = {
            'name_solid': 'Grid',  # label for power output
            'color_solid': '#333333',  # color for power output in powerflow
            'capex': capex,  # CapEx [USD]
            'opex_fix': opex_fix,  # fixed OpEx [USD/yr]
            'life': life,  # maximum life [yr]
            'data': 0,  # no datasets were used
            'is_re': False  # nonrenewable
        }
        settings.update(kwargs)  # replace default settings with input settings

        # initialize base class
        super().__init__(**settings)

        # adjustable cost parameters
        self.rate_use = rate_use  # rate [USD/kWh]
        self.rate_nmt = rate_nmt  # sellback rate [USD/kWh]

        # update initialized parameters if essential data is complete
        self._update_config()

    def rec_pow(self, pow_dc, hr):
        """Records the power at a specified time step.

        Parameters
        ----------
        pow_rec : ndarray
            Power [kW] sto be recorded into self.pow.
        hr : int
            Time [h] in the simulation.

        """
        # record discharges
        self.pow = np.minimum(self.size, pow_dc*(pow_dc > 0))
        self.enr_tot += self.pow  # total energy [kWh]

        # record charges
        self.pow_nmt = np.minimum(self.size, -pow_dc*(pow_dc < 0))
        self.enr_nmt += self.pow_nmt

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
        self.cost_c = self.capex*np.ones(self.num_case)

        # operating costs [USD]
        opex_fix = np.atleast_1d(  # fixed OpEx [USD/yr]
            self.opex_fix*np.sum(1/(1+infl)**np.arange(1, yr_proj+1))
        )
        opex_var = (
            self.enr_tot*self.rate_use -  # grid use
            self.enr_nmt*self.rate_nmt  # net metering
        )*(np.sum(1/(1+infl)**np.arange(1, yr_proj+1)))  # annuity
        self.cost_o = opex_fix+opex_var

        # calculate replacement frequency [yr]
        rep_freq = self.life*np.ones(self.num_case)  # frequency of replacement

        # replace nan's in rep_freq to prevent errors with arange
        rep_freq[np.isnan(rep_freq)] = yr_proj+1  # no replacement

        # replacement costs [USD], size [kW] based
        disc_rep = np.zeros(self.num_case)  # initialize sum of annuity factors
        for i in range(0, self.num_case):
            disc_rep[i] = np.sum(
                1/(1+infl) **
                np.arange(0, yr_proj, rep_freq[i])[1:]  # remove year 0
            )
        self.cost_r = self.repex*disc_rep

        # total cost [USD]
        self.cost = self.cost_c+self.cost_o+self.cost_r

    def _config(self):
        """Updates other parameters once essential parameters are complete."""

        pass
