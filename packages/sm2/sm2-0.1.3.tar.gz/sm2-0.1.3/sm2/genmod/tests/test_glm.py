"""
Test functions for models.GLM
"""
from __future__ import division
import copy
import os
import warnings

from six.moves import range

import pytest
import numpy as np
from numpy.testing import assert_almost_equal, assert_equal, assert_allclose
from scipy import stats
import pandas as pd

import sm2.api as sm
from sm2.genmod.generalized_linear_model import GLM
from sm2.genmod.families import links
from sm2.tools.tools import add_constant
from sm2.tools.sm_exceptions import PerfectSeparationError

from sm2.discrete import discrete_model as discrete

from .results import glmnet_r_results, results_glm

# Test Precisions
DECIMAL_4 = 4
DECIMAL_3 = 3
DECIMAL_2 = 2
DECIMAL_1 = 1
DECIMAL_0 = 0

pdf_output = False
if pdf_output:
    from matplotlib.backends.backend_pdf import PdfPages
    pdf = PdfPages("test_glm.pdf")
else:
    pdf = None


def close_or_save(pdf, fig):
    if pdf_output:
        pdf.savefig(fig)


def teardown_module():
    if pdf_output:
        pdf.close()


@pytest.mark.not_vetted
class CheckModelResultsMixin(object):
    """
    res2 is reference results from results_glm
    """

    decimal_params = DECIMAL_4

    def test_params(self):
        assert_almost_equal(self.res1.params,
                            self.res2.params,
                            self.decimal_params)

    decimal_bse = DECIMAL_4

    def test_standard_errors(self):
        assert_almost_equal(self.res1.bse,
                            self.res2.bse,
                            self.decimal_bse)

    decimal_resids = DECIMAL_4

    def test_residuals(self):
        # fix incorrect numbers in resid_working results
        # residuals for Poisson are also tested in test_glm_weights.py
        # new numpy would have copy method
        resid2 = copy.copy(self.res2.resids)
        resid2[:, 2] *= self.res1.family.link.deriv(self.res1.mu)**2

        atol = 10**(-self.decimal_resids)
        resids = np.column_stack((self.res1.resid_pearson,
                                  self.res1.resid_deviance,
                                  self.res1.resid_working,
                                  self.res1.resid_anscombe,
                                  self.res1.resid_response))
        assert_allclose(resids, resid2, rtol=1e-6, atol=atol)

    def test_resid_response(self):
        # GH5255
        assert_allclose(self.res1.resid,
                        self.res1.resid_response,
                        rtol=1e-13)

    decimal_aic_R = DECIMAL_4

    def test_aic_R(self):
        # R includes the estimation of the scale as a lost dof
        # Doesn't with Gamma though
        if self.res1.scale != 1:
            dof = 2
        else:
            dof = 0
        if isinstance(self.res1.model.family, (sm.families.NegativeBinomial)):
            llf = self.res1.model.family.loglike(self.res1.model.endog,
                                                 self.res1.mu,
                                                 self.res1.model.var_weights,
                                                 self.res1.model.freq_weights,
                                                 scale=1)
            aic = (-2 * llf + 2 * (self.res1.df_model + 1))
        else:
            aic = self.res1.aic
        assert_almost_equal(aic + dof,
                            self.res2.aic_R,
                            self.decimal_aic_R)

    decimal_aic_Stata = DECIMAL_4

    def test_aic_Stata(self):
        # Stata uses the below llf for aic definition for these families
        if isinstance(self.res1.model.family, (sm.families.Gamma,
                                               sm.families.InverseGaussian,
                                               sm.families.NegativeBinomial)):
            llf = self.res1.model.family.loglike(self.res1.model.endog,
                                                 self.res1.mu,
                                                 self.res1.model.var_weights,
                                                 self.res1.model.freq_weights,
                                                 scale=1)
            aic = (-2 * llf + 2 * (self.res1.df_model + 1)) / self.res1.nobs
        else:
            aic = self.res1.aic / self.res1.nobs
        assert_almost_equal(aic, self.res2.aic_Stata, self.decimal_aic_Stata)

    decimal_deviance = DECIMAL_4

    def test_deviance(self):
        assert_almost_equal(self.res1.deviance,
                            self.res2.deviance,
                            self.decimal_deviance)

    decimal_scale = DECIMAL_4

    def test_scale(self):
        assert_almost_equal(self.res1.scale,
                            self.res2.scale,
                            self.decimal_scale)

    decimal_loglike = DECIMAL_4

    def test_loglike(self):
        # Stata uses the below llf for these families
        # We differ with R for them
        if isinstance(self.res1.model.family, (sm.families.Gamma,
                                               sm.families.InverseGaussian,
                                               sm.families.NegativeBinomial)):
            llf = self.res1.model.family.loglike(self.res1.model.endog,
                                                 self.res1.mu,
                                                 self.res1.model.var_weights,
                                                 self.res1.model.freq_weights,
                                                 scale=1)
        else:
            llf = self.res1.llf
        assert_almost_equal(llf, self.res2.llf, self.decimal_loglike)

    decimal_null_deviance = DECIMAL_4

    def test_null_deviance(self):
        assert_almost_equal(self.res1.null_deviance, self.res2.null_deviance,
                            self.decimal_null_deviance)

    decimal_bic = DECIMAL_4

    def test_bic(self):
        assert_almost_equal(self.res1.bic, self.res2.bic_Stata,
                            self.decimal_bic)

    def test_degrees(self):
        assert self.res1.model.df_resid == self.res2.df_resid

    decimal_fittedvalues = DECIMAL_4

    def test_fittedvalues(self):
        assert_almost_equal(self.res1.fittedvalues, self.res2.fittedvalues,
                            self.decimal_fittedvalues)

    def test_tpvalues(self):
        # test comparing tvalues and pvalues with normal implementation
        # make sure they use normal distribution (inherited in results class)
        params = self.res1.params
        tvalues = params / self.res1.bse
        pvalues = stats.norm.sf(np.abs(tvalues)) * 2
        half_width = stats.norm.isf(0.025) * self.res1.bse
        conf_int = np.column_stack((params - half_width, params + half_width))

        assert_almost_equal(self.res1.tvalues, tvalues)
        assert_almost_equal(self.res1.pvalues, pvalues)
        assert_almost_equal(self.res1.conf_int(), conf_int)

    def test_pearson_chi2(self):
        if hasattr(self.res2, 'pearson_chi2'):
            assert_allclose(self.res1.pearson_chi2, self.res2.pearson_chi2,
                            atol=1e-6, rtol=1e-6)

    @pytest.mark.smoke
    def test_summary(self):
        self.res1.summary()

    @pytest.mark.skip(reason="summary2 not ported from upstream")
    @pytest.mark.smoke
    def test_summary2(self):
        self.res1.summary2()


class CheckComparisonMixin(object):
    def test_params(self):
        assert_allclose(self.res1.params,
                        self.resd.params,
                        rtol=1e-10)

    def test_llf(self):
        assert_allclose(self.res1.llf,
                        self.resd.llf,
                        rtol=1e-10)

    def test_score_obs(self):
        # upstream added the 0.98 terms in GH#4630; presumably so the
        # params wouldn't be at an optimum and we wouldn't be comparing
        # against zero
        score_obs1 = self.res1.model.score_obs(self.res1.params * 0.98)
        score_obsd = self.resd.model.score_obs(self.resd.params * 0.98)
        assert_allclose(score_obs1,
                        score_obsd,
                        rtol=1e-10)

    def test_score(self):
        # See comment in test_score_obs regarding 0.98 term
        res1 = self.res1
        score_obs1 = res1.model.score_obs(self.res1.params * 0.98)
        score1 = res1.model.score(res1.params * 0.98)
        assert_allclose(score1,
                        score_obs1.sum(0),
                        atol=1e-20)
        score0 = res1.model.score(res1.params)
        assert_allclose(score0,
                        np.zeros(score_obs1.shape[1]),
                        atol=2e-7)
        # Note: upstream has atol=5e-7; locally 1e-7 passes and Travis fails
        # but would be OK with 1.01e-7

    def test_compare_discrete(self):
        # TODO: redundant with test_score above?
        res1 = self.res1

        # score
        score0 = res1.model.score(res1.params)
        score1 = res1.model.score(res1.params * 0.98)  # near-optimum
        score_obs1 = res1.model.score_obs(res1.params * 0.98)

        assert_allclose(score1, score_obs1.sum(0), atol=1e-20)
        assert_allclose(score0, np.zeros(score_obs1.shape[1]), atol=5e-7)
        # FIXME: locally the above assertion passes with atol=1e-7, but on
        # Travis I'm just barely seeing failures 2018-03-21 with
        # the first entry of score1 being -1.006265e-07
        # ... 2018-05-18 GH#4640 changed the tol to 5e-7, no documentation
        # as to why.

    def test_hessian_unobserved(self):
        res1 = self.res1
        resd = self.resd
        hessian1 = res1.model.hessian(res1.params * 0.98, observed=False)
        hessiand = resd.model.hessian(resd.params * 0.98)
        assert_allclose(hessian1,
                        hessiand,
                        rtol=1e-10)

    def test_hessian_observed(self):
        res1 = self.res1
        resd = self.resd
        hessian1 = res1.model.hessian(res1.params * 0.98, observed=True)
        hessiand = resd.model.hessian(resd.params * 0.98)
        assert_allclose(hessian1,
                        hessiand,
                        rtol=1e-9)

    def test_score_test(self):
        res1 = self.res1
        # fake example, should be zero, k_constraint should be 0
        st, pv, df = res1.model.score_test(res1.params, k_constraints=1)
        assert_allclose(st, 0, atol=1e-20)
        assert_allclose(pv, 1, atol=1e-10)
        assert df == 1

        st, pv, df = res1.model.score_test(res1.params, k_constraints=0)
        assert_allclose(st, 0, atol=1e-20)
        assert np.isnan(pv)
        assert df == 0

        # TODO: no verified numbers largely SMOKE test
        exog_extra = res1.model.exog[:, 1]**2
        st, pv, df = res1.model.score_test(res1.params, exog_extra=exog_extra)
        assert 0.1 < st
        assert 0.1 < pv
        assert df == 1


