"""
Test for BDS test for IID time series

References
----------

Kanzler, Ludwig. 1998.
BDS: MATLAB Module to Calculate Brock, Dechert & Scheinkman Test for
Independence.
Statistical Software Components. Boston College Department of Economics.
http://ideas.repec.org/c/boc/bocode/t871803.html.

"""

import os

import pytest
import pandas as pd
import numpy as np
from numpy.testing import assert_almost_equal

from sm2.tsa.stattools import bds

curdir = os.path.dirname(os.path.abspath(__file__))
data_file = os.path.join(curdir, "results", "bds_data.csv")
data = pd.read_csv(data_file, header=None)

res_file = os.path.join(curdir, "results", "bds_results.csv")
results = pd.read_csv(res_file, header=None)


@pytest.mark.not_vetted
class CheckBDS(object):
    """
    Test values from Kanzler's MATLAB program bds.
    """
    def test_stat(self):
        assert_almost_equal(self.res[0],
                            self.bds_stats,
                            8)

    def test_pvalue(self):
        assert_almost_equal(self.res[1],
                            self.pvalues,
                            8)


@pytest.mark.not_vetted
class TestBDSSequence(CheckBDS):
    """
    BDS Test on np.arange(1, 26)
    """
    @classmethod
    def setup_class(cls):
        cls.results = results[results[0] == 1]
        cls.bds_stats = np.array(cls.results[2][1:])
        cls.pvalues = np.array(cls.results[3][1:])

        cls.data = data[0][data[0].notnull()]
        cls.res = bds(cls.data, 5)


@pytest.mark.not_vetted
class TestBDSNormal(CheckBDS):
    """
    BDS Test on np.random.normal(size=25)
    """
    @classmethod
    def setup_class(cls):
        cls.results = results[results[0] == 2]
        cls.bds_stats = np.array(cls.results[2][1:])
        cls.pvalues = np.array(cls.results[3][1:])

        cls.data = data[1][data[1].notnull()]
        cls.res = bds(cls.data, 5)


@pytest.mark.not_vetted
class TestBDSCombined(CheckBDS):
    """
    BDS Test on np.r_[np.random.normal(size=25), np.random.uniform(size=25)]
    """
    @classmethod
    def setup_class(cls):
        cls.results = results[results[0] == 3]
        cls.bds_stats = np.array(cls.results[2][1:])
        cls.pvalues = np.array(cls.results[3][1:])

        cls.data = data[2][data[2].notnull()]
        cls.res = bds(cls.data, 5)


@pytest.mark.not_vetted
class TestBDSGDPC1(CheckBDS):
    """
    BDS Test on GDPC1: 1947Q1 - 2013Q1

    References
    ----------
    http://research.stlouisfed.org/fred2/series/GDPC1
    """
    @classmethod
    def setup_class(cls):
        cls.results = results[results[0] == 4]
        cls.bds_stats = np.array(cls.results[2][1:])
        cls.pvalues = np.array(cls.results[3][1:])

        cls.data = data[3][data[3].notnull()]
        cls.res = bds(cls.data, 5)
