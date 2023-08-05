from abc import abstractmethod

import numpy as np

# ignore numpy errors
np.seterr(divide='ignore', invalid='ignore')


class Component(object):
    """Base class for energy components.

    Parameters
    ----------
    capex : float
        Capital expenses [USD/kW] or [USD/kWh]. Depends on size.
    opex_fix : float
        Fixed yearly operating expenses [USD/kW-yr] or [USD/kWh-yr]. Depends
        on size.
    opex_var : float
        Variable yearly operating expenses [USD/kWh-yr]. Depends on energy
        produced.
    repex : float
        Replacement costs [USD/kW] or [USD/kWh]. Depends on size. Equal to
        CapEx by default.
    life : float
        Maximum life [yr] before the component is replaced.
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
        Size of the component [kW]. This is set by the Control module.
    data : ndarray
        Dataset. No dataset is required for this component.
    is_re : bool
        True if the resource is renewable.

    """

    def __init__(self, **kwargs):
        """Initializes the base class."""

        # adjustable essential parameters
        self.num_case = kwargs.pop('num_case', None)  # num of cases to simu
        self.data = kwargs.pop('data', None)  # project lifetime [yr]
        self.size = kwargs.pop('size', None)  # size of component [kW] or [kWh]
        self.is_re = kwargs.pop('is_re', None)  # True if renewable

        # adjustable graphing parameters
        self.name_solid = kwargs.pop('name_solid', None)  # label of solid
        self.color_solid = kwargs.pop('color_solid', None)  # color of solid
        self.name_line = kwargs.pop('name_line', None)  # label of line
        self.color_line = kwargs.pop('color_line', None)  # color of line

        # initialize component parameters
        self.pow = np.array([])  # instantaneous power [kW] of component
        self.enr_tot = np.array([])  # total energy output [kWh] of component

        # adjustable economic parameters
        self.capex = kwargs.pop('capex', 0)  # capital cost [USD/kW(h)]
        self.opex_fix = kwargs.pop('opex_fix', 0)  # fixed OpEx [USD/kW(h)-y]
        self.opex_var = kwargs.pop('opex_var', 0)  # variable OpEx [USD/kWh]
        self.repex = kwargs.pop('repex', self.capex)  # replacement [USD/kW(h)]
        self.life = kwargs.pop('life', 0)  # lifetime [yr] of the component

        # initialize cost parameters
        self.cost_c = np.array([])  # capital cost [USD] of component
        self.cost_o = np.array([])  # operating cost [USD] of component
        self.cost_r = np.array([])  # replacement cost [USD] of component
        self.cost_f = np.array([])  # fuel cost [USD] of component
        self.cost = np.array([])  # total cost [USD] of component

        # adjustable failure parameters
        self.fail_prob = kwargs.pop('fail_prob', 0.0)  # prob of failure

        # initialize failure parameters
        self.fail = np.array([])  # prob of failure

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
        pass

    @abstractmethod  # implementation required
    def cost_calc(self, yr_proj, infl):
        """Calculates the cost of the component.

        Parameters
        ----------
        yr_proj : float
            Project lifetime [yr].
        infl : float
            Inflation rate.

        """
        pass

    def fail_calc(self):
        """Calculates the probability of failure of the component."""
        # set default value of failure probability
        self.fail = self.fail_prob*np.ones(self.num_case)

    def get_pow(self, hr):
        """Returns the power output [kW] at the specified time [h].

        Parameters
        ----------
        hr : int
            Time [h] in the simulation.

        """
        pass

    def set_data(self, data):
        """Changes the dataset to be used by the component. Used by the Control module.

        Parameters
        ----------
        data : ndarray
            Dataset to be used by the component.

        """
        # set dataset
        self.data = data

        # update initialized parameters if essential data is complete
        self._update_config()

    def set_num(self, num_case):
        """Changes the number of cases to simulate. Used by the Control module.

        Parameters
        ----------
        num_case : int
            Number of scenarios to simultaneously simulate. This is set by the
            Control module.

        """
        # set number of cases
        self.num_case = num_case

        # update initialized parameters if essential data is complete
        self._update_config()

    def set_size(self, size):
        """Changes the size of the components. Used by the Control module.

        Parameters
        ----------
        size : int
            Size of the component [kWh]. This is set by the Control module.

        """
        # set sizes [kW] or [kWh]
        self.size = np.atleast_1d(size)  # must be in array form

        # update initialized parameters if essential data is complete
        self._update_config()

    def rec_pow(self, pow_rec, hr):
        """Records the power at a specified time step.

        Parameters
        ----------
        pow_rec : ndarray
            Power [kW] to be recorded by component.
        hr : int
            Time [h] in the simulation.

        """
        pass

    @abstractmethod  # implementation required
    def _config(self):
        """Updates other parameters once essential parameters are complete."""

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
            self.enr_tot = np.zeros(self.num_case)  # total energy output [kWh]

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
