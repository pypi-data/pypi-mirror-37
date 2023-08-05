#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import pytest

try:
    import matplotlib
    matplotlib.use('agg')
    HAVE_MATPLOTLIB = True
except ImportError:
    HAVE_MATPLOTLIB = False


def pytest_addoption(parser):
    parser.addoption("--skip-slow", action="store_true",
                     help="skip slow tests")
    parser.addoption("--only-slow", action="store_true",
                     help="run only slow tests")
    parser.addoption("--skip-examples", action="store_true",
                     help="skip tests of examples")
    parser.addoption("--skip-matplotlib", action="store_true",
                     help="skip tests that depend on matplotlib")

    parser.addoption("--skip-smoke", action="store_true",
                     help="skip tests marked as smoke (i.e. smoke-tests)")
    parser.addoption("--only-smoke", action="store_true",
                     help="run only smoke tests")

    parser.addoption("--skip-not_vetted", action="store_true",
                     help="skip tests marked as not_vetted")


def pytest_runtest_setup(item):
    if 'slow' in item.keywords and item.config.getoption("--skip-slow"):
        pytest.skip("skipping due to --skip-slow")

    if 'slow' not in item.keywords and item.config.getoption("--only-slow"):
        pytest.skip("skipping due to --only-slow")

    if 'example' in item.keywords and item.config.getoption("--skip-examples"):
        pytest.skip("skipping due to --skip-examples")

    if 'matplotlib' in item.keywords and \
            item.config.getoption("--skip-matplotlib"):
        pytest.skip("skipping due to --skip-matplotlib")

    if 'matplotlib' in item.keywords and not HAVE_MATPLOTLIB:
        pytest.skip("skipping since matplotlib is not intalled")

    if 'smoke' in item.keywords and item.config.getoption("--skip-smoke"):
        pytest.skip("skipping due to --skip-smoke")

    if 'smoke' not in item.keywords and item.config.getoption('--only-smoke'):
        pytest.skip("skipping due to --only-smoke")

    if ('not_vetted' in item.keywords and
            item.config.getoption("--skip-not_vetted")):
        pytest.skip("skipping due to --skip-not_vetted")


def pytest_configure(config):
    try:
        import matplotlib
        matplotlib.use('agg')
    except ImportError:
        pass


@pytest.fixture()
def close_figures():
    """
    Fixture that closes all figures after a test function has completed

    Returns
    -------
    closer : callable
        Function that will close all figures when called.

    Notes
    -----
    Used by passing as an argument to the function that produces a plot,
    for example

    def test_some_plot(close_figures):
        <test code>

    If a function creates many figures, then these can be destroyed within a
    test function by calling close_figures to ensure that the number of
    figures does not become too large.

    def test_many_plots(close_figures):
        for i in range(100000):
            plt.plot(x,y)
            close_figures()
    """
    try:
        import matplotlib.pyplot

        def close():
            matplotlib.pyplot.close('all')

    except ImportError:
        def close():
            pass

    yield close
    close()


@pytest.fixture()
def reset_randomstate():
    """
    Fixture that set the global RandomState to the fixed seed 1

    Notes
    -----
    Used by passing as an argument to the function that uses the global
    RandomState

    def test_some_plot(reset_randomstate):
        <test code>

    Returns the state after the test function exits
    """
    state = np.random.get_state()
    np.random.seed(1)
    yield
    np.random.set_state(state)