# TODO:
# Non-Canonical Links for the Binomial family require the algorithm to be
# slightly changed
# class TestGlmBinomialLog(CheckModelResultsMixin):
# class TestGlmBinomialLogit(CheckModelResultsMixin):
# class TestGlmBinomialProbit(CheckModelResultsMixin):
# class TestGlmBinomialCloglog(CheckModelResultsMixin):
# class TestGlmBinomialPower(CheckModelResultsMixin):
# class TestGlmBinomialLoglog(CheckModelResultsMixin):
# class TestGlmBinomialLogc(CheckModelResultsMixin):
#    TODO: need include logc link
# class TestGlmBernoulliIdentity(CheckModelResultsMixin):
# class TestGlmBernoulliLog(CheckModelResultsMixin):
# class TestGlmBernoulliProbit(CheckModelResultsMixin):
# class TestGlmBernoulliCloglog(CheckModelResultsMixin):
# class TestGlmBernoulliPower(CheckModelResultsMixin):
# class TestGlmBernoulliLoglog(CheckModelResultsMixin):
# class test_glm_bernoulli_logc(CheckModelResultsMixin):
# class TestGlmPoissonIdentity(CheckModelResultsMixin):
# class TestGlmPoissonPower(CheckModelResultsMixin):
# class TestGlmNegbinomial_log(CheckModelResultsMixin):
# class TestGlmNegbinomial_power(CheckModelResultsMixin):
# class TestGlmNegbinomial_nbinom(CheckModelResultsMixin):


@pytest.mark.not_vetted
class TestGlmGaussian(CheckModelResultsMixin):
    res2 = results_glm.Longley

    decimal_resids = DECIMAL_3
    decimal_params = DECIMAL_2
    decimal_bic = DECIMAL_0
    decimal_bse = DECIMAL_3

    @classmethod
    def setup_class(cls):
        """
        Test Gaussian family with canonical identity link
        """
        cls.data = sm.datasets.longley.load(as_pandas=False)
        cls.data.exog = add_constant(cls.data.exog, prepend=False)
        cls.res1 = GLM(cls.data.endog, cls.data.exog,
                       family=sm.families.Gaussian()).fit()

    def test_compare_OLS(self):
        res1 = self.res1
        # OLS doesn't define score_obs
        resd = sm.OLS(self.data.endog, self.data.exog).fit()
        self.resd = resd  # attach to access from the outside

        assert_allclose(res1.llf, resd.llf, rtol=1e-10)
        score_obs1 = res1.model.score_obs(res1.params, scale=None)
        score_obsd = resd.resid[:, None] / resd.scale * resd.model.exog
        # low precision because of badly scaled exog
        assert_allclose(score_obs1, score_obsd, rtol=1e-8)

        score_obs1 = res1.model.score_obs(res1.params, scale=1)
        score_obsd = resd.resid[:, None] * resd.model.exog
        assert_allclose(score_obs1, score_obsd, rtol=1e-8)

        hess_obs1 = res1.model.hessian(res1.params, scale=None)
        hess_obsd = -1. / resd.scale * resd.model.exog.T.dot(resd.model.exog)
        # low precision because of badly scaled exog
        assert_allclose(hess_obs1, hess_obsd, rtol=1e-8)


@pytest.mark.not_vetted
class TestGaussianLog(CheckModelResultsMixin):
    res2 = results_glm.GaussianLog

    decimal_aic_R = DECIMAL_0
    decimal_aic_Stata = DECIMAL_2
    decimal_loglike = DECIMAL_0
    decimal_null_deviance = DECIMAL_1

    @classmethod
    def setup_class(cls):
        nobs = 100
        x = np.arange(nobs)
        np.random.seed(54321)
        cls.X = np.c_[np.ones((nobs, 1)), x, x**2]
        cls.lny = (np.exp(-(-1.0 + 0.02 * x + 0.0001 * x**2)) +
                   0.001 * np.random.randn(nobs))

        GaussLog_Model = GLM(cls.lny, cls.X,
                             family=sm.families.Gaussian(links.log()))
        cls.res1 = GaussLog_Model.fit()


@pytest.mark.not_vetted
class TestGaussianInverse(CheckModelResultsMixin):
    res2 = results_glm.GaussianInverse

    decimal_bic = DECIMAL_1
    decimal_aic_R = DECIMAL_1
    decimal_aic_Stata = DECIMAL_3
    decimal_loglike = DECIMAL_1
    decimal_resids = DECIMAL_3

    @classmethod
    def setup_class(cls):
        nobs = 100
        x = np.arange(nobs)
        np.random.seed(54321)
        y = 1.0 + 2.0 * x + x**2 + 0.1 * np.random.randn(nobs)
        cls.X = np.c_[np.ones((nobs, 1)), x, x**2]
        cls.y_inv = ((1. + .02 * x + .001 * x**2)**-1 +
                     .001 * np.random.randn(nobs))
        fam = sm.families.Gaussian(links.inverse_power())
        InverseLink_Model = GLM(cls.y_inv, cls.X, family=fam)
        InverseLink_Res = InverseLink_Model.fit()
        cls.res1 = InverseLink_Res


@pytest.mark.not_vetted
class TestGlmBinomial(CheckModelResultsMixin):
    res2 = results_glm.Star98

    decimal_resids = DECIMAL_1
    decimal_bic = DECIMAL_2

    @classmethod
    def setup_class(cls):
        """
        Test Binomial family with canonical logit link using star98 dataset.
        """
        data = sm.datasets.star98.load(as_pandas=False)
        data.exog = add_constant(data.exog, prepend=False)
        cls.res1 = GLM(data.endog, data.exog,
                       family=sm.families.Binomial()).fit()


@pytest.mark.not_vetted
class TestGlmBernoulli(CheckModelResultsMixin, CheckComparisonMixin):
    res2 = results_glm.Lbw

    @classmethod
    def setup_class(cls):
        cls.res1 = GLM(cls.res2.endog, cls.res2.exog,
                       family=sm.families.Binomial()).fit()

        modd = discrete.Logit(cls.res2.endog, cls.res2.exog)
        cls.resd = modd.fit(start_params=cls.res1.params * 0.9, disp=False)

    def test_score_r(self):
        res1 = self.res1
        res2 = self.res2
        st, pv, df = res1.model.score_test(res1.params,
                                           exog_extra=res1.model.exog[:, 1]**2)
        st_res = 0.2837680293459376  # (-0.5326988167303712)**2
        assert_allclose(st, st_res, rtol=1e-4)

        st, pv, df = res1.model.score_test(res1.params,
                                           exog_extra=res1.model.exog[:, 0]**2)
        st_res = 0.6713492821514992  # (-0.8193590679009413)**2
        assert_allclose(st, st_res, rtol=1e-4)

        select = list(range(9))
        select.pop(7)

        res1b = GLM(res2.endog, res2.exog[:, select],
                    family=sm.families.Binomial()).fit()
        tres = res1b.model.score_test(res1b.params,
                                      exog_extra=res1.model.exog[:, -2])
        tres = np.asarray(tres[:2]).ravel()
        tres_r = (2.7864148487452, 0.0950667)
        assert_allclose(tres, tres_r, rtol=1e-4)

        # The next string is a variable "cmd_r" upstream; I think that
        # means that it is the command used to produce comparison
        # results in R
        """
        data = read.csv("...statsmodels\\statsmodels\\genmod\\tests\\results\\stata_lbw_glm.csv")

        data["race_black"] = data["race"] == "black"
        data["race_other"] = data["race"] == "other"
        mod = glm(low ~ age + lwt + race_black + race_other + smoke + ptl + ht + ui, family=binomial, data=data)
        options(digits=16)
        anova(mod, test="Rao")

        library(statmod)
        s = glm.scoretest(mod, data["age"]**2)
        s**2
        s = glm.scoretest(mod, data["lwt"]**2)
        s**2
        """  # noqa:E501


