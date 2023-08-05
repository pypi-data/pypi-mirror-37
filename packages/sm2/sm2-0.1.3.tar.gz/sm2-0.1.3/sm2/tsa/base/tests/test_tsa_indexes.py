"""
Test index support in time series models

1. Test support for passing / constructing the underlying index in __init__
2. Test wrapping of output using the underlying index
3. Test wrapping of prediction / forecasting using the underlying index or
   extensions of it.

Author: Chad Fulton
License: BSD-3
"""
from __future__ import division, absolute_import, print_function
import warnings

import numpy as np
import pandas as pd
import pytest

from sm2.tsa.base import tsa_model

nobs = 5
base_dta = np.arange(nobs)
dta = [base_dta.tolist(),
       base_dta,
       pd.Series(base_dta),
       pd.DataFrame(base_dta)]

base_date_indexes = [
    # (usual candidates)
    pd.DatetimeIndex(start='1950-01-01', periods=nobs, freq='D'),
    pd.DatetimeIndex(start='1950-01-01', periods=nobs, freq='W'),
    pd.DatetimeIndex(start='1950-01-01', periods=nobs, freq='M'),
    pd.DatetimeIndex(start='1950-01-01', periods=nobs, freq='Q'),
    pd.DatetimeIndex(start='1950-01-01', periods=nobs, freq='A'),
    # (some more complicated frequencies)
    pd.DatetimeIndex(start='1950-01-01', periods=nobs, freq='2Q'),
    pd.DatetimeIndex(start='1950-01-01', periods=nobs, freq='2QS'),
    pd.DatetimeIndex(start='1950-01-01', periods=nobs, freq='5s'),
    pd.DatetimeIndex(start='1950-01-01', periods=nobs, freq='1D10min')]

# Note: we separate datetime indexes and period indexes because the
# date coercion does not handle string versions of PeriodIndex objects
# most of the time.
base_period_indexes = [
    pd.PeriodIndex(start='1950-01-01', periods=nobs, freq='D'),
    pd.PeriodIndex(start='1950-01-01', periods=nobs, freq='W'),
    pd.PeriodIndex(start='1950-01-01', periods=nobs, freq='M'),
    pd.PeriodIndex(start='1950-01-01', periods=nobs, freq='Q'),
    pd.PeriodIndex(start='1950-01-01', periods=nobs, freq='A'),
    pd.PeriodIndex(start='1950-01-01', periods=nobs, freq='2Q'),
    pd.PeriodIndex(start='1950-01-01', periods=nobs, freq='5s'),
    pd.PeriodIndex(start='1950-01-01', periods=nobs, freq='1D10min')]


date_indexes = [(x, None) for x in base_date_indexes]
period_indexes = [(x, None) for x in base_period_indexes]

numpy_datestr_indexes = [(x.map(str), x.freq) for x in base_date_indexes]
list_datestr_indexes = [(x.tolist(), y) for x, y in numpy_datestr_indexes]
series_datestr_indexes = [(pd.Series(x), y) for x, y in list_datestr_indexes]

numpy_datetime_indexes = [(x.to_pydatetime(), x.freq)
                          for x in base_date_indexes]
list_datetime_indexes = [(x.tolist(), y) for x, y in numpy_datetime_indexes]
series_datetime_indexes = [(pd.Series(x, dtype=object), y)
                           for x, y in list_datetime_indexes]

series_timestamp_indexes = [(pd.Series(x), x.freq) for x in base_date_indexes]

# Supported increment indexes
supported_increment_indexes = [
    (pd.Int64Index(np.arange(nobs)), None),
    (pd.RangeIndex(start=0, stop=nobs, step=1), None),
    (pd.RangeIndex(start=-5, stop=nobs - 5, step=1), None),
    (pd.RangeIndex(start=0, stop=nobs * 6, step=6), None)]

# Supported date indexes
# Only the Int64Index and the `date_indexes` are valid without
# frequency information
supported_date_indexes = (numpy_datestr_indexes +
                          list_datestr_indexes + series_datestr_indexes +
                          numpy_datetime_indexes + list_datetime_indexes +
                          series_datetime_indexes + series_timestamp_indexes)

