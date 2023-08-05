import numpy as np

from .Dispatch import Dispatch


class LoadFollow(Dispatch):
    """Load Following dispatch strategy.

    Parameters
    ----------
    comp_list : list of Component
        List of initialized components.
    size : dict
        Sizes [kW] or [kWh] of the components. Use component objects as
        keys and sizes as values.
    spin_res : float
        Spinning reserve.

    Other Parameters
    ----------------
    tol : float
        Tolerance when checking if power meets the load.

    """

    def __init__(self, comp_list, size, spin_res, **kwargs):
        """Initializes the base class."""
        # initialize superclass
        super().__init__(comp_list, size, spin_res)

        # record parameters
        self.tol = kwargs.pop('tol', 1e-2)

        # get size of spinning reserve
        self.pow_sr = spin_res*self.ld.pow_max

    def step(self):
        """Increments the timestep."""

        # get fixed power and load
        pow_fx = self.fx.get_pow(self.hr)
        pow_ld = self.ld.get_pow(self.hr)

        # case 0: fixed power does not supply load
        # case 1: fixed power supploes load
        case0 = pow_fx < pow_ld
        case1 = pow_fx >= pow_ld

        # 1: determine power for charging
        pow_c = pow_fx-pow_ld

        # case 10: storage is not fully charged
        # case 11: storage is fully charged
        case10 = np.logical_and(
            case1,
            np.logical_not(self.st.is_full)
        )
        case11 = np.logical_and(
            case1,
            self.st.is_full
        )

        # 11: determine power for net metering
        gdc11 = case11*pow_c

        # determine maximum charge rate
        pow_maxc = self.st.pow_maxc

        # case 100: not beyond max charge
        # case 101: beyond max charge
        case100 = np.logical_and(
            case10,
            pow_c <= pow_maxc
        )
        case101 = np.logical_and(
            case10,
            pow_c > pow_maxc
        )

        # 100: determine power for charging
        stc100 = case100*pow_c

        # 101: max charge then give excess to grid
        stc101 = case101*pow_maxc
        gdc101 = case101*(pow_c-pow_maxc)

        # 0: calculate combined power of fixed and storage
        pow_stmax = self.st.pow_maxdc
        pow_fsmax = pow_fx+pow_stmax

        # case 00: fixed + storage cannot supply load
        # case 01: fixed + storage can supply load
        case00 = np.logical_and(
            case0,
            pow_fsmax < pow_ld
        )
        case01 = np.logical_and(
            case0,
            pow_fsmax >= pow_ld
        )

        # 01: determine excess power
        pow_xs = pow_fsmax-pow_ld

        # case 010: spinning reserve not satisfied
        # case 011: spinning reserve satisfied
        case010 = np.logical_and(
            case01,
            pow_xs < self.pow_sr
        )
        case011 = np.logical_and(
            case01,
            pow_xs >= self.pow_sr
        )

        # 011: lower discharge from storage
        std011 = case011*((pow_ld+self.pow_sr)-pow_fx)

        # 010: run adjustable resource
        pow_adreq = (pow_ld+self.pow_sr)-pow_fsmax  # required power
        pow_ad = self.ad.calc_pow(pow_adreq, self.hr)  # output power
        ad010 = case010*pow_ad

        # case 0100: fixed, storage, and adj do not suffice
        # case 0101: fixed, storage, and adj suffice
        case0100 = np.logical_and(
            case010,
            (pow_ld+self.pow_sr) > (pow_fsmax+pow_ad)
        )
        case0101 = np.logical_and(
            case010,
            (pow_ld+self.pow_sr) <= (pow_fsmax+pow_ad)
        )

        # 0100: discharge storage
        std0100 = case0100*pow_stmax

        # 0100: use grid
        gdd0100 = case0100*((pow_ld+self.pow_sr)-(pow_fsmax+pow_ad))

        # 0101: lower storage discharge so that output just meets SR
        pow_st = (pow_ld+self.pow_sr)-(pow_fx+pow_ad)

        # case 01010: storage is no longer necessary
        # case 01011: storage is still necessary
        case01010 = np.logical_and(
            case0101,
            pow_st < 0
        )
        case01011 = np.logical_and(
            case0101,
            pow_st >= 0
        )

        # case 010100: storage is not fully charged
        # case 010101: storage is fully charged
        case010100 = np.logical_and(
            case01010,
            self.st.soc != 1
        )
        case010101 = np.logical_and(
            case01010,
            self.st.soc == 1
        )

        # 010101: determine power for net metering
        gdc010101 = case010101*pow_c

        # case 0101000: not beyond max charge
        # case 0101001: beyond max charge
        case0101000 = np.logical_and(
            case010100,
            pow_c <= pow_maxc
        )
        case0101001 = np.logical_and(
            case010100,
            pow_c > pow_maxc
        )

        # 0101000: determine power for charging
        stc0101000 = case0101000*pow_c

        # 101: max charge then give excess to grid
        stc0101001 = case0101001*pow_maxc
        gdc0101001 = case0101001*(pow_c-pow_maxc)

        # 01011: adjust storage output
        std01011 = case01011*pow_st

        # case 000: fix, store, adj does not supply load and SR
        # case 001: fix, store, adj supplies load and SR
        case000 = np.logical_and(
            case00,
            (pow_ld+self.pow_sr) > (pow_fsmax+pow_ad)
        )
        case001 = np.logical_and(
            case00,
            (pow_ld+self.pow_sr) <= (pow_fsmax+pow_ad)
        )

        # 000: use grid
        gdd000 = case000*((pow_ld+self.pow_sr)-(pow_fsmax+pow_ad))

        # 000: calculate adjustable power output
        ad000 = case000*pow_ad

        # 000: storage use
        std000 = case000*pow_stmax

        # 001: calculate adjustable power output
        ad001 = case001*pow_ad

        # case 0010: storage no longer necessary
        # case 0011: storage still necessary
        case0010 = np.logical_and(
            case001,
            pow_st < 0
        )
        case0011 = np.logical_and(
            case001,
            pow_st >= 0
        )

        # case 00100: storage is not fully charged
        # case 00101: storage is fully charged
        case00100 = np.logical_and(
            case0010,
            self.st.soc != 1
        )
        case00101 = np.logical_and(
            case0010,
            self.st.soc == 1
        )

        # 00101: determine power for net metering
        gdc00101 = case00101*pow_c

        # case 001000: not beyond max charge
        # case 001001: beyond max charge
        case001000 = np.logical_and(
            case00100,
            pow_c <= pow_maxc
        )
        case001001 = np.logical_and(
            case00100,
            pow_c > pow_maxc
        )

        # 001000: determine power for charging
        stc001000 = case001000*pow_c

        # 001001: max charge then give excess to grid
        stc001001 = case001001*pow_maxc
        gdc001001 = case001001*(pow_c-pow_maxc)

        # 0011: adjust storage output
        std0011 = case0011*pow_st

        # collect total powers
        stc_tot = np.maximum(
            (  # charge storage
                stc001000+stc001001+stc0101000 +
                stc0101001+stc100+stc101
            ),
            0
        )
        std_tot = np.maximum(
            (  # discharge storage
                std0011+std0100+std01011+std011+std000
            ),
            0
        )
        gdc_tot = np.maximum(
            (  # net metering to grid
                gdc001001+gdc00101+gdc0101001 +
                gdc010101+gdc101+gdc11
            ),
            0
        )
        gdd_tot = np.maximum(
            (  # take power from grid
                gdd000+gdd0100
            ),
            0
        )
        ad_tot = np.maximum(
            (  # power taken from adjustable sources
                ad010+ad000+ad001
            ),
            0
        )

        # convention: discharge is positive
        self.st.rec_pow(std_tot-stc_tot, self.hr)
        self.gd.rec_pow(gdd_tot-gdc_tot, self.hr)
        self.ad.rec_pow(ad_tot, self.hr)

        # calculate power deficit
        pow_miss = pow_ld - (
            pow_fx+ad_tot +
            std_tot-stc_tot +
            gdd_tot-gdc_tot
        )
        self.pow_def += pow_miss*(pow_miss > 0)
        self.num_def += pow_miss > 0

        # check if setup is still feasible
        val_soc = self.st.soc >= 1-self.st.dod_max
        val_ld = pow_ld <= (pow_fx+ad_tot+std_tot+self.gd.pow)*(1+self.tol)
        val_ot = np.logical_not(np.isnan(
            pow_fx+ad_tot+std_tot-stc_tot+self.st.soc+gdd_tot-gdc_tot
        ))
        self.feas = np.logical_and.reduce([
            val_soc, val_ld, val_ot, self.feas
        ])

        # increment
        self.hr += 1