@pytest.mark.not_vetted
class TestGlmGamma(CheckModelResultsMixin):
    decimal_aic_R = -1  # TODO: off by about 1, we are right with Stata
    decimal_resids = DECIMAL_2

    @classmethod
    def setup_class(cls):
        """
        Tests Gamma family with canonical inverse link (power -1)
        """
        data = sm.datasets.scotland.load(as_pandas=False)
        data.exog = add_constant(data.exog, prepend=False)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            res1 = GLM(data.endog, data.exog,
                       family=sm.families.Gamma()).fit()
        cls.res1 = res1
        res2 = results_glm.Scotvote
        # FIXME: dont update in-place?
        # R doesn't count degree of freedom for scale with gamma
        res2.aic_R += 2
        cls.res2 = res2


@pytest.mark.not_vetted
class TestGlmGammaLog(CheckModelResultsMixin):
    res2 = results_glm.CancerLog

    decimal_resids = DECIMAL_3
    decimal_aic_R = DECIMAL_0
    decimal_fittedvalues = DECIMAL_3

    @classmethod
    def setup_class(cls):
        cls.res1 = GLM(cls.res2.endog, cls.res2.exog,
                       family=sm.families.Gamma(link=links.log())).fit()


@pytest.mark.not_vetted
class TestGlmGammaIdentity(CheckModelResultsMixin):
    res2 = results_glm.CancerIdentity()
    decimal_resids = -100  # TODO Very off from Stata?
    decimal_params = DECIMAL_2
    decimal_aic_R = DECIMAL_0
    decimal_loglike = DECIMAL_1

    @classmethod
    def setup_class(cls):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            model = GLM(cls.res2.endog, cls.res2.exog,
                        family=sm.families.Gamma(link=links.identity()))
            cls.res1 = model.fit()


@pytest.mark.not_vetted
class TestGlmPoisson(CheckModelResultsMixin, CheckComparisonMixin):
    res2 = results_glm.Cpunish

    @classmethod
    def setup_class(cls):
        """
        Tests Poisson family with canonical log link.

        Test results were obtained by R.
        """
        cls.data = sm.datasets.cpunish.load(as_pandas=False)
        cls.data.exog[:, 3] = np.log(cls.data.exog[:, 3])
        cls.data.exog = add_constant(cls.data.exog, prepend=False)
        cls.res1 = GLM(cls.data.endog, cls.data.exog,
                       family=sm.families.Poisson()).fit()
        # compare with discrete, start close to save time
        modd = discrete.Poisson(cls.data.endog, cls.data.exog)
        cls.resd = modd.fit(start_params=cls.res1.params * 0.9, disp=False)


@pytest.mark.not_vetted
class TestGlmInvgauss(CheckModelResultsMixin):
    res2 = results_glm.InvGauss()

    decimal_aic_R = DECIMAL_0
    decimal_loglike = DECIMAL_0

    @classmethod
    def setup_class(cls):
        """
        Tests the Inverse Gaussian family in GLM.

        Notes
        -----
        Used the rndivgx.ado file provided by Hardin and Hilbe to
        generate the data.  Results are read from model_results, which
        were obtained by running R_ig.s
        """
        res1 = GLM(cls.res2.endog, cls.res2.exog,
                   family=sm.families.InverseGaussian()).fit()
        cls.res1 = res1


@pytest.mark.not_vetted
class TestGlmInvgaussLog(CheckModelResultsMixin):
    res2 = results_glm.InvGaussLog

    decimal_aic_R = -10  # TODO: Big difference vs R.
    decimal_resids = DECIMAL_3

    @classmethod
    def setup_class(cls):
        model = GLM(cls.res2.endog, cls.res2.exog,
                    family=sm.families.InverseGaussian(link=links.log()))
        cls.res1 = model.fit()


@pytest.mark.not_vetted
class TestGlmInvgaussIdentity(CheckModelResultsMixin):
    res2 = results_glm.InvGaussIdentity
    decimal_aic_R = -10  # TODO: Big difference vs R
    decimal_fittedvalues = DECIMAL_3
    decimal_params = DECIMAL_3

    @classmethod
    def setup_class(cls):
        data = results_glm.Medpar1
        family = sm.families.InverseGaussian(link=links.identity())
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            cls.res1 = GLM(data.endog, data.exog, family=family).fit()


@pytest.mark.not_vetted
class TestGlmNegbinomial(CheckModelResultsMixin):
    decimal_resid = DECIMAL_1
    decimal_params = DECIMAL_3
    decimal_resids = -1  # 1 % mismatch at 0
    decimal_fittedvalues = DECIMAL_1

    @classmethod
    def setup_class(cls):
        """
        Test Negative Binomial family with log link
        """
        cls.data = sm.datasets.committee.load(as_pandas=False)
        cls.data.exog[:, 2] = np.log(cls.data.exog[:, 2])
        interaction = cls.data.exog[:, 2] * cls.data.exog[:, 1]
        cls.data.exog = np.column_stack((cls.data.exog, interaction))
        cls.data.exog = add_constant(cls.data.exog, prepend=False)
        cls.res1 = GLM(cls.data.endog, cls.data.exog,
                       family=sm.families.NegativeBinomial()).fit(scale='x2')
        res2 = results_glm.Committee
        # FIXME: Not sure editing in-place is a good idea
        res2.aic_R += 2  # They don't count a degree of freedom for the scale
        cls.res2 = res2


@pytest.mark.not_vetted
class TestGlmPoissonOffset(CheckModelResultsMixin):
    res2 = results_glm.Cpunish_offset

    decimal_params = DECIMAL_4
    decimal_bse = DECIMAL_4
    decimal_aic_R = 3

    @classmethod
    def setup_class(cls):
        data = sm.datasets.cpunish.load(as_pandas=False)
        data.exog[:, 3] = np.log(data.exog[:, 3])
        data.exog = add_constant(data.exog, prepend=True)
        exposure = [100] * len(data.endog)
        cls.data = data
        cls.exposure = exposure
        cls.res1 = GLM(data.endog, data.exog, family=sm.families.Poisson(),
                       exposure=exposure).fit()

    def test_missing(self):
        # make sure offset is dropped correctly
        endog = self.data.endog.copy()
        endog[[2, 4, 6, 8]] = np.nan
        mod = GLM(endog, self.data.exog, family=sm.families.Poisson(),
                  exposure=self.exposure, missing='drop')
        assert mod.exposure.shape[0] == 13

    def test_offset_exposure(self):
        # exposure=x and offset=log(x) should have the same effect
        np.random.seed(382304)
        endog = np.random.randint(0, 10, 100)
        exog = np.random.normal(size=(100, 3))
        exposure = np.random.uniform(1, 2, 100)
        offset = np.random.uniform(1, 2, 100)
        mod1 = GLM(endog, exog, family=sm.families.Poisson(),
                   offset=offset, exposure=exposure).fit()
        offset2 = offset + np.log(exposure)
        mod2 = GLM(endog, exog, family=sm.families.Poisson(),
                   offset=offset2).fit()
        assert_almost_equal(mod1.params, mod2.params)
        assert_allclose(mod1.null, mod2.null, rtol=1e-10)

        # test recreating model
        mod1_ = mod1.model
        kwds = mod1_._get_init_kwds()
        assert_allclose(kwds['exposure'], exposure, rtol=1e-14)
        assert_allclose(kwds['offset'], mod1_.offset, rtol=1e-14)
        mod3 = mod1_.__class__(mod1_.endog, mod1_.exog, **kwds)
        assert_allclose(mod3.exposure, mod1_.exposure, rtol=1e-14)
        assert_allclose(mod3.offset, mod1_.offset, rtol=1e-14)

        # test fit_regularized exposure, see GH#4605
        resr1 = mod1.model.fit_regularized()
        resr2 = mod2.model.fit_regularized()
        assert_allclose(resr1.params, resr2.params, rtol=1e-10)

    def test_predict(self):
        np.random.seed(382304)
        endog = np.random.randint(0, 10, 100)
        exog = np.random.normal(size=(100, 3))
        exposure = np.random.uniform(1, 2, 100)
        mod1 = GLM(endog, exog, family=sm.families.Poisson(),
                   exposure=exposure).fit()
        exog1 = np.random.normal(size=(10, 3))
        exposure1 = np.random.uniform(1, 2, 10)

        # Doubling exposure time should double expected response
        pred1 = mod1.predict(exog=exog1, exposure=exposure1)
        pred2 = mod1.predict(exog=exog1, exposure=2 * exposure1)
        assert_almost_equal(pred2, 2 * pred1)

        # Check exposure defaults
        pred3 = mod1.predict()
        pred4 = mod1.predict(exposure=exposure)
        pred5 = mod1.predict(exog=exog, exposure=exposure)
        assert_almost_equal(pred3, pred4)
        assert_almost_equal(pred4, pred5)

        # Check offset defaults
        offset = np.random.uniform(1, 2, 100)
        mod2 = GLM(endog, exog, offset=offset,
                   family=sm.families.Poisson()).fit()
        pred1 = mod2.predict()
        pred2 = mod2.predict(offset=offset)
        pred3 = mod2.predict(exog=exog, offset=offset)
        assert_almost_equal(pred1, pred2)
        assert_almost_equal(pred2, pred3)

        # Check that offset shifts the linear predictor
        mod3 = GLM(endog, exog, family=sm.families.Poisson()).fit()
        offset = np.random.uniform(1, 2, 10)
        pred1 = mod3.predict(exog=exog1, offset=offset, linear=True)
        pred2 = mod3.predict(exog=exog1, offset=2 * offset, linear=True)
        assert_almost_equal(pred2, pred1 + offset)


