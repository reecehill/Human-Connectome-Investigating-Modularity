"""
This type stub file was generated by pyright.
"""

"""Miscellaneous utility functions
"""
def human_order_sorted(l): # -> list[Unknown]:
    """Sorts string in human order (i.e. 'stat10' will go after 'stat2')"""
    ...

def trim(docstring, marker=...): # -> str:
    ...

def find_indices(condition): # -> NDArray[intp]:
    "Return the indices where ravel(condition) is true"
    ...

def is_container(item): # -> bool:
    """Checks if item is a container (list, tuple, dict, set)

    Parameters
    ----------
    item : object
        object to check for .__iter__

    Returns
    -------
    output : Boolean
        True if container
        False if not (eg string)
    """
    ...

def container_to_string(cont): # -> str:
    """Convert a container to a command line string.

    Elements of the container are joined with a space between them,
    suitable for a command line parameter.

    If the container `cont` is only a sequence, like a string and not a
    container, it is returned unmodified.

    Parameters
    ----------
    cont : container
       A container object like a list, tuple, dict, or a set.

    Returns
    -------
    cont_str : string
        Container elements joined into a string.

    """
    ...

def package_check(pkg_name, version=..., app=..., checker=..., exc_failed_import=..., exc_failed_check=...): # -> None:
    """Check that the minimal version of the required package is installed.

    Parameters
    ----------
    pkg_name : string
        Name of the required package.
    version : string, optional
        Minimal version number for required package.
    app : string, optional
        Application that is performing the check.  For instance, the
        name of the tutorial being executed that depends on specific
        packages.  Default is *Nipype*.
    checker : object, optional
        The class that will perform the version checking.  Default is
        nipype.external.version.LooseVersion.
    exc_failed_import : Exception, optional
        Class of the exception to be thrown if import failed.
    exc_failed_check : Exception, optional
        Class of the exception to be thrown if version check failed.

    Examples
    --------
    package_check('numpy', '1.3')
    package_check('scipy', '0.7', 'tutorial1')

    """
    ...

def str2bool(v): # -> bool:
    """
    Convert strings (and bytearrays) to boolean values

    >>> all([str2bool(v) for v in (True, "yes", "true",
    ...      "y", "t", "Yes", "True", "1", "on", "On")])
    True
    >>> all([str2bool(v.encode('utf-8'))
    ...      for v in ("yes", "true", "y", "t", "1", "Yes", "on", "On")])
    True
    >>> any([str2bool(v) for v in (False, "no", "false", "n", "f",
    ...      "False", "0", "off", "Off")])
    False
    >>> any([str2bool(v.encode('utf-8'))
    ...      for v in ("no", "false", "n", "f", "0", "off", "Off")])
    False
    >>> str2bool(None)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    ValueError: ...
    >>> str2bool('/some/path')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    ValueError: ...
    >>> str2bool('Agg')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    ValueError: ...
    >>> str2bool('INFO')  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    ValueError: ...
    >>> str2bool('/some/bytes/path'.encode('utf-8'))  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    ValueError: ...

    """
    ...

def flatten(S):
    ...

def unflatten(in_list, prev_structure): # -> list[Unknown]:
    ...

def normalize_mc_params(params, source): # -> NDArray[float64]:
    """
    Normalize a single row of motion parameters to the SPM format.

    SPM saves motion parameters as:
        x   Right-Left          (mm)
        y   Anterior-Posterior  (mm)
        z   Superior-Inferior   (mm)
        rx  Pitch               (rad)
        ry  Roll                (rad)
        rz  Yaw                 (rad)
    """
    ...

def dict_diff(dold, dnew, indent=...): # -> str:
    """Helper to log what actually changed from old to new values of
    dictionaries.

    typical use -- log difference for hashed_inputs
    """
    ...

def rgetcwd(error=...): # -> str:
    """
    Robust replacement for getcwd when folders get removed
    If error==True, this is just an alias for os.getcwd()
    """
    ...
