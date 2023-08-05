"""
Test functions for models.regression
"""
# TODO: Test for LM
import warnings
import os
import re
import textwrap

import pytest
import pandas as pd
import numpy as np
from numpy.testing import (assert_almost_equal,
                           assert_equal, assert_allclose)
from scipy.linalg import toeplitz
from scipy import stats
from patsy import PatsyError

from sm2.tools.sm_exceptions import MissingDataError
from sm2.tools.tools import add_constant, categorical
from sm2.regression.linear_model import OLS, WLS, GLS, GLSAR
from sm2 import datasets

from .results import results_regression
from . import glmnet_r_results  # used by TestRegularizedFit

cur_dir = os.path.dirname(os.path.abspath(__file__))
lasso_path = os.path.join(cur_dir, "results", "lasso_data.csv")
lasso_data = np.loadtxt(lasso_path, delimiter=",")
# lasso_data used by TestRegularizedFit

DECIMAL_7 = 7
DECIMAL_4 = 4


@pytest.mark.not_vetted
class CheckRegressionResults(object):
    """
    res2 contains results from Rmodelwrap or were obtained from a statistical
    packages such as R, Stata, or SAS and were written to model_results
    """
    _do_check_wresid = True

    def test_params(self):
        assert_almost_equal(self.res1.params,
                            self.res2.params,
                            DECIMAL_4)

    def test_standarderrors(self):
        assert_almost_equal(self.res1.bse,
                            self.res2.bse,
                            DECIMAL_4)

    def test_confidenceintervals(self):
        # NOTE: stata rounds residuals (at least) to sig digits so approx_equal
        conf1 = self.res1.conf_int()
        conf2 = self.res2.conf_int()
        for i in range(len(conf1)):
            assert_allclose(conf1[i][0],
                            conf2[i][0],
                            rtol=1e-4)
            assert_allclose(conf1[i][1],
                            conf2[i][1],
                            rtol=1e-4)

    def test_conf_int_subset(self):
        if len(self.res1.params) > 1:
            ci1 = self.res1.conf_int(cols=(1, 2))
            ci2 = self.res1.conf_int()[1:3]
            assert_almost_equal(ci1,
                                ci2,
                                DECIMAL_4)
        else:
            pass

    def test_scale(self):
        assert_almost_equal(self.res1.scale,
                            self.res2.scale,
                            DECIMAL_4)

    def test_rsquared(self):
        assert_almost_equal(self.res1.rsquared,
                            self.res2.rsquared,
                            DECIMAL_4)

    def test_rsquared_adj(self):
        assert_almost_equal(self.res1.rsquared_adj,
                            self.res2.rsquared_adj,
                            DECIMAL_4)

    def test_degrees(self):
        assert self.res1.model.df_model == self.res2.df_model
        assert self.res1.model.df_resid == self.res2.df_resid

    def test_ess(self):
        # Explained Sum of Squares
        assert_almost_equal(self.res1.ess,
                            self.res2.ess,
                            DECIMAL_4)

    def test_sumof_squaredresids(self):
        assert_almost_equal(self.res1.ssr,
                            self.res2.ssr,
                            DECIMAL_4)

    def test_mse_resid(self):
        # Mean squared error of residuals
        assert_almost_equal(self.res1.mse_model,
                            self.res2.mse_model,
                            DECIMAL_4)

    def test_mse_model(self):
        assert_almost_equal(self.res1.mse_resid,
                            self.res2.mse_resid,
                            DECIMAL_4)

    def test_mse_total(self):
        assert_almost_equal(self.res1.mse_total,
                            self.res2.mse_total,
                            DECIMAL_4,
                            err_msg="Test class %s" % self)

    def test_fvalue(self):
        # didn't change this, not sure it should complain -inf not equal -inf
        # if not (np.isinf(self.res1.fvalue) and np.isinf(self.res2.fvalue)):
        assert_almost_equal(self.res1.fvalue,
                            self.res2.fvalue,
                            DECIMAL_4)

    def test_loglike(self):
        assert_almost_equal(self.res1.llf,
                            self.res2.llf,
                            DECIMAL_4)

    def test_aic(self):
        assert_almost_equal(self.res1.aic,
                            self.res2.aic,
                            DECIMAL_4)

    def test_bic(self):
        assert_almost_equal(self.res1.bic,
                            self.res2.bic,
                            DECIMAL_4)

    def test_pvalues(self):
        assert_almost_equal(self.res1.pvalues,
                            self.res2.pvalues,
                            DECIMAL_4)

    def test_wresid(self):
        if not self._do_check_wresid:  # TODO: pytest.skip?
            return
        assert_almost_equal(self.res1.wresid,
                            self.res2.wresid,
                            DECIMAL_4)

    def test_resids(self):
        assert_almost_equal(self.res1.resid,
                            self.res2.resid,
                            DECIMAL_4)

    def test_norm_resids(self):
        assert_almost_equal(self.res1.resid_pearson,
                            self.res2.resid_pearson,
                            DECIMAL_4)


# TODO: test fittedvalues and what else?