@pytest.mark.not_vetted
class TestStartParams(CheckModelResultsMixin):
    res2 = results_glm.Longley

    decimal_resids = DECIMAL_3
    decimal_params = DECIMAL_2
    decimal_bic = DECIMAL_0
    decimal_bse = DECIMAL_3

    @classmethod
    def setup_class(cls):
        """
        Test Gaussian family with canonical identity link
        """
        cls.data = sm.datasets.longley.load(as_pandas=False)
        cls.data.exog = add_constant(cls.data.exog, prepend=False)
        params = sm.OLS(cls.data.endog, cls.data.exog).fit().params
        cls.res1 = GLM(cls.data.endog, cls.data.exog,
                       family=sm.families.Gaussian()).fit(start_params=params)


@pytest.mark.not_vetted
class CheckWtdDuplicationMixin(object):
    decimal_params = DECIMAL_4

    @classmethod
    def setup_class(cls):
        cls.data = sm.datasets.cpunish.load(as_pandas=False)
        cls.endog = cls.data.endog
        cls.exog = cls.data.exog
        np.random.seed(1234)
        cls.weight = np.random.randint(5, 100, len(cls.endog))
        cls.endog_big = np.repeat(cls.endog, cls.weight)
        cls.exog_big = np.repeat(cls.exog, cls.weight, axis=0)

    def test_params(self):
        assert_allclose(self.res1.params,
                        self.res2.params,
                        atol=1e-6, rtol=1e-6)

    decimal_bse = DECIMAL_4

    def test_standard_errors(self):
        assert_allclose(self.res1.bse,
                        self.res2.bse,
                        rtol=1e-5, atol=1e-6)

    decimal_resids = DECIMAL_4

    # TODO: This doesn't work... Arrays are of different shape.
    # Perhaps we use self.res1.model.family.resid_XXX()?
    """
    def test_residuals(self):
        resids1 = np.column_stack((self.res1.resid_pearson,
                                   self.res1.resid_deviance,
                                   self.res1.resid_working,
                                   self.res1.resid_anscombe,
                                   self.res1.resid_response))
        resids2 = np.column_stack((self.res1.resid_pearson,
                                   self.res2.resid_deviance,
                                   self.res2.resid_working,
                                   self.res2.resid_anscombe,
                                   self.res2.resid_response))
        assert_allclose(resids1, resids2, self.decimal_resids)
    """

    def test_aic(self):
        # R includes the estimation of the scale as a lost dof
        # Doesn't with Gamma though
        assert_allclose(self.res1.aic,
                        self.res2.aic,
                        atol=1e-6, rtol=1e-6)

    def test_deviance(self):
        assert_allclose(self.res1.deviance,
                        self.res2.deviance,
                        atol=1e-6, rtol=1e-6)

    def test_scale(self):
        assert_allclose(self.res1.scale,
                        self.res2.scale,
                        atol=1e-6, rtol=1e-6)

    def test_loglike(self):
        # Stata uses the below llf for these families
        # We differ with R for them
        assert_allclose(self.res1.llf,
                        self.res2.llf,
                        1e-6)

    decimal_null_deviance = DECIMAL_4

    def test_null_deviance(self):
        assert_allclose(self.res1.null_deviance,
                        self.res2.null_deviance,
                        atol=1e-6, rtol=1e-6)

    decimal_bic = DECIMAL_4

    def test_bic(self):
        assert_allclose(self.res1.bic,
                        self.res2.bic,
                        atol=1e-6, rtol=1e-6)

    decimal_fittedvalues = DECIMAL_4

    def test_fittedvalues(self):
        res2_fitted = self.res2.predict(self.res1.model.exog)
        assert_allclose(self.res1.fittedvalues,
                        res2_fitted,
                        atol=1e-5, rtol=1e-5)

    decimal_tpvalues = DECIMAL_4

    def test_tpvalues(self):
        # test comparing tvalues and pvalues with normal implementation
        # make sure they use normal distribution (inherited in results class)
        assert_allclose(self.res1.tvalues,
                        self.res2.tvalues,
                        atol=1e-6, rtol=2e-4)
        assert_allclose(self.res1.pvalues,
                        self.res2.pvalues,
                        atol=1e-6, rtol=1e-6)
        assert_allclose(self.res1.conf_int(),
                        self.res2.conf_int(),
                        atol=1e-6, rtol=1e-6)


@pytest.mark.not_vetted
class TestWtdGlmPoisson(CheckWtdDuplicationMixin):
    @classmethod
    def setup_class(cls):
        """
        Tests Poisson family with canonical log link.
        """
        super(TestWtdGlmPoisson, cls).setup_class()
        cls.res1 = GLM(cls.endog, cls.exog,
                       freq_weights=cls.weight,
                       family=sm.families.Poisson()).fit()
        cls.res2 = GLM(cls.endog_big, cls.exog_big,
                       family=sm.families.Poisson()).fit()


@pytest.mark.not_vetted
class TestWtdGlmPoissonNewton(CheckWtdDuplicationMixin):
    @classmethod
    def setup_class(cls):
        """
        Tests Poisson family with canonical log link.
        """
        super(TestWtdGlmPoissonNewton, cls).setup_class()

        start_params = np.array([1.82794424e-04, -4.76785037e-02,
                                 -9.48249717e-02, -2.92293226e-04,
                                 2.63728909e+00, -2.05934384e+01])

        fit_kwds = dict(method='newton')
        cls.res1 = GLM(cls.endog, cls.exog,
                       freq_weights=cls.weight,
                       family=sm.families.Poisson()).fit(**fit_kwds)
        fit_kwds = dict(method='newton', start_params=start_params)
        cls.res2 = GLM(cls.endog_big, cls.exog_big,
                       family=sm.families.Poisson()).fit(**fit_kwds)


@pytest.mark.not_vetted
class TestWtdGlmPoissonHC0(CheckWtdDuplicationMixin):
    @classmethod
    def setup_class(cls):
        """
        Tests Poisson family with canonical log link.
        """
        super(TestWtdGlmPoissonHC0, cls).setup_class()

        start_params = np.array([1.82794424e-04, -4.76785037e-02,
                                 -9.48249717e-02, -2.92293226e-04,
                                 2.63728909e+00, -2.05934384e+01])

        fit_kwds = dict(cov_type='HC0')
        cls.res1 = GLM(cls.endog, cls.exog,
                       freq_weights=cls.weight,
                       family=sm.families.Poisson()).fit(**fit_kwds)
        fit_kwds = dict(cov_type='HC0', start_params=start_params)
        cls.res2 = GLM(cls.endog_big, cls.exog_big,
                       family=sm.families.Poisson()).fit(**fit_kwds)


@pytest.mark.not_vetted
class TestWtdGlmPoissonClu(CheckWtdDuplicationMixin):
    @classmethod
    def setup_class(cls):
        """
        Tests Poisson family with canonical log link.
        """
        super(TestWtdGlmPoissonClu, cls).setup_class()

        start_params = np.array([1.82794424e-04, -4.76785037e-02,
                                 -9.48249717e-02, -2.92293226e-04,
                                 2.63728909e+00, -2.05934384e+01])

        gid = np.arange(1, len(cls.endog) + 1) // 2
        fit_kwds = dict(cov_type='cluster',
                        cov_kwds={'groups': gid, 'use_correction': False})

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            cls.res1 = GLM(cls.endog, cls.exog,
                           freq_weights=cls.weight,
                           family=sm.families.Poisson()).fit(**fit_kwds)
            gidr = np.repeat(gid, cls.weight)
            fit_kwds = dict(cov_type='cluster',
                            cov_kwds={'groups': gidr, 'use_correction': False})
            model = GLM(cls.endog_big, cls.exog_big,
                        family=sm.families.Poisson())
            cls.res2 = model.fit(start_params=start_params, **fit_kwds)


