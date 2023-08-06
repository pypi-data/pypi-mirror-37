# vim: set expandtab ts=4 sw=4:

# This file is part of python-megdata
# For copyright and redistribution details, please see the COPYING file

import numpy as np
from os.path import join, abspath

from megdata.test import megdatatestpath, array_assert
from megdata.test.support import MEGDataTestBase

# This will raise if it can't find the test data directory
MEGDATATEST = megdatatestpath()

DATADIR = abspath(join(MEGDATATEST, 'naf', 'meg', 'ctfreaders'))

class TestCtfReader(MEGDataTestBase):

    def postSetUp(self):
        import h5py
        h = h5py.File(join(DATADIR, 'soft002data_03.testhdf5'), 'r')
        # Why do we store this data the wrong way around?
        self.orig_data = h['testdata'][...]
        # The data needs scaling by 10^-15 as we want the data in T
        # whereas the Matlab code has it in fT
        self.orig_data *= 10**-15
        self.orig_order = h['testdata'].attrs['chanorder']
        h.close()


    def test_ctf_data_load_slice(self):
        """Test that we load CTF data correctly by slice"""
        from megdata import CTFDataset

        c = CTFDataset.from_file(join(MEGDATATEST, 'ctfdata/SOFT002/08104_CrossSite_20101215_03.ds/08104_CrossSite_20101215_03.res4'))

        slices_per_epoch = c.res.no_samples

        # Sort out our channel scaling
        scales = []
        for chan in c.res.channels:
            # We don't scale the data in the same was as the Matlab reader
            # as we want the MEG data in T, not fT
            scales.append( 1.0 / (chan.gain * chan.q_gain) )
        scales = np.array(scales)

        for e in range(self.orig_data.shape[1]):
            start = e * slices_per_epoch
            end = start + 1000
            new_dat = c.read_raw_data(slices=(start, end),
                                      indices=c.meg_indices).T
            # Need to apply the gains
            new_dat = new_dat * scales[c.meg_indices, np.newaxis]

            array_assert(new_dat, self.orig_data[:, e, :], decimal=8)

