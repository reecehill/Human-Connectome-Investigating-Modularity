"""
This type stub file was generated by pyright.
"""

import os

"""
Backports of fixes for joblib dependencies
"""
class Version:
    """Backport from deprecated distutils

    We maintain this backport to avoid introducing a new dependency on
    `packaging`.

    We might rexplore this choice in the future if all major Python projects
    introduce a dependency on packaging anyway.
    """
    def __init__(self, vstring=...) -> None:
        ...
    
    def __repr__(self): # -> str:
        ...
    
    def __eq__(self, other) -> bool:
        ...
    
    def __lt__(self, other) -> bool:
        ...
    
    def __le__(self, other) -> bool:
        ...
    
    def __gt__(self, other) -> bool:
        ...
    
    def __ge__(self, other) -> bool:
        ...
    


class LooseVersion(Version):
    """Backport from deprecated distutils

    We maintain this backport to avoid introducing a new dependency on
    `packaging`.

    We might rexplore this choice in the future if all major Python projects
    introduce a dependency on packaging anyway.
    """
    component_re = ...
    def __init__(self, vstring=...) -> None:
        ...
    
    def parse(self, vstring): # -> None:
        ...
    
    def __str__(self) -> str:
        ...
    
    def __repr__(self): # -> str:
        ...
    


def make_memmap(filename, dtype=..., mode=..., offset=..., shape=..., order=..., unlink_on_gc_collect=...): # -> memmap[Unknown, Unknown]:
    """Custom memmap constructor compatible with numpy.memmap.

        This function:
        - is a backport the numpy memmap offset fix (See
          https://github.com/numpy/numpy/pull/8443 for more details.
          The numpy fix is available starting numpy 1.13)
        - adds ``unlink_on_gc_collect``, which specifies  explicitly whether
          the process re-constructing the memmap owns a reference to the
          underlying file. If set to True, it adds a finalizer to the
          newly-created memmap that sends a maybe_unlink request for the
          memmaped file to resource_tracker.
        """
    ...

if os.name == 'nt':
    access_denied_errors = ...
    def concurrency_safe_rename(src, dst): # -> None:
        """Renames ``src`` into ``dst`` overwriting ``dst`` if it exists.

        On Windows os.replace can yield permission errors if executed by two
        different processes.
        """
        ...
    
else:
    ...