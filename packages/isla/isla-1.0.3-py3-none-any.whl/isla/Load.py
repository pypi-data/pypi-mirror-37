import numpy as np
from scipy.stats import norm

from .LoadComponent import LoadComponent

# ignore numpy errors
np.seterr(divide='ignore', invalid='ignore')


class Load(LoadComponent):
    """Load module.

    Parameters
    ----------
    data : dict or ndarray
        Dataset. Pass a dict with 'load' as the key for the hourly load demand
        [kW] for one year. An ndarray can be passed as well.

    Other Parameters
    ----------------
    name_line : str
        Label for the load demand. This will be used in generated graphs and
        files.
    color_line : str
        Hex code (e.g. '#33CC33') of the color for the load demand. This will
        be used in generated graphs.
    num_case : int
        Number of scenarios to simultaneously simulate. This is set by the
        Control module.
    stat_data : dict, str, or None
        Statistical data used for load variance. Set to None to remove load
        variability. Set to 'auto' to automatically make noise based on
        dataset. Pass a dict with 'var' as key and variance as value to
        manually adjust noise.

    """

    def __init__(self, data, **kwargs):
        """Initializes the base class."""

        # base class parameters
        settings = {
            'name_line': 'Load',  # label for load
            'color_line': '#666666',  # color for load in powerflow
            'capex': 0.0,  # CapEx [USD/kWh]
            'opex_fix': 0.0,  # size-dependent OpEx [USD/kWh-yr]
            'opex_var': 0.0,  # output-dependent OpEx [USD/kWh-yr]
            'size': 0.0,  # no size needed, must not be None
            'data': data  # dataset
        }
        settings.update(kwargs)  # replace default settings with input settings

        # initialize base class
        super().__init__(**settings)

        # extract dataset
        if isinstance(self.data, dict):  # pass dict
            self.pow_ld = self.data['load']  # load [kW]
        elif isinstance(self.data, np.ndarray):  # pass ndarray
            self.pow_ld = self.data

        # convert dataset to 1D array
        self.pow_ld = np.ravel(self.pow_ld)

        # derivable load parameters
        self.pow_max = np.max(self.pow_ld)  # largest power in load [kW]
        self.enr_tot = np.sum(self.pow_ld)  # yearly consumption [kWh]

        # adjustable reliability parameters
        self.stat_data = kwargs.pop('stat_data', None)

        # initalize reliability parameters
        self.stat_var = 0.0

        # update initialized parameters if essential data is complete
        self._update_config()

    def get_pow(self, hr):
        """Returns the power output [kW] at the specified time [h].

        Parameters
        ----------
        hr : int
            Time [h] in the simulation.

        """
        # check if noise has to be simulated
        if self.stat_data is None:
            noise = 1
        elif self.stat_data == 'auto':
            noise = 1+np.random.normal(
                0.0, self.stat_var[hr % 24], self.num_case
            )
        else:
            noise = 1+np.random.normal(
                0.0, self.stat_var, self.num_case
            )

        # record power
        self.pow = self.pow_ld[hr]*np.ones(self.num_case)*noise

        # get data from the timestep
        return self.pow

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

    def _config(self):
        """Updates other parameters once essential parameters are complete."""

        # update reliability parameters
        if isinstance(self.stat_data, dict):
            self.stat_var = self.stat_data['var']
        elif self.stat_data == 'auto':
            self.stat_var = self._stat_solve()

    def _stat_solve(self):
        """Solves for parameters for reliability calculations."""

        # solve for variance between hours per day
        var_list = []  # list of variances
        norm_arr = self.pow_ld/np.max(self.pow_ld)  # normalize
        for i in range(24):
            loc_i, var_i = norm.fit(norm_arr[i::24])  # variance per hour
            var_list.append(var_i)  # append variance

        return np.array(var_list)
