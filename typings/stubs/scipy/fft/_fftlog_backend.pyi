"""
This type stub file was generated by pyright.
"""

__all__ = ['fht', 'ifht', 'fhtoffset']
LN_2 = ...
def fht(a, dln, mu, offset=..., bias=...): # -> Any | NDArray[Any]:
    ...

def ifht(A, dln, mu, offset=..., bias=...): # -> Any | NDArray[Any]:
    ...

def fhtcoeff(n, dln, mu, offset=..., bias=..., inverse=...): # -> Array | NDArray[Any]:
    """Compute the coefficient array for a fast Hankel transform."""
    ...

def fhtoffset(dln, mu, initial=..., bias=...):
    """Return optimal offset for a fast Hankel transform.

    Returns an offset close to `initial` that fulfils the low-ringing
    condition of [1]_ for the fast Hankel transform `fht` with logarithmic
    spacing `dln`, order `mu` and bias `bias`.

    Parameters
    ----------
    dln : float
        Uniform logarithmic spacing of the transform.
    mu : float
        Order of the Hankel transform, any positive or negative real number.
    initial : float, optional
        Initial value for the offset. Returns the closest value that fulfils
        the low-ringing condition.
    bias : float, optional
        Exponent of power law bias, any positive or negative real number.

    Returns
    -------
    offset : float
        Optimal offset of the uniform logarithmic spacing of the transform that
        fulfils a low-ringing condition.

    Examples
    --------
    >>> from scipy.fft import fhtoffset
    >>> dln = 0.1
    >>> mu = 2.0
    >>> initial = 0.5
    >>> bias = 0.0
    >>> offset = fhtoffset(dln, mu, initial, bias)
    >>> offset
    0.5454581477676637

    See Also
    --------
    fht : Definition of the fast Hankel transform.

    References
    ----------
    .. [1] Hamilton A. J. S., 2000, MNRAS, 312, 257 (astro-ph/9905191)

    """
    ...
