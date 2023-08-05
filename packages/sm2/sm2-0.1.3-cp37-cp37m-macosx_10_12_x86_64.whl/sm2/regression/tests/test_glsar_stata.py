# -*- coding: utf-8 -*-
"""Testing GLSAR against STATA

Created on Wed May 30 09:25:24 2012

Author: Josef Perktold
"""
import pytest
import numpy as np
from numpy.testing import assert_almost_equal, assert_allclose, assert_equal

from sm2.regression.linear_model import GLSAR
from sm2.tools.tools import add_constant
from sm2.datasets import macrodata
from sm2.tsa.arima_model import ARMA

from .results.macro_gr_corc_stata import results


@pytest.mark.not_vetted
class CheckStataResultsMixin(object):
    def test_params_table(self):
        res = self.res
        assert_almost_equal(res.params,
                            results.params,
                            3)
        assert_almost_equal(res.bse,
                            results.bse,
                            3)
        assert_allclose(res.tvalues,
                        results.tvalues,
                        atol=0, rtol=0.004)
        assert_allclose(res.pvalues,
                        results.pvalues,
                        atol=1e-7, rtol=0.004)


@pytest.mark.not_vetted
class CheckStataResultsPMixin(CheckStataResultsMixin):
    def test_predicted(self):
        res = self.res
        assert_allclose(res.fittedvalues,
                        results.fittedvalues,
                        rtol=0.002)
        predicted = res.predict(res.model.exog)  # should be equal
        assert_allclose(predicted,
                        results.fittedvalues,
                        rtol=0.0016)
        # not yet
        #assert_almost_equal(res.fittedvalues_se,
        #                    results.fittedvalues_se, 4)


@pytest.mark.not_vetted
class TestGLSARCorc(CheckStataResultsPMixin):
    @classmethod
    def setup_class(cls):
        d2 = macrodata.load_pandas().data
        g_gdp = 400 * np.diff(np.log(d2['realgdp'].values))
        g_inv = 400 * np.diff(np.log(d2['realinv'].values))
        exogg = add_constant(np.c_[g_gdp, d2['realint'][:-1].values],
                             prepend=False)

        mod1 = GLSAR(g_inv, exogg, 1)
        cls.res = mod1.iterative_fit(5)

    def test_rho(self):
        assert_almost_equal(self.res.model.rho,
                            results.rho,
                            3)
        assert_almost_equal(self.res.llf,
                            results.ll,
                            4)

    def test_glsar_arima(self):
        endog = self.res.model.endog
        exog = self.res.model.exog
        mod1 = GLSAR(endog, exog, 3)
        res = mod1.iterative_fit(10)
        mod_arma = ARMA(endog, order=(3, 0), exog=exog[:, :-1])
        res_arma = mod_arma.fit(method='css', iprint=0, disp=0)

        assert_allclose(res.params,
                        res_arma.params[[1, 2, 0]],
                        atol=0.01, rtol=1e-3)
        assert_allclose(res.model.rho,
                        res_arma.params[3:],
                        atol=0.05, rtol=1e-3)
        assert_allclose(res.bse,
                        res_arma.bse[[1, 2, 0]],
                        atol=0.015, rtol=1e-3)

        assert len(res.history['params']) == 5
        # this should be identical, history has last fit
        assert_equal(res.history['params'][-1],
                     res.params)

        res2 = mod1.iterative_fit(4, rtol=0)
        assert len(res2.history['params']) == 4
        assert len(res2.history['rho']) == 4

    def test_glsar_iter0(self):
        endog = self.res.model.endog
        exog = self.res.model.exog

        rho = np.array([0.207, 0.275, 1.033])
        mod1 = GLSAR(endog, exog, rho)
        res1 = mod1.fit()
        res0 = mod1.iterative_fit(0)
        res0b = mod1.iterative_fit(1)
        # check iterative_fit(0) or iterative_fit(1) doesn't update rho
        assert_allclose(res0.params,
                        res1.params,
                        rtol=1e-11)
        assert_allclose(res0b.params,
                        res1.params,
                        rtol=1e-11)
        assert_allclose(res0.model.rho,
                        rho,
                        rtol=1e-11)
        assert_allclose(res0b.model.rho,
                        rho,
                        rtol=1e-11)
