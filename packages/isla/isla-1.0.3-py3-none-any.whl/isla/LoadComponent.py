from abc import abstractmethod

import numpy as np

from .Component import Component

# ignore numpy errors
np.seterr(divide='ignore', invalid='ignore')


class LoadComponent(Component):
    """Base class for load components.

    Parameters
    ----------
    capex : float
        Capital expenses [USD/kW]. Depends on size.
    opex_fix : float
        Fixed yearly operating expenses [USD/kW-yr]. Depends on size.
    opex_var : float
        Variable yearly operating expenses [USD/kWh-yr]. Depends on energy
        produced.
    repex : float
        Replacement costs [USD/kW]. Depends on size. Equal to CapEx by
        default.
    life : float
        Maximum life [yr] before the component is replaced
    fail_prob : float
        Probability of failure of the component
    name_line : str
        Label for the load demand. This will be used in generated graphs
        and files.
    color_line : str
        Hex code (e.g. '#33CC33') of the color for the load demand. This
        will be used in generated graphs.

    """

    def __init__(self, **kwargs):
        """Initializes the base class.

        """
        # initialize component
        super().__init__(**kwargs)

    @abstractmethod  # implementation required
    def cost_calc(self):
        """Calculates the cost of the component.

        """
        pass

    @abstractmethod  # implementation required
    def get_pow(self, hr):
        """Returns the power output [kW] at the specified time [h].

        Parameters
        ----------
        hr : int
            Time [h] in the simulation.

        """
        pass

    @abstractmethod  # implementation required
    def _config(self):
        """Updates other parameters once essential parameters are complete.

        """
        pass

    def _update_config(self):
        """Updates some parameters once essential parameters are complete."""

        # check if all essential parameters are in
        if (
            self.num_case is not None and  # number of cases to simulate
            self.size is not None and  # size [kW] or [kWh]
            self.data is not None  # dataset
        ):
            # update component parameters
            self.pow = np.zeros(self.num_case)  # instantaneous power [kW]

            # update cost parameters
            self.cost_c = np.zeros(self.num_case)  # CapEx [USD] of component
            self.cost_o = np.zeros(self.num_case)  # OpEx [USD] of component
            self.cost_r = np.zeros(self.num_case)  # repl cost [USD] of comp
            self.cost_f = np.zeros(self.num_case)  # fuel cost [USD] of comp
            self.cost = np.zeros(self.num_case)  # total cost [USD] of comp

            # update failure parameters
            self.fail = np.zeros(self.num_case)  # prob of failure

            # update other parameters
            self._config()
