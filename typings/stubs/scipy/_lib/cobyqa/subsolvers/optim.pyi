"""
This type stub file was generated by pyright.
"""

import numpy as np

TINY = np.finfo(float).tiny
EPS = np.finfo(float).eps
def tangential_byrd_omojokun(grad, hess_prod, xl, xu, delta, debug, **kwargs):
    r"""
    Minimize approximately a quadratic function subject to bound constraints in
    a trust region.

    This function solves approximately

    .. math::

        \min_{s \in \mathbb{R}^n} \quad g^{\mathsf{T}} s + \frac{1}{2}
        s^{\mathsf{T}} H s \quad \text{s.t.} \quad
        \left\{ \begin{array}{l}
            l \le s \le u\\
            \lVert s \rVert \le \Delta,
        \end{array} \right.

    using an active-set variation of the truncated conjugate gradient method.

    Parameters
    ----------
    grad : `numpy.ndarray`, shape (n,)
        Gradient :math:`g` as shown above.
    hess_prod : callable
        Product of the Hessian matrix :math:`H` with any vector.

            ``hess_prod(s) -> `numpy.ndarray`, shape (n,)``

        returns the product :math:`H s`.
    xl : `numpy.ndarray`, shape (n,)
        Lower bounds :math:`l` as shown above.
    xu : `numpy.ndarray`, shape (n,)
        Upper bounds :math:`u` as shown above.
    delta : float
        Trust-region radius :math:`\Delta` as shown above.
    debug : bool
        Whether to make debugging tests during the execution.

    Returns
    -------
    `numpy.ndarray`, shape (n,)
        Approximate solution :math:`s`.

    Other Parameters
    ----------------
    improve_tcg : bool, optional
        If True, a solution generated by the truncated conjugate gradient
        method that is on the boundary of the trust region is improved by
        moving around the trust-region boundary on the two-dimensional space
        spanned by the solution and the gradient of the quadratic function at
        the solution (default is True).

    Notes
    -----
    This function implements Algorithm 6.2 of [1]_. It is assumed that the
    origin is feasible with respect to the bound constraints and that `delta`
    is finite and positive.

    References
    ----------
    .. [1] T. M. Ragonneau. *Model-Based Derivative-Free Optimization Methods
       and Software*. PhD thesis, Department of Applied Mathematics, The Hong
       Kong Polytechnic University, Hong Kong, China, 2022. URL:
       https://theses.lib.polyu.edu.hk/handle/200/12294.
    """
    ...

def constrained_tangential_byrd_omojokun(grad, hess_prod, xl, xu, aub, bub, aeq, delta, debug, **kwargs):
    r"""
    Minimize approximately a quadratic function subject to bound and linear
    constraints in a trust region.

    This function solves approximately

    .. math::

        \min_{s \in \mathbb{R}^n} \quad g^{\mathsf{T}} s + \frac{1}{2}
        s^{\mathsf{T}} H s \quad \text{s.t.} \quad
        \left\{ \begin{array}{l}
            l \le s \le u,\\
            A_{\scriptscriptstyle I} s \le b_{\scriptscriptstyle I},\\
            A_{\scriptscriptstyle E} s = 0,\\
            \lVert s \rVert \le \Delta,
        \end{array} \right.

    using an active-set variation of the truncated conjugate gradient method.

    Parameters
    ----------
    grad : `numpy.ndarray`, shape (n,)
        Gradient :math:`g` as shown above.
    hess_prod : callable
        Product of the Hessian matrix :math:`H` with any vector.

            ``hess_prod(s) -> `numpy.ndarray`, shape (n,)``

        returns the product :math:`H s`.
    xl : `numpy.ndarray`, shape (n,)
        Lower bounds :math:`l` as shown above.
    xu : `numpy.ndarray`, shape (n,)
        Upper bounds :math:`u` as shown above.
    aub : `numpy.ndarray`, shape (m_linear_ub, n)
        Coefficient matrix :math:`A_{\scriptscriptstyle I}` as shown above.
    bub : `numpy.ndarray`, shape (m_linear_ub,)
        Right-hand side :math:`b_{\scriptscriptstyle I}` as shown above.
    aeq : `numpy.ndarray`, shape (m_linear_eq, n)
        Coefficient matrix :math:`A_{\scriptscriptstyle E}` as shown above.
    delta : float
        Trust-region radius :math:`\Delta` as shown above.
    debug : bool
        Whether to make debugging tests during the execution.

    Returns
    -------
    `numpy.ndarray`, shape (n,)
        Approximate solution :math:`s`.

    Other Parameters
    ----------------
    improve_tcg : bool, optional
        If True, a solution generated by the truncated conjugate gradient
        method that is on the boundary of the trust region is improved by
        moving around the trust-region boundary on the two-dimensional space
        spanned by the solution and the gradient of the quadratic function at
        the solution (default is True).

    Notes
    -----
    This function implements Algorithm 6.3 of [1]_. It is assumed that the
    origin is feasible with respect to the bound and linear constraints, and
    that `delta` is finite and positive.

    References
    ----------
    .. [1] T. M. Ragonneau. *Model-Based Derivative-Free Optimization Methods
       and Software*. PhD thesis, Department of Applied Mathematics, The Hong
       Kong Polytechnic University, Hong Kong, China, 2022. URL:
       https://theses.lib.polyu.edu.hk/handle/200/12294.
    """
    ...

