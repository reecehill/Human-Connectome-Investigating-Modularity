"""
This type stub file was generated by pyright.
"""

"""Progress bar implementations to be used.

Should not be imported until we know that interface needs it
"""
class ProgressBarBase:
    """Base class for any progress bar"""
    def __init__(self, label=..., fill_text=..., total=..., out=..., unit=..., initial=...) -> None:
        ...
    
    def refresh(self): # -> None:
        """Force update"""
        ...
    
    def update(self, size, increment=...): # -> None:
        ...
    
    @property
    def current(self): # -> int:
        ...
    
    @current.setter
    def current(self, value): # -> None:
        ...
    
    def start(self, initial=...): # -> None:
        ...
    
    def finish(self, partial=...): # -> None:
        """

        Parameters
        ----------
        partial: bool
          To signal that finish is called possibly before the activity properly
          finished, so .total count might have not been reached

        Returns
        -------

        """
        ...
    
    def clear(self): # -> None:
        ...
    
    def set_desc(self, value): # -> None:
        ...
    


class SilentProgressBar(ProgressBarBase):
    def __init__(self, label=..., fill_text=..., total=..., unit=..., out=...) -> None:
        ...
    


class LogProgressBar(ProgressBarBase):
    """A progress bar which logs upon completion of the item

    Note that there is also :func:`~datalad.log.log_progress` which can be used
    to get progress bars when attached to a tty but incremental log messages
    otherwise (as opposed to just the final log message provided by
    `LogProgressBar`).
    """
    def __init__(self, *args, **kwargs) -> None:
        ...
    
    def finish(self, partial=...): # -> None:
        ...
    


progressbars = ...
class tqdmProgressBar(ProgressBarBase):
    """Adapter for tqdm.ProgressBar"""
    backend = ...
    _frontends = ...
    _default_pbar_params = ...
    def __init__(self, label=..., fill_text=..., total=..., unit=..., out=..., leave=..., frontend=...) -> None:
        """

            Parameters
            ----------
            label
            fill_text
            total
            unit
            out
            leave
            frontend: (None, 'ipython'), optional
              tqdm module to use.  Could be tqdm_notebook if under IPython
            """
        ...
    
    def update(self, size, increment=...): # -> None:
        ...
    
    def start(self): # -> None:
        ...
    
    def refresh(self): # -> None:
        ...
    
    def finish(self, clear=..., partial=...): # -> None:
        """

            Parameters
            ----------
            clear : bool, optional
              Explicitly clear the progress bar. Note that we are
              creating them with leave=False so they should disappear on their
              own and explicit clear call should not be necessary

            Returns
            -------

            """
        ...
    
    def clear(self): # -> None:
        ...
    
    def set_desc(self, value): # -> None:
        ...
    


class AnnexSpecialRemoteProgressBar(ProgressBarBase):
    """Hook up to the special remote and report progress back to annex"""
    def __init__(self, *args, **kwargs) -> None:
        ...
    
    def update(self, *args, **kwargs): # -> None:
        ...
    