@pytest.mark.not_vetted
class TestWtdGlmBinomial(CheckWtdDuplicationMixin):
    @classmethod
    def setup_class(cls):
        """
        Tests Binomial family with canonical logit link.
        """
        super(TestWtdGlmBinomial, cls).setup_class()
        cls.endog = cls.endog / 100
        cls.endog_big = cls.endog_big / 100
        cls.res1 = GLM(cls.endog, cls.exog,
                       freq_weights=cls.weight,
                       family=sm.families.Binomial()).fit()
        cls.res2 = GLM(cls.endog_big, cls.exog_big,
                       family=sm.families.Binomial()).fit()


@pytest.mark.not_vetted
class TestWtdGlmNegativeBinomial(CheckWtdDuplicationMixin):
    @classmethod
    def setup_class(cls):
        """
        Tests Negative Binomial family with canonical link
        g(p) = log(p/(p + 1/alpha))
        """
        super(TestWtdGlmNegativeBinomial, cls).setup_class()
        alpha = 1.
        family_link = sm.families.NegativeBinomial(
            link=links.nbinom(alpha=alpha),
            alpha=alpha)
        cls.res1 = GLM(cls.endog, cls.exog,
                       freq_weights=cls.weight,
                       family=family_link).fit()
        cls.res2 = GLM(cls.endog_big, cls.exog_big,
                       family=family_link).fit()


@pytest.mark.not_vetted
class TestWtdGlmGamma(CheckWtdDuplicationMixin):
    @classmethod
    def setup_class(cls):
        """
        Tests Gamma family with log link.
        """
        super(TestWtdGlmGamma, cls).setup_class()
        family_link = sm.families.Gamma(links.log())
        cls.res1 = GLM(cls.endog, cls.exog,
                       freq_weights=cls.weight,
                       family=family_link).fit()
        cls.res2 = GLM(cls.endog_big, cls.exog_big,
                       family=family_link).fit()


@pytest.mark.not_vetted
class TestWtdGlmGaussian(CheckWtdDuplicationMixin):
    @classmethod
    def setup_class(cls):
        """
        Tests Gaussian family with log link.
        """
        super(TestWtdGlmGaussian, cls).setup_class()
        family_link = sm.families.Gaussian(links.log())
        cls.res1 = GLM(cls.endog, cls.exog,
                       freq_weights=cls.weight,
                       family=family_link).fit()
        cls.res2 = GLM(cls.endog_big, cls.exog_big,
                       family=family_link).fit()


@pytest.mark.not_vetted
class TestWtdGlmInverseGaussian(CheckWtdDuplicationMixin):
    @classmethod
    def setup_class(cls):
        """
        Tests InverseGuassian family with log link.
        """
        super(TestWtdGlmInverseGaussian, cls).setup_class()
        family_link = sm.families.InverseGaussian(links.log())
        cls.res1 = GLM(cls.endog, cls.exog,
                       freq_weights=cls.weight,
                       family=family_link).fit()
        cls.res2 = GLM(cls.endog_big, cls.exog_big,
                       family=family_link).fit()


@pytest.mark.not_vetted
class TestWtdGlmGammaNewton(CheckWtdDuplicationMixin):
    @classmethod
    def setup_class(cls):
        """
        Tests Gamma family with log link.
        """
        super(TestWtdGlmGammaNewton, cls).setup_class()
        family_link = sm.families.Gamma(links.log())
        cls.res1 = GLM(cls.endog, cls.exog,
                       freq_weights=cls.weight,
                       family=family_link,
                       method='newton').fit()
        cls.res2 = GLM(cls.endog_big, cls.exog_big,
                       family=family_link,
                       method='newton').fit()


@pytest.mark.not_vetted
class TestWtdGlmGammaScale_X2(CheckWtdDuplicationMixin):
    @classmethod
    def setup_class(cls):
        """
        Tests Gamma family with log link.
        """
        super(TestWtdGlmGammaScale_X2, cls).setup_class()
        family_link = sm.families.Gamma(links.log())
        cls.res1 = GLM(cls.endog, cls.exog,
                       freq_weights=cls.weight,
                       family=family_link,
                       scale='X2').fit()
        cls.res2 = GLM(cls.endog_big, cls.exog_big,
                       family=family_link,
                       scale='X2').fit()


@pytest.mark.not_vetted
class TestWtdGlmGammaScale_dev(CheckWtdDuplicationMixin):
    @classmethod
    def setup_class(cls):
        """
        Tests Gamma family with log link.
        """
        super(TestWtdGlmGammaScale_dev, cls).setup_class()
        family_link = sm.families.Gamma(links.log())
        cls.res1 = GLM(cls.endog, cls.exog,
                       freq_weights=cls.weight,
                       family=family_link,
                       scale='dev').fit()
        cls.res2 = GLM(cls.endog_big, cls.exog_big,
                       family=family_link,
                       scale='dev').fit()

    def test_missing(self):
        endog = self.data.endog.copy()
        exog = self.data.exog.copy()
        exog[0, 0] = np.nan
        endog[[2, 4, 6, 8]] = np.nan
        freq_weights = self.weight
        mod_misisng = GLM(endog, exog, family=self.res1.model.family,
                          freq_weights=freq_weights, missing='drop')
        assert mod_misisng.freq_weights.shape[0] == mod_misisng.endog.shape[0]
        assert mod_misisng.freq_weights.shape[0] == mod_misisng.exog.shape[0]
        keep_idx = np.array([1, 3, 5, 7, 9, 10, 11, 12, 13, 14, 15, 16])
        assert_equal(mod_misisng.freq_weights, self.weight[keep_idx])


@pytest.mark.not_vetted
class TestWtdTweedieLog(CheckWtdDuplicationMixin):
    @classmethod
    def setup_class(cls):
        """
        Tests Tweedie family with log link and var_power=1.
        """
        super(TestWtdTweedieLog, cls).setup_class()
        family_link = sm.families.Tweedie(link=links.log(),
                                          var_power=1)
        cls.res1 = GLM(cls.endog, cls.exog,
                       freq_weights=cls.weight,
                       family=family_link).fit()
        cls.res2 = GLM(cls.endog_big, cls.exog_big,
                       family=family_link).fit()


@pytest.mark.not_vetted
class TestWtdTweediePower2(CheckWtdDuplicationMixin):
    @classmethod
    def setup_class(cls):
        """
        Tests Tweedie family with Power(1) link and var_power=2.
        """
        cls.data = sm.datasets.cpunish.load_pandas()
        cls.endog = cls.data.endog
        cls.exog = cls.data.exog[['INCOME', 'SOUTH']]
        np.random.seed(1234)
        cls.weight = np.random.randint(5, 100, len(cls.endog))
        cls.endog_big = np.repeat(cls.endog.values, cls.weight)
        cls.exog_big = np.repeat(cls.exog.values, cls.weight, axis=0)
        link = links.Power
        family_link = sm.families.Tweedie(link=link, var_power=2)
        cls.res1 = GLM(cls.endog, cls.exog,
                       freq_weights=cls.weight,
                       family=family_link).fit()
        cls.res2 = GLM(cls.endog_big, cls.exog_big,
                       family=family_link).fit()


@pytest.mark.not_vetted
class TestWtdTweediePower15(CheckWtdDuplicationMixin):
    @classmethod
    def setup_class(cls):
        """
        Tests Tweedie family with Power(0.5) link and var_power=1.5.
        """
        super(TestWtdTweediePower15, cls).setup_class()
        family_link = sm.families.Tweedie(link=links.Power(0.5),
                                          var_power=1.5)
        cls.res1 = GLM(cls.endog, cls.exog,
                       freq_weights=cls.weight,
                       family=family_link).fit()
        cls.res2 = GLM(cls.endog_big, cls.exog_big,
                       family=family_link).fit()


@pytest.mark.not_vetted
class CheckTweedie(object):
    def test_resid(self):
        r1len = len(self.res1.resid_response) - 1
        l2 = len(self.res2.resid_response) - 1
        assert_allclose(np.concatenate((self.res1.resid_response[:17],
                                        [self.res1.resid_response[r1len]])),
                        np.concatenate((self.res2.resid_response[:17],
                                        [self.res2.resid_response[l2]])),
                        rtol=1e-5, atol=1e-5)

        assert_allclose(np.concatenate((self.res1.resid_pearson[:17],
                                        [self.res1.resid_pearson[r1len]])),
                        np.concatenate((self.res2.resid_pearson[:17],
                                        [self.res2.resid_pearson[l2]])),
                        rtol=1e-5, atol=1e-5)

        assert_allclose(np.concatenate((self.res1.resid_deviance[:17],
                                        [self.res1.resid_deviance[r1len]])),
                        np.concatenate((self.res2.resid_deviance[:17],
                                        [self.res2.resid_deviance[l2]])),
                        rtol=1e-5, atol=1e-5)

        assert_allclose(np.concatenate((self.res1.resid_working[:17],
                                        [self.res1.resid_working[r1len]])),
                        np.concatenate((self.res2.resid_working[:17],
                                        [self.res2.resid_working[l2]])),
                        rtol=1e-5, atol=1e-5)

    def test_bse(self):
        assert_allclose(self.res1.bse,
                        self.res2.bse,
                        atol=1e-6, rtol=1e6)

    def test_params(self):
        assert_allclose(self.res1.params,
                        self.res2.params,
                        atol=1e-5, rtol=1e-5)

    def test_deviance(self):
        assert_allclose(self.res1.deviance,
                        self.res2.deviance,
                        atol=1e-6, rtol=1e-6)

    def test_df(self):
        assert self.res1.df_model == self.res2.df_model
        assert self.res1.df_resid == self.res2.df_resid

    def test_fittedvalues(self):
        r1len = len(self.res1.fittedvalues) - 1
        l2 = len(self.res2.resid_response) - 1
        assert_allclose(np.concatenate((self.res1.fittedvalues[:17],
                                        [self.res1.fittedvalues[r1len]])),
                        np.concatenate((self.res2.fittedvalues[:17],
                                        [self.res2.fittedvalues[l2]])),
                        atol=1e-4, rtol=1e-4)

    @pytest.mark.smoke
    def test_summary(self):
        self.res1.summary()

    @pytest.mark.skip(reason="summary2 not ported from upstream")
    @pytest.mark.smoke
    def test_summary2(self):
        self.res1.summary2()


