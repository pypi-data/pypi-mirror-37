import numpy as np

from .Connector import Connector


class GridConnector(Connector):
    """Base class for grid component connector. This is used by the Control
    module to manipulate components simultaneously.

    Parameters
    ----------
    comp_list : list
        List of initialized component objects.

    """

    def __init__(self, comp_list):
        """Initializes the base class."""

        # initialize base class
        super().__init__(comp_list)

        # initialize parameters
        self.pow_nmt = np.array([])  # power for net metering [kW]
        self.enr_nmt = np.array([])  # energy for net metering [kWh]

    def set_size(self, size):
        """Changes the size of the components. Used by the Control module.

        Parameters
        ----------
        size : dict
            Sizes [kWh] of the components. Use component objects as keys and
            sizes as values.

        """
        # reset total size
        self.size_tot = 0

        # iterate per component
        for cp in self.comp_list:
            cp.set_size(size[cp])  # set size of individual module
            self.size[cp] = size[cp]  # record in size matrix
            self.size_tot = self.size_tot+size[cp]

    def set_num(self, num_case):
        """Changes the number of cases to simulate. Used by the Control module.

        Parameters
        ----------
        num_case : int
            Number of scenarios to simultaneously simulate. This is set by the
            Control module.

        """
        # change number of cases
        for cp in self.comp_list:
            cp.set_num(num_case)

        # change number of cases
        self.num_case = num_case
        self.pow = np.zeros(num_case)  # instantaneous power [kW]
        self.pow_nmt = np.zeros(num_case)  # net metering [kW]
        self.enr_tot = np.zeros(num_case)  # total energy output [kWh]
        self.enr_nmt = np.zeros(num_case)  # net metering [kWh]

    def rec_pow(self, pow_rec, hr):
        """Records the power at a specified time step.

        Parameters
        ----------
        pow_rec : ndarray
            Power [kW] sto be recorded into self.pow[hr, :]
        hr : int
            Time [h] in the simulation.

        """
        # record power generated [kW]
        self.pow = np.minimum(pow_rec*(pow_rec > 0), self.size_tot)
        self.enr_tot += self.pow
        self.pow_nmt = np.minimum(pow_rec*(pow_rec < 0), self.size_tot)
        self.enr_nmt += self.pow_nmt

        for cp in self.comp_list:

            # determine if charging (-) or discharging (+)
            is_dc = pow_rec >= 0
            is_c = pow_rec < 0
            pow_dc = pow_rec*is_dc
            pow_c = -pow_rec*is_c

            # calculate (dis)charge for component
            cp_dc = is_dc*np.minimum(cp.size, pow_dc)
            cp_c = is_c*np.minimum(cp.size, pow_c)

            # calculate remaining power to distribute
            pow_rec[is_dc] = pow_rec[is_dc]-cp_dc[is_dc]
            pow_rec[is_c] = pow_rec[is_c]+cp_c[is_c]

            # record power
            cp.rec_pow(cp_dc-cp_c, hr)