@pytest.mark.not_vetted
class TestOLS(CheckRegressionResults):
    res2 = results_regression.Longley()
    _do_check_wresid = False

    @classmethod
    def setup_class(cls):
        data = datasets.longley.load(as_pandas=False)
        data.exog = add_constant(data.exog, prepend=False)
        cls.res1 = OLS(data.endog, data.exog).fit()
        #cls.res2.wresid = cls.res1.wresid  # workaround hack

        res_qr = OLS(data.endog, data.exog).fit(method="qr")

        model_qr = OLS(data.endog, data.exog)
        Q, R = np.linalg.qr(data.exog)
        model_qr.exog_Q, model_qr.exog_R = Q, R
        model_qr.normalized_cov_params = np.linalg.inv(np.dot(R.T, R))
        model_qr.rank = np.linalg.matrix_rank(R)
        res_qr2 = model_qr.fit(method="qr")

        cls.res_qr = res_qr
        cls.res_qr_manual = res_qr2

    def test_eigenvalues(self):
        eigenval_perc_diff = (self.res_qr.eigenvals -
                              self.res_qr_manual.eigenvals)
        eigenval_perc_diff /= self.res_qr.eigenvals
        zeros = np.zeros_like(eigenval_perc_diff)
        assert_almost_equal(eigenval_perc_diff, zeros, DECIMAL_7)

    # Robust error tests.  Compare values computed with SAS
    def test_HC0_errors(self):
        # They are split up because the copied results do not have any
        # DECIMAL_4 places for the last place.
        assert_almost_equal(self.res1.HC0_se[:-1],
                            self.res2.HC0_se[:-1],
                            DECIMAL_4)
        assert_allclose(np.round(self.res1.HC0_se[-1]),
                        self.res2.HC0_se[-1])

    def test_HC1_errors(self):
        assert_almost_equal(self.res1.HC1_se[:-1],
                            self.res2.HC1_se[:-1],
                            DECIMAL_4)
        # Note: tolerance is tight; rtol=3e-7 fails while 4e-7 passes
        assert_allclose(self.res1.HC1_se[-1], self.res2.HC1_se[-1],
                        rtol=4e-7)

    def test_HC2_errors(self):
        assert_almost_equal(self.res1.HC2_se[:-1],
                            self.res2.HC2_se[:-1],
                            DECIMAL_4)
        # Note: tolerance is tight; rtol=4e-7 fails while 5e-7 passes
        assert_allclose(self.res1.HC2_se[-1], self.res2.HC2_se[-1],
                        rtol=5e-7)

    def test_HC3_errors(self):
        assert_almost_equal(self.res1.HC3_se[:-1],
                            self.res2.HC3_se[:-1],
                            DECIMAL_4)
        # Note: tolerance is tight; rtol=1e-7 fails while 1.5e-7 passes
        assert_allclose(self.res1.HC3_se[-1], self.res2.HC3_se[-1],
                        rtol=1.5e-7)

    def test_qr_params(self):
        assert_almost_equal(self.res1.params,
                            self.res_qr.params,
                            6)

    def test_qr_normalized_cov_params(self):
        # TODO: need assert_close
        assert_almost_equal(np.ones_like(self.res1.normalized_cov_params),
                            self.res1.normalized_cov_params /
                            self.res_qr.normalized_cov_params,
                            5)

    def test_missing(self):
        data = datasets.longley.load(as_pandas=False)
        data.exog = add_constant(data.exog, prepend=False)
        data.endog[[3, 7, 14]] = np.nan
        mod = OLS(data.endog, data.exog, missing='drop')
        assert mod.endog.shape[0] == 13
        assert mod.exog.shape[0] == 13

    def test_rsquared_adj_overfit(self):
        # Test that if df_resid = 0, rsquared_adj = 0.
        # This is a regression test for user issue:
        # GH#868
        with warnings.catch_warnings(record=True):
            x = np.random.randn(5)
            y = np.random.randn(5, 6)
            results = OLS(x, y).fit()
            rsquared_adj = results.rsquared_adj
            assert_equal(rsquared_adj, np.nan)

    def test_qr_alternatives(self):
        assert_allclose(self.res_qr.params,
                        self.res_qr_manual.params,
                        rtol=5e-12)

    def test_norm_resid(self):
        resid = self.res1.wresid
        norm_resid = resid / np.sqrt(np.sum(resid**2.0) / self.res1.df_resid)
        model_norm_resid = self.res1.resid_pearson
        assert_almost_equal(model_norm_resid,
                            norm_resid,
                            DECIMAL_7)

    def test_norm_resid_zero_variance(self):
        with warnings.catch_warnings(record=True):
            y = self.res1.model.endog
            res = OLS(y, y).fit()
            assert_allclose(res.scale, 0,
                            atol=1e-20)
            assert_allclose(res.wresid,
                            res.resid_pearson,
                            atol=5e-11)


@pytest.mark.not_vetted
class TestRTO(CheckRegressionResults):
    res2 = results_regression.LongleyRTO()
    _do_check_wresid = False

    @classmethod
    def setup_class(cls):
        data = datasets.longley.load(as_pandas=False)
        res1 = OLS(data.endog, data.exog).fit()
        cls.res1 = res1
        #cls.res2.wresid = res1.wresid  # workaround hack

        res_qr = OLS(data.endog, data.exog).fit(method="qr")
        cls.res_qr = res_qr


@pytest.mark.not_vetted
class TestGLS_alt_sigma(CheckRegressionResults):
    """
    Test that GLS with no argument is equivalent to OLS.
    """
    @classmethod
    def setup_class(cls):
        data = datasets.longley.load(as_pandas=False)
        data.exog = add_constant(data.exog, prepend=False)
        ols_res = OLS(data.endog, data.exog).fit()
        gls_res = GLS(data.endog, data.exog).fit()
        gls_res_scalar = GLS(data.endog, data.exog, sigma=1)
        cls.endog = data.endog
        cls.exog = data.exog
        cls.res1 = gls_res
        cls.res2 = ols_res
        cls.res3 = gls_res_scalar  # TODO: Do something with this?

    def test_wrong_size_sigma_1d(self):
        n = len(self.endog)
        with pytest.raises(ValueError):
            GLS(self.endog, self.exog, sigma=np.ones(n - 1))

    def test_wrong_size_sigma_2d(self):
        n = len(self.endog)
        with pytest.raises(ValueError):
            GLS(self.endog, self.exog, sigma=np.ones((n - 1, n - 1)))


@pytest.mark.not_vetted
class TestWLSExogWeights(CheckRegressionResults):
    # Test WLS with Greene's credit card data
    # reg avgexp age income incomesq ownrent [aw=1/incomesq]
    res2 = results_regression.CCardWLS()
    _do_check_wresid = False

    @classmethod
    def setup_class(cls):
        dta = datasets.ccard.load(as_pandas=False)

        dta.exog = add_constant(dta.exog, prepend=False)
        nobs = 72.

        weights = 1 / dta.exog[:, 2]
        # for comparison with stata analytic weights
        scaled_weights = ((weights * nobs) / weights.sum())

        cls.res1 = WLS(dta.endog, dta.exog, weights=scaled_weights).fit()
        #cls.res2.wresid = scaled_weights ** .5 * cls.res2.resid

        # correction because we use different definition for loglike/llf
        corr_ic = 2 * (cls.res1.llf - cls.res2.llf)
        cls.res2.aic -= corr_ic
        cls.res2.bic -= corr_ic
        cls.res2.llf += 0.5 * np.sum(np.log(cls.res1.model.weights))


@pytest.mark.not_vetted
class TestWLSScalarVsArray(CheckRegressionResults):
    @classmethod
    def setup_class(cls):
        dta = datasets.longley.load(as_pandas=False)
        dta.exog = add_constant(dta.exog, prepend=True)

        wls_scalar = WLS(dta.endog, dta.exog, weights=1. / 3).fit()
        cls.res1 = wls_scalar

        weights = [1 / 3.] * len(dta.endog)
        wls_array = WLS(dta.endog, dta.exog, weights=weights).fit()
        cls.res2 = wls_array