# Unsupported (but still valid) indexes
unsupported_indexes = [
    # Non-incrementing-from-zero indexes
    (np.arange(1, nobs + 1), None),
    (np.arange(nobs)[::-1], None),
    # Float indexes, even if they increment from zero
    (np.arange(nobs) * 1.0, None),
    # Non-date-string indexes
    ([x for x in 'abcde'], None),
    # Non-date-object indexes
    ([str, 1, 'a', -30.1, {}], None)]

# Unsupported date indexes (i.e. those without inferrable frequency)
unsupported_date_indexes = [(['1950', '1952', '1941', '1954', '1991'], None),
                            (['1950-01-01', '1950-01-02', '1950-01-03',
                              '1950-01-04', '1950-01-06'], None)]


@pytest.mark.not_vetted
def test_instantiation_no_dates():
    # See long comment in test_instantiation valid

    # Baseline: list, numpy endog with no dates, no freq
    for endog in dta[:2]:
        # No indexes, should not raise warnings
        with warnings.catch_warnings():
            warnings.simplefilter('error')

            mod = tsa_model.TimeSeriesModel(endog)
            assert isinstance(mod._index, (pd.Int64Index, pd.RangeIndex))
            assert mod._index_none is True
            assert mod._index_dates is False
            assert mod._index_generated is True
            assert mod.data.dates is None
            assert mod.data.freq is None


@pytest.mark.not_vetted
@pytest.mark.parametrize('endog', dta)
def test_instantiation_no_index_dti_or_pi(endog):
    # See long comment in test_instantiation valid
    # Test list, numpy endog, pandas w/o index; with dates / freq argument
    # dti --> DatetimeIndex
    # pi  --> PeriodIndex
    # Supported date indexes, should not raise warnings, do not need freq
    with warnings.catch_warnings():
        warnings.simplefilter('error')

        for ix, freq in date_indexes + period_indexes:
            mod = tsa_model.TimeSeriesModel(endog, dates=ix)
            if freq is None:
                freq = ix.freq
            if not isinstance(freq, str):
                freq = freq.freqstr
            assert isinstance(mod._index, (pd.DatetimeIndex,
                                           pd.PeriodIndex))
            assert mod._index_none is False
            assert mod._index_dates is True
            assert mod._index_generated is False
            assert mod._index.freq == mod._index_freq
            assert mod.data.dates.equals(mod._index) is True
            assert mod.data.freq == freq


@pytest.mark.not_vetted
@pytest.mark.parametrize('endog', dta)
def test_instantiation_no_index(endog):
    # See long comment in test_instantiation valid
    # Test list, numpy endog, pandas w/o index; with dates / freq argument

    # Supported date indexes, should not raise warnings, can use valid freq
    with warnings.catch_warnings():
        warnings.simplefilter('error')

        for ix, freq in date_indexes + period_indexes:
            mod = tsa_model.TimeSeriesModel(endog, dates=ix, freq=freq)
            if freq is None:
                freq = ix.freq
            if not isinstance(freq, str):
                freq = freq.freqstr
            assert isinstance(mod._index, (pd.DatetimeIndex, pd.PeriodIndex))
            assert mod._index_none is False
            assert mod._index_dates is True
            assert mod._index_generated is False
            assert mod._index.freq == mod._index_freq
            assert mod.data.dates.equals(mod._index)
            assert mod.data.freq == freq

    # Other supported indexes, with valid freq, should not raise warnings
    with warnings.catch_warnings():
        warnings.simplefilter('error')

        for ix, freq in supported_date_indexes:
            mod = tsa_model.TimeSeriesModel(endog, dates=ix, freq=freq)
            if freq is None:
                freq = ix.freq
            if not isinstance(freq, str):
                freq = freq.freqstr
            assert isinstance(mod._index, (pd.DatetimeIndex, pd.PeriodIndex))
            assert mod._index_none is False
            assert mod._index_dates is True
            assert mod._index_generated is False
            assert mod._index.freq == mod._index_freq
            assert mod.data.dates.equals(mod._index)
            assert mod.data.freq == freq

    # Since only supported indexes are valid `dates` arguments, everything
    # else is invalid here
    for ix, freq in supported_increment_indexes + unsupported_indexes:
        with pytest.raises(ValueError):
            tsa_model.TimeSeriesModel(endog, dates=ix)


