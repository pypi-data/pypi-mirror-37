#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""tests for some time series analysis functions"""

from six.moves import zip

import pytest
import numpy as np
from numpy.testing import (assert_array_almost_equal, assert_equal,
                           assert_array_equal)
import pandas as pd
from pandas.tseries.frequencies import to_offset
import pandas.util.testing as tm

from sm2 import datasets

from sm2.tsa import stattools, tsatools
from sm2.tsa.tests.results import savedrvs
from sm2.tsa.tests.results.datamlw_tls import mlpacf


xo = savedrvs.rvsdata.xar2
x100 = xo[-100:] / 1000.
x1000 = xo / 1000.


@pytest.mark.not_vetted
def test_pacf_ols():
    pacfols = stattools.pacf_ols(x100, 20)
    assert_array_almost_equal(mlpacf.pacf100.ravel(), pacfols, 8)
    pacfols = stattools.pacf_ols(x1000, 20)
    assert_array_almost_equal(mlpacf.pacf1000.ravel(), pacfols, 8)


@pytest.mark.not_vetted
def test_duplication_matrix():
    for k in range(2, 10):
        m = tsatools.unvech(np.random.randn(k * (k + 1) // 2))
        Dk = tsatools.duplication_matrix(k)
        assert (np.array_equal(tsatools.vec(m), np.dot(Dk, tsatools.vech(m))))


@pytest.mark.not_vetted
def test_elimination_matrix():
    for k in range(2, 10):
        m = np.random.randn(k, k)
        Lk = tsatools.elimination_matrix(k)
        assert (np.array_equal(tsatools.vech(m), np.dot(Lk, tsatools.vec(m))))


@pytest.mark.not_vetted
def test_commutation_matrix():
    m = np.random.randn(4, 3)
    K = tsatools.commutation_matrix(4, 3)
    assert (np.array_equal(tsatools.vec(m.T), np.dot(K, tsatools.vec(m))))


@pytest.mark.not_vetted
def test_vec():
    arr = np.array([[1, 2],
                    [3, 4]])
    assert (np.array_equal(tsatools.vec(arr), [1, 3, 2, 4]))


@pytest.mark.not_vetted
def test_vech():
    arr = np.array([[1, 2, 3],
                    [4, 5, 6],
                    [7, 8, 9]])
    assert (np.array_equal(tsatools.vech(arr), [1, 4, 7, 5, 8, 9]))


@pytest.mark.not_vetted
class TestLagmat(object):
    @classmethod
    def setup_class(cls):
        data = datasets.macrodata.load_pandas()
        cls.macro_df = data.data[['year', 'quarter', 'realgdp', 'cpi']]
        cols = list(cls.macro_df.columns)
        cls.realgdp_loc = cols.index('realgdp')
        cls.cpi_loc = cols.index('cpi')
        cls.random_data = np.random.randn(100)

        index = [str(int(yr)) + '-Q' + str(int(qu))
                 for yr, qu in zip(cls.macro_df.year, cls.macro_df.quarter)]
        cls.macro_df.index = index
        cls.series = cls.macro_df.cpi

    @pytest.mark.skip(reason="add_lag not ported from upstream")
    def test_add_lag_insert(self):
        data = self.macro_df.values
        nddata = data.astype(float)
        lagmat = tsatools.lagmat(nddata[:, 2], 3, trim='Both')
        results = np.column_stack((nddata[3:, :3], lagmat, nddata[3:, -1]))
        lag_data = tsatools.add_lag(data, self.realgdp_loc, 3)
        assert_equal(lag_data, results)

    @pytest.mark.skip(reason="add_lag not ported from upstream")
    def test_add_lag_noinsert(self):
        data = self.macro_df.values
        nddata = data.astype(float)
        lagmat = tsatools.lagmat(nddata[:, 2], 3, trim='Both')
        results = np.column_stack((nddata[3:, :], lagmat))
        lag_data = tsatools.add_lag(data, self.realgdp_loc, 3, insert=False)
        assert_equal(lag_data, results)

    @pytest.mark.skip(reason="add_lag not ported from upstream")
    def test_add_lag_noinsert_atend(self):
        data = self.macro_df.values
        nddata = data.astype(float)
        lagmat = tsatools.lagmat(nddata[:, -1], 3, trim='Both')
        results = np.column_stack((nddata[3:, :], lagmat))
        lag_data = tsatools.add_lag(data, self.cpi_loc, 3, insert=False)
        assert_equal(lag_data, results)

        # should be the same as insert
        lag_data2 = tsatools.add_lag(data, self.cpi_loc, 3, insert=True)
        assert_equal(lag_data2, results)

    @pytest.mark.skip(reason="add_lag not ported from upstream")
    def test_add_lag_ndarray(self):
        data = self.macro_df.values
        nddata = data.astype(float)
        lagmat = tsatools.lagmat(nddata[:, 2], 3, trim='Both')
        results = np.column_stack((nddata[3:, :3], lagmat, nddata[3:, -1]))
        lag_data = tsatools.add_lag(nddata, 2, 3)
        assert_equal(lag_data, results)

    @pytest.mark.skip(reason="add_lag not ported from upstream")
    def test_add_lag_noinsert_ndarray(self):
        data = self.macro_df.values
        nddata = data.astype(float)
        lagmat = tsatools.lagmat(nddata[:, 2], 3, trim='Both')
        results = np.column_stack((nddata[3:, :], lagmat))
        lag_data = tsatools.add_lag(nddata, 2, 3, insert=False)
        assert_equal(lag_data, results)

    @pytest.mark.skip(reason="add_lag not ported from upstream")
    def test_add_lag_noinsertatend_ndarray(self):
        data = self.macro_df.values
        nddata = data.astype(float)
        lagmat = tsatools.lagmat(nddata[:, -1], 3, trim='Both')
        results = np.column_stack((nddata[3:, :], lagmat))
        lag_data = tsatools.add_lag(nddata, 3, 3, insert=False)
        assert_equal(lag_data, results)
        # should be the same as insert also check negative col number
        lag_data2 = tsatools.add_lag(nddata, -1, 3, insert=True)
        assert_equal(lag_data2, results)

    def test_sep_return(self):
        data = self.random_data
        n = data.shape[0]
        lagmat, leads = tsatools.lagmat(data, 3, trim='none', original='sep')
        expected = np.zeros((n + 3, 4))
        for i in range(4):
            expected[i:i + n, i] = data
        expected_leads = expected[:, :1]
        expected_lags = expected[:, 1:]
        assert_equal(expected_lags, lagmat)
        assert_equal(expected_leads, leads)

    @pytest.mark.skip(reason="add_lag not ported from upstream")
    def test_add_lag1d(self):
        data = self.random_data
        lagmat = tsatools.lagmat(data, 3, trim='Both')
        results = np.column_stack((data[3:], lagmat))
        lag_data = tsatools.add_lag(data, lags=3, insert=True)
        assert_equal(results, lag_data)

        # add index
        data = data[:, None]
        lagmat = tsatools.lagmat(data, 3, trim='Both')  # test for lagmat too
        results = np.column_stack((data[3:], lagmat))
        lag_data = tsatools.add_lag(data, lags=3, insert=True)
        assert_equal(results, lag_data)

    @pytest.mark.skip(reason="add_lag not ported from upstream")
    def test_add_lag1d_drop(self):
        data = self.random_data
        lagmat = tsatools.lagmat(data, 3, trim='Both')
        lag_data = tsatools.add_lag(data, lags=3, drop=True, insert=True)
        assert_equal(lagmat, lag_data)

        # no insert, should be the same
        lag_data = tsatools.add_lag(data, lags=3, drop=True, insert=False)
        assert_equal(lagmat, lag_data)

    @pytest.mark.skip(reason="add_lag not ported from upstream")
    def test_add_lag1d_struct(self):
        data = np.zeros(100, dtype=[('variable', float)])
        nddata = self.random_data
        data['variable'] = nddata

        lagmat = tsatools.lagmat(nddata, 3, trim='Both', original='in')
        lag_data = tsatools.add_lag(data, 'variable', lags=3, insert=True)
        assert_equal(lagmat, lag_data.view((float, 4)))

        lag_data = tsatools.add_lag(data, 'variable', lags=3, insert=False)
        assert_equal(lagmat, lag_data.view((float, 4)))

        lag_data = tsatools.add_lag(data, lags=3, insert=True)
        assert_equal(lagmat, lag_data.view((float, 4)))

    @pytest.mark.skip(reason="add_lag not ported from upstream")
    def test_add_lag_1d_drop_struct(self):
        data = np.zeros(100, dtype=[('variable', float)])
        nddata = self.random_data
        data['variable'] = nddata

        lagmat = tsatools.lagmat(nddata, 3, trim='Both')
        lag_data = tsatools.add_lag(data, lags=3, drop=True)
        assert_equal(lagmat, lag_data.view((float, 3)))

    @pytest.mark.skip(reason="add_lag not ported from upstream")
    def test_add_lag_drop_insert(self):
        data = self.macro_df.values
        nddata = data.astype(float)
        lagmat = tsatools.lagmat(nddata[:, 2], 3, trim='Both')
        results = np.column_stack((nddata[3:, :2], lagmat, nddata[3:, -1]))
        lag_data = tsatools.add_lag(data, self.realgdp_loc, 3, drop=True)
        assert_equal(lag_data, results)

    @pytest.mark.skip(reason="add_lag not ported from upstream")
    def test_add_lag_drop_noinsert(self):
        data = self.macro_df.values
        nddata = data.astype(float)
        lagmat = tsatools.lagmat(nddata[:, 2], 3, trim='Both')
        results = np.column_stack((nddata[3:, np.array([0, 1, 3])], lagmat))
        lag_data = tsatools.add_lag(data, self.realgdp_loc, 3,
                                    insert=False, drop=True)
        assert_equal(lag_data, results)

    def test_dataframe_without_pandas(self):
        data = self.macro_df
        both = tsatools.lagmat(data, 3, trim='both', original='in')
        both_np = tsatools.lagmat(data.values, 3, trim='both', original='in')
        assert_equal(both, both_np)

        lags = tsatools.lagmat(data, 3, trim='none', original='ex')
        lags_np = tsatools.lagmat(data.values, 3, trim='none', original='ex')
        assert_equal(lags, lags_np)

        lags, lead = tsatools.lagmat(data, 3, trim='forward', original='sep')
        lags_np, lead_np = tsatools.lagmat(data.values, 3,
                                           trim='forward', original='sep')
        assert_equal(lags, lags_np)
        assert_equal(lead, lead_np)

    def test_dataframe_both(self):
        data = self.macro_df
        columns = list(data.columns)
        n = data.shape[0]
        values = np.zeros((n + 3, 16))
        values[:n, :4] = data.values
        for lag in range(1, 4):
            new_cols = [col + '.L.' + str(lag) for col in data]
            columns.extend(new_cols)
            values[lag:n + lag, 4 * lag:4 * (lag + 1)] = data.values
        index = data.index
        values = values[:n]
        expected = pd.DataFrame(values, columns=columns, index=index)
        expected = expected.iloc[3:]

        both = tsatools.lagmat(self.macro_df, 3, trim='both',
                               original='in', use_pandas=True)
        tm.assert_frame_equal(both, expected)
        lags = tsatools.lagmat(self.macro_df, 3, trim='both',
                               original='ex', use_pandas=True)
        tm.assert_frame_equal(lags, expected.iloc[:, 4:])
        lags, lead = tsatools.lagmat(self.macro_df, 3, trim='both',
                                     original='sep', use_pandas=True)
        tm.assert_frame_equal(lags, expected.iloc[:, 4:])
        tm.assert_frame_equal(lead, expected.iloc[:, :4])

    def test_too_few_observations(self):
        with pytest.raises(ValueError):
            tsatools.lagmat(self.macro_df, 300, use_pandas=True)

        with pytest.raises(ValueError):
            tsatools.lagmat(self.macro_df.values, 300)

    def test_unknown_trim(self):
        with pytest.raises(ValueError):
            tsatools.lagmat(self.macro_df, 3, trim='unknown', use_pandas=True)

        with pytest.raises(ValueError):
            tsatools.lagmat(self.macro_df.values, 3, trim='unknown')

    def test_dataframe_forward(self):
        data = self.macro_df
        columns = list(data.columns)
        n = data.shape[0]
        values = np.zeros((n + 3, 16))
        values[:n, :4] = data.values
        for lag in range(1, 4):
            new_cols = [col + '.L.' + str(lag) for col in data]
            columns.extend(new_cols)
            values[lag:n + lag, 4 * lag:4 * (lag + 1)] = data.values
        index = data.index
        values = values[:n]
        expected = pd.DataFrame(values, columns=columns, index=index)
        both = tsatools.lagmat(self.macro_df, 3, trim='forward', original='in',
                               use_pandas=True)
        tm.assert_frame_equal(both, expected)
        lags = tsatools.lagmat(self.macro_df, 3, trim='forward', original='ex',
                               use_pandas=True)
        tm.assert_frame_equal(lags, expected.iloc[:, 4:])
        lags, lead = tsatools.lagmat(self.macro_df, 3, trim='forward',
                                     original='sep', use_pandas=True)
        tm.assert_frame_equal(lags, expected.iloc[:, 4:])
        tm.assert_frame_equal(lead, expected.iloc[:, :4])

    def test_pandas_errors(self):
        # TODO: parametrize?
        for trim in ['none', 'backward']:
            for data in [self.macro_df, self.series]:
                with pytest.raises(ValueError):
                    tsatools.lagmat(data, 3, trim=trim, use_pandas=True)

    def test_series_forward(self):
        expected = pd.DataFrame(index=self.series.index,
                                columns=['cpi', 'cpi.L.1', 'cpi.L.2',
                                         'cpi.L.3'])
        expected['cpi'] = self.series
        for lag in range(1, 4):
            expected['cpi.L.' + str(int(lag))] = self.series.shift(lag)
        expected = expected.fillna(0.0)

        both = tsatools.lagmat(self.series, 3, trim='forward',
                               original='in', use_pandas=True)
        tm.assert_frame_equal(both, expected)
        lags = tsatools.lagmat(self.series, 3, trim='forward',
                               original='ex', use_pandas=True)
        tm.assert_frame_equal(lags, expected.iloc[:, 1:])
        lags, lead = tsatools.lagmat(self.series, 3, trim='forward',
                                     original='sep', use_pandas=True)
        tm.assert_frame_equal(lead, expected.iloc[:, :1])
        tm.assert_frame_equal(lags, expected.iloc[:, 1:])

    def test_series_both(self):
        expected = pd.DataFrame(index=self.series.index,
                                columns=['cpi', 'cpi.L.1', 'cpi.L.2',
                                         'cpi.L.3'])
        expected['cpi'] = self.series
        for lag in range(1, 4):
            expected['cpi.L.' + str(int(lag))] = self.series.shift(lag)
        expected = expected.iloc[3:]

        both = tsatools.lagmat(self.series, 3, trim='both',
                               original='in', use_pandas=True)
        tm.assert_frame_equal(both, expected)
        lags = tsatools.lagmat(self.series, 3, trim='both',
                               original='ex', use_pandas=True)
        tm.assert_frame_equal(lags, expected.iloc[:, 1:])
        lags, lead = tsatools.lagmat(self.series, 3, trim='both',
                                     original='sep', use_pandas=True)
        tm.assert_frame_equal(lead, expected.iloc[:, :1])
        tm.assert_frame_equal(lags, expected.iloc[:, 1:])


@pytest.mark.skip(reason="freq_to_period not ported from upstream (yet)")
@pytest.mark.not_vetted
def test_freq_to_period():
    freqs = ['A', 'AS-MAR', 'Q', 'QS', 'QS-APR', 'W', 'W-MON', 'B', 'D', 'H']
    expected = [1, 1, 4, 4, 4, 52, 52, 5, 7, 24]
    for i, j in zip(freqs, expected):
        assert_equal(tsatools.freq_to_period(i), j)
        assert_equal(tsatools.freq_to_period(to_offset(i)), j)


@pytest.mark.skip(reason="detrend not ported from upstream")
@pytest.mark.not_vetted
class TestDetrend(object):
    @classmethod
    def setup_class(cls):
        cls.data_1d = np.arange(5.0)
        cls.data_2d = np.arange(10.0).reshape(5, 2)

    def test_detrend_1d(self):
        data = self.data_1d
        assert_array_almost_equal(tsatools.detrend(data, order=1),
                                  np.zeros_like(data))
        assert_array_almost_equal(tsatools.detrend(data, order=0),
                                  [-2, -1, 0, 1, 2])

    def test_detrend_2d(self):
        data = self.data_2d
        assert_array_almost_equal(tsatools.detrend(data, order=1, axis=0),
                                  np.zeros_like(data))
        assert_array_almost_equal(tsatools.detrend(data, order=0, axis=0),
                                  [[-4, -4], [-2, -2], [0, 0], [2, 2], [4, 4]])
        assert_array_almost_equal(tsatools.detrend(data, order=0, axis=1),
                                  [[-0.5, 0.5], [-0.5, 0.5],
                                  [-0.5, 0.5], [-0.5, 0.5],
                                  [-0.5, 0.5]])

    def test_detrend_series(self):
        data = pd.Series(self.data_1d, name='one')
        detrended = tsatools.detrend(data, order=1)
        assert_array_almost_equal(detrended.values, np.zeros_like(data))
        tm.assert_series_equal(detrended,
                               pd.Series(detrended.values, name='one'))
        detrended = tsatools.detrend(data, order=0)
        assert_array_almost_equal(detrended.values,
                                  pd.Series([-2, -1, 0, 1, 2]))
        tm.assert_series_equal(detrended,
                               pd.Series(detrended.values, name='one'))

    def test_detrend_dataframe(self):
        columns = ['one', 'two']
        index = [c for c in 'abcde']
        data = pd.DataFrame(self.data_2d, columns=columns, index=index)

        detrended = tsatools.detrend(data, order=1, axis=0)
        assert_array_almost_equal(detrended.values, np.zeros_like(data))
        tm.assert_frame_equal(detrended,
                              pd.DataFrame(detrended.values,
                                           columns=columns, index=index))

        detrended = tsatools.detrend(data, order=0, axis=0)
        assert_array_almost_equal(detrended.values,
                                  [[-4, -4], [-2, -2], [0, 0], [2, 2], [4, 4]])
        tm.assert_frame_equal(detrended,
                              pd.DataFrame(detrended.values,
                                           columns=columns, index=index))

        detrended = tsatools.detrend(data, order=0, axis=1)
        assert_array_almost_equal(detrended.values,
                                  [[-0.5, 0.5], [-0.5, 0.5],
                                   [-0.5, 0.5], [-0.5, 0.5],
                                   [-0.5, 0.5]])
        tm.assert_frame_equal(detrended,
                              pd.DataFrame(detrended.values,
                                           columns=columns, index=index))

    def test_detrend_dim_too_large(self):
        with pytest.raises(NotImplementedError):
            tsatools.detrend(np.ones((3, 3, 3)))


@pytest.mark.not_vetted
class TestAddTrend(object):
    @classmethod
    def setup_class(cls):
        cls.n = 200
        cls.arr_1d = np.arange(float(cls.n))
        cls.arr_2d = np.tile(np.arange(float(cls.n))[:, None], 2)
        cls.c = np.ones(cls.n)
        cls.t = np.arange(1.0, cls.n + 1)

    def test_series(self):
        s = pd.Series(self.arr_1d)
        appended = tsatools.add_trend(s)
        expected = pd.DataFrame(s)
        expected['const'] = self.c
        tm.assert_frame_equal(expected, appended)

        prepended = tsatools.add_trend(s, prepend=True)
        expected = pd.DataFrame(s)
        expected.insert(0, 'const', self.c)
        tm.assert_frame_equal(expected, prepended)

        s = pd.Series(self.arr_1d)
        appended = tsatools.add_trend(s, trend='ct')
        expected = pd.DataFrame(s)
        expected['const'] = self.c
        expected['trend'] = self.t
        tm.assert_frame_equal(expected, appended)

    def test_dataframe(self):
        df = pd.DataFrame(self.arr_2d)
        appended = tsatools.add_trend(df)
        expected = df.copy()
        expected['const'] = self.c
        tm.assert_frame_equal(expected, appended)

        prepended = tsatools.add_trend(df, prepend=True)
        expected = df.copy()
        expected.insert(0, 'const', self.c)
        tm.assert_frame_equal(expected, prepended)

        df = pd.DataFrame(self.arr_2d)
        appended = tsatools.add_trend(df, trend='t')
        expected = df.copy()
        expected['trend'] = self.t
        tm.assert_frame_equal(expected, appended)

        df = pd.DataFrame(self.arr_2d)
        appended = tsatools.add_trend(df, trend='ctt')
        expected = df.copy()
        expected['const'] = self.c
        expected['trend'] = self.t
        expected['trend_squared'] = self.t ** 2
        tm.assert_frame_equal(expected, appended)

    def test_recarray(self):
        df = pd.DataFrame(self.arr_2d)
        recarray = df.to_records(index=False)
        appended = tsatools.add_trend(recarray)
        expected = pd.DataFrame(self.arr_2d)
        expected['const'] = self.c
        expected = expected.to_records(index=False)
        assert_equal(expected, appended)

        prepended = tsatools.add_trend(recarray, prepend=True)
        expected = pd.DataFrame(self.arr_2d)
        expected.insert(0, 'const', self.c)
        expected = expected.to_records(index=False)
        assert_equal(expected, prepended)

        appended = tsatools.add_trend(recarray, trend='ctt')
        expected = pd.DataFrame(self.arr_2d)
        expected['const'] = self.c
        expected['trend'] = self.t
        expected['trend_squared'] = self.t ** 2
        expected = expected.to_records(index=False)
        assert_equal(expected, appended)

    def test_duplicate_const(self):
        # TODO: parametrize?
        df = pd.DataFrame(self.c)
        for trend in ['c', 'ct']:
            for data in [self.c, df]:
                with pytest.raises(ValueError):
                    tsatools.add_trend(x=data, trend=trend,
                                       has_constant='raise')

        skipped = tsatools.add_trend(self.c, trend='c')
        assert_equal(skipped, self.c[:, None])

        skipped_const = tsatools.add_trend(self.c, trend='ct',
                                           has_constant='skip')
        expected = np.vstack((self.c, self.t)).T
        assert_equal(skipped_const, expected)

        added = tsatools.add_trend(self.c, trend='c', has_constant='add')
        expected = np.vstack((self.c, self.c)).T
        assert_equal(added, expected)

        added = tsatools.add_trend(self.c, trend='ct', has_constant='add')
        expected = np.vstack((self.c, self.c, self.t)).T
        assert_equal(added, expected)

    def test_mixed_recarray(self):
        dt = np.dtype([('c0', np.float64), ('c1', np.int8), ('c2', 'S4')])
        ra = np.array([(1.0, 1, 'aaaa'), (1.1, 2, 'bbbb')],
                      dtype=dt).view(np.recarray)
        added = tsatools.add_trend(ra, trend='ct')
        dt = np.dtype([('c0', np.float64), ('c1', np.int8), ('c2', 'S4'),
                       ('const', np.float64), ('trend', np.float64)])
        expected = np.array([(1.0, 1, 'aaaa', 1.0, 1.0),
                             (1.1, 2, 'bbbb', 1.0, 2.0)],
                            dtype=dt).view(np.recarray)
        assert_equal(added, expected)

    def test_dataframe_duplicate(self):
        df = pd.DataFrame(self.arr_2d, columns=['const', 'trend'])
        tsatools.add_trend(df, trend='ct')
        tsatools.add_trend(df, trend='ct', prepend=True)

    def test_array(self):
        base = np.vstack((self.arr_1d, self.c, self.t, self.t ** 2)).T
        assert_equal(tsatools.add_trend(self.arr_1d), base[:, :2])
        assert_equal(tsatools.add_trend(self.arr_1d, trend='t'),
                     base[:, [0, 2]])
        assert_equal(tsatools.add_trend(self.arr_1d, trend='ct'), base[:, :3])
        assert_equal(tsatools.add_trend(self.arr_1d, trend='ctt'), base)

        base = np.hstack((self.c[:, None],
                          self.t[:, None],
                          self.t[:, None]**2,
                          self.arr_2d))
        assert_equal(tsatools.add_trend(self.arr_2d,
                                        prepend=True),
                     base[:, [0, 3, 4]])

        assert_equal(tsatools.add_trend(self.arr_2d, trend='t',
                                        prepend=True),
                     base[:, [1, 3, 4]])

        assert_equal(tsatools.add_trend(self.arr_2d, trend='ct',
                                        prepend=True),
                     base[:, [0, 1, 3, 4]])

        assert_equal(tsatools.add_trend(self.arr_2d,
                                        trend='ctt', prepend=True),
                     base)

    def test_unknown_trend(self):
        with pytest.raises(ValueError):
            tsatools.add_trend(x=self.arr_1d, trend='unknown')


@pytest.mark.not_vetted
class TestLagmat2DS(object):
    @classmethod
    def setup_class(cls):
        data = datasets.macrodata.load_pandas()
        cls.macro_df = data.data[['year', 'quarter', 'realgdp', 'cpi']]
        cls.random_data = np.random.randn(100)
        index = [str(int(yr)) + '-Q' + str(int(qu))
                 for yr, qu in zip(cls.macro_df.year, cls.macro_df.quarter)]
        cls.macro_df.index = index
        cls.series = cls.macro_df.cpi

    @staticmethod
    def _prepare_expected(data, lags, trim='front'):
        t, k = data.shape
        expected = np.zeros((t + lags, (lags + 1) * k))
        for col in range(k):
            for i in range(lags + 1):
                if i < lags:
                    expected[i:-lags + i, (lags + 1) * col + i] = data[:, col]
                else:
                    expected[i:, (lags + 1) * col + i] = data[:, col]
        if trim == 'front':
            expected = expected[:-lags]
        return expected

    def test_lagmat2ds_numpy(self):
        data = self.macro_df
        npdata = data.values
        lagmat = tsatools.lagmat2ds(npdata, 2)
        expected = self._prepare_expected(npdata, 2)
        assert_array_equal(lagmat, expected)

        lagmat = tsatools.lagmat2ds(npdata[:, :2], 3)
        expected = self._prepare_expected(npdata[:, :2], 3)
        assert_array_equal(lagmat, expected)

        npdata = self.series.values
        lagmat = tsatools.lagmat2ds(npdata, 5)
        expected = self._prepare_expected(npdata[:, None], 5)
        assert_array_equal(lagmat, expected)

    def test_lagmat2ds_pandas(self):
        data = self.macro_df
        lagmat = tsatools.lagmat2ds(data, 2)
        expected = self._prepare_expected(data.values, 2)
        assert_array_equal(lagmat, expected)

        lagmat = tsatools.lagmat2ds(data.iloc[:, :2], 3, trim='both')
        expected = self._prepare_expected(data.values[:, :2], 3)
        expected = expected[3:]
        assert_array_equal(lagmat, expected)

        data = self.series
        lagmat = tsatools.lagmat2ds(data, 5)
        expected = self._prepare_expected(data.values[:, None], 5)
        assert_array_equal(lagmat, expected)

    def test_lagmat2ds_use_pandas(self):
        data = self.macro_df
        lagmat = tsatools.lagmat2ds(data, 2, use_pandas=True)
        expected = self._prepare_expected(data.values, 2)
        cols = []
        for c in data:
            for lags in range(3):
                if lags == 0:
                    cols.append(c)
                else:
                    cols.append(c + '.L.' + str(lags))
        expected = pd.DataFrame(expected, index=data.index, columns=cols)
        tm.assert_frame_equal(lagmat, expected)

        lagmat = tsatools.lagmat2ds(data.iloc[:, :2], 3,
                                    use_pandas=True, trim='both')
        expected = self._prepare_expected(data.values[:, :2], 3)
        cols = []
        for c in data.iloc[:, :2]:
            for lags in range(4):
                if lags == 0:
                    cols.append(c)
                else:
                    cols.append(c + '.L.' + str(lags))
        expected = pd.DataFrame(expected, index=data.index, columns=cols)
        expected = expected.iloc[3:]
        tm.assert_frame_equal(lagmat, expected)

        data = self.series
        lagmat = tsatools.lagmat2ds(data, 5, use_pandas=True)
        expected = self._prepare_expected(data.values[:, None], 5)

        cols = []
        c = data.name
        for lags in range(6):
            if lags == 0:
                cols.append(c)
            else:
                cols.append(c + '.L.' + str(lags))

        expected = pd.DataFrame(expected, index=data.index, columns=cols)
        tm.assert_frame_equal(lagmat, expected)

    def test_3d_error(self):
        data = np.array(2)
        with pytest.raises(ValueError):
            tsatools.lagmat2ds(data, 5)

        data = np.zeros((100, 2, 2))
        with pytest.raises(ValueError):
            tsatools.lagmat2ds(data, 5)