@pytest.mark.not_vetted
class TestWLS_OLS(CheckRegressionResults):
    @classmethod
    def setup_class(cls):
        data = datasets.longley.load(as_pandas=False)
        data.exog = add_constant(data.exog, prepend=False)
        cls.res1 = OLS(data.endog, data.exog).fit()
        cls.res2 = WLS(data.endog, data.exog).fit()


@pytest.mark.not_vetted
class TestGLS_OLS(CheckRegressionResults):
    @classmethod
    def setup_class(cls):
        data = datasets.longley.load(as_pandas=False)
        data.exog = add_constant(data.exog, prepend=False)
        cls.res1 = GLS(data.endog, data.exog).fit()
        cls.res2 = OLS(data.endog, data.exog).fit()


# FIXME: dont comment-out
# class TestWLS_GLS(CheckRegressionResults):
#    @classmethod
#    def setup_class(cls):
#        data = datasets.ccard.load(as_pandas=False)
#        cls.res1 = WLS(data.endog, data.exog,
#                        weights=1 / data.exog[:, 2]).fit()
#        cls.res2 = GLS(data.endog, data.exog, sigma=data.exog[:, 2]).fit()


# TODO: test AR
# why the two-stage in AR?
# class test_ar(object):
#     data = datasets.sunspots.load(as_pandas=False)
#     model = AR(data.endog, rho=4).fit()
#     R_res = RModel(data.endog, aic="FALSE", order_max=4)#
#
#     def test_params(self):
#         assert_almost_equal(self.model.rho,
#         pass
#
#     def test_order(self):
#        # In R this can be defined or chosen by minimizing the AIC if aic=True
#        pass

# -------------------------------------------------------------
# Data Dimensions

@pytest.mark.not_vetted
class TestDataDimensions(CheckRegressionResults):
    @classmethod
    def setup_class(cls):
        np.random.seed(54321)
        cls.endog_n_ = np.random.uniform(0, 20, size=30)
        cls.endog_n_one = cls.endog_n_[:, None]
        cls.exog_n_ = np.random.uniform(0, 20, size=30)
        cls.exog_n_one = cls.exog_n_[:, None]
        cls.degen_exog = cls.exog_n_one[:-1]
        cls.mod1 = OLS(cls.endog_n_one, cls.exog_n_one)
        cls.mod1.df_model += 1
        cls.res1 = cls.mod1.fit()
        # Note that these are created for every subclass..
        # A little extra overhead probably
        cls.mod2 = OLS(cls.endog_n_one, cls.exog_n_one)
        cls.mod2.df_model += 1
        cls.res2 = cls.mod2.fit()


@pytest.mark.not_vetted
class TestGLS_large_data(TestDataDimensions):

    @classmethod
    def setup_class(cls):
        super(TestGLS_large_data, cls).setup_class()
        nobs = 1000
        y = np.random.randn(nobs, 1)
        X = np.random.randn(nobs, 20)
        sigma = np.ones_like(y)
        cls.gls_res = GLS(y, X, sigma=sigma).fit()
        cls.gls_res_scalar = GLS(y, X, sigma=1).fit()
        cls.gls_res_none = GLS(y, X).fit()
        cls.ols_res = OLS(y, X).fit()

    def test_large_equal_params(self):
        assert_almost_equal(self.ols_res.params,
                            self.gls_res.params,
                            DECIMAL_7)

    def test_large_equal_loglike(self):
        assert_almost_equal(self.ols_res.llf,
                            self.gls_res.llf,
                            DECIMAL_7)

    def test_large_equal_params_none(self):
        assert_almost_equal(self.gls_res.params,
                            self.gls_res_none.params,
                            DECIMAL_7)


@pytest.mark.not_vetted
class TestNxNx(TestDataDimensions):
    @classmethod
    def setup_class(cls):
        super(TestNxNx, cls).setup_class()
        cls.mod2 = OLS(cls.endog_n_, cls.exog_n_)
        cls.mod2.df_model += 1
        cls.res2 = cls.mod2.fit()


@pytest.mark.not_vetted
class TestNxOneNx(TestDataDimensions):
    @classmethod
    def setup_class(cls):
        super(TestNxOneNx, cls).setup_class()
        cls.mod2 = OLS(cls.endog_n_one, cls.exog_n_)
        cls.mod2.df_model += 1
        cls.res2 = cls.mod2.fit()


@pytest.mark.not_vetted
class TestNxNxOne(TestDataDimensions):
    @classmethod
    def setup_class(cls):
        super(TestNxNxOne, cls).setup_class()
        cls.mod2 = OLS(cls.endog_n_, cls.exog_n_one)
        cls.mod2.df_model += 1
        cls.res2 = cls.mod2.fit()


# -------------------------------------------------------------
# Model Equivalances

@pytest.mark.not_vetted
class TestOLS_GLS_WLS_equivalence(object):

    @classmethod
    def setup_class(cls):
        data = datasets.longley.load(as_pandas=False)
        data.exog = add_constant(data.exog, prepend=False)
        y = data.endog
        X = data.exog
        n = y.shape[0]
        w = np.ones(n)
        cls.results = []
        cls.results.append(OLS(y, X).fit())
        cls.results.append(WLS(y, X, w).fit())
        cls.results.append(GLS(y, X, 100 * w).fit())
        cls.results.append(GLS(y, X, np.diag(0.1 * w)).fit())

    def test_ll(self):
        llf = np.array([r.llf for r in self.results])
        llf_1 = np.ones_like(llf) * self.results[0].llf
        assert_almost_equal(llf,
                            llf_1,
                            DECIMAL_7)

        ic = np.array([r.aic for r in self.results])
        ic_1 = np.ones_like(ic) * self.results[0].aic
        assert_almost_equal(ic,
                            ic_1,
                            DECIMAL_7)

        ic = np.array([r.bic for r in self.results])
        ic_1 = np.ones_like(ic) * self.results[0].bic
        assert_almost_equal(ic,
                            ic_1,
                            DECIMAL_7)

    def test_params(self):
        params = np.array([r.params for r in self.results])
        params_1 = np.array([self.results[0].params] * len(self.results))
        assert_allclose(params, params_1)

    def test_ss(self):
        bse = np.array([r.bse for r in self.results])
        bse_1 = np.array([self.results[0].bse] * len(self.results))
        assert_allclose(bse, bse_1)

    def test_rsquared(self):
        rsquared = np.array([r.rsquared for r in self.results])
        rsquared_1 = np.array([self.results[0].rsquared] * len(self.results))
        assert_almost_equal(rsquared,
                            rsquared_1,
                            DECIMAL_7)


