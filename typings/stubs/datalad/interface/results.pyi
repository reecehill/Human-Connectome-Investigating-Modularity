"""
This type stub file was generated by pyright.
"""

"""Interface result handling functions

"""
__docformat__ = ...
lgr = ...
success_status_map = ...
def get_status_dict(action=..., ds=..., path=..., type=..., logger=..., refds=..., status=..., message=..., **kwargs): # -> dict[Unknown, Unknown]:
    """Helper to create a result dictionary.

    Most arguments match their key in the resulting dict. Only exceptions are
    listed here.

    Parameters
    ----------
    ds : Dataset instance
      If given, the `path` and `type` values are populated with the path of the
      datasets and 'dataset' as the type. Giving additional values for both
      keys will overwrite these pre-populated values.

    Returns
    -------
    dict
    """
    ...

def results_from_paths(paths, action=..., type=..., logger=..., refds=..., status=..., message=...): # -> Generator[dict[Unknown, Unknown], None, None]:
    """
    Helper to yield analog result dicts for each path in a sequence.

    Parameters
    ----------
    message: str
      A result message. May contain `%s` which will be replaced by the
      respective `path`.

    Returns
    -------
    generator

    """
    ...

def is_ok_dataset(r):
    """Convenience test for a non-failure dataset-related result dict"""
    ...

class ResultXFM:
    """Abstract definition of the result transformer API"""
    def __call__(self, res):
        """This is called with one result dict at a time"""
        ...
    


class YieldDatasets(ResultXFM):
    """Result transformer to return a Dataset instance from matching result.

    If the `success_only` flag is given only dataset with 'ok' or 'notneeded'
    status are returned'.

    `None` is returned for any other result.
    """
    def __init__(self, success_only=...) -> None:
        ...
    
    def __call__(self, res): # -> Dataset | None:
        ...
    


class YieldRelativePaths(ResultXFM):
    """Result transformer to return relative paths for a result

    Relative paths are determined from the 'refds' value in the result. If
    no such value is found, `None` is returned.
    """
    def __call__(self, res): # -> None:
        ...
    


class YieldField(ResultXFM):
    """Result transformer to return an arbitrary value from a result dict"""
    def __init__(self, field) -> None:
        """
        Parameters
        ----------
        field : str
          Key of the field to return.
        """
        ...
    
    def __call__(self, res): # -> None:
        ...
    


known_result_xfms = ...
translate_annex_notes = ...
def annexjson2result(d, ds, **kwargs): # -> dict[Unknown, Unknown]:
    """Helper to convert an annex JSON result to a datalad result dict

    Info from annex is rather heterogenous, partly because some of it
    our support functions are faking.

    This helper should be extended with all needed special cases to
    homogenize the information.

    Parameters
    ----------
    d : dict
      Annex info dict.
    ds : Dataset instance
      Used to determine absolute paths for `file` results. This dataset
      is not used to set `refds` in the result, pass this as a separate
      kwarg if needed.
    **kwargs
      Passes as-is to `get_status_dict`. Must not contain `refds`.
    """
    ...

def count_results(res, **kwargs): # -> int:
    """Return number if results that match all property values in kwargs"""
    ...

def only_matching_paths(res, **kwargs): # -> bool:
    ...

@staticmethod
def is_result_matching_pathsource_argument(res, **kwargs): # -> bool:
    ...

def results_from_annex_noinfo(ds, requested_paths, respath_by_status, dir_fail_msg, noinfo_dir_msg, noinfo_file_msg, noinfo_status=..., **kwargs): # -> Generator[dict[Unknown, Unknown], None, None]:
    """Helper to yield results based on what information git annex did no give us.

    The helper assumes that the annex command returned without an error code,
    and interprets which of the requested paths we have heard nothing about,
    and assumes that git annex was happy with their current state.

    Parameters
    ==========
    ds : Dataset
      All results have to be concerning this single dataset (used to resolve
      relpaths).
    requested_paths : list
      List of path arguments sent to `git annex`
    respath_by_status : dict
      Mapping of 'success' or 'failure' labels to lists of result paths
      reported by `git annex`. Everything that is not in here, we assume
      that `git annex` was happy about.
    dir_fail_msg : str
      Message template to inject into the result for a requested directory where
      a failure was reported for some of its content. The template contains two
      string placeholders that will be expanded with 1) the path of the
      directory, and 2) the content failure paths for that directory
    noinfo_dir_msg : str
      Message template to inject into the result for a requested directory that
      `git annex` was silent about (incl. any content). There must be one string
      placeholder that is expanded with the path of that directory.
    noinfo_file_msg : str
      Message to inject into the result for a requested file that `git
      annex` was silent about.
    noinfo_status : str
      Status to report when annex provides no information
    **kwargs
      Any further kwargs are included in the yielded result dictionary.
    """
    ...
