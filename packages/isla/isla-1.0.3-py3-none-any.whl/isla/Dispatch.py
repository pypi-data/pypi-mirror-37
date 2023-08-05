from abc import abstractmethod

import numpy as np

from .Connector import Connector
from .FixedComponent import FixedComponent
from .AdjustComponent import AdjustComponent
from .StorageComponent import StorageComponent
from .LoadComponent import LoadComponent
from .GridComponent import GridComponent
from .Component import Component
from .FixedConnector import FixedConnector
from .AdjustConnector import AdjustConnector
from .StorageConnector import StorageConnector
from .LoadConnector import LoadConnector
from .GridConnector import GridConnector
from .NullComp import NullComp


class Dispatch(object):
    """Base class for dispatch strategies.

    Parameters
    ----------
    comp_list : list of Component
        List of initialized components.
    size : dict
        Sizes [kW] or [kWh] of the components. Use component objects as
        keys and sizes as values.
    spin_res : float
        Spinning reserve.

    """

    def __init__(self, comp_list, size, spin_res):
        """Initializes the base class."""

        # store parameters
        self.comp_list = comp_list
        self.size = size
        self.spin_res = spin_res

        # make placeholders if component is not present
        self.fx_null = NullComp()
        self.ad_null = NullComp()
        self.st_null = NullComp()
        self.gd_null = NullComp()

        # initialize list of components
        fx_list = []
        ad_list = []
        st_list = []
        ld_list = []
        gd_list = []

        # sort components in comp_list into lists
        for cp in comp_list:
            if isinstance(cp, FixedComponent):
                fx_list.append(cp)
            elif isinstance(cp, AdjustComponent):
                ad_list.append(cp)
            elif isinstance(cp, StorageComponent):
                st_list.append(cp)
            elif isinstance(cp, LoadComponent):
                ld_list.append(cp)
            elif isinstance(cp, GridComponent):
                gd_list.append(cp)

        # append the null components if component is absent
        if not fx_list:  # empty list
            fx_list.append(self.fx_null)
            size.update({self.fx_null: 0})
        if not ad_list:
            ad_list.append(self.ad_null)
            size.update({self.ad_null: 0})
        if not st_list:
            st_list.append(self.st_null)
            size.update({self.st_null: 0})
        if not ld_list:  # no load
            raise ValueError('No load was given.')  # load needed
        if not gd_list:
            gd_list.append(self.gd_null)
            size.update({self.gd_null: 0})

        # create connectors
        self.fx = FixedConnector(fx_list)
        self.ad = AdjustConnector(ad_list)
        self.st = StorageConnector(st_list)
        self.ld = LoadConnector(ld_list)
        self.gd = GridConnector(gd_list)

        # determine number of cases to simulate
        num_case = np.atleast_1d(list(size.values())[0]).size

        # initialize connectors
        cn_dict = {  # gives correspondin list wit component
            self.fx: fx_list, self.ad: ad_list, self.st: st_list,
            self.gd: gd_list, self.ld: ld_list
        }
        for cn in [self.fx, self.ad, self.st, self.gd, self.ld]:
            cn.set_num(num_case)  # number of cases to simulate
            if cn is not self.ld:
                cp_dict = dict((i, size[i]) for i in cn_dict[cn] if i in size)
                cn.set_size(cp_dict)  # sizes of components

        # initialize
        self.pow_def = np.zeros(num_case)  # power deficit
        self.num_def = np.zeros(num_case)  # number of deficits
        self.feas = np.ones(num_case, dtype=bool)  # feasibility array
        self.hr = 0  # timestep [hr]

    @abstractmethod  # implementation required
    def step(self):
        """Increments the timestep."""

        pass