@pytest.mark.not_vetted
class TestGLS_WLS_equivalence(TestOLS_GLS_WLS_equivalence):

    @classmethod
    def setup_class(cls):
        data = datasets.longley.load(as_pandas=False)
        data.exog = add_constant(data.exog, prepend=False)
        y = data.endog
        X = data.exog
        n = y.shape[0]
        np.random.seed(5)
        w = np.random.uniform(0.5, 1, n)
        w_inv = 1. / w

        cls.results = []
        cls.results.append(WLS(y, X, w).fit())
        cls.results.append(WLS(y, X, 0.01 * w).fit())
        cls.results.append(GLS(y, X, 100 * w_inv).fit())
        cls.results.append(GLS(y, X, np.diag(0.1 * w_inv)).fit())


# -------------------------------------------------------------
# T-Test, F-Test

@pytest.mark.not_vetted
class TestFtest(object):
    """
    Tests f_test vs. RegressionResults
    """
    @classmethod
    def setup_class(cls):
        data = datasets.longley.load(as_pandas=False)
        data.exog = add_constant(data.exog, prepend=False)
        cls.res1 = OLS(data.endog, data.exog).fit()
        R = np.identity(7)[:-1, :]
        cls.Ftest = cls.res1.f_test(R)

    def test_F(self):
        assert_almost_equal(self.Ftest.fvalue,
                            self.res1.fvalue,
                            DECIMAL_4)

    def test_p(self):
        assert_almost_equal(self.Ftest.pvalue,
                            self.res1.f_pvalue,
                            DECIMAL_4)

    def test_Df_denom(self):
        # TODO: should be res1.df_resid, not res1.model.df_resid
        assert self.Ftest.df_denom == self.res1.model.df_resid

    def test_Df_num(self):
        assert self.Ftest.df_num == 6


@pytest.mark.not_vetted
class TestFTest2(object):
    """
    A joint test that the coefficient on
    GNP = the coefficient on UNEMP  and that the coefficient on
    POP = the coefficient on YEAR for the Longley dataset.

    Ftest1 is from sm.  Results are from Rpy using R's car library.
    """
    @classmethod
    def setup_class(cls):
        data = datasets.longley.load(as_pandas=False)
        data.exog = add_constant(data.exog, prepend=False)
        res1 = OLS(data.endog, data.exog).fit()
        R2 = [[0, 1, -1, 0, 0, 0, 0],
              [0, 0, 0, 0, 1, -1, 0]]
        cls.Ftest1 = res1.f_test(R2)
        hyp = 'x2 = x3, x5 = x6'
        cls.NewFtest1 = res1.f_test(hyp)

    def test_new_ftest(self):
        assert_equal(self.NewFtest1.fvalue, self.Ftest1.fvalue)

    def test_fvalue(self):
        assert_almost_equal(self.Ftest1.fvalue,
                            9.7404618732968196,
                            DECIMAL_4)

    def test_pvalue(self):
        assert_almost_equal(self.Ftest1.pvalue,
                            0.0056052885317493459,
                            DECIMAL_4)

    def test_df_denom(self):
        assert self.Ftest1.df_denom == 9

    def test_df_num(self):
        assert self.Ftest1.df_num == 2


@pytest.mark.not_vetted
class TestFtestQ(object):
    """
    A joint hypothesis test that Rb = q.  Coefficient tests are essentially
    made up.  Test values taken from Stata.
    """
    @classmethod
    def setup_class(cls):
        data = datasets.longley.load(as_pandas=False)
        data.exog = add_constant(data.exog, prepend=False)
        res1 = OLS(data.endog, data.exog).fit()
        R = np.array([[0, 1, 1, 0, 0, 0, 0],
                      [0, 1, 0, 1, 0, 0, 0],
                      [0, 1, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 1, 0, 0],
                      [0, 0, 0, 0, 0, 1, 0]])
        q = np.array([0, 0, 0, 1, 0])
        cls.Ftest1 = res1.f_test((R, q))

    def test_fvalue(self):
        assert_almost_equal(self.Ftest1.fvalue, 70.115557, 5)

    def test_pvalue(self):
        assert_almost_equal(self.Ftest1.pvalue, 6.229e-07, 10)

    def test_df_denom(self):
        assert self.Ftest1.df_denom == 9

    def test_df_num(self):
        assert self.Ftest1.df_num == 5


@pytest.mark.not_vetted
class TestTtest(object):
    """
    Test individual t-tests.  Ie., are the coefficients significantly
    different than zero.
    """
    @classmethod
    def setup_class(cls):
        data = datasets.longley.load(as_pandas=False)
        data.exog = add_constant(data.exog, prepend=False)
        cls.res1 = OLS(data.endog, data.exog).fit()
        R = np.identity(7)
        cls.Ttest = cls.res1.t_test(R)
        hyp = 'x1 = 0, x2 = 0, x3 = 0, x4 = 0, x5 = 0, x6 = 0, const = 0'
        cls.NewTTest = cls.res1.t_test(hyp)

    def test_new_tvalue(self):
        assert_equal(self.NewTTest.tvalue,
                     self.Ttest.tvalue)

    def test_tvalue(self):
        assert_almost_equal(self.Ttest.tvalue,
                            self.res1.tvalues,
                            DECIMAL_4)

    def test_sd(self):
        assert_almost_equal(self.Ttest.sd,
                            self.res1.bse,
                            DECIMAL_4)

    def test_pvalue(self):
        assert_almost_equal(self.Ttest.pvalue,
                            stats.t.sf(np.abs(self.res1.tvalues),
                                       self.res1.model.df_resid) * 2,
                            DECIMAL_4)

    def test_df_denom(self):
        assert_equal(self.Ttest.df_denom,
                     self.res1.model.df_resid)

    def test_effect(self):
        assert_almost_equal(self.Ttest.effect,
                            self.res1.params)


@pytest.mark.not_vetted
class TestTtest2(object):
    """
    Tests the hypothesis that the coefficients on POP and YEAR
    are equal.

    Results from RPy using 'car' package.
    """
    @classmethod
    def setup_class(cls):
        R = np.zeros(7)
        R[4:6] = [1, -1]
        data = datasets.longley.load(as_pandas=False)
        data.exog = add_constant(data.exog, prepend=False)
        res1 = OLS(data.endog, data.exog).fit()
        cls.Ttest1 = res1.t_test(R)

    def test_tvalue(self):
        assert_almost_equal(self.Ttest1.tvalue,
                            -4.0167754636397284,
                            DECIMAL_4)

    def test_sd(self):
        assert_almost_equal(self.Ttest1.sd,
                            455.39079425195314,
                            DECIMAL_4)

    def test_pvalue(self):
        assert_almost_equal(self.Ttest1.pvalue,
                            2 * 0.0015163772380932246,
                            DECIMAL_4)

    def test_df_denom(self):
        assert self.Ttest1.df_denom == 9

    def test_effect(self):
        assert_almost_equal(self.Ttest1.effect,
                            -1829.2025687186533,
                            DECIMAL_4)


