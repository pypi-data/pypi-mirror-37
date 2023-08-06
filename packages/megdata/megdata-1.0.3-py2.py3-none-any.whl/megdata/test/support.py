# vim: set expandtab ts=4 sw=4:

# This file is part of the python-megdata package
# For copyright and redistribution details, please see the COPYING file

import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

def find_path(varname, sentinal, subdir=None):
    """
    Looks for a directory using the environment variable given and raises an
    exception if it can't find the sentinal file.

    If subdir is set, it adds a sub directory to the directory found in
    the environment variable
    """

    dir = os.environ.get(varname, None)
    if not dir:
        raise Exception("%s is not set, cannot find test files" % varname)

    if subdir is not None:
        dir = os.path.join(dir, subdir)

    if not os.path.isdir(dir):
        raise Exception("%s is not a directory" % varname)

    # Our test file
    if not os.path.isfile(os.path.join(dir, sentinal)):
        raise Exception("%s does not seem to contain sentinal file %s" % (varname, sentinal))

    return os.path.abspath(dir)


def megdatatestpath():
    """Looks for the directory of meg test data using the environment variable MEGTEST.
    Raises an exception if it can't find the sentinal file $MEGTEST/README.naftest"""

    return find_path('MEGDATATEST', 'README.naftest')

def remove_file(filename):
    from os import unlink
    try:
        unlink(filename)
    except Exception as e:
        pass

def h5pytempfile():
    import h5py
    from tempfile import mkstemp
    from os import close

    fd, name = mkstemp()

    # This is a race condition but is as good as we can do at the moment
    close(fd)
    return h5py.File(name, 'w')


def array_assert(a, b, decimal=None, **kwargs):
    if decimal is None:
        if a.shape != b.shape:
            raise AssertionError("Sizes of matrices don't match (%s vs %s)" % (str(a.shape), str(b.shape)))

        if ((a == b).all()):
            return

        # Otherwise give some info as to why we're asserting
        raise AssertionError("Arrays are not the same:\nArray A:%s\nArray B:%s" % (a, b))
    else:
        from numpy.testing import assert_almost_equal
        assert_almost_equal(a, b, decimal, *kwargs)

class MEGDataTestBase(unittest.TestCase):
    """
    Use when an output directory is needed to write test files into
    """
    def setUp(self):
        self.preSetUp()
        self.tempdir = tempfile.mkdtemp()
        if 'MEGDATADEBUG' in os.environ:
            print("Temporary directory: ", self.tempdir)
        self.postSetUp()

    @property
    def megdatatestdir(self):
        return megdatatestpath()

    def preSetUp(self):
        pass

    def postSetUp(self):
        pass

    def tearDown(self):
        self.preTearDown()
        if 'MEGDATADEBUG' in os.environ:
            print("Not removing temporary directory %s as MEGDATADEBUG is set" % self.tempdir)
        else:
            shutil.rmtree(self.tempdir)
        self.postTearDown()

    def preTearDown(self):
        pass

    def postTearDown(self):
        pass

    def mkdir(self, dirname):
        from errno import EEXIST
        abs_dirname = os.path.join(self.tempdir, dirname)
        try:
            os.makedirs(abs_dirname)
        except OSError as e:
            if e.errno != EEXIST:
                raise e

        return abs_dirname

    def copyfile(self, frompath, relto):
        self.mkdir(os.path.dirname(relto))
        abs_to = os.path.join(self.tempdir, relto)
        shutil.copyfile(frompath, abs_to)

    def check_file_exists(self, filename):
        abs_filename = os.path.join(self.tempdir, filename)
        os.stat(abs_filename)

