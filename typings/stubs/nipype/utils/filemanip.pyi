"""
This type stub file was generated by pyright.
"""

import contextlib

"""Miscellaneous file manipulation functions
"""
fmlogger = ...
related_filetype_sets = ...
def path_resolve(path, strict=...):
    ...

def split_filename(fname): # -> tuple[Unknown, Unknown, Unknown]:
    """Split a filename into parts: path, base filename and extension.

    Parameters
    ----------
    fname : str
        file or path name

    Returns
    -------
    pth : str
        base path from fname
    fname : str
        filename from fname, without extension
    ext : str
        file extension from fname

    Examples
    --------
    >>> from nipype.utils.filemanip import split_filename
    >>> pth, fname, ext = split_filename('/home/data/subject.nii.gz')
    >>> pth
    '/home/data'

    >>> fname
    'subject'

    >>> ext
    '.nii.gz'

    """
    ...

def fname_presuffix(fname, prefix=..., suffix=..., newpath=..., use_ext=...):
    """Manipulates path and name of input filename

    Parameters
    ----------
    fname : string
        A filename (may or may not include path)
    prefix : string
        Characters to prepend to the filename
    suffix : string
        Characters to append to the filename
    newpath : string
        Path to replace the path of the input fname
    use_ext : boolean
        If True (default), appends the extension of the original file
        to the output name.

    Returns
    -------
    Absolute path of the modified filename

    >>> from nipype.utils.filemanip import fname_presuffix
    >>> fname = 'foo.nii.gz'
    >>> fname_presuffix(fname,'pre','post','/tmp')
    '/tmp/prefoopost.nii.gz'

    >>> from nipype.interfaces.base import Undefined
    >>> fname_presuffix(fname, 'pre', 'post', Undefined) == \
            fname_presuffix(fname, 'pre', 'post')
    True

    """
    ...

def fnames_presuffix(fnames, prefix=..., suffix=..., newpath=..., use_ext=...): # -> list[Unknown]:
    """Calls fname_presuffix for a list of files."""
    ...

def hash_rename(filename, hashvalue): # -> str:
    """renames a file given original filename and hash
    and sets path to output_directory
    """
    ...

def check_forhash(filename): # -> tuple[Literal[True], list[Any]] | tuple[Literal[False], None]:
    """checks if file has a hash in its filename"""
    ...

def hash_infile(afile, chunk_len=..., crypto=..., raise_notfound=...): # -> str | None:
    """
    Computes hash of a file using 'crypto' module

    >>> hash_infile('smri_ants_registration_settings.json')
    'f225785dfb0db9032aa5a0e4f2c730ad'

    >>> hash_infile('surf01.vtk')
    'fdf1cf359b4e346034372cdeb58f9a88'

    >>> hash_infile('spminfo')
    '0dc55e3888c98a182dab179b976dfffc'

    >>> hash_infile('fsl_motion_outliers_fd.txt')
    'defd1812c22405b1ee4431aac5bbdd73'


    """
    ...

def hash_timestamp(afile): # -> str | None:
    """Computes md5 hash of the timestamp of a file"""
    ...

_cifs_table = ...
def on_cifs(fname): # -> bool | Any:
    """
    Checks whether a file path is on a CIFS filesystem mounted in a POSIX
    host (i.e., has the ``mount`` command).

    On Windows, Docker mounts host directories into containers through CIFS
    shares, which has support for Minshall+French symlinks, or text files that
    the CIFS driver exposes to the OS as symlinks.
    We have found that under concurrent access to the filesystem, this feature
    can result in failures to create or read recently-created symlinks,
    leading to inconsistent behavior and ``FileNotFoundError``.

    This check is written to support disabling symlinks on CIFS shares.

    """
    ...

def copyfile(originalfile, newfile, copy=..., create_new=..., hashmethod=..., use_hardlink=..., copy_related_files=...):
    """Copy or link ``originalfile`` to ``newfile``.

    If ``use_hardlink`` is True, and the file can be hard-linked, then a
    link is created, instead of copying the file.

    If a hard link is not created and ``copy`` is False, then a symbolic
    link is created.

    Parameters
    ----------
    originalfile : str
        full path to original file
    newfile : str
        full path to new file
    copy : Bool
        specifies whether to copy or symlink files
        (default=False) but only for POSIX systems
    use_hardlink : Bool
        specifies whether to hard-link files, when able
        (Default=False), taking precedence over copy
    copy_related_files : Bool
        specifies whether to also operate on related files, as defined in
        ``related_filetype_sets``

    Returns
    -------
    None

    """
    ...