# -------------------------------------------------------------
# Unsorted

@pytest.mark.not_vetted
class TestRegularizedFit(object):
    # Make sure there are no problems when no variables are selected.
    @pytest.mark.not_vetted
    def test_empty_model(self):
        np.random.seed(742)
        n = 100
        endog = np.random.normal(size=n)
        exog = np.random.normal(size=(n, 3))

        for cls in [OLS, WLS, GLS]:
            model = cls(endog, exog)
            result = model.fit_regularized(alpha=1000)
            assert_equal(result.params, 0.)

    # TODO: Does this need to be part of the class?  doesnt use self
    @pytest.mark.not_vetted
    @pytest.mark.parametrize('attr', [x for x in dir(glmnet_r_results)
                                      if x.startswith("rslt_")])
    def test_regularized(self, attr):
        vec = getattr(glmnet_r_results, attr)

        n = vec[0]
        p = vec[1]
        L1_wt = float(vec[2])
        lam = float(vec[3])
        params = vec[4:].astype(np.float64)

        endog = lasso_data[0:int(n), 0]
        exog = lasso_data[0:int(n), 1:(int(p) + 1)]

        endog = endog - endog.mean()
        endog /= endog.std(ddof=1)
        exog = exog - exog.mean(0)
        exog /= exog.std(0, ddof=1)

        # TOOD: parametrize another level?
        for cls in [OLS, WLS, GLS]:
            mod = cls(endog, exog)
            rslt = mod.fit_regularized(L1_wt=L1_wt, alpha=lam)
            assert_almost_equal(rslt.params, params, decimal=3)

            # TODO: mark/separate smoke tests
            # Smoke test for summary
            # 2018-03-05 disabling smoketest from upstream
            # rslt.summary()
            #
            # Smoke test for profile likeihood
            # mod.fit_regularized(L1_wt=L1_wt, alpha=lam,
            #                     profile_scale=True)

    @pytest.mark.not_vetted
    def test_regularized_weights(self):
        np.random.seed(1432)
        exog1 = np.random.normal(size=(100, 3))
        endog1 = exog1[:, 0] + exog1[:, 1] + np.random.normal(size=100)
        exog2 = np.random.normal(size=(100, 3))
        endog2 = exog2[:, 0] + exog2[:, 1] + np.random.normal(size=100)

        exog_a = np.vstack((exog1, exog1, exog2))
        endog_a = np.concatenate((endog1, endog1, endog2))

        # Should be equivalent to exog_a, endog_a.
        exog_b = np.vstack((exog1, exog2))
        endog_b = np.concatenate((endog1, endog2))
        wgts = np.ones(200)
        wgts[0:100] = 2
        sigma = np.diag(1 / wgts)

        # TODO: parametrize?
        for L1_wt in [0, 0.5, 1]:
            for alpha in [0, 1]:
                mod1 = OLS(endog_a, exog_a)
                rslt1 = mod1.fit_regularized(L1_wt=L1_wt, alpha=alpha)

                mod2 = WLS(endog_b, exog_b, weights=wgts)
                rslt2 = mod2.fit_regularized(L1_wt=L1_wt, alpha=alpha)

                mod3 = GLS(endog_b, exog_b, sigma=sigma)
                rslt3 = mod3.fit_regularized(L1_wt=L1_wt, alpha=alpha)

                assert_almost_equal(rslt1.params, rslt2.params, decimal=3)
                assert_almost_equal(rslt1.params, rslt3.params, decimal=3)


@pytest.mark.not_vetted
class TestLM(object):

    @classmethod
    def setup_class(cls):
        # TODO: Test HAC method
        X = np.random.randn(100, 3)
        b = np.ones((3, 1))
        e = np.random.randn(100, 1)
        y = np.dot(X, b) + e
        # Cases?
        # Homoskedastic
        # HC0
        cls.res1_full = OLS(y, X).fit()
        cls.res1_restricted = OLS(y, X[:, 0]).fit()

        cls.res2_full = cls.res1_full.get_robustcov_results('HC0')
        cls.res2_restricted = cls.res1_restricted.get_robustcov_results('HC0')

        cls.X = X
        cls.Y = y

    def test_LM_homoskedastic(self):
        resid = self.res1_restricted.wresid
        n = resid.shape[0]
        X = self.X
        S = np.dot(resid, resid) / n * np.dot(X.T, X) / n
        Sinv = np.linalg.inv(S)
        s = np.mean(X * resid[:, None], 0)
        LMstat = n * np.dot(np.dot(s, Sinv), s.T)
        LMstat_OLS = self.res1_full.compare_lm_test(self.res1_restricted)
        LMstat2 = LMstat_OLS[0]
        assert_almost_equal(LMstat, LMstat2, DECIMAL_7)

    def test_LM_heteroskedastic_nodemean(self):
        resid = self.res1_restricted.wresid
        n = resid.shape[0]
        X = self.X
        scores = X * resid[:, None]
        S = np.dot(scores.T, scores) / n
        Sinv = np.linalg.inv(S)
        s = np.mean(scores, 0)
        LMstat = n * np.dot(np.dot(s, Sinv), s.T)
        LMstat_OLS = self.res2_full.compare_lm_test(self.res2_restricted,
                                                    demean=False)
        LMstat2 = LMstat_OLS[0]
        assert_almost_equal(LMstat, LMstat2, DECIMAL_7)

    def test_LM_heteroskedastic_demean(self):
        resid = self.res1_restricted.wresid
        n = resid.shape[0]
        X = self.X
        scores = X * resid[:, None]
        scores_demean = scores - scores.mean(0)
        S = np.dot(scores_demean.T, scores_demean) / n
        Sinv = np.linalg.inv(S)
        s = np.mean(scores, 0)
        LMstat = n * np.dot(np.dot(s, Sinv), s.T)
        LMstat_OLS = self.res2_full.compare_lm_test(self.res2_restricted)
        LMstat2 = LMstat_OLS[0]
        assert_almost_equal(LMstat, LMstat2, DECIMAL_7)

    def test_LM_heteroskedastic_LRversion(self):
        resid = self.res1_restricted.wresid
        resid_full = self.res1_full.wresid
        n = resid.shape[0]
        X = self.X
        scores = X * resid[:, None]
        s = np.mean(scores, 0)
        scores = X * resid_full[:, None]
        S = np.dot(scores.T, scores) / n
        Sinv = np.linalg.inv(S)
        LMstat = n * np.dot(np.dot(s, Sinv), s.T)
        LMstat_OLS = self.res2_full.compare_lm_test(self.res2_restricted,
                                                    use_lr=True)
        LMstat2 = LMstat_OLS[0]
        assert_almost_equal(LMstat, LMstat2, DECIMAL_7)

    def test_LM_nonnested(self):
        with pytest.raises(ValueError):
            self.res2_restricted.compare_lm_test(self.res2_full)


