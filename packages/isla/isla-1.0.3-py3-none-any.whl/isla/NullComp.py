import numpy as np

from .Component import Component

# ignore numpy errors
np.seterr(divide='ignore', invalid='ignore')


class NullComp(Component):
    """Placeholder module. This is used by the Control module if a type of
    component is not present.

    """

    def __init__(self):
        """Initializes the base class."""

        # initialize base class
        settings = {
            'size': 0,  # no size needed, must not be None
            'num_case': 0,  # no number of cases needed, must not be None
            'data': 0  # no dataset needed, must not be None
        }

        # initialize base class
        super().__init__(**settings)

        # storage parameters
        self.dod_max = 1

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
        # placeholder does not provide power
        return np.zeros(self.num_case)

    def get_pow(self, hr):
        """Returns the power output [kW] at the specified time [h].

        Parameters
        ----------
        hr : int
            Time [h] in the simulation.

        """
        # placeholder does not provide power
        return np.zeros(self.num_case)

    def rec_pow(self, pow_dc, hr):
        """Records the power at a specified time step.

        Parameters
        ----------
        pow_rec : ndarray
            Power [kW] sto be recorded into self.pow.
        hr : int
            Time [h] in the simulation.

        """
        # placeholder does nothing
        pass

    def cost_calc(self, yr_proj, infl):
        """Calculates the cost of the component.

        Parameters
        ----------
        yr_proj : float
            Project lifetime [yr].
        infl : float
            Inflation rate.

        """
        # placeholder does nothing
        pass

    def _config(self):
        """Updates other parameters once essential parameters are complete."""

        # update battery parameters
        # Control module asks for these for a StorageComponent
        self.pow_maxc = np.zeros(self.num_case)  # maximum charge pow [kW]
        self.pow_maxdc = np.zeros(self.num_case)  # maximum discharge pow [kW]
        self.soc = np.ones(self.num_case)  # SOC
        self.is_full = np.ones(self.num_case, dtype=bool)  # True if full
