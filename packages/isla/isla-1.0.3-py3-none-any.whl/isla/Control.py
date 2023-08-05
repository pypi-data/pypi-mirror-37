import os
import itertools
import copy
import warnings
import time

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from .LoadFollow import LoadFollow
from .NullComp import NullComp
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

# ignore numpy errors
np.seterr(divide='ignore', invalid='ignore')


class Control(object):
    """Power system controller module.

    Parameters
    ----------
    comp_list : list
        List of initialized component objects.

    """

    def __init__(self, comp_list):
        """Initializes the base class."""

        # store parameters
        self.comp_list = comp_list  # list of components

        # initialize data storage
        self.algo = None  # dispatch algorithm
        self.ts = dict(  # time series data for power
            (i, np.zeros(8760)) for i in comp_list
        )
        self.ts_soc = dict(  # time series data for SOC
            (i, np.ones(8760)) for i in comp_list
            if isinstance(i, StorageComponent)
        )

        # initialize metrics arrays
        self.lcoe = np.array([])  # LCOE
        self.re_frac = np.array([])  # RE-share
        self.lolp = np.array([])

    def simu(
        self, size, spin_res=0.1, yr_proj=20.0, infl=0.1,
        proj_capex=0.0, proj_opex=0.0, algo=LoadFollow, **kwargs
    ):
        """Simulates a scenario given a set of sizes and calculates the LCOE.

        Parameters
        ----------
        size : dict
            Sizes [kW] or [kWh] of the components. Use component objects as
            keys and sizes as values.
        spin_res : float
            Spinning reserve.
        yr_proj : float
            Project lifetime [yr].
        infl : float
            Inflation rate.
        proj_capex : float
            Capital expenses [USD] of the project.
        proj_opex : float
            Fixed yearly operating expenses [USD/yr] of the project.
        algo : Dispatch
            The dispatch algorithm to be used.

        Other Parameters
        ----------------
        do_inval : bool
            True if invalid cases should have nan LCOE and RE-share.
        print_prog : bool
            True if calculation progress should be printed.
        print_out : bool
            True if results should be printed. Invokes res_print().

        Notes
        -----
        Sets LCOE to nan when the size combination is infeasible.

        """
        # get keyword arguments
        do_inval = kwargs.pop('do_inval', True)
        print_prog = kwargs.pop('print_prog', True)
        print_out = kwargs.pop('print_out', True)

        # initialize for console output
        t0 = time.time()  # time
        mark = np.arange(0, 8760, 876)  # markers for simulation

        # initialize dispatch algorithm
        al = algo(self.comp_list, size, spin_res)

        # perform simulation
        for hr in range(8760):
            al.step()  # increment simulation
            for cp in self.comp_list:
                self.ts[cp][hr] = cp.pow  # record power at timestep
                if isinstance(cp, StorageComponent):
                    self.ts_soc[cp][hr] = cp.soc  # record SOC at timestep
            if print_prog and hr in mark:  # display progress
                print(
                    'Simulation Progress: {:.0f}%'.format((hr+1)/87.6),
                    flush=True
                )

        # store completed dispatch algorithm object
        self.algo = al

        # calculate LCOE
        self.lcoe = Control._lcoe(
            al, yr_proj, infl, proj_capex, proj_opex
        )[0]

        # calculate RE-share
        pow_ldts = np.zeros(8760)  # time-series data of total load
        enr_tot = np.zeros(8760)  # total energy
        enr_re = np.zeros(8760)  # total renewable energy
        for cp in self.comp_list:
            if isinstance(cp, LoadComponent):
                pow_ldts += self.ts[cp]  # time series data of total load
        for cp in self.comp_list:
            if not isinstance(cp, LoadComponent) and cp.is_re is not None:
                ld_def = np.maximum(pow_ldts-enr_tot, 0)  # load deficit
                enr_tot += np.minimum(  # add to energy
                    self.ts[cp], ld_def  # do not go over load
                )
                if cp.is_re:  # add to RE energy
                    enr_re += np.minimum(  # add to energy
                        self.ts[cp], ld_def  # do not go over load
                    )
        self.re_frac = np.sum(enr_re)/np.sum(enr_tot)

        # check if invalid
        if do_inval and not al.feas:
            self.lcoe = np.nan
            self.re_frac = np.nan

        # print results
        if print_prog:
            t1 = time.time()
            print('Simulation completed in {:.4f} s.'.format(t1-t0))
        if print_out:
            self.res_print()

    def opt(
        self, spin_res=0.1, yr_proj=20.0, infl=0.1,
        proj_capex=0.0, proj_opex=0.0, size_max=None,
        size_min=None, algo=LoadFollow, **kwargs
    ):
        """Set component sizes such that LCOE is optimized.

        Parameters
        ----------
        spin_res : float
            Spinning reserve.
        yr_proj : float
            Project lifetime [yr].
        infl : float
            Inflation rate.
        proj_capex : float
            Capital expenses [USD] of the project.
        proj_opex : float
            Fixed yearly operating expenses [USD/yr] of the project.
        size_max : dict
            Maximum size constraint. Use the component object as keys and the
            size constraint as values.
        size_min : dict
            Minimum size constraint. Use the component object as keys and the
            size constraint as values.

        Other Parameters
        ----------------
        fx_range : tuple of float or str
            Boundaries of the search space for the sizes of fixed power
            components. Input as (min, max). Set to 'auto' to automatically
            find the search space.
        ad_range : tuple of float or str
            Boundaries of the search space for the sizes of adjustable power
            components. Input as (min, max). Set to 'auto' to automatically
            find the search space.
        st_range : tuple of float or str
            Boundaries of the search space for the sizes of energy storage
            components. Input as (min, max). Set to 'auto' to automatically
            find the search space.
        gd_range : tuple of float or str
            Boundaries of the search space for the size of the grid. Input as
            (min, max). Set to 'auto' to automatically find the search space.
        iter_simu : int
            Number of cases to simulate simultaneously.
        iter_lcoe : int
            Number of iterations to find the LCOE.
        batch_size : int
            Number of simulations to be carried out simultaneously. Prevents
            the program from consuming too much memory.
        print_lcoe : bool
            True if opimization progress should be printed.
        print_simu : bool
            True if simulation progress should be printed.
        print_res : bool
            True if results should be printed.

        """
        # get keyword arguments
        fx_range = kwargs.pop('fx_range', 'auto')
        ad_range = kwargs.pop('ad_range', 'auto')
        st_range = kwargs.pop('st_range', 'auto')
        gd_range = kwargs.pop('gd_range', 'auto')
        iter_simu = kwargs.pop('iter_simu', 10)
        iter_lcoe = kwargs.pop('iter_lcoe', 5)
        batch_size = kwargs.pop('batch_size', 10000)
        print_prog = kwargs.pop('print_prog', True)
        print_out = kwargs.pop('print_out', True)

        # initialize for console output
        t0 = time.time()  # time

        # replace constraints with empty dict if there are none
        if size_max is None:
            size_max = {}
        if size_min is None:
            size_min = {}

        # check if adj or grid components are present
        has_ad = any(isinstance(i, AdjustComponent) for i in self.comp_list)
        has_gd = any(isinstance(i, GridComponent) for i in self.comp_list)
        if has_ad or has_gd:  # no adjustable or grid components
            small_size = True  # use smaller search space
        else:
            small_size = False  # use larger search space

        # use smaller search space if adj or grid is present
        if small_size:  # based on peak
            pow_max = sum(  # sum of peak loads
                i.pow_max for i in self.comp_list
                if isinstance(i, LoadComponent)
            )
            auto_range = (0, pow_max*3.5)
        else:  # based on daily consumption
            enr_tot = sum(  # total annual load
                i.enr_tot for i in self.comp_list
                if isinstance(i, LoadComponent)
            )
            auto_range = (0, enr_tot*2/365)

        # determine number of components to be sized:
        num_comp = sum(  # load is not counted
            1 for i in self.comp_list if not isinstance(i, LoadComponent)
        )

        # initialize
        rng_list = [fx_range, ad_range, st_range, gd_range]  # ranges
        rng_dict = {}  # dict with ranges
        cls_list = [  # list of component classes
            FixedComponent, AdjustComponent,
            StorageComponent, GridComponent
        ]

        # assign auto search spaces
        for i in range(0, 4):
            if rng_list[i] == 'auto':  # replace auto ranges
                rng_list[i] = auto_range

        # create dict of ranges
        for cp in self.comp_list:
            for i in range(0, 4):
                if isinstance(cp, cls_list[i]):  # sort by component type
                    rng_dict[cp] = rng_list[i]  # copy the range

        # make a copy of the original ranges
        orig_dict = copy.deepcopy(rng_dict)

        # calculate batch size
        num_case_all = iter_simu**num_comp  # total number of cases
        num_batch = int(np.ceil(num_case_all/batch_size))  # number of batches

        # initialize for subset iteration
        size_dict = {}  # dict with sizes
        sub_dict = {}  # dict with subset of sizes
        opt_dict = {}  # dict with optimum sizes
        opt_lcoe = np.inf  # optimum LCOE

        # begin iteration
        for i in range(0, iter_lcoe):  # number of optimization loops

            # convert ranges into sizes
            for cp in rng_dict:

                # determine upper bound of component
                if cp in list(size_max.keys()):
                    ub = np.min([rng_dict[cp][1], size_max[cp]])
                else:
                    ub = rng_dict[cp][1]

                # determine lower bound of component
                if cp in list(size_min.keys()):
                    lb = np.max([rng_dict[cp][0], size_min[cp]])
                else:
                    lb = rng_dict[cp][0]

                # create range
                size_dict[cp] = np.linspace(lb, ub, num=iter_simu)

            # create generator object that dispenses size combinations
            gen = (itertools.product(*list(size_dict.values())))

            # begin iteration per batch
            for j in range(0, num_batch):

                # subset initial list of sizes
                sub_arr = np.array(list(
                    next(gen) for i in range(0, batch_size)
                ))  # extracts combinations

                # assign sizes to subset array
                comp = 0
                for cp in size_dict:
                    sub_dict[cp] = sub_arr[:, comp]
                    comp += 1

                # initialize dispatch algorithm
                # note: this modifies sub_dict by ading NullComps
                al = algo(self.comp_list, sub_dict, spin_res)

                # perform simulation
                for hr in range(0, 8760):
                    al.step()

                # calculate LCOE
                lcoe = Control._lcoe(
                    al, yr_proj, infl, proj_capex, proj_opex
                )

                # determine invalid cases
                inval = np.logical_not(al.feas)

                # continue with next loop if all invalid
                if np.all(inval):
                    continue

                # find array index of lowest valid LCOE
                lcoe[inval] = np.nan
                opt_ind = np.nanargmin(lcoe)

                # remove NullComp from sub_dict
                sub_dict = dict(
                    (i, j) for i, j in zip(sub_dict.keys(), sub_dict.values())
                    if not isinstance(i, NullComp)
                )

                # check if lcoe of this subset is lower than before
                if lcoe[opt_ind] < opt_lcoe:
                    opt_lcoe = lcoe[opt_ind]  # set optimum LCOE
                    for cp in sub_dict:  # set optimum sizes
                        opt_dict[cp] = sub_dict[cp][opt_ind]

            # prepare new list
            for cp in rng_dict:
                sep = size_dict[cp][1]-size_dict[cp][0]
                lb = np.maximum(opt_dict[cp]-sep, 0)  # new lower bound
                ub = np.maximum(opt_dict[cp]+sep, 0)  # new upper bound
                rng_dict[cp] = (lb, ub)

            # output progress
            if print_prog:
                prog = (i+1)*100/iter_lcoe
                out = 'Optimization progress: {:.2f}%'.format(prog)
                print(out, flush=True)

        # set components to optimum
        self.simu(
            opt_dict, spin_res, yr_proj, infl,
            proj_capex, proj_opex, algo,
            print_prog=False, print_out=False
        )

        # print results
        if print_prog:
            t1 = time.time()
            out = 'Optimization completed in {:.4f} min.'.format((t1-t0)/60)
            print(out, flush=True)
        if print_out:
            self.res_print()

    def rel(
        self, size, var=0.1, num_pts=100, spin_res=0.1,
        algo=LoadFollow, **kwargs
    ):
        """Simulates a scenario given a set of sizes and calculates the LCOE.

        Parameters
        ----------
        size : dict
            Sizes [kW] or [kWh] of the components. Use component objects as
            keys and sizes as values.
        var : float
            Load variance.
        num_pts : int
            Number of points to use for Monte Carlo.
        spin_res : float
            Spinning reserve.
        algo : Dispatch
            The dispatch algorithm to be used.

        Other Parameters
        ----------------
        batch_max : int
            Maximum number of simulations to be carried out simultaneously.
            Prevents the program from consuming too much memory.
        do_inval : bool
            True if invalid cases should have nan LCOE and RE-share.
        print_prog : bool
            True if calculation progress should be printed.
        print_out : bool
            True if results should be printed. Invokes res_print().
        tol : float
            Tolerance when checking if power meets the load.

        """
        # get keyword arguments
        max_size = kwargs.pop('batch_max', 10000)
        print_prog = kwargs.pop('print_prog', True)
        print_out = kwargs.pop('print_out', True)
        tol = kwargs.pop('tol', 1e-2)

        # initialize for console output
        t0 = time.time()  # time
        mark = np.arange(0, 8760, 876)  # markers for simulation

        # modify size array
        size_dict = {}
        for cp in size:
            size_dict[cp] = size[cp]*np.ones(num_pts)

        # initialize dispatch algorithm
        al = algo(self.comp_list, size_dict, spin_res)

        # create probability tables
        fail_list = []  # list of failure probabilities
        num_comp_ld = 0  # number of non-load components
        for cp in size:
            if not isinstance(cp, LoadComponent):
                fail_list.append(cp.fail_prob)  # ignore load components
                num_comp_ld += 1
        fail_list = np.array(fail_list)  # to numpy array
        comb_table = np.array(list(  # combination table
            itertools.product([0, 1], repeat=num_comp_ld)
        ))
        fail_arr = comb_table*fail_list  # probability of failure
        sucs_arr = (1-comb_table)*(1-fail_list)  # probability of success
        prob_arr = np.atleast_2d(np.prod(fail_arr+sucs_arr, axis=1)).T

        # begin simulations
        lolp = np.zeros(num_pts)
        for hr in range(8760):

            # perform step
            al.step()

            # make power table
            pow_arr = np.zeros((0, num_pts))
            for cp in size:
                if not isinstance(cp, LoadComponent):
                    pow_arr = np.append(pow_arr, np.atleast_2d(cp.pow), axis=0)
            pow_arr = np.atleast_3d(pow_arr)
            pow_arr = np.repeat(pow_arr, 2**num_comp_ld, axis=2)

            # determine power at different cases
            pow_case = np.rot90(pow_arr, axes=(0, 2))
            pow_case = np.rot90(pow_case, axes=(0, 1))*(1-comb_table)
            pow_case = np.fliplr(np.sum(pow_case, axis=2).T)

            # get probability of each case
            is_nopow = pow_case*(1+tol) < al.ld.pow
            prob_list = np.sum(is_nopow*prob_arr, axis=0)

            # add to LOLP
            lolp += prob_list

            # display progress
            if print_prog and hr in mark:
                print(
                    'Calculation Progress: {:.0f}%'.format((hr+1)/87.6),
                    flush=True
                )

        # divide by hours per year
        self.lolp = np.average(lolp/8760)

        # print results
        if print_prog:
            t1 = time.time()
            print('Simulation completed in {:.4f} s.'.format(t1-t0))
        if print_out:

            # print sizes
            print('SYSTEM SUMMARY')
            print('Sizes [kW] or [kWh]:')
            for cp in self.comp_list:
                if not isinstance(cp, LoadComponent):
                    if np.atleast_1d(cp.size).size == 1:  # one scenario only
                        print(
                            '    {:15}: {:>12.4f}'
                            .format(cp.name_solid, cp.size[0])
                        )
                    else:  # multiple scenarios simulated
                        print(
                            '    {:15}: '.format(cp.name_solid) +
                            str(cp.size[0])
                        )

            # other parameters
            print('Parameters:')
            print('    LOLP           : {:>12.4f}'.format(self.lolp))

    def powflow_plot(self, time_range=(0, 168)):
        """Generates a power flow of the system.

        Parameters
        ----------
        time_range : tuple
            Range of times to plot.

        """
        # initialize dicts
        name_solid = {}  # dict of components and names
        color_solid = {}  # dict of components and colors
        pow_solid = {}  # dict of components and powers
        name_line = {}  # dict of components and names
        color_line = {}  # dict of components and colors
        pow_line = {}  # dict of components and powers
        soc_line = {}  # dict of components and SOC

        # get names, colors, and value of each component
        for cp in self.comp_list:
            if cp.color_solid is not None:  # stacked graph for power sources
                name_solid[cp] = cp.name_solid
                color_solid[cp] = cp.color_solid
                pow_solid[cp] = self.ts[cp][time_range[0]:time_range[1]]
            if cp.color_line is not None:  # line graph for load and SOC
                if isinstance(cp, StorageComponent):  # storage has SOC
                    name_line[cp] = cp.name_line
                    color_line[cp] = cp.color_line
                    soc_line[cp] = self.ts_soc[cp][time_range[0]:time_range[1]]
                if isinstance(cp, LoadComponent):  # load
                    name_line[cp] = cp.name_line
                    color_line[cp] = cp.color_line
                    pow_line[cp] = self.ts[cp][time_range[0]:time_range[1]]

        # generate x-axis (list of times)
        t_axis = np.linspace(
            time_range[0], time_range[1],
            num=time_range[1]-time_range[0]
        )

        # create left axis for power
        fig, pow_axis = plt.subplots(figsize=(12, 5))
        plt.xticks(
            np.arange(
                np.ceil(time_range[0]/12)*12,
                np.floor(time_range[1]/12)*12+1, step=12
            )
        )

        # axes labels
        pow_axis.set_xlabel('Time [h]')
        pow_axis.set_ylabel('Power [kW]')

        # initialize
        plot_list = []  # list of plot objects
        name_list = []  # list of corresponding names

        # plot power sources (solid graphs)
        pow_stack = 0  # total power below the graph
        for cp in name_solid:

            # add to list of plots
            plot_list.append(
                pow_axis.fill_between(
                    t_axis, pow_stack,
                    pow_stack+pow_solid[cp],
                    color=color_solid[cp]
                )
            )

            # add to list of names
            name_list.append(name_solid[cp])

            # increase pow stack
            pow_stack = pow_stack+pow_solid[cp]

        # plot power sources (line graphs)
        for cp in pow_line:

            # add to list of plots
            line_plot = pow_axis.plot(
                t_axis, pow_line[cp], color=color_line[cp]
            )
            plot_list.append(line_plot[0])

            # add to list of names
            name_list.append(name_line[cp])

        # plot soc on right axis
        soc_axis = pow_axis.twinx()  # make right y-axis
        soc_axis.set_ylabel('SOC')
        soc_axis.set_ylim(0, 1.1)

        # plot lines that represent SOC's
        for cp in soc_line.keys():

            # add to list of plots
            line_plot = soc_axis.plot(
                t_axis, soc_line[cp], color=color_line[cp]
            )
            plot_list.append(line_plot[0])

            # add to list of names
            name_list.append(name_line[cp])

        # generate plot
        plt.legend(tuple(plot_list), tuple(name_list))
        plt.show()

    def powflow_csv(self, file):
        """Generates a .csv file with the power flow.

        Parameters
        ----------
        file : str
            Filename for output file.

        """
        # initialize array with powers
        pow_out = np.arange(0, 8760).reshape((8760, 1))

        # initialize headers
        pow_head = ['Hour']

        # get the names and values of each component
        for cp in self.comp_list:
            if cp.name_solid is not None:
                pow_head.append(cp.name_solid)  # append component
                pow_out = np.append(
                    pow_out, self.ts[cp].reshape((8760, 1)), axis=1
                )
            if cp.name_line is not None:
                if isinstance(cp, StorageComponent):  # storage has SOC
                    pow_head.append(cp.name_line)  # append battery SOC
                    pow_out = np.append(
                        pow_out, self.ts_soc[cp].reshape((8760, 1)), axis=1
                    )
                if isinstance(cp, LoadComponent):
                    pow_head.append(cp.name_line)  # append load
                    pow_out = np.append(
                        pow_out, self.ts[cp].reshape((8760, 1)), axis=1
                    )

        pd.DataFrame(pow_out).to_csv(file, index=False, header=pow_head)

    def size_csv(self, file):
        """Generates a .csv file with the sizes.

        Parameters
        ----------
        file : str
            Filename for output file.

        """
        # initialize file
        file_out = open(file, mode='w')

        # get the sizes of each component
        for cp in self.comp_list:
            if cp.name_solid is not None:
                file_out.writelines(cp.name_solid+','+str(cp.size))

        file_out.writelines('LCOE,'+str(self.lcoe[0])+'\n')

    def res_print(self):
        """Prints the sizes and calculated parameters in the console."""

        # print results
        print('SYSTEM SUMMARY')

        # sizes
        print('Sizes [kW] or [kWh]:')
        for cp in self.comp_list:
            if not isinstance(cp, LoadComponent):
                if np.atleast_1d(cp.size).size == 1:  # one scenario only
                    print(
                        '    {:15}: {:>12.4f}'
                        .format(cp.name_solid, cp.size[0])
                    )
                else:  # multiple scenarios simulated
                    print('    {:15}: '.format(cp.name_solid)+str(cp.size[0]))

        # other parameters
        print('Parameters:')
        print('    LCOE [USD/kWh] : {:>12.4f}'.format(self.lcoe))
        print('    RE-Share       : {:>12.4f}'.format(self.re_frac))

    @staticmethod
    def _lcoe(dis, yr_proj, infl, proj_capex, proj_opex):
        """Calculates the LCOE.

        Parameters
        ----------
        dis : Dispatch
            A Dispatch object from which to calculate the LCOE.
        yr_proj : float
            Project lifetime [yr].
        infl : float
            Inflation rate.
        proj_capex : float
            Capital expenses [USD] of the project.
        proj_opex : float
            Fixed yearly operating expenses [USD/yr] of the project.

        Returns
        -------
        lcoe : ndarray
            The LCOE of each scenario. Returns nan if scenario is invalid.

        """
        # start cost calculation in each module
        dis.fx.cost_calc(yr_proj, infl)
        dis.ad.cost_calc(yr_proj, infl)
        dis.st.cost_calc(yr_proj, infl)
        dis.gd.cost_calc(yr_proj, infl)
        dis.ld.cost_calc(yr_proj, infl)

        # calculate total cost
        cost_c = (
            dis.fx.cost_c+dis.ad.cost_c +
            dis.st.cost_c+dis.gd.cost_c +
            dis.ld.cost_c+proj_capex
        )
        cost_o = (
            dis.fx.cost_o+dis.ad.cost_o +
            dis.st.cost_o+dis.gd.cost_o +
            dis.ld.cost_o+proj_opex*np.sum(1/(1+infl)**np.arange(1, 1+yr_proj))
        )
        cost_r = (
            dis.fx.cost_r+dis.ad.cost_r +
            dis.st.cost_r+dis.gd.cost_r +
            dis.ld.cost_r
        )
        cost_f = (
            dis.fx.cost_f+dis.ad.cost_f +
            dis.st.cost_f+dis.gd.cost_f +
            dis.ld.cost_f
        )
        cost = (
            dis.fx.cost+dis.ad.cost +
            dis.st.cost+dis.gd.cost +
            dis.ld.cost+proj_capex +
            proj_opex*np.sum(1/(1+infl)**np.arange(1, 1+yr_proj))
        )

        # calculate LCOE
        crf = infl*(1+infl)**yr_proj/((1+infl)**yr_proj-1)
        lcoe = crf*cost/dis.ld.enr_tot

        return lcoe