@pytest.mark.not_vetted
class TestGLS(object):
    """
    These test results were obtained by replication with R.
    """
    res2 = results_regression.LongleyGls()

    @classmethod
    def setup_class(cls):
        data = datasets.longley.load(as_pandas=False)
        exog = add_constant(np.column_stack((data.exog[:, 1],
                                             data.exog[:, 4])),
                            prepend=False)
        tmp_results = OLS(data.endog, exog).fit()
        rho = np.corrcoef(tmp_results.resid[1:],
                          tmp_results.resid[:-1])[0][1]  # by assumption
        order = toeplitz(np.arange(16))
        sigma = rho**order
        cls.res1 = GLS(data.endog, exog, sigma=sigma).fit()
        # attach for test_missing
        cls.sigma = sigma
        cls.exog = exog
        cls.endog = data.endog

    def test_aic(self):
        # Note: tolerance is tight; rtol=3e-3 fails while 4e-3 passes
        assert_allclose(self.res1.aic + 2,
                        self.res2.aic,
                        rtol=4e-3)

    def test_bic(self):
        # Note: tolerance is tight; rtol=1e-2 fails while 1.5e-2 passes
        assert_allclose(self.res1.bic,
                        self.res2.bic,
                        rtol=1.5e-2)

    def test_loglike(self):
        assert_almost_equal(self.res1.llf,
                            self.res2.llf,
                            0)  # TODO: Why so imprecise?

    def test_params(self):
        assert_almost_equal(self.res1.params,
                            self.res2.params,
                            1)  # TODO: Why so imprecise?

    def test_resid(self):
        assert_almost_equal(self.res1.resid,
                            self.res2.resid,
                            DECIMAL_4)

    def test_scale(self):
        assert_almost_equal(self.res1.scale,
                            self.res2.scale,
                            DECIMAL_4)

    def test_tvalues(self):
        assert_almost_equal(self.res1.tvalues,
                            self.res2.tvalues,
                            DECIMAL_4)

    def test_standarderrors(self):
        assert_almost_equal(self.res1.bse,
                            self.res2.bse,
                            DECIMAL_4)

    def test_fittedvalues(self):
        assert_almost_equal(self.res1.fittedvalues,
                            self.res2.fittedvalues,
                            DECIMAL_4)

    def test_pvalues(self):
        assert_almost_equal(self.res1.pvalues,
                            self.res2.pvalues,
                            DECIMAL_4)

    def test_missing(self):
        endog = self.endog.copy()  # copy or changes endog for other methods
        endog[[4, 7, 14]] = np.nan
        mod = GLS(endog, self.exog, sigma=self.sigma, missing='drop')
        assert mod.endog.shape[0] == 13
        assert mod.exog.shape[0] == 13
        assert mod.sigma.shape == (13, 13)


# -------------------------------------------------------------


# TODO: WTF why is this a class?
@pytest.mark.not_vetted
class TestNonFit(object):
    @classmethod
    def setup_class(cls):
        data = datasets.longley.load(as_pandas=False)
        data.exog = add_constant(data.exog, prepend=False)
        cls.endog = data.endog
        cls.exog = data.exog
        cls.ols_model = OLS(data.endog, data.exog)

    def test_df_resid(self):
        df_resid = self.endog.shape[0] - self.exog.shape[1]
        # TODO: do something with df_resid?
        assert self.ols_model.df_resid == 9


# TODO: WTF why is this a class?
@pytest.mark.not_vetted
class TestWLS_CornerCases(object):
    @classmethod
    def setup_class(cls):
        cls.exog = np.ones((1,))
        cls.endog = np.ones((1,))
        weights = 1
        cls.wls_res = WLS(cls.endog, cls.exog, weights=weights).fit()

    def test_wrong_size_weights(self):
        with pytest.raises(ValueError):
            WLS(self.endog, self.exog, weights=np.ones((10, 10)))


@pytest.mark.not_vetted
def test_const_indicator():
    np.random.seed(12345)
    X = np.random.randint(0, 3, size=30)
    X = categorical(X, drop=True)
    y = np.dot(X, [1., 2., 3.]) + np.random.normal(size=30)
    modc = OLS(y, add_constant(X[:, 1:], prepend=True)).fit()
    mod = OLS(y, X, hasconst=True).fit()
    assert_almost_equal(modc.rsquared, mod.rsquared, 12)


@pytest.mark.not_vetted
def test_wls_example():
    # example from the docstring, there was a note about a bug, should
    # be fixed now
    Y = [1, 3, 4, 5, 2, 3, 4]
    X = list(range(1, 8))
    X = add_constant(X, prepend=False)
    wls_model = WLS(Y, X, weights=list(range(1, 8))).fit()
    # taken from R lm.summary
    assert_almost_equal(wls_model.fvalue, 0.127337843215, 6)
    assert_almost_equal(wls_model.scale, 2.44608530786**2, 6)


@pytest.mark.not_vetted
def test_wls_tss():
    y = np.array([22, 22, 22, 23, 23, 23])
    X = [[1, 0], [1, 0], [1, 1], [0, 1], [0, 1], [0, 1]]

    ols_mod = OLS(y, add_constant(X, prepend=False)).fit()

    yw = np.array([22, 22, 23.])
    Xw = [[1, 0], [1, 1], [0, 1]]
    w = np.array([2, 1, 3.])

    wls_mod = WLS(yw, add_constant(Xw, prepend=False), weights=w).fit()
    assert_equal(ols_mod.centered_tss, wls_mod.centered_tss)


@pytest.mark.not_vetted
def test_wls_missing():
    data = datasets.ccard.load(as_pandas=False)
    endog = data.endog
    endog[[10, 25]] = np.nan
    mod = WLS(data.endog, data.exog, weights=1 / data.exog[:, 2],
              missing='drop')
    assert mod.endog.shape[0] == 70
    assert mod.exog.shape[0] == 70
    assert mod.weights.shape[0] == 70