@pytest.mark.not_vetted
class TestTweediePower15(CheckTweedie):
    res2 = results_glm.CpunishTweediePower15

    @classmethod
    def setup_class(cls):
        cls.data = sm.datasets.cpunish.load_pandas()
        cls.exog = cls.data.exog[['INCOME', 'SOUTH']]
        cls.endog = cls.data.endog
        family_link = sm.families.Tweedie(link=links.Power(1),
                                          var_power=1.5)
        cls.res1 = sm.GLM(endog=cls.data.endog,
                          exog=cls.data.exog[['INCOME', 'SOUTH']],
                          family=family_link).fit()


@pytest.mark.not_vetted
class TestTweediePower2(CheckTweedie):
    res2 = results_glm.CpunishTweediePower2

    @classmethod
    def setup_class(cls):
        cls.data = sm.datasets.cpunish.load_pandas()
        cls.exog = cls.data.exog[['INCOME', 'SOUTH']]
        cls.endog = cls.data.endog
        family_link = sm.families.Tweedie(link=links.Power(1),
                                          var_power=2.)
        cls.res1 = sm.GLM(endog=cls.data.endog,
                          exog=cls.data.exog[['INCOME', 'SOUTH']],
                          family=family_link).fit()


@pytest.mark.not_vetted
class TestTweedieLog1(CheckTweedie):
    res2 = results_glm.CpunishTweedieLog1

    @classmethod
    def setup_class(cls):
        cls.data = sm.datasets.cpunish.load_pandas()
        cls.exog = cls.data.exog[['INCOME', 'SOUTH']]
        cls.endog = cls.data.endog
        family_link = sm.families.Tweedie(link=links.log(),
                                          var_power=1.)
        cls.res1 = sm.GLM(endog=cls.data.endog,
                          exog=cls.data.exog[['INCOME', 'SOUTH']],
                          family=family_link).fit()


@pytest.mark.not_vetted
class TestTweedieLog15Fair(CheckTweedie):
    res2 = results_glm.FairTweedieLog15

    @classmethod
    def setup_class(cls):
        data = sm.datasets.fair.load_pandas()
        family_link = sm.families.Tweedie(link=links.log(),
                                          var_power=1.5)
        cls.res1 = sm.GLM(endog=data.endog,
                          exog=data.exog[['rate_marriage', 'age',
                                          'yrs_married']],
                          family=family_link).fit()


@pytest.mark.not_vetted
class CheckTweedieSpecial(object):
    def test_mu(self):
        assert_allclose(self.res1.mu,
                        self.res2.mu,
                        rtol=1e-5, atol=1e-5)

    def test_resid(self):
        assert_allclose(self.res1.resid_response,
                        self.res2.resid_response,
                        rtol=1e-5, atol=1e-5)
        assert_allclose(self.res1.resid_pearson,
                        self.res2.resid_pearson,
                        rtol=1e-5, atol=1e-5)
        assert_allclose(self.res1.resid_deviance,
                        self.res2.resid_deviance,
                        rtol=1e-5, atol=1e-5)
        assert_allclose(self.res1.resid_working,
                        self.res2.resid_working,
                        rtol=1e-5, atol=1e-5)
        assert_allclose(self.res1.resid_anscombe,
                        self.res2.resid_anscombe,
                        rtol=1e-5, atol=1e-5)


@pytest.mark.not_vetted
class TestTweedieSpecialLog0(CheckTweedieSpecial):
    @classmethod
    def setup_class(cls):
        cls.data = sm.datasets.cpunish.load_pandas()
        cls.exog = cls.data.exog[['INCOME', 'SOUTH']]
        cls.endog = cls.data.endog
        family1 = sm.families.Gaussian(link=links.log())
        cls.res1 = sm.GLM(endog=cls.data.endog,
                          exog=cls.data.exog[['INCOME', 'SOUTH']],
                          family=family1).fit()
        family2 = sm.families.Tweedie(link=links.log(),
                                      var_power=0)
        cls.res2 = sm.GLM(endog=cls.data.endog,
                          exog=cls.data.exog[['INCOME', 'SOUTH']],
                          family=family2).fit()


@pytest.mark.not_vetted
class TestTweedieSpecialLog1(CheckTweedieSpecial):
    @classmethod
    def setup_class(cls):
        cls.data = sm.datasets.cpunish.load_pandas()
        cls.exog = cls.data.exog[['INCOME', 'SOUTH']]
        cls.endog = cls.data.endog
        family1 = sm.families.Poisson(link=links.log())
        cls.res1 = sm.GLM(endog=cls.data.endog,
                          exog=cls.data.exog[['INCOME', 'SOUTH']],
                          family=family1).fit()
        family2 = sm.families.Tweedie(link=links.log(),
                                      var_power=1)
        cls.res2 = sm.GLM(endog=cls.data.endog,
                          exog=cls.data.exog[['INCOME', 'SOUTH']],
                          family=family2).fit()


@pytest.mark.not_vetted
class TestTweedieSpecialLog2(CheckTweedieSpecial):
    @classmethod
    def setup_class(cls):
        cls.data = sm.datasets.cpunish.load_pandas()
        cls.exog = cls.data.exog[['INCOME', 'SOUTH']]
        cls.endog = cls.data.endog
        family1 = sm.families.Gamma(link=links.log())
        cls.res1 = sm.GLM(endog=cls.data.endog,
                          exog=cls.data.exog[['INCOME', 'SOUTH']],
                          family=family1).fit()
        family2 = sm.families.Tweedie(link=links.log(),
                                      var_power=2)
        cls.res2 = sm.GLM(endog=cls.data.endog,
                          exog=cls.data.exog[['INCOME', 'SOUTH']],
                          family=family2).fit()


@pytest.mark.not_vetted
class TestTweedieSpecialLog3(CheckTweedieSpecial):
    @classmethod
    def setup_class(cls):
        cls.data = sm.datasets.cpunish.load_pandas()
        cls.exog = cls.data.exog[['INCOME', 'SOUTH']]
        cls.endog = cls.data.endog
        family1 = sm.families.InverseGaussian(link=links.log())
        cls.res1 = sm.GLM(endog=cls.data.endog,
                          exog=cls.data.exog[['INCOME', 'SOUTH']],
                          family=family1).fit()
        family2 = sm.families.Tweedie(link=links.log(),
                                      var_power=3)
        cls.res2 = sm.GLM(endog=cls.data.endog,
                          exog=cls.data.exog[['INCOME', 'SOUTH']],
                          family=family2).fit()


@pytest.mark.not_vetted
class TestRegularized(object):
    # TODO: Does this need to be a class?
    def test_regularized(self):
        for dtype in ["binomial", "poisson"]:
            cur_dir = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(cur_dir, "results", "enet_%s.csv" % dtype)
            data = np.loadtxt(path, delimiter=",")

            endog = data[:, 0]
            exog = data[:, 1:]

            fam = {"binomial": sm.families.Binomial,
                   "poisson": sm.families.Poisson}[dtype]

            for j in range(9):
                vn = "rslt_%s_%d" % (dtype, j)
                r_result = getattr(glmnet_r_results, vn)
                L1_wt = r_result[0]
                alpha = r_result[1]
                params = r_result[2:]

                model = GLM(endog, exog, family=fam())
                sm_result = model.fit_regularized(L1_wt=L1_wt, alpha=alpha)

                # Agreement is OK, see below for further check
                assert_allclose(params, sm_result.params,
                                atol=1e-2, rtol=0.3)

                # The penalized log-likelihood that we are maximizing.
                def plf(params):
                    llf = model.loglike(params) / len(endog)
                    llf = (llf -
                           alpha * ((1 - L1_wt) * np.sum(params**2) / 2 +
                                    L1_wt * np.sum(np.abs(params))))
                    return llf

                # Confirm that we are doing better than glmnet.
                llf_r = plf(params)
                llf_sm = plf(sm_result.params)
                assert np.sign(llf_sm - llf_r) == 1