@pytest.mark.not_vetted
def test_instantiation_valid_datetimeindex_periodindex():
    # See long comment in test_instantiation valid
    # Test pandas (Series, DataFrame); with index (no dates/freq argument)
    for base_endog in dta[2:4]:
        # DatetimeIndex and PeriodIndex, should not raise warnings
        with warnings.catch_warnings():
            warnings.simplefilter('error')

            for ix, freq in date_indexes + period_indexes:
                endog = base_endog.copy()
                endog.index = ix

                mod = tsa_model.TimeSeriesModel(endog)
                if freq is None:
                    freq = ix.freq
                if not isinstance(freq, str):
                    freq = freq.freqstr
                assert isinstance(mod._index,
                                  (pd.DatetimeIndex, pd.PeriodIndex))
                assert mod._index_none is False
                assert mod._index_dates is True
                assert mod._index_generated is False
                assert mod._index.freq == mod._index_freq
                assert mod.data.dates.equals(mod._index)
                assert mod.data.freq == freq


@pytest.mark.not_vetted
def test_instantiation_valid_supported_with_freq():
    # See long comment in test_instantiation valid
    # Supported indexes *when a freq is given*, should not raise a warning
    for base_endog in dta[2:4]:
        with warnings.catch_warnings():
            warnings.simplefilter('error')

            for ix, freq in supported_date_indexes:
                endog = base_endog.copy()
                endog.index = ix

                mod = tsa_model.TimeSeriesModel(endog, freq=freq)
                if freq is None:
                    freq = ix.freq
                if not isinstance(freq, str):
                    freq = freq.freqstr
                assert isinstance(mod._index,
                                  (pd.DatetimeIndex, pd.PeriodIndex))
                assert mod._index_none is False
                assert mod._index_dates is True
                assert mod._index_generated is False
                assert mod._index.freq == mod._index_freq
                assert mod.data.dates.equals(mod._index) is True
                assert mod.data.freq == freq


@pytest.mark.not_vetted
def test_instantiation_valid_range_index():
    # GH#4457
    # See long comment in `test_instantiation_valid`
    for base_endog in dta[2:4]:
        # RangeIndex (start=0, end=nobs, so equivalent to increment index)
        endog = base_endog.copy()
        endog.index = supported_increment_indexes[1][0]

        mod = tsa_model.TimeSeriesModel(endog)
        assert type(mod._index) is pd.RangeIndex  # noqa:E721
        assert mod._index_none is False
        assert mod._index_dates is False
        assert mod._index_generated is False
        assert mod._index_freq is None
        assert mod.data.dates is None
        assert mod.data.freq is None