def get_related_files(filename, include_this_file=...): # -> list[Unknown]:
    """Returns a list of related files, as defined in
    ``related_filetype_sets``, for a filename. (e.g., Nifti-Pair, Analyze (SPM)
    and AFNI files).

    Parameters
    ----------
    filename : str
        File name to find related filetypes of.
    include_this_file : bool
        If true, output includes the input filename.
    """
    ...

def copyfiles(filelist, dest, copy=..., create_new=...): # -> list[Unknown]:
    """Copy or symlink files in ``filelist`` to ``dest`` directory.

    Parameters
    ----------
    filelist : list
        List of files to copy.
    dest : path/files
        full path to destination. If it is a list of length greater
        than 1, then it assumes that these are the names of the new
        files.
    copy : Bool
        specifies whether to copy or symlink files
        (default=False) but only for posix systems

    Returns
    -------
    None

    """
    ...

def ensure_list(filename): # -> list[str | bytes] | list[Unknown] | None:
    """Returns a list given either a string or a list"""
    ...

def simplify_list(filelist):
    """Returns a list if filelist is a list of length greater than 1,
    otherwise returns the first element
    """
    ...

filename_to_list = ...
list_to_filename = ...
def check_depends(targets, dependencies): # -> Literal[False]:
    """Return true if all targets exist and are newer than all dependencies.

    An OSError will be raised if there are missing dependencies.
    """
    ...

def save_json(filename, data): # -> None:
    """Save data to a json file

    Parameters
    ----------
    filename : str
        Filename to save data in.
    data : dict
        Dictionary to save in json file.

    """
    ...

def load_json(filename): # -> Any:
    """Load data from a json file

    Parameters
    ----------
    filename : str
        Filename to load data from.

    Returns
    -------
    data : dict

    """
    ...

def loadcrash(infile, *args): # -> Any:
    ...

def loadpkl(infile): # -> Any:
    """Load a zipped or plain cPickled file."""
    ...

def crash2txt(filename, record): # -> None:
    """Write out plain text crash file"""
    ...

def read_stream(stream, logger=..., encoding=...):
    """
    Robustly reads a stream, sending a warning to a logger
    if some decoding error was raised.

    >>> read_stream(bytearray([65, 0xc7, 65, 10, 66]))  # doctest: +ELLIPSIS
    ['A...A', 'B']


    """
    ...

def savepkl(filename, record, versioning=...): # -> None:
    ...

rst_levels = ...
def write_rst_header(header, level=...): # -> str:
    ...

def write_rst_list(items, prefix=...): # -> LiteralString:
    ...

def write_rst_dict(info, prefix=...): # -> LiteralString:
    ...

def dist_is_editable(dist): # -> bool:
    """Is distribution an editable install?

    Parameters
    ----------
    dist : string
        Package name

    # Borrowed from `pip`'s' API
    """
    ...

def emptydirs(path, noexist_ok=...): # -> Literal[True] | None:
    """
    Empty an existing directory, without deleting it. Do not
    raise error if the path does not exist and noexist_ok is True.

    Parameters
    ----------
    path : directory that should be empty

    """
    ...

def silentrm(filename): # -> bool:
    """
    Equivalent to ``rm -f``, returns ``False`` if the file did not
    exist.

    Parameters
    ----------

    filename : str
        file to be deleted

    """
    ...

def which(cmd, env=..., pathext=...): # -> None:
    """
    Return the path to an executable which would be run if the given
    cmd was called. If no cmd would be called, return ``None``.

    Code for Python < 3.3 is based on a code snippet from
    http://orip.org/2009/08/python-checking-if-executable-exists-in.html

    """
    ...

def get_dependencies(name, environ): # -> str | bytes:
    """Return library dependencies of a dynamically linked executable

    Uses otool on darwin, ldd on linux. Currently doesn't support windows.

    """
    ...

def canonicalize_env(env):
    """Windows requires that environment be dicts with str as keys and values
    This function converts any unicode entries for Windows only, returning the
    dictionary untouched in other environments.

    Parameters
    ----------
    env : dict
        environment dictionary with unicode or bytes keys and values

    Returns
    -------
    env : dict
        Windows: environment dictionary with str keys and values
        Other: untouched input ``env``
    """
    ...

def relpath(path, start=...): # -> str:
    """Return a relative version of a path"""
    ...

@contextlib.contextmanager
def indirectory(path): # -> Generator[None, None, None]:
    ...
