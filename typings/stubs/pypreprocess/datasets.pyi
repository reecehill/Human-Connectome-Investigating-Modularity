"""
This type stub file was generated by pyright.
"""

SPM_AUDITORY_DATA_FILES = ...
FSL_FEEDS_DATA_FILES = ...
def fetch_spm_auditory(data_dir=..., data_name=..., subject_id=..., verbose=...): # -> Bunch | None:
    """Function to fetch SPM auditory single-subject data.

    Parameters
    ----------
    data_dir: string
        path of the data directory. Used to force data storage in a specified
        location. If the data is already present there, then will simply
        glob it.

    Returns
    -------
    data: sklearn.utils.Bunch
        Dictionary-like object, the interest attributes are:
        - 'func': string list. Paths to functional images
        - 'anat': string list. Path to anat image

    References
    ----------
    :download:
        http://www.fil.ion.ucl.ac.uk/spm/data/auditory/

    """
    ...

def fetch_fsl_feeds(data_dir=..., data_name=..., verbose=...): # -> Bunch | None:
    """Function to fetch FSL FEEDS dataset (single-subject)

    Parameters
    ----------
    data_dir: string
        path of the data directory. Used to force data storage in a specified
        location. If the data is already present there, then will simply
        glob it.

    Returns
    -------
    data: sklearn.utils.Bunch
        Dictionary-like object, the interest attributes are:
        - 'func': string list. Paths to functional images
        - 'anat': string list. Path to anat image

    """
    ...

def fetch_spm_multimodal_fmri(data_dir=..., data_name=..., subject_id=..., verbose=...): # -> Bunch | None:
    """Fetcher for Multi-modal Face Dataset.

    Parameters
    ----------
    data_dir: string
        path of the data directory. Used to force data storage in a specified
        location. If the data is already present there, then will simply
        glob it.

    Returns
    -------
    data: sklearn.utils.Bunch
        Dictionary-like object, the interest attributes are:
        - 'func1': string list. Paths to functional images for session 1
        - 'func2': string list. Paths to functional images for session 2
        - 'trials_ses1': string list. Path to onsets file for session 1
        - 'trials_ses2': string list. Path to onsets file for session 2
        - 'anat': string. Path to anat file

    References
    ----------
    :download:
        http://www.fil.ion.ucl.ac.uk/spm/data/mmfaces/

    """
    ...

def fetch_openfmri(data_dir, dataset_id, force_download=..., verbose=...):
    ...
