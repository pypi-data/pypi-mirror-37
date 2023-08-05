import numpy as np

from .FixedComponent import FixedComponent

# ignore numpy errors
np.seterr(divide='ignore', invalid='ignore')


class H2Electrolyzer(FixedComponent):
    """Hydrogen electrolyzer module.

    Parameters
    ----------
    capex : float
        Capital expenses [USD/kW]. Depends on size.
    opex_fix : float
        Fixed yearly operating expenses [USD/kW-yr]. Depends on size.
    repex : float
        Replacement costs [USD/kW]. Depends on size. Equal to CapEx by default.
    life : float
        Maximum life [yr] before the component is replaced

    Other Parameters
    ----------------
    num_case : int
        Number of scenarios to simultaneously simulate. This is set by the
        Control module.
    yr_proj : int
        Project lifetime [yr]. This is set by the Control module.
    size : int
        Size of the component [kWh]. This is set by the Control module.
    infl : float
        Inflation rate. This is set by the Control module.
    data : ndarray
        Dataset. No dataset is required for this component.

    Notes
    -----
    This module models only the charging power [kW] of the hydrogen system. A
    H2Storage and H2FuelCell module should also be initialized to model the
    energy [kWh] and discharge power respectively.

    """

    def __init__(self, capex=150.0, opex_fix=6.0, life=10.0, **kwargs):
        """Initializes the base class."""

        # base class parameters
        settings = {
            'name_solid': 'H2 Electrolyzer',  # label for power output
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
        """This is here to maintain the functionality of the Control module."""
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

        # capital costs [USD], size [kW] based
        if callable(self.capex):  # if experience curve is given
            self.cost_c = np.atleast_1d(self.capex(0)*self.size)
        else:  # if fixed value is given
            self.cost_c = self.capex*self.size

        # operating costs [USD]
        if callable(self.opex_fix):
            opex_fix = self.size*np.sum(
                self.opex_fix(i)*ann_func(i)
                for i in np.arange(1, yr_proj+1)
            )
        else:
            opex_fix = self.opex_fix*self.size*np.sum(
               1/(1+infl)**np.arange(1, yr_proj+1)
            )

        # calculate replacement frequency [yr]
        rep_freq = self.life*np.ones(self.num_case)  # replacement frequency

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
    def exp_curve(yr, yr_0=2016, **kwargs):
        """Experience curve for Solar PV.
        Returns the cost [USD/kW] at the given year.

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
        a = kwargs.pop('a', 3762)
        b = kwargs.pop('b', 0.282)

        # calculate cost [USD/kWh]
        cap = a_sat/(1+(a_sat-a_base)/a_base*np.exp(-r*(yr+(yr_0-2011))))
        cost = a*cap**(-b)

        return cost