@pytest.mark.not_vetted
def test_instantiation_valid():
    tsa_model.__warningregistry__ = {}

    # The primary goal of this test function is to make sure the
    # combinations that are supposed to be valid are actually valid, and
    # that valid but unsupported options give the appropriate warning
    # Secondarily, it also has some tests that invalid combinations raise
    # exceptions, although it's not intended to be comprehensive.
    #
    # Each of `endog`, `exog` can be in the following categories:
    # 0. None (only for exog)
    # 1. list
    # 2. numpy array
    # 3. pandas series
    # 4. pandas dataframe
    #
    # Each pandas index (of `endog`, `exog`, or passed to `dates`) can be:
    # 0. None
    # 1. RangeIndex (if applicable; i.e. if Pandas >= 0.18)
    # 2. Int64Index with values exactly equal to 0, 1, ..., nobs-1
    # 3. DatetimeIndex with frequency
    # 4. PeriodIndex with frequency
    # 5. Anything that doesn't fall into the above categories also should
    #    only raise an exception if it was passed to dates, and may trigger
    #    a warning otherwise.
    #
    # `date` can be one of the following:
    # 0. None
    # 2. Pandas index #2
    # 3. Pandas index #3
    # 4. List of date strings (requires freq)
    # 5. List of datetime objects (requires freq)
    # 6. Array of date strings (requires freq)
    # 7. Array of datetime objects (requires freq)
    # 8. Series of date strings (requires freq)
    # 9. Series of datetime objects (requires freq)
    # 10. Series of pandas timestamps (requires freq)
    # 11. Anything that doesn't fall into the above categories should raise
    #     an exception.
    #
    # `freq` can be:
    # 0. None
    # 1. Something that can be passed to `pd.to_offset`
    # 2. Anything that can't should raise an Exception
    #
    # Each test will be denoted by:
    # endog.index:exog.index/date/freq where the corresponding
    # location is the integer from above; e.g. 1.0:0.0/9/1 corresponds to
    # - List endog (with no index)
    # - No exog
    # - Series of datetime objects
    # - Something valid for `pd.to_offset` (e.g. 'D', if that works with
    #   dates)
    #
    # Notice that the endog.index:exog.index really collapses to a single
    # element, which is the evaluated `row_label`. This is first the exog
    # index, if exists, then the endog index, if it exists, or None
    # otherwise. **Thus, we will not test `exog` here.**
    #
    # Example valid combinations of row_label/date/freq include:
    # - */0/0 (i.e. anything is valid if date and freq are not passed)
    # - */%/% where %/% denotes a valid date/freq combination (i.e. any
    #   row_label is valid if a valid date/freq combination is given)
    #
    # Example invalid combinations include:
    # - [1-2],[3-4].4/0/[1-2] (i.e. if have freq, then must have, or
    #   coerce, a date index)
    # - */[4-10]/0 (i.e. for some types of dates, freq must be passed)

    # Test pandas (Series, DataFrame); with index (no dates/freq argument)
    for base_endog in dta[2:4]:
        # Increment index (this is a "supported" index in the sense that it
        # doesn't raise a warning, but obviously not a date index)
        endog = base_endog.copy()
        endog.index = supported_increment_indexes[0][0]

        mod = tsa_model.TimeSeriesModel(endog)
        assert isinstance(mod._index, (pd.Int64Index, pd.RangeIndex))
        assert mod._index_none is False
        assert mod._index_dates is False
        assert mod._index_generated is False
        assert mod._index_freq is None
        assert mod.data.dates is None
        assert mod.data.freq is None

        # Unsupported (or any) indexes to the given series, *when a supported
        # date and freq is given*, should not raise a warning
        with warnings.catch_warnings():
            warnings.simplefilter('error')

            for ix, freq in supported_date_indexes:
                endog = base_endog.copy()
                endog.index = unsupported_indexes[0][0]

                mod = tsa_model.TimeSeriesModel(endog, dates=ix, freq=freq)
                if freq is None:
                    freq = ix.freq
                if not isinstance(freq, str):
                    freq = freq.freqstr
                assert isinstance(mod._index,
                                  (pd.DatetimeIndex, pd.PeriodIndex))
                assert mod._index_none is False
                assert mod._index_dates is True
                assert mod._index_generated is False
                assert mod._index.freq == mod._index_freq
                assert mod.data.dates.equals(mod._index)
                assert mod.data.freq == freq

        # Date indexes with inferrable freq, but no given freq, should all give
        # warnings
        message = ('No frequency information was provided,'
                   ' so inferred frequency %s will be used.')
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')

            for ix, freq in supported_date_indexes:
                endog = base_endog.copy()
                endog.index = ix
                mod = tsa_model.TimeSeriesModel(endog)
                if freq is None:
                    freq = ix.freq
                if not isinstance(freq, str):
                    freq = freq.freqstr
                assert isinstance(mod._index, pd.DatetimeIndex)
                assert mod._index_none is False
                assert mod._index_dates is True
                assert mod._index_generated is False
                assert mod._index.freq == mod._index_freq
                assert mod.data.dates.equals(mod._index)

                # Note: here, we need to hedge the test a little bit because
                # inferred frequencies aren't always the same as the original
                # frequency. From the examples above, when the actual freq is
                # 2QS-OCT, the inferred freq is 2QS-JAN. This is an issue with
                # inferred frequencies, but since we are warning the user, it's
                # not a failure of the code. Thus we only test the "major" part
                # of the freq, and just test that the right message is given
                # (even though it won't have the actual freq of the data in
                # it).
                assert mod.data.freq.split('-')[0] == freq.split('-')[0]
                assert str(w[-1].message) == message % mod.data.freq

        # Unsupported (but valid) indexes, should all give warnings
        message = ('An unsupported index was provided and will be'
                   ' ignored when e.g. forecasting.')
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')

            for ix, freq in unsupported_indexes:
                endog = base_endog.copy()
                endog.index = ix
                mod = tsa_model.TimeSeriesModel(endog)
                assert isinstance(mod._index, (pd.Int64Index, pd.RangeIndex))
                assert mod._index_none is False
                assert mod._index_dates is False
                assert mod._index_generated is True
                assert mod._index_freq is None
                assert mod.data.dates is None
                assert mod.data.freq is None

                assert str(w[0].message) == message

        # Date indexes without inferrable freq, and with no given freq, should
        # all give warnings
        message = ('A date index has been provided, but it has no'
                   ' associated frequency information and so will be'
                   ' ignored when e.g. forecasting.')
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')

            for ix, freq in unsupported_date_indexes:
                endog = base_endog.copy()
                endog.index = ix
                mod = tsa_model.TimeSeriesModel(endog)
                assert isinstance(mod._index, (pd.Int64Index, pd.RangeIndex))
                assert mod._index_none is False
                assert mod._index_dates is False
                assert mod._index_generated is True
                assert mod._index_freq is None
                assert mod.data.dates is None
                assert mod.data.freq is None

                assert str(w[0].message) == message


