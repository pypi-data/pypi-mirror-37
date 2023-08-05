from __future__ import absolute_import

import numpy as np


# TODO: de-privatize?
def _next_regular(target):  # noqa:C901
    """
    Find the next regular number greater than or equal to target.
    Regular numbers are composites of the prime factors 2, 3, and 5.
    Also known as 5-smooth numbers or Hamming numbers, these are the optimal
    size for inputs to FFTPACK.

    Target must be a positive integer.
    """
    if target <= 6:
        return target

    # Quickly check if it's already a power of 2
    if not (target & (target - 1)):
        return target

    match = float('inf')  # Anything found will be smaller
    p5 = 1
    while p5 < target:
        p35 = p5
        while p35 < target:
            # Ceiling integer division, avoiding conversion to float
            # (quotient = ceil(target / p35))
            quotient = -(-target // p35)
            # Quickly find next power of 2 >= quotient
            p2 = 2 ** ((quotient - 1).bit_length())

            N = p2 * p35
            if N == target:
                return N
            elif N < match:
                match = N
            p35 *= 3
            if p35 == target:
                return p35

        if p35 < match:
            match = p35
        p5 *= 5
        if p5 == target:
            return p5

    if p5 < match:
        match = p5
    return match


def _valarray(shape, value=np.nan, typecode=None):
    """Return an array of all value.
    """

    out = np.ones(shape, dtype=bool) * value
    if typecode is not None:
        out = out.astype(typecode)
    if not isinstance(out, np.ndarray):
        out = np.asarray(out)
    return out


def _lazywhere(cond, arrays, f, fillvalue=None, f2=None):
    """
    np.where(cond, x, fillvalue) always evaluates x even where cond is False.
    This one only evaluates f(arr1[cond], arr2[cond], ...).
    For example,
    >>> a, b = np.array([1, 2, 3, 4]), np.array([5, 6, 7, 8])
    >>> def f(a, b):
        return a*b
    >>> _lazywhere(a > 2, (a, b), f, np.nan)
    array([ nan,  nan,  21.,  32.])
    Notice it assumes that all `arrays` are of the same shape, or can be
    broadcasted together.
    """
    if fillvalue is None:
        if f2 is None:  # pragma: no cover
            raise ValueError("One of (fillvalue, f2) must be given.")
        else:
            fillvalue = np.nan
    else:
        if f2 is not None:  # pragma: no cover
            raise ValueError("Only one of (fillvalue, f2) can be given.")

    arrays = np.broadcast_arrays(*arrays)
    temp = tuple(np.extract(cond, arr) for arr in arrays)
    tcode = np.mintypecode([a.dtype.char for a in arrays])
    out = _valarray(np.shape(arrays[0]), value=fillvalue, typecode=tcode)
    np.place(out, cond, f(*temp))
    if f2 is not None:
        temp = tuple(np.extract(~cond, arr) for arr in arrays)
        np.place(out, ~cond, f2(*temp))

    return out


# Work around for complex chnges in gammaln in 1.0.0.
# loggamma introduced in 0.18.
try:
    from scipy.special import loggamma
except ImportError:
    from scipy.special import gammaln
    loggamma = gammaln


# Moved in 1.0 to special
try:
    from scipy.special import logsumexp, factorial, factorial2  # noqa:F401
except ImportError:
    from scipy.misc import logsumexp, factorial, factorial2  # noqa:F401