@pytest.mark.not_vetted
class TestConvergence(object):
    @classmethod
    def setup_class(cls):
        """
        Test Binomial family with canonical logit link using star98 dataset.
        """
        data = sm.datasets.star98.load(as_pandas=False)
        data.exog = add_constant(data.exog, prepend=False)
        cls.model = GLM(data.endog, data.exog,
                        family=sm.families.Binomial())

    def _when_converged(self, atol=1e-8, rtol=0, tol_criterion='deviance'):
        for i, dev in enumerate(self.res.fit_history[tol_criterion]):
            orig = self.res.fit_history[tol_criterion][i]
            new = self.res.fit_history[tol_criterion][i + 1]
            if np.allclose(orig, new, atol=atol, rtol=rtol):
                return i
        raise ValueError("CONVERGENCE CHECK: It seems this doens't converge!")

    def test_convergence_atol_only(self):
        atol = 1e-8
        rtol = 0
        self.res = self.model.fit(atol=atol, rtol=rtol)
        expected_iterations = self._when_converged(atol=atol, rtol=rtol)
        actual_iterations = self.res.fit_history['iteration']
        # Note the first value is the list is np.inf. The second value
        # is the initial guess based off of start_params or the
        # estimate thereof. The third value (index = 2) is the actual "first
        # iteration"
        assert expected_iterations == actual_iterations
        assert len(self.res.fit_history['deviance']) - 2 == actual_iterations

    def test_convergence_rtol_only(self):
        atol = 0
        rtol = 1e-8
        self.res = self.model.fit(atol=atol, rtol=rtol)
        expected_iterations = self._when_converged(atol=atol, rtol=rtol)
        actual_iterations = self.res.fit_history['iteration']
        # Note the first value is the list is np.inf. The second value
        # is the initial guess based off of start_params or the
        # estimate thereof. The third value (index = 2) is the actual "first
        # iteration"
        assert expected_iterations == actual_iterations
        assert len(self.res.fit_history['deviance']) - 2 == actual_iterations

    def test_convergence_atol_rtol(self):
        atol = 1e-8
        rtol = 1e-8
        self.res = self.model.fit(atol=atol, rtol=rtol)
        expected_iterations = self._when_converged(atol=atol, rtol=rtol)
        actual_iterations = self.res.fit_history['iteration']
        # Note the first value is the list is np.inf. The second value
        # is the initial guess based off of start_params or the
        # estimate thereof. The third value (index = 2) is the actual "first
        # iteration"
        assert expected_iterations == actual_iterations
        assert len(self.res.fit_history['deviance']) - 2 == actual_iterations

    def test_convergence_atol_only_params(self):
        atol = 1e-8
        rtol = 0
        self.res = self.model.fit(atol=atol, rtol=rtol, tol_criterion='params')
        expected_iterations = self._when_converged(atol=atol, rtol=rtol,
                                                   tol_criterion='params')
        actual_iterations = self.res.fit_history['iteration']
        # Note the first value is the list is np.inf. The second value
        # is the initial guess based off of start_params or the
        # estimate thereof. The third value (index = 2) is the actual "first
        # iteration"
        assert expected_iterations == actual_iterations
        assert len(self.res.fit_history['deviance']) - 2 == actual_iterations

    def test_convergence_rtol_only_params(self):
        atol = 0
        rtol = 1e-8
        self.res = self.model.fit(atol=atol, rtol=rtol, tol_criterion='params')
        expected_iterations = self._when_converged(atol=atol, rtol=rtol,
                                                   tol_criterion='params')
        actual_iterations = self.res.fit_history['iteration']
        # Note the first value is the list is np.inf. The second value
        # is the initial guess based off of start_params or the
        # estimate thereof. The third value (index = 2) is the actual "first
        # iteration"
        assert expected_iterations == actual_iterations
        assert len(self.res.fit_history['deviance']) - 2 == actual_iterations

    def test_convergence_atol_rtol_params(self):
        atol = 1e-8
        rtol = 1e-8
        self.res = self.model.fit(atol=atol, rtol=rtol, tol_criterion='params')
        expected_iterations = self._when_converged(atol=atol, rtol=rtol,
                                                   tol_criterion='params')
        actual_iterations = self.res.fit_history['iteration']
        # Note the first value is the list is np.inf. The second value
        # is the initial guess based off of start_params or the
        # estimate thereof. The third value (index = 2) is the actual "first
        # iteration"
        assert expected_iterations == actual_iterations
        assert len(self.res.fit_history['deviance']) - 2 == actual_iterations


# ------------------------------------------------------------
# Unsorted

@pytest.mark.not_vetted
def test_tweedie_power_estimate():
    # Test the Pearson estimate of the Tweedie variance and scale parameters.
    #
    # Ideally, this would match the following R code, but I can't
    # make it work...
    #
    # setwd('c:/workspace')
    # data <- read.csv('cpunish.csv', sep=",")
    #
    # library(tweedie)
    #
    # y <- c(1.00113835e+05, 6.89668315e+03, 6.15726842e+03,
    #        1.41718806e+03, 5.11776456e+02, 2.55369154e+02,
    #        1.07147443e+01, 3.56874698e+00, 4.06797842e-02,
    #        7.06996731e-05, 2.10165106e-07, 4.34276938e-08,
    #        1.56354040e-09, 0.00000000e+00, 0.00000000e+00,
    #        0.00000000e+00, 0.00000000e+00)
    #
    # data$NewY <- y
    #
    # out <- tweedie.profile( NewY ~ INCOME + SOUTH - 1,
    #                         p.vec=c(1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8,
    #                                 1.9), link.power=0,
    #                         data=data, do.plot = TRUE)
    data = sm.datasets.cpunish.load_pandas()
    y = [1.00113835e+05, 6.89668315e+03, 6.15726842e+03,
         1.41718806e+03, 5.11776456e+02, 2.55369154e+02,
         1.07147443e+01, 3.56874698e+00, 4.06797842e-02,
         7.06996731e-05, 2.10165106e-07, 4.34276938e-08,
         1.56354040e-09, 0.00000000e+00, 0.00000000e+00,
         0.00000000e+00, 0.00000000e+00]
    model1 = sm.GLM(y, data.exog[['INCOME', 'SOUTH']],
                    family=sm.families.Tweedie(link=links.log(),
                                               var_power=1.5))
    res1 = model1.fit()
    model2 = sm.GLM((y - res1.mu) ** 2,
                    np.column_stack((np.ones(len(res1.mu)), np.log(res1.mu))),
                    family=sm.families.Gamma(links.log()))
    res2 = model2.fit()
    # Sample may be too small for this...
    # assert_allclose(res1.scale, np.exp(res2.params[0]), rtol=0.25)
    p = model1.estimate_tweedie_power(res1.mu)
    assert_allclose(p, res2.params[1], rtol=0.25)


@pytest.mark.not_vetted
def test_glm_start_params():
    # see GH#1604
    y2 = np.array('0 1 0 0 0 1'.split(), int)
    wt = np.array([50, 1, 50, 1, 5, 10])
    y2 = np.repeat(y2, wt)
    x2 = np.repeat([0, 0, 0.001, 100, -1, -1], wt)
    mod = sm.GLM(y2, sm.add_constant(x2), family=sm.families.Binomial())
    res = mod.fit(start_params=[-4, -5])
    np.testing.assert_almost_equal(res.params,
                                   [-4.60305022, -5.29634545],
                                   6)


@pytest.mark.not_vetted
def test_loglike_no_opt():
    # see GH#1728
    y = np.asarray([0, 1, 0, 0, 1, 1, 0, 1, 1, 1])
    x = np.arange(10, dtype=np.float64)

    def llf(params):
        lin_pred = params[0] + params[1] * x
        pr = 1 / (1 + np.exp(-lin_pred))
        return np.sum(y * np.log(pr) + (1 - y) * np.log(1 - pr))

    for params in [[0, 0], [0, 1], [0.5, 0.5]]:
        mod = sm.GLM(y, sm.add_constant(x), family=sm.families.Binomial())
        res = mod.fit(start_params=params, maxiter=0)
        like = llf(params)
        assert_almost_equal(like, res.llf)


@pytest.mark.not_vetted
def test_formula_missing_exposure():
    # see GH#2083
    d = {'Foo': [1, 2, 10, 149], 'Bar': [1, 2, 3, np.nan],
         'constant': [1] * 4, 'exposure': np.random.uniform(size=4),
         'x': [1, 3, 2, 1.5]}
    df = pd.DataFrame(d)

    family = sm.families.Gaussian(link=links.log())

    mod = GLM.from_formula("Foo ~ Bar", data=df, exposure=df.exposure,
                           family=family)
    assert type(mod.exposure) is np.ndarray

    exposure = pd.Series(np.random.uniform(size=5))
    df.loc[3, 'Bar'] = 4   # nan not relevant for ValueError for shape mismatch

    with pytest.raises(ValueError):
        GLM.from_formula("Foo ~ Bar", data=df,
                         exposure=exposure, family=family)
    with pytest.raises(ValueError):
        GLM(df.Foo, df[['constant', 'Bar']],
            exposure=exposure, family=family)