@pytest.mark.not_vetted
def test_instantiation_invalid():
    # See long comment in test_instantiation_valid
    # Test (invalid) freq with no index
    endog = dta[0]
    with pytest.raises(ValueError):
        tsa_model.TimeSeriesModel(endog, freq=date_indexes[1][0].freq)

    # Test conflicting index, freq specifications
    endog = dta[2].copy()
    endog.index = date_indexes[0][0]
    with pytest.raises(ValueError):
        tsa_model.TimeSeriesModel(endog, freq=date_indexes[1][0].freq)

    # Test unsupported index, but a freq specification
    endog = dta[2].copy()
    endog.index = unsupported_indexes[0][0]
    with pytest.raises(ValueError):
        tsa_model.TimeSeriesModel(endog, freq=date_indexes[1][0].freq)

    # Test index that can coerce to date time but incorrect freq
    endog = dta[2].copy()
    endog.index = numpy_datestr_indexes[0][0]
    with pytest.raises(ValueError):
        tsa_model.TimeSeriesModel(endog, freq=date_indexes[1][0].freq)


@pytest.mark.not_vetted
def test_prediction_increment_unsupported():
    # a. Generated from unsupported index
    endog = dta[2].copy()
    endog.index = unsupported_indexes[-2][0]
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter('ignore')
        mod = tsa_model.TimeSeriesModel(endog)

    # Basic prediction: [0, end]; notice that since this is an in-sample
    # prediction, the index returned is the (unsupported) original index
    start_key = 0
    end_key = None
    start, end, out_of_sample, prediction_index = (
        mod._get_prediction_index(start_key, end_key))

    assert start == 0
    assert end == nobs - 1
    assert out_of_sample == 0
    assert prediction_index.equals(mod.data.row_labels)

    # Negative index: [-2, end]; notice that since this is an in-sample
    # prediction, the index returned is a piece of the (unsupported)
    # original index
    start_key = -2
    end_key = -1
    start, end, out_of_sample, prediction_index = (
        mod._get_prediction_index(start_key, end_key))

    assert start == 3
    assert end == 4
    assert out_of_sample == 0
    assert prediction_index.equals(mod.data.row_labels[3:])

    # Forecasting: [1, 5], notice that since an unsupported index was given,
    # a warning will be issued
    start_key = 1
    end_key = nobs
    message = ('No supported index is available.'
               ' Prediction results will be given with'
               ' an integer index beginning at `start`.')
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter('always')

        start, end, out_of_sample, prediction_index = (
            mod._get_prediction_index(start_key, end_key))

        # FIXME: 2018-09-21 this fails on appveyor, but inconsistently
        # FIXME: dont comment-out code
        #assert str(w[0].message) == message

    assert start == 1
    assert end == 4
    assert out_of_sample == 1
    assert prediction_index.equals(pd.Index(np.arange(1, 6)))


