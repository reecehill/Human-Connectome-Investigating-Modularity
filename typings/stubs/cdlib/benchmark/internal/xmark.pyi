"""
This type stub file was generated by pyright.
"""

__all__ = ["XMark_benchmark"]
def zeta(x, q, tolerance): # -> Any | Literal[0]:
    """The Hurwitz zeta function, or the Riemann zeta function of two
    arguments.
    ``x`` must be greater than one and ``q`` must be positive.
    This function repeatedly computes subsequent partial sums until
    convergence, as decided by ``tolerance``.
    """
    ...

def XMark_benchmark(n, tau1, tau2, mu, labels=..., std=..., noise=..., lab_imb=..., average_degree=..., min_degree=..., max_degree=..., min_community=..., max_community=..., tol=..., max_iters=..., seed=..., type_attr=...): # -> Graph:
    ...
