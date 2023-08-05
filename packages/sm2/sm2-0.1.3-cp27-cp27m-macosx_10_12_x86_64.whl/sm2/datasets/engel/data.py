"""Name of dataset."""
from sm2.datasets import utils as du

__docformat__ = 'restructuredtext'

COPYRIGHT = """This is public domain."""
TITLE = """Engel (1857) food expenditure data"""
SOURCE = """
This dataset was used in Koenker and Bassett (1982) and distributed alongside
the ``quantreg`` package for R.

Koenker, R. and Bassett, G (1982) Robust Tests of Heteroscedasticity based on
Regression Quantiles; Econometrica 50, 43-61.

Roger Koenker (2012). quantreg: Quantile Regression. R package version 4.94.
http://CRAN.R-project.org/package=quantreg
"""

DESCRSHORT = """Engel food expenditure data."""

DESCRLONG = """
Data on income and food expenditure for 235 working class households
in 1857 Belgium.
"""

NOTE = """

    Number of observations: 235
    Number of variables: 2
    Variable name definitions:
        income - annual household income (Belgian francs)
        foodexp - annual household food expenditure (Belgian francs)
"""


def load(as_pandas=None):
    """
    Load the data and return a Dataset class instance.

    Parameters
    ----------
    as_pandas : bool
        Flag indicating whether to return pandas DataFrames and Series
        or numpy recarrays and arrays.  If True, returns pandas.

    Returns
    -------
    Dataset instance:
        See DATASET_PROPOSAL.txt for more information.
    """
    return du.as_numpy_dataset(load_pandas(), as_pandas=as_pandas)


def load_pandas():
    data = _get_data()
    return du.process_pandas(data, endog_idx=0, exog_idx=None)


def _get_data():
    return du.load_csv(__file__, 'engel.csv')