@pytest.mark.not_vetted
def test_prediction_increment_nonpandas():
    endog = dta[0]
    mod = tsa_model.TimeSeriesModel(endog)

    # Basic prediction: [0, end]; since there was no index at all and the data
    # is not Pandas, the returned prediction_index is None
    start_key = 0
    end_key = None
    start, end, out_of_sample, prediction_index = (
        mod._get_prediction_index(start_key, end_key))

    assert start == 0
    assert end == nobs - 1
    assert out_of_sample == 0
    assert prediction_index is None

    # Negative index: [-2, end]; since there was no index at all and the data
    # is not Pandas, the returned prediction_index is None
    start_key = -2
    end_key = -1
    start, end, out_of_sample, prediction_index = (
        mod._get_prediction_index(start_key, end_key))

    assert start == 3
    assert end == 4
    assert out_of_sample == 0
    assert prediction_index is None

    # Forecasting: [1, 5]; since there was no index at all and the data
    # is not Pandas, the returned prediction_index is None
    start_key = 1
    end_key = nobs
    start, end, out_of_sample, prediction_index = (
        mod._get_prediction_index(start_key, end_key))

    assert start == 1
    assert end == 4
    assert out_of_sample == 1
    assert prediction_index is None


@pytest.mark.not_vetted
def test_prediction_increment_pandas_noindex():
    endog = dta[2].copy()
    mod = tsa_model.TimeSeriesModel(endog)

    # Basic prediction: [0, end]; since there was no index and the data is
    # Pandas, the index is the generated incrementing index, and no warning is
    # issued
    start_key = 0
    end_key = None
    start, end, out_of_sample, prediction_index = (
        mod._get_prediction_index(start_key, end_key))

    assert start == 0
    assert end == nobs - 1
    assert out_of_sample == 0
    assert prediction_index.equals(mod._index)

    # Negative index: [-2, end]; since there was no index and the data is
    # Pandas, the index is the generated incrementing index, and no warning is
    # issued
    start_key = -2
    end_key = -1
    start, end, out_of_sample, prediction_index = (
        mod._get_prediction_index(start_key, end_key))

    assert start == 3
    assert end == 4
    assert out_of_sample == 0
    assert prediction_index.equals(mod._index[3:])

    # Forecasting: [1, 5]; since there was no index and the data is
    # Pandas, the index is the generated incrementing index, and no warning is
    # issued
    start_key = 1
    end_key = nobs
    start, end, out_of_sample, prediction_index = (
        mod._get_prediction_index(start_key, end_key))

    assert start == 1
    assert end == 4
    assert out_of_sample == 1
    assert prediction_index.equals(pd.Index(np.arange(1, 6)))