@pytest.mark.not_vetted
def test_ridge():
    n = 100
    p = 5
    np.random.seed(3132)
    xmat = np.random.normal(size=(n, p))
    yvec = xmat.sum(1) + np.random.normal(size=n)

    v = np.ones(p)
    v[0] = 0

    for a in [0, 1, 10]:
        for alpha in (a, a * np.ones(p), a * v):
            model1 = OLS(yvec, xmat)
            result1 = model1._fit_ridge(alpha=alpha)
            model2 = OLS(yvec, xmat)
            result2 = model2.fit_regularized(alpha=alpha, L1_wt=0)
            assert_allclose(result1.params, result2.params)
            model3 = OLS(yvec, xmat)
            result3 = model3.fit_regularized(alpha=alpha, L1_wt=1e-10)
            assert_allclose(result1.params, result3.params)

    fv1 = result1.fittedvalues
    fv2 = np.dot(xmat, result1.params)
    assert_allclose(fv1, fv2)


@pytest.mark.not_vetted
def test_regularized_refit():
    n = 100
    p = 5
    np.random.seed(3132)
    xmat = np.random.normal(size=(n, p))
    # covariates 0 and 2 matter
    yvec = xmat[:, 0] + xmat[:, 2] + np.random.normal(size=n)
    model1 = OLS(yvec, xmat)
    result1 = model1.fit_regularized(alpha=2., L1_wt=0.5, refit=True)

    model2 = OLS(yvec, xmat[:, [0, 2]])
    result2 = model2.fit()
    ii = [0, 2]
    assert_allclose(result1.params[ii], result2.params)
    assert_allclose(result1.bse[ii], result2.bse)


@pytest.mark.not_vetted
def test_regularized_predict():
    n = 100
    p = 5
    np.random.seed(3132)
    xmat = np.random.normal(size=(n, p))
    yvec = xmat.sum(1) + np.random.normal(size=n)
    wgt = np.random.uniform(1, 2, n)

    for klass in [WLS, GLS]:
        model1 = klass(yvec, xmat, weights=wgt)
        result1 = model1.fit_regularized(alpha=2., L1_wt=0.5, refit=True)

        params = result1.params
        fittedvalues = np.dot(xmat, params)
        pr = model1.predict(result1.params)
        assert_allclose(fittedvalues, pr)
        assert_allclose(result1.fittedvalues, pr)

        pr = result1.predict()
        assert_allclose(fittedvalues, pr)


@pytest.mark.not_vetted
def test_regularized_options():
    n = 100
    p = 5
    np.random.seed(3132)
    xmat = np.random.normal(size=(n, p))
    yvec = xmat.sum(1) + np.random.normal(size=n)

    model1 = OLS(yvec - 1, xmat)
    result1 = model1.fit_regularized(alpha=1., L1_wt=0.5)

    model2 = OLS(yvec, xmat, offset=1)
    result2 = model2.fit_regularized(alpha=1., L1_wt=0.5,
                                     start_params=np.zeros(5))

    assert_allclose(result1.params, result2.params)


@pytest.mark.not_vetted
def test_formula_missing_cat():
    # GH#805
    dta = datasets.grunfeld.load_pandas().data
    dta.loc[dta.index[0], 'firm'] = np.nan
    formula = 'value ~ invest + capital + firm + year'

    mod = OLS.from_formula(formula=formula, data=dta.dropna())
    res = mod.fit()

    mod2 = OLS.from_formula(formula=formula, data=dta)
    res2 = mod2.fit()

    assert_almost_equal(res.params.values,
                        res2.params.values)

    with pytest.raises(PatsyError):
        OLS.from_formula(formula, data=dta, missing='raise')


@pytest.mark.not_vetted
@pytest.mark.smoke
def test_missing_formula_predict():
    # GH#2171
    nsample = 30

    data = pd.DataFrame({'x': np.linspace(0, 10, nsample)})
    null = pd.DataFrame({'x': np.array([np.nan])})
    data = pd.concat([data, null])
    beta = np.array([1, 0.1])
    e = np.random.normal(size=nsample + 1)
    data['y'] = beta[0] + beta[1] * data['x'] + e
    model = OLS.from_formula('y ~ x', data=data)
    fit = model.fit()
    fit.predict(exog=data[:-1])


# -------------------------------------------------------------
# Vetted Tests, May Need GH References

def test_ols_bad_size_raises():
    # TODO: GH reference?
    np.random.seed(54321)
    data = np.random.uniform(0, 20, 31)
    with pytest.raises(ValueError):
        OLS(data, data[1:])


@pytest.mark.parametrize('mod', [OLS, GLS, WLS, GLSAR])
@pytest.mark.parametrize('bad_value', [np.nan, np.inf])
@pytest.mark.parametrize('use_pandas', [True, False])
def test_test_finite_check(mod, bad_value, use_pandas):
    # GH#4969
    endog = np.random.randn(100)
    exog = np.random.randn(100, 2)
    if use_pandas:
        endog = pd.Series(endog)
        exog = pd.DataFrame(exog)

    endog_missing = endog.copy()
    endog_missing[50] = bad_value

    with pytest.raises(MissingDataError) as err:
        mod(endog_missing, exog)

    assert err.type is MissingDataError
    assert 'endog' in err.value.args[0]

    if bad_value is np.nan:
        mod(endog_missing, exog, missing='drop')

    arr = exog.values if use_pandas else exog
    arr[0] = bad_value
    with pytest.raises(MissingDataError) as err:
        mod(endog, exog)

    assert err.type is MissingDataError
    assert 'exog' in err.value.args[0]

    if bad_value is np.nan:
        mod(endog, exog, missing='drop')


@pytest.mark.parametrize('use_pandas', [True, False])
@pytest.mark.parametrize('bad_value', [np.nan, np.inf])
def test_finite_weight_sigma(bad_value, use_pandas):
    # GH#4969
    endog = np.random.randn(100)
    exog = np.random.randn(100, 2)
    weights = sigma = np.ones(100)
    weights[-2:] = bad_value
    if use_pandas:
        sigma = weights = pd.Series(weights)

    with pytest.raises(MissingDataError) as err:
        WLS(endog, exog, weights=weights)

    assert err.type is MissingDataError
    assert 'weights' in err.value.args[0]

    with pytest.raises(MissingDataError) as err:
        GLS(endog, exog, sigma=sigma)

    assert err.type is MissingDataError
    assert 'sigma' in err.value.args[0]


# -------------------------------------------------------------
# Issue Regression Tests

