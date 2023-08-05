import numpy as np

from .FixedComponent import FixedComponent

# ignore numpy errors
np.seterr(divide='ignore', invalid='ignore')


class VRBPower(FixedComponent):
    """Vanadium redox flow battery (VRB) plant module.

    Parameters
    ----------
    capex : float or callable
        Capital expenses [USD/kWh]. Depends on size. Can be a callable
        function that returns capital cost starting from year zero to end of
        project lifetime.
    opex_fix : float or callable
        Fixed yearly operating expenses [USD/kWh-yr]. Depends on size. Can be
        a callable function that returns the fixed operating cost starting
        from year zero to end of project lifetime.
    life : float
        Maximum life [yr] before the component is replaced

    Other Parameters
    ----------------
    repex : float or callable
        Replacement costs [USD/kWh]. Depends on size. Equal to CapEx by
        default. Can be a callable function that returns replacement costs
        starting from year zero to end of project lifetime.
    num_case : int
        Number of scenarios to simultaneously simulate. This is set by the
        Control module
    size : int
        Size of the component [kWh]. This is set by the Control module.
    data : ndarray
        Dataset. No dataset is required for this component.

    Notes
    -----
    This module models only the power [kW] of the VRB. A VRBEnergy module
    should also be initialized to model the energy [kWh].

    """

    def __init__(self, capex=150.0, opex_fix=6.0, life=10.0, **kwargs):
        """Initializes the base class."""

        # base class parameters
        settings = {
            'name_solid': 'VRB Power',  # label for power output
            'capex': capex,  # CapEx [USD/kW]
            'opex_fix': opex_fix,  # size-dependent OpEx [USD/kW-yr]
            'life': life,  # maximum battery life [yr]
            'data': 0,  # no datasets were used
            'is_re': True  # renewable
        }
        settings.update(kwargs)  # replace default settings with input settings

        # initialize base class
        super().__init__(**settings)

        # update initialized parameters if essential data is complete
        self._update_config()

    def get_pow(self, hr):
        """This is here to maintain the functionality of the Control module.
        All power should be recorded in the VRBEnergy module.

        """
        return np.zeros(self.num_case)

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
            self.cost_o = self.size*np.sum(
                self.opex_fix(i)*ann_func(i)
                for i in np.arange(1, yr_proj+1)
            )
        else:
            self.cost_o = self.opex_fix*self.size*np.sum(
               1/(1+infl)**np.arange(1, yr_proj+1)
            )

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