@pytest.mark.not_vetted
def test_prediction_increment_pandas_dates():
    # Date-based index
    endog = dta[2].copy()
    endog.index = date_indexes[0][0]  # Daily, 1950-01-01, 1950-01-02, ...
    mod = tsa_model.TimeSeriesModel(endog)

    # Basic prediction: [0, end]; the index is the date index
    start_key = 0
    end_key = None
    start, end, out_of_sample, prediction_index = (
        mod._get_prediction_index(start_key, end_key))

    assert start == 0
    assert end == nobs - 1
    assert out_of_sample == 0
    assert type(prediction_index) is type(endog.index)  # noqa: E721
    assert prediction_index.equals(mod._index)

    # Negative index: [-2, end]
    start_key = -2
    end_key = -1
    start, end, out_of_sample, prediction_index = (
        mod._get_prediction_index(start_key, end_key))

    assert start == 3
    assert end == 4
    assert out_of_sample == 0
    assert type(prediction_index) is type(endog.index)  # noqa: E721
    assert prediction_index.equals(mod._index[3:])

    # Forecasting: [1, 5]; the index is an extended version of the date index
    start_key = 1
    end_key = nobs
    start, end, out_of_sample, prediction_index = (
        mod._get_prediction_index(start_key, end_key))

    assert start == 1
    assert end == 4
    assert out_of_sample == 1
    desired_index = pd.DatetimeIndex(start='1950-01-02', periods=5, freq='D')
    assert prediction_index.equals(desired_index)

    # Date-based keys
    start_key = '1950-01-01'
    end_key = '1950-01-08'
    start, end, out_of_sample, prediction_index = (
        mod._get_prediction_index(start_key, end_key))

    assert start == 0
    assert end == 4
    assert out_of_sample == 3
    desired_index = pd.DatetimeIndex(start='1950-01-01', periods=8, freq='D')
    assert prediction_index.equals(desired_index)


@pytest.mark.not_vetted
def test_prediction_increment_pandas_dates_nanosecond():
    # upstream has a try/except that skips this test for pandas <= 0.14.  Since
    # that is several years old, we assume that case away.

    # Date-based index
    endog = dta[2].copy()
    endog.index = pd.DatetimeIndex(start='1970-01-01', periods=len(endog),
                                   freq='N')
    mod = tsa_model.TimeSeriesModel(endog)

    # Basic prediction: [0, end]; the index is the date index
    start_key = 0
    end_key = None
    start, end, out_of_sample, prediction_index = (
        mod._get_prediction_index(start_key, end_key))

    assert start == 0
    assert end == nobs - 1
    assert out_of_sample == 0
    assert type(prediction_index) is type(endog.index)  # noqa: E721
    assert prediction_index.equals(mod._index)

    # Negative index: [-2, end]
    start_key = -2
    end_key = -1
    start, end, out_of_sample, prediction_index = (
        mod._get_prediction_index(start_key, end_key))

    assert start == 3
    assert end == 4
    assert out_of_sample == 0
    assert type(prediction_index) is type(endog.index)  # noqa: E721
    assert prediction_index.equals(mod._index[3:])

    # Forecasting: [1, 5]; the index is an extended version of the date index
    start_key = 1
    end_key = nobs
    start, end, out_of_sample, prediction_index = (
        mod._get_prediction_index(start_key, end_key))

    assert start == 1
    assert end == 4
    assert out_of_sample == 1
    desired_index = pd.DatetimeIndex(start='1970-01-01',
                                     periods=6, freq='N')[1:]
    assert prediction_index.equals(desired_index)

    # Date-based keys
    start_key = pd.Timestamp('1970-01-01')
    end_key = pd.Timestamp(start_key.value + 7)
    start, end, out_of_sample, prediction_index = (
        mod._get_prediction_index(start_key, end_key))

    assert start == 0
    assert end == 4
    assert out_of_sample == 3
    desired_index = pd.DatetimeIndex(start='1970-01-01', periods=8, freq='N')
    assert prediction_index.equals(desired_index)


@pytest.mark.not_vetted
def test_custom_index():
    tsa_model.__warningregistry__ = {}

    endog = pd.Series(np.random.normal(size=5),
                      index=['a', 'b', 'c', 'd', 'e'])
    message = ('An unsupported index was provided and will be ignored when'
               ' e.g. forecasting.')
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter('always')

        mod = tsa_model.TimeSeriesModel(endog)
        assert str(w[0].message) == message
    start_key = -2
    end_key = -1
    start, end, out_of_sample, prediction_index = (
        mod._get_prediction_index(start_key, end_key))

    # Test the default output index
    assert prediction_index.equals(pd.Index(['d', 'e']))
    start, end, out_of_sample, prediction_index = (
        mod._get_prediction_index(start_key, end_key, index=['f', 'g']))

    # Test custom output index
    assert prediction_index.equals(pd.Index(['f', 'g']))

    # Test out-of-sample
    start_key = 4
    end_key = 5
    message = ('No supported index is available.'
               ' Prediction results will be given with'
               ' an integer index beginning at `start`.')
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter('always')

        start, end, out_of_sample, prediction_index = (
            mod._get_prediction_index(start_key, end_key))
        assert prediction_index.equals(pd.Index([4, 5]))
        assert str(w[0].message) == message

    # Test out-of-sample custom index
    start, end, out_of_sample, prediction_index = (
        mod._get_prediction_index(start_key, end_key, index=['f', 'g']))
    assert prediction_index.equals(pd.Index(['f', 'g']))

    # Test invalid custom index
    with pytest.raises(ValueError):
        mod._get_prediction_index(start_key, end_key, index=['f', 'g', 'h'])


