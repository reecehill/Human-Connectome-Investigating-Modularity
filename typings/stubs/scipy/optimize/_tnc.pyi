"""
This type stub file was generated by pyright.
"""

"""
TNC: A Python interface to the TNC non-linear optimizer

TNC is a non-linear optimizer. To use it, you must provide a function to
minimize. The function must take one argument: the list of coordinates where to
evaluate the function; and it must return either a tuple, whose first element is the
value of the function, and whose second argument is the gradient of the function
(as a list of values); or None, to abort the minimization.
"""
__all__ = ['fmin_tnc']
MSG_NONE = ...
MSG_ITER = ...
MSG_INFO = ...
MSG_VERS = ...
MSG_EXIT = ...
MSG_ALL = ...
MSGS = ...
INFEASIBLE = ...
LOCALMINIMUM = ...
FCONVERGED = ...
XCONVERGED = ...
MAXFUN = ...
LSFAIL = ...
CONSTANT = ...
NOPROGRESS = ...
USERABORT = ...
RCSTRINGS = ...
def fmin_tnc(func, x0, fprime=..., args=..., approx_grad=..., bounds=..., epsilon=..., scale=..., offset=..., messages=..., maxCGit=..., maxfun=..., eta=..., stepmx=..., accuracy=..., fmin=..., ftol=..., xtol=..., pgtol=..., rescale=..., disp=..., callback=...): # -> tuple[Any, Any, Any]:
    """
    Minimize a function with variables subject to bounds, using
    gradient information in a truncated Newton algorithm. This
    method wraps a C implementation of the algorithm.

    Parameters
    ----------
    func : callable ``func(x, *args)``
        Function to minimize.  Must do one of:

        1. Return f and g, where f is the value of the function and g its
           gradient (a list of floats).

        2. Return the function value but supply gradient function
           separately as `fprime`.

        3. Return the function value and set ``approx_grad=True``.

        If the function returns None, the minimization
        is aborted.
    x0 : array_like
        Initial estimate of minimum.
    fprime : callable ``fprime(x, *args)``, optional
        Gradient of `func`. If None, then either `func` must return the
        function value and the gradient (``f,g = func(x, *args)``)
        or `approx_grad` must be True.
    args : tuple, optional
        Arguments to pass to function.
    approx_grad : bool, optional
        If true, approximate the gradient numerically.
    bounds : list, optional
        (min, max) pairs for each element in x0, defining the
        bounds on that parameter. Use None or +/-inf for one of
        min or max when there is no bound in that direction.
    epsilon : float, optional
        Used if approx_grad is True. The stepsize in a finite
        difference approximation for fprime.
    scale : array_like, optional
        Scaling factors to apply to each variable. If None, the
        factors are up-low for interval bounded variables and
        1+|x| for the others. Defaults to None.
    offset : array_like, optional
        Value to subtract from each variable. If None, the
        offsets are (up+low)/2 for interval bounded variables
        and x for the others.
    messages : int, optional
        Bit mask used to select messages display during
        minimization values defined in the MSGS dict. Defaults to
        MGS_ALL.
    disp : int, optional
        Integer interface to messages. 0 = no message, 5 = all messages
    maxCGit : int, optional
        Maximum number of hessian*vector evaluations per main
        iteration. If maxCGit == 0, the direction chosen is
        -gradient if maxCGit < 0, maxCGit is set to
        max(1,min(50,n/2)). Defaults to -1.
    maxfun : int, optional
        Maximum number of function evaluation. If None, maxfun is
        set to max(100, 10*len(x0)). Defaults to None. Note that this function
        may violate the limit because of evaluating gradients by numerical
        differentiation.
    eta : float, optional
        Severity of the line search. If < 0 or > 1, set to 0.25.
        Defaults to -1.
    stepmx : float, optional
        Maximum step for the line search. May be increased during
        call. If too small, it will be set to 10.0. Defaults to 0.
    accuracy : float, optional
        Relative precision for finite difference calculations. If
        <= machine_precision, set to sqrt(machine_precision).
        Defaults to 0.
    fmin : float, optional
        Minimum function value estimate. Defaults to 0.
    ftol : float, optional
        Precision goal for the value of f in the stopping criterion.
        If ftol < 0.0, ftol is set to 0.0 defaults to -1.
    xtol : float, optional
        Precision goal for the value of x in the stopping
        criterion (after applying x scaling factors). If xtol <
        0.0, xtol is set to sqrt(machine_precision). Defaults to
        -1.
    pgtol : float, optional
        Precision goal for the value of the projected gradient in
        the stopping criterion (after applying x scaling factors).
        If pgtol < 0.0, pgtol is set to 1e-2 * sqrt(accuracy).
        Setting it to 0.0 is not recommended. Defaults to -1.
    rescale : float, optional
        Scaling factor (in log10) used to trigger f value
        rescaling. If 0, rescale at each iteration. If a large
        value, never rescale. If < 0, rescale is set to 1.3.
    callback : callable, optional
        Called after each iteration, as callback(xk), where xk is the
        current parameter vector.

    Returns
    -------
    x : ndarray
        The solution.
    nfeval : int
        The number of function evaluations.
    rc : int
        Return code, see below

    See also
    --------
    minimize: Interface to minimization algorithms for multivariate
        functions. See the 'TNC' `method` in particular.

    Notes
    -----
    The underlying algorithm is truncated Newton, also called
    Newton Conjugate-Gradient. This method differs from
    scipy.optimize.fmin_ncg in that

    1. it wraps a C implementation of the algorithm
    2. it allows each variable to be given an upper and lower bound.

    The algorithm incorporates the bound constraints by determining
    the descent direction as in an unconstrained truncated Newton,
    but never taking a step-size large enough to leave the space
    of feasible x's. The algorithm keeps track of a set of
    currently active constraints, and ignores them when computing
    the minimum allowable step size. (The x's associated with the
    active constraint are kept fixed.) If the maximum allowable
    step size is zero then a new constraint is added. At the end
    of each iteration one of the constraints may be deemed no
    longer active and removed. A constraint is considered
    no longer active is if it is currently active
    but the gradient for that variable points inward from the
    constraint. The specific constraint removed is the one
    associated with the variable of largest index whose
    constraint is no longer active.

    Return codes are defined as follows::

        -1 : Infeasible (lower bound > upper bound)
         0 : Local minimum reached (|pg| ~= 0)
         1 : Converged (|f_n-f_(n-1)| ~= 0)
         2 : Converged (|x_n-x_(n-1)| ~= 0)
         3 : Max. number of function evaluations reached
         4 : Linear search failed
         5 : All lower bounds are equal to the upper bounds
         6 : Unable to progress
         7 : User requested end of minimization

    References
    ----------
    Wright S., Nocedal J. (2006), 'Numerical Optimization'

    Nash S.G. (1984), "Newton-Type Minimization Via the Lanczos Method",
    SIAM Journal of Numerical Analysis 21, pp. 770-778

    """
    ...
