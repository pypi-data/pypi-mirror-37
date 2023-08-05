import numpy as np

from .Connector import Connector

# ignore numpy errors
np.seterr(divide='ignore', invalid='ignore')


class StorageConnector(Connector):
    """Base class for energy component connector. This is used by the Control
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

        # store comp list
        self.comp_list = comp_list
        self.size_blank = dict.fromkeys(comp_list)

        # initialize parameters
        self.soc = np.array([])  # SOC array
        self.pow_maxc = np.array([])  # max charge
        self.pow_maxdc = np.array([])  # max discharge
        self.size_tot = 0  # total size
        self.dod_max = 0  # maximum dod
        self.is_full = np.array([])  # check if battery is full

    def set_num(self, num_case):
        """Changes the number of cases to simulate. Used by the Control module.

        Parameters
        ----------
        num_case : int
            Number of scenarios to simultaneously simulate. This is set by the
            Control module

        """
        # change number of cases
        for cp in self.comp_list:
            cp.set_num(num_case)

        # set power and soc array
        self.soc = np.ones(num_case)

        # set number of cases
        self.num_case = num_case
        self.pow = np.zeros(num_case)  # instantaneous power [kW]
        self.enr_tot = np.zeros(num_case)  # total energy output [kWh]

        # array to check if battery is full
        self.is_full = np.ones(self.num_case, dtype=bool)

        # update initialized parameters if essential data is complete
        self._update_config()

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

        # update initialized parameters if essential data is complete
        self._update_config()

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
        self.pow = pow_rec
        self.enr_tot += pow_rec

        # initialize
        self.pow_maxc = 0
        self.pow_maxdc = 0

        for cp in self.comp_list:

            # determine if charging (-) or discharging (+)
            is_dc = pow_rec >= 0
            is_c = pow_rec < 0
            pow_dc = pow_rec*is_dc
            pow_c = -pow_rec*is_c

            # calculate (dis)charge for component
            cp_dc = is_dc*np.minimum(cp.pow_maxdc, pow_dc)
            cp_c = is_c*np.minimum(cp.pow_maxc, pow_c)

            # calculate remaining power to distribute
            pow_rec[is_dc] = pow_rec[is_dc]-cp_dc[is_dc]
            pow_rec[is_c] = pow_rec[is_c]+cp_c[is_c]

            # record power
            cp.rec_pow(cp_dc-cp_c, hr)

            # calculate SOC: sum(soc_i*size_i)/(total size)
            self.soc += cp.soc*np.nan_to_num(cp.size/self.size_tot)

            # calculate max charge and discharge
            self.pow_maxc += cp.pow_maxc
            self.pow_maxdc += cp.pow_maxdc

            # check if full
            self.is_full = np.logical_and(self.is_full, cp.is_full)

    def _update_config(self):
        """Updates some parameters once essential parameters are complete."""

        if (  # check ALL parameters to make sure pow_maxdc is calculated
            self.num_case != 0 and  # nonzero num_case
            not any(i is None for i in list(self.size.values()))  # sizes
        ):
            # set powers
            self.pow_maxc = np.zeros(self.num_case)
            self.pow_maxdc = 0
            self.dod_max = 0
            for cp in self.comp_list:
                self.pow_maxdc += cp.pow_maxdc
                sz_rat = cp.size/self.size_tot
                sz_rat[self.size_tot == 0] = 1  # prevents errors with NullComp
                self.dod_max += cp.dod_max*sz_rat