@pytest.mark.not_vetted
def test_poisson_deviance():
    # see GH#3355 missing term in deviance if resid_response.sum() != 0
    np.random.seed(123987)
    nobs, k_vars = 50, 3 - 1
    x = sm.add_constant(np.random.randn(nobs, k_vars))

    mu_true = np.exp(x.sum(1))
    y = np.random.poisson(mu_true, size=nobs)

    mod = sm.GLM(y, x[:, :], family=sm.genmod.families.Poisson())
    res = mod.fit()

    d_i = res.resid_deviance
    d = res.deviance
    lr = (mod.family.loglike(y, y + 1e-20) -
          mod.family.loglike(y, res.fittedvalues)) * 2

    assert_allclose(d, (d_i**2).sum(), rtol=1e-12)
    assert_allclose(d, lr, rtol=1e-12)

    # case without constant, resid_response.sum() != 0
    mod_nc = sm.GLM(y, x[:, 1:], family=sm.genmod.families.Poisson())
    res_nc = mod_nc.fit()

    d_i = res_nc.resid_deviance
    d = res_nc.deviance
    lr = (mod.family.loglike(y, y + 1e-20) -
          mod.family.loglike(y, res_nc.fittedvalues)) * 2

    assert_allclose(d, (d_i**2).sum(), rtol=1e-12)
    assert_allclose(d, lr, rtol=1e-12)


@pytest.mark.not_vetted
def test_wtd_patsy_missing():
    data = sm.datasets.cpunish.load(as_pandas=False)
    data.exog[0, 0] = np.nan
    data.endog[[2, 4, 6, 8]] = np.nan
    data.pandas = pd.DataFrame(data.exog, columns=data.exog_name)
    data.pandas['EXECUTIONS'] = data.endog
    weights = np.arange(1, len(data.endog) + 1)
    formula = """EXECUTIONS ~ INCOME + PERPOVERTY + PERBLACK + VC100k96 +
                 SOUTH + DEGREE"""
    mod_misisng = GLM.from_formula(formula, data=data.pandas,
                                   freq_weights=weights)
    assert mod_misisng.freq_weights.shape[0] == mod_misisng.endog.shape[0]
    assert mod_misisng.freq_weights.shape[0] == mod_misisng.exog.shape[0]
    assert mod_misisng.freq_weights.shape[0] == 12
    keep_weights = np.array([2, 4, 6, 8, 10, 11, 12, 13, 14, 15, 16, 17])
    assert_equal(mod_misisng.freq_weights, keep_weights)


@pytest.mark.not_vetted
def test_glm_irls_method():
    nobs, k_vars = 50, 4
    np.random.seed(987126)
    x = np.random.randn(nobs, k_vars - 1)
    exog = add_constant(x, has_constant='add')
    y = exog.sum(1) + np.random.randn(nobs)

    mod = GLM(y, exog)
    res1 = mod.fit()
    res2 = mod.fit(wls_method='pinv', attach_wls=True)
    res3 = mod.fit(wls_method='qr', attach_wls=True)
    # fit_gradient does not attach mle_settings
    res_g1 = mod.fit(start_params=res1.params, method='bfgs')

    for r in [res1, res2, res3]:
        assert r.mle_settings['optimizer'] == 'IRLS'
        assert r.method == 'IRLS'

    assert res1.mle_settings['wls_method'] == 'lstsq'
    assert res2.mle_settings['wls_method'] == 'pinv'
    assert res3.mle_settings['wls_method'] == 'qr'

    assert hasattr(res2.results_wls.model, 'pinv_wexog')
    assert hasattr(res3.results_wls.model, 'exog_Q')

    # fit_gradient currently does not attach mle_settings
    assert res_g1.method == 'bfgs'


@pytest.mark.not_vetted
def test_score_test_OLS():
    # nicer example than Longley
    np.random.seed(5)
    nobs = 100
    sige = 0.5
    x = np.random.uniform(0, 1, size=(nobs, 5))
    x[:, 0] = 1
    beta = 1. / np.arange(1., x.shape[1] + 1)
    y = x.dot(beta) + sige * np.random.randn(nobs)

    res_ols = sm.OLS(y, x).fit()
    res_olsc = sm.OLS(y, x[:, :-2]).fit()
    co = res_ols.compare_lm_test(res_olsc, demean=False)

    res_glm = GLM(y, x[:, :-2], family=sm.families.Gaussian()).fit()
    co2 = res_glm.model.score_test(res_glm.params, exog_extra=x[:, -2:])
    # difference in df_resid versus nobs in scale see GH#1786
    assert_allclose(co[0] * 97 / 100., co2[0], rtol=1e-13)


# ------------------------------------------------------------
# Unapologetic Smoke Tests

@pytest.mark.not_vetted
@pytest.mark.smoke
@pytest.mark.skip(reason="plotting functions not ported from upstream")
@pytest.mark.matplotlib
def test_plots(close_figures):
    np.random.seed(378)
    n = 200
    exog = np.random.normal(size=(n, 2))
    lin_pred = exog[:, 0] + exog[:, 1]**2
    prob = 1 / (1 + np.exp(-lin_pred))
    endog = 1 * (np.random.uniform(size=n) < prob)

    model = sm.GLM(endog, exog, family=sm.families.Binomial())
    result = model.fit()

    from statsmodels.graphics.regressionplots import add_lowess

    # array interface
    for j in [0, 1]:
        fig = result.plot_added_variable(j)
        add_lowess(fig.axes[0], frac=0.5)
        close_or_save(pdf, fig)
        fig = result.plot_partial_residuals(j)
        add_lowess(fig.axes[0], frac=0.5)
        close_or_save(pdf, fig)
        fig = result.plot_ceres_residuals(j)
        add_lowess(fig.axes[0], frac=0.5)
        close_or_save(pdf, fig)

    # formula interface
    data = pd.DataFrame({"y": endog, "x1": exog[:, 0], "x2": exog[:, 1]})
    model = sm.GLM.from_formula("y ~ x1 + x2", data,
                                family=sm.families.Binomial())
    result = model.fit()
    for j in [0, 1]:
        xname = ["x1", "x2"][j]
        fig = result.plot_added_variable(xname)
        add_lowess(fig.axes[0], frac=0.5)
        close_or_save(pdf, fig)
        fig = result.plot_partial_residuals(xname)
        add_lowess(fig.axes[0], frac=0.5)
        close_or_save(pdf, fig)
        fig = result.plot_ceres_residuals(xname)
        add_lowess(fig.axes[0], frac=0.5)
        close_or_save(pdf, fig)


@pytest.mark.smoke
def test_summary():
    np.random.seed(4323)

    n = 100
    exog = np.random.normal(size=(n, 2))
    exog[:, 0] = 1
    endog = np.random.normal(size=n)

    for method in ["irls", "cg"]:
        fa = sm.families.Gaussian()
        model = sm.GLM(endog, exog, family=fa)
        rslt = model.fit(method=method)
        rslt.summary()


# ------------------------------------------------------------
# Regression tests for an identifiable behavior for which GH references
# have not been found

@pytest.mark.not_vetted
def test_non_invertible_hessian_fails_summary():
    # Test when the hessian fails the summary is still available.
    # TODO: GH reference?
    data = sm.datasets.cpunish.load_pandas()

    data.endog[:] = 1
    mod = sm.GLM(data.endog, data.exog, family=sm.families.Gamma())
    res = mod.fit(maxiter=1, method='bfgs', max_start_irls=0)
    res.summary()


def test_attribute_writable_resettable():
    # Regression test for mutables and class constructors.
    # TODO: GH reference?
    data = sm.datasets.longley.load(as_pandas=False)
    endog, exog = data.endog, data.exog
    glm_model = sm.GLM(endog, exog)
    assert glm_model.family.link.power == 1.0
    glm_model.family.link.power = 2.
    assert glm_model.family.link.power == 2.0
    glm_model2 = sm.GLM(endog, exog)
    assert glm_model2.family.link.power == 1.0


def test_perfect_pred():
    # test that PerfectSeparationError is raised when appropriate
    # TODO: GH reference?
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    iris = np.genfromtxt(os.path.join(cur_dir, 'results', 'iris.csv'),
                         delimiter=",", skip_header=1)
    y = iris[:, -1]
    X = iris[:, :-1]
    X = X[y != 2]
    y = y[y != 2]
    X = add_constant(X, prepend=True)
    glm = GLM(y, X, family=sm.families.Binomial())
    with pytest.raises(PerfectSeparationError):
        glm.fit()

# ------------------------------------------------------------
# Issue-Specific Regression Tests
