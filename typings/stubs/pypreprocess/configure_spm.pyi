"""
This type stub file was generated by pyright.
"""

"""
Automatic configuration of MATLAB/SPM back-end
"""
def prepare_logging(log_stream=..., log_file=...): # -> Logger:
    """ Define the logger handlers.

    Parameters
    ----------
    log_stream: bool, default True
        if True create a stream INFO handler.
    log_file: str, default './configure_spm.log'
        if specified create a file DEBUG handler, if None don't create such
        handler.
    """
    ...

_logger = ...
_ACCEPT_SPM_MCR_WITH_UNKNOWN_VERSION = ...
_ACCEPT_SPM_MCR_WITH_AMBIGUOUS_VERSION = ...
_SPM_DEFAULTS = ...
class _IsValidMCR:
    """used to validate path to SPM MCR and capture path to matching SPM dir.

    meant to be used as the 'check' argument of _find_dep_loc.
    """
    def __init__(self, cli_spm_dir, config_spm_dir, defaults) -> None:
        """
        specify the locations in which a matching SPM dir will be seeked.

        Parameters
        ----------
        cli_spm_dir: str
        first location tried when looking for SPM dir.
        (supposed to have been specified from the command line)

        config_spm_dir: str
        next location to be tried.
        (supposed to have been specified in a config file)

        defaults: dict
        mapping of relevant environment variables and default locations
        in which to look if cli and config fail. Must provide the same semantics
        as configure_spm._SPM_DEFAULTS. (but not necessarily every key present
        in it: if some of the keys provided in _SPM_DEFAULTS are missing from
        defaults, they will simply not be used). see documentation for
        _get_defaults for more details.

        Returns
        -------
        None

        """
        ...
    
    def __call__(self, spm_mcr): # -> bool:
        """check that path points to SPM MCR and a matching SPM dir exists

        first, check that path points to an executable file and if it does,
        look for an SPM directory with matching version. If one is found,
        remember it in self.found_spm_dir_.

        Parameters
        ----------
        spm_mcr: path to (supposed) SPM MCR to be examined.

        Returns
        -------
        True
        if path points to an MCR and an SPM home directory with
        matching version number was found (it can then be looked up
        in self.found_spm_dir_).
        False
        otherwise.

        """
        ...
    

