"""
This type stub file was generated by pyright.
"""

__all__ = ["NdBSpline"]
class NdBSpline:
    """Tensor product spline object.

    The value at point ``xp = (x1, x2, ..., xN)`` is evaluated as a linear
    combination of products of one-dimensional b-splines in each of the ``N``
    dimensions::

       c[i1, i2, ..., iN] * B(x1; i1, t1) * B(x2; i2, t2) * ... * B(xN; iN, tN)


    Here ``B(x; i, t)`` is the ``i``-th b-spline defined by the knot vector
    ``t`` evaluated at ``x``.

    Parameters
    ----------
    t : tuple of 1D ndarrays
        knot vectors in directions 1, 2, ... N,
        ``len(t[i]) == n[i] + k + 1``
    c : ndarray, shape (n1, n2, ..., nN, ...)
        b-spline coefficients
    k : int or length-d tuple of integers
        spline degrees.
        A single integer is interpreted as having this degree for
        all dimensions.
    extrapolate : bool, optional
        Whether to extrapolate out-of-bounds inputs, or return `nan`.
        Default is to extrapolate.

    Attributes
    ----------
    t : tuple of ndarrays
        Knots vectors.
    c : ndarray
        Coefficients of the tensor-produce spline.
    k : tuple of integers
        Degrees for each dimension.
    extrapolate : bool, optional
        Whether to extrapolate or return nans for out-of-bounds inputs.
        Defaults to true.

    Methods
    -------
    __call__
    design_matrix

    See Also
    --------
    BSpline : a one-dimensional B-spline object
    NdPPoly : an N-dimensional piecewise tensor product polynomial

    """
    def __init__(self, t, c, k, *, extrapolate=...) -> None:
        ...
    
    def __call__(self, xi, *, nu=..., extrapolate=...): # -> ndarray[Any, dtype[complexfloating[_64Bit, _64Bit] | floating[_64Bit]]]:
        """Evaluate the tensor product b-spline at ``xi``.

        Parameters
        ----------
        xi : array_like, shape(..., ndim)
            The coordinates to evaluate the interpolator at.
            This can be a list or tuple of ndim-dimensional points
            or an array with the shape (num_points, ndim).
        nu : array_like, optional, shape (ndim,)
            Orders of derivatives to evaluate. Each must be non-negative.
            Defaults to the zeroth derivivative.
        extrapolate : bool, optional
            Whether to exrapolate based on first and last intervals in each
            dimension, or return `nan`. Default is to ``self.extrapolate``.

        Returns
        -------
        values : ndarray, shape ``xi.shape[:-1] + self.c.shape[ndim:]``
            Interpolated values at ``xi``
        """
        ...
    
    @classmethod
    def design_matrix(cls, xvals, t, k, extrapolate=...): # -> csr_array:
        """Construct the design matrix as a CSR format sparse array.

        Parameters
        ----------
        xvals :  ndarray, shape(npts, ndim)
            Data points. ``xvals[j, :]`` gives the ``j``-th data point as an
            ``ndim``-dimensional array.
        t : tuple of 1D ndarrays, length-ndim
            Knot vectors in directions 1, 2, ... ndim,
        k : int
            B-spline degree.
        extrapolate : bool, optional
            Whether to extrapolate out-of-bounds values of raise a `ValueError`

        Returns
        -------
        design_matrix : a CSR array
            Each row of the design matrix corresponds to a value in `xvals` and
            contains values of b-spline basis elements which are non-zero
            at this value.

        """
        ...
    


def make_ndbspl(points, values, k=..., *, solver=..., **solver_args): # -> NdBSpline:
    """Construct an interpolating NdBspline.

    Parameters
    ----------
    points : tuple of ndarrays of float, with shapes (m1,), ... (mN,)
        The points defining the regular grid in N dimensions. The points in
        each dimension (i.e. every element of the `points` tuple) must be
        strictly ascending or descending.      
    values : ndarray of float, shape (m1, ..., mN, ...)
        The data on the regular grid in n dimensions.
    k : int, optional
        The spline degree. Must be odd. Default is cubic, k=3
    solver : a `scipy.sparse.linalg` solver (iterative or direct), optional.
        An iterative solver from `scipy.sparse.linalg` or a direct one,
        `sparse.sparse.linalg.spsolve`.
        Used to solve the sparse linear system
        ``design_matrix @ coefficients = rhs`` for the coefficients.
        Default is `scipy.sparse.linalg.gcrotmk`
    solver_args : dict, optional
        Additional arguments for the solver. The call signature is
        ``solver(csr_array, rhs_vector, **solver_args)``

    Returns
    -------
    spl : NdBSpline object

    Notes
    -----
    Boundary conditions are not-a-knot in all dimensions.
    """
    ...