def test_range_index():
    # GH#4457
    tsa_model.__warningregistry__ = {}

    endog = pd.Series(np.random.normal(size=5))
    assert isinstance(endog.index, pd.RangeIndex)
    # Warning should not be given
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter('always')
        tsa_model.TimeSeriesModel(endog)
        assert len(w) == 0


def test_prediction_rangeindex():
    # GH#4457
    index = supported_increment_indexes[2][0]
    endog = pd.Series(dta[0], index=index)
    mod = tsa_model.TimeSeriesModel(endog)

    # Tests three common use cases: basic prediction, negative indexes, and
    # out-of-sample indexes.

    # Basic prediction: [0, end]
    start_key = 0
    end_key = None
    start, end, out_of_sample, prediction_index = (
        mod._get_prediction_index(start_key, end_key))

    assert start == 0
    assert end == nobs - 1
    assert out_of_sample == 0
    desired_index = pd.RangeIndex(start=-5, stop=0, step=1)
    assert prediction_index.equals(desired_index)

    # Negative index: [-2, end]
    start_key = -2
    end_key = -1
    start, end, out_of_sample, prediction_index = (
        mod._get_prediction_index(start_key, end_key))

    assert start == 3
    assert end == 4
    assert out_of_sample == 0
    desired_index = pd.RangeIndex(start=-2, stop=0, step=1)
    assert prediction_index.equals(desired_index)

    # Forecasting: [1, 5]
    start_key = 1
    end_key = nobs
    start, end, out_of_sample, prediction_index = (
        mod._get_prediction_index(start_key, end_key))

    assert start == 1
    assert end == 4
    assert out_of_sample == 1
    desired_index = pd.RangeIndex(start=-4, stop=1, step=1)
    assert prediction_index.equals(desired_index)


def test_prediction_rangeindex_withstep():
    # GH#4457
    index = supported_increment_indexes[3][0]
    endog = pd.Series(dta[0], index=index)
    mod = tsa_model.TimeSeriesModel(endog)

    # Tests three common use cases: basic prediction, negative indexes, and
    # out-of-sample indexes.

    # Basic prediction: [0, end]
    start_key = 0
    end_key = None
    start, end, out_of_sample, prediction_index = (
        mod._get_prediction_index(start_key, end_key))

    assert start == 0
    assert end == nobs - 1
    assert out_of_sample == 0
    desired_index = pd.RangeIndex(start=0, stop=nobs * 6, step=6)
    assert prediction_index.equals(desired_index)

    # Negative index: [-2, end]
    start_key = -2
    end_key = -1
    start, end, out_of_sample, prediction_index = (
        mod._get_prediction_index(start_key, end_key))

    assert start == 3
    assert end == 4
    assert out_of_sample == 0
    desired_index = pd.RangeIndex(start=3 * 6, stop=nobs * 6, step=6)
    assert prediction_index.equals(desired_index)

    # Forecasting: [1, 5]
    start_key = 1
    end_key = nobs
    start, end, out_of_sample, prediction_index = (
        mod._get_prediction_index(start_key, end_key))

    assert start == 1
    assert end == 4
    assert out_of_sample == 1
    desired_index = pd.RangeIndex(start=1 * 6, stop=(nobs + 1) * 6, step=6)
    assert prediction_index.equals(desired_index)