def normal_byrd_omojokun(aub, bub, aeq, beq, xl, xu, delta, debug, **kwargs):
    r"""
    Minimize approximately a linear constraint violation subject to bound
    constraints in a trust region.

    This function solves approximately

    .. math::

        \min_{s \in \mathbb{R}^n} \quad \frac{1}{2} \big( \lVert \max \{
        A_{\scriptscriptstyle I} s - b_{\scriptscriptstyle I}, 0 \} \rVert^2 +
        \lVert A_{\scriptscriptstyle E} s - b_{\scriptscriptstyle E} \rVert^2
        \big) \quad \text{s.t.}
        \quad
        \left\{ \begin{array}{l}
            l \le s \le u,\\
            \lVert s \rVert \le \Delta,
        \end{array} \right.

    using a variation of the truncated conjugate gradient method.

    Parameters
    ----------
    aub : `numpy.ndarray`, shape (m_linear_ub, n)
        Matrix :math:`A_{\scriptscriptstyle I}` as shown above.
    bub : `numpy.ndarray`, shape (m_linear_ub,)
        Vector :math:`b_{\scriptscriptstyle I}` as shown above.
    aeq : `numpy.ndarray`, shape (m_linear_eq, n)
        Matrix :math:`A_{\scriptscriptstyle E}` as shown above.
    beq : `numpy.ndarray`, shape (m_linear_eq,)
        Vector :math:`b_{\scriptscriptstyle E}` as shown above.
    xl : `numpy.ndarray`, shape (n,)
        Lower bounds :math:`l` as shown above.
    xu : `numpy.ndarray`, shape (n,)
        Upper bounds :math:`u` as shown above.
    delta : float
        Trust-region radius :math:`\Delta` as shown above.
    debug : bool
        Whether to make debugging tests during the execution.

    Returns
    -------
    `numpy.ndarray`, shape (n,)
        Approximate solution :math:`s`.

    Other Parameters
    ----------------
    improve_tcg : bool, optional
        If True, a solution generated by the truncated conjugate gradient
        method that is on the boundary of the trust region is improved by
        moving around the trust-region boundary on the two-dimensional space
        spanned by the solution and the gradient of the quadratic function at
        the solution (default is True).

    Notes
    -----
    This function implements Algorithm 6.4 of [1]_. It is assumed that the
    origin is feasible with respect to the bound constraints and that `delta`
    is finite and positive.

    References
    ----------
    .. [1] T. M. Ragonneau. *Model-Based Derivative-Free Optimization Methods
       and Software*. PhD thesis, Department of Applied Mathematics, The Hong
       Kong Polytechnic University, Hong Kong, China, 2022. URL:
       https://theses.lib.polyu.edu.hk/handle/200/12294.
    """
    ...

def qr_tangential_byrd_omojokun(aub, aeq, free_xl, free_xu, free_ub): # -> tuple[int, NDArray[Any] | tuple[NDArray[Any], NDArray[Any]] | tuple[Any, Any] | Any]:
    ...

def qr_normal_byrd_omojokun(aub, free_xl, free_xu, free_slack, free_ub): # -> tuple[int, NDArray[Any] | tuple[NDArray[Any], NDArray[Any]] | tuple[Any, Any] | Any]:
    ...