def test_fvalue_only_constant():
    # GH#3642 if only constant in model, fvalue and f_pvalue should be np.nan
    nobs = 20
    np.random.seed(2)
    x = np.ones(nobs)
    y = np.random.randn(nobs)

    res = OLS(y, x).fit(cov_type='hac', cov_kwds={'maxlags': 3})
    assert np.isnan(res.fvalue)
    assert np.isnan(res.f_pvalue)
    # 2018-03-05 disabling smoke-test from upstream
    # res.summary()

    res = WLS(y, x).fit(cov_type='HC1')
    assert np.isnan(res.fvalue)
    assert np.isnan(res.f_pvalue)
    # 2018-03-05 disabling smoke-test from upstream
    # res.summary()


def test_fvalue_implicit_constant():
    # GH#2444 if constant is implicit, return nan see
    nobs = 100
    np.random.seed(2)
    x = np.random.randn(nobs, 1)
    x = ((x > 0) == [True, False]).astype(int)
    y = x.sum(1) + np.random.randn(nobs)

    res = OLS(y, x).fit(cov_type='HC1')
    assert np.isnan(res.fvalue)
    assert np.isnan(res.f_pvalue)
    # 2018-03-05 disabling smoke-test from upstream
    # res.summary()

    res = WLS(y, x).fit(cov_type='HC1')
    assert np.isnan(res.fvalue)
    assert np.isnan(res.f_pvalue)
    # 2018-03-05 disabling smoke-test from upstream
    # res.summary()


def test_conf_int_single_regressor():
    # GH#706 single-regressor model (i.e. no intercept) with 1D exog
    # should get passed to DataFrame for conf_int
    y = pd.Series(np.random.randn(10))
    x = pd.Series(np.ones(10))
    res = OLS(y, x).fit()
    conf_int = res.conf_int()
    assert conf_int.shape == (1, 2)
    assert isinstance(conf_int, pd.DataFrame)


def test_summary_as_latex():
    # GH#734
    dta = datasets.longley.load_pandas()
    X = dta.exog
    X["constant"] = 1
    y = dta.endog
    with warnings.catch_warnings(record=True):
        res = OLS(y, X).fit()
        table = res.summary().as_latex()

    # replace the date and time
    table = re.sub("(?<=\n\\\\textbf\{Date:\}             &).+?&",
                   " Sun, 07 Apr 2013 &", table)
    table = re.sub("(?<=\n\\\\textbf\{Time:\}             &).+?&",
                   "     13:46:07     &", table)

    expected = textwrap.dedent("""
    \\begin{center}
    \\begin{tabular}{lclc}
    \\toprule
    \\textbf{Dep. Variable:}    &      TOTEMP      & \\textbf{  R-squared:         } &     0.995   \\\\
    \\textbf{Model:}            &       OLS        & \\textbf{  Adj. R-squared:    } &     0.992   \\\\
    \\textbf{Method:}           &  Least Squares   & \\textbf{  F-statistic:       } &     330.3   \\\\
    \\textbf{Date:}             & Sun, 07 Apr 2013 & \\textbf{  Prob (F-statistic):} &  4.98e-10   \\\\
    \\textbf{Time:}             &     13:46:07     & \\textbf{  Log-Likelihood:    } &   -109.62   \\\\
    \\textbf{No. Observations:} &          16      & \\textbf{  AIC:               } &     233.2   \\\\
    \\textbf{Df Residuals:}     &           9      & \\textbf{  BIC:               } &     238.6   \\\\
    \\textbf{Df Model:}         &           6      & \\textbf{                     } &             \\\\
    \\bottomrule
    \\end{tabular}
    \\begin{tabular}{lcccccc}
                      & \\textbf{coef} & \\textbf{std err} & \\textbf{t} & \\textbf{P$>$$|$t$|$} & \\textbf{[0.025} & \\textbf{0.975]}  \\\\
    \\midrule
    \\textbf{GNPDEFL}  &      15.0619  &       84.915     &     0.177  &         0.863        &     -177.029    &      207.153     \\\\
    \\textbf{GNP}      &      -0.0358  &        0.033     &    -1.070  &         0.313        &       -0.112    &        0.040     \\\\
    \\textbf{UNEMP}    &      -2.0202  &        0.488     &    -4.136  &         0.003        &       -3.125    &       -0.915     \\\\
    \\textbf{ARMED}    &      -1.0332  &        0.214     &    -4.822  &         0.001        &       -1.518    &       -0.549     \\\\
    \\textbf{POP}      &      -0.0511  &        0.226     &    -0.226  &         0.826        &       -0.563    &        0.460     \\\\
    \\textbf{YEAR}     &    1829.1515  &      455.478     &     4.016  &         0.003        &      798.788    &     2859.515     \\\\
    \\textbf{constant} &   -3.482e+06  &      8.9e+05     &    -3.911  &         0.004        &     -5.5e+06    &    -1.47e+06     \\\\
    \\bottomrule
    \\end{tabular}
    \\begin{tabular}{lclc}
    \\textbf{Omnibus:}       &  0.749 & \\textbf{  Durbin-Watson:     } &    2.559  \\\\
    \\textbf{Prob(Omnibus):} &  0.688 & \\textbf{  Jarque-Bera (JB):  } &    0.684  \\\\
    \\textbf{Skew:}          &  0.420 & \\textbf{  Prob(JB):          } &    0.710  \\\\
    \\textbf{Kurtosis:}      &  2.434 & \\textbf{  Cond. No.          } & 4.86e+09  \\\\
    \\bottomrule
    \\end{tabular}
    %\\caption{OLS Regression Results}
    \\end{center}

    Warnings: \\newline
     [1] Standard Errors assume that the covariance matrix of the errors is correctly specified. \\newline
     [2] The condition number is large, 4.86e+09. This might indicate that there are \\newline
     strong multicollinearity or other numerical problems.""").strip()  # noqa:E501

    assert_equal(table, expected)


def test_summary_rsquared_label():
    # GH#5083
    # Check that the "uncentered" label is correctly added after rsquared
    # Note: upstream this is in test_summary2.TestSummaryLabels
    x = [1, 5, 7, 3, 5, 2, 5, 3]
    y = [6, 4, 2, 7, 4, 9, 10, 2]
    reg_with_constant = OLS(y, x, hasconst=True).fit()
    # assert 'R-squared:' in str(reg_with_constant.summary2())
    assert 'R-squared:' in str(reg_with_constant.summary())

    reg_without_constant = OLS(y, x, hasconst=False).fit()
    # assert 'R-squared (uncentered):' in str(reg_without_constant.summary2())
    assert 'R-squared (uncentered):' in str(reg_without_constant.summary())
