"""
This type stub file was generated by pyright.
"""

"""
:Module: spm_realign
:Synopsis: MRI within-modality Motion Correction, SPM style
:Author: DOHMATOB Elvis Dopgima

"""
INFINITY = ...
class MRIMotionCorrection:
    """
    Implements within-modality multi-session rigid-body registration of MRI
    volumes.

    The fit(...) method  estimates affine transformations necessary to
    rigidly align the other volumes to the first volume (hereafter referred
    to as the reference), whilst the transform(...) method actually writes
    these realigned files unto disk, optionally reslicing them.

    Paremeters
    ----------
    quality: float, optional (default .9)
        quality versus speed trade-off.  Highest quality (1) gives most
        precise results, whereas lower qualities gives faster realignment.
        The idea is that some voxels contribute little to the estimation
        of the realignment parameters. This parameter is involved in
        selecting the number of voxels that are used.

    tol: float, optional (defaul 1e-8)
        tolerance for Gauss-Newton LS iterations

    fwhm: float, optional (default 10)
        the FWHM of the Gaussian smoothing kernel (mm) applied to the
        images before estimating the realignment parameters.

    sep: intx, optional (default 4)
        the default separation (mm) to sample the images

    interp: int, optional (default 3)
        B-spline degree used for interpolation

    lkp: arry_like of ints, optional (default [0, 1, 2, 3, 4, 5])
        affine transformation parameters sought-for. Possible values of
        elements of the list are:
        0  - x translation
        1  - y translation
        2  - z translation
        3  - x rotation about - {pitch} (radians)
        4  - y rotation about - {roll}  (radians)
        5  - z rotation about - {yaw}   (radians)
        6  - x scaling
        7  - y scaling
        8  - z scaling
        9  - x shear
        10 - y shear
        11 - z shear

    verbose: int, optional (default 1)
        controls verbosity level. 0 means no verbose at all

    n_iterations: int, optional (dafault 64)
        max number of Gauss-Newton iterations when solving LSP for
        registering a volume to the reference

    smooth_func: function, optional (default pypreprocess' smooth_image)
        the smoothing function to apply during estimation. The given function
        must accept 2 positional args (vol, fwhm)

    Attributes
    ----------
    realignment_parameters_: 3D array of shape (n_sessions, n_scans_session, 6)
        the realigment parameters for each volume of each session

    References
    ----------
    [1] Rigid Body Registration, by J. Ashburner and K. Friston

    """
    def __init__(self, sep=..., interp=..., fwhm=..., quality=..., tol=..., lkp=..., verbose=..., n_iterations=..., n_sessions=..., smooth_func=...) -> None:
        ...
    
    def __repr__(self): # -> str:
        ...
    
    def fit(self, vols, n_jobs=...): # -> Self@MRIMotionCorrection:
        """Estimation of within-modality rigid-body movement parameters.

        All operations are performed relative to the first image. That is,
        registration is to the first image, and resampling of images is
        into the space of the first image.

        The algorithm is a Gauss-Netwon iterative refinememnt of an l2 loss
        (squared difference between images)

        Parameters
        ----------
        vols: list of lists
            list of single 4D images or nibabel image objects
            (one per session), or list of lists of filenames or nibabel image
            objects (one list per session)

        n_jobs: int
            number of parallel jobs

        Returns
        -------
        `MRIMotionCorrection` instance
            fitted object

        Raises
        ------
        RuntimeError, ValueError

        """
        ...
    
    def transform(self, output_dir=..., reslice=..., prefix=..., basenames=..., ext=..., concat=...): # -> dict[str, list[Unknown]]:
        """
        Saves realigned volumes and the realigment parameters to disk.
        Realigment parameters are stored in output_dir/rp.txt and Volumes
        are saved in output_dir/prefix_vol.ext where and t is the scan
        number of the corresponding (3D) volume.

        Parameters
        ----------
        reslice: bool, optional (default False)
            reslice the realigned volumes

        output_dir: string, optional (dafault None)
            existing dirname where output will be written

        prefix: string, optional (default 'r')
            prefix for output filenames.

        ext: string, optional (default ".nii.gz")
            file extension for ouput images; can be ".img", ".nii", or
            ".nii.gz"

        concat: boolean, optional (default False)
            concatenate the ouput volumes for each session into a single
            4D film

        Returns
        -------
        output: dict
            output dict. items are:
            rvols: list of `nibabel.Nifti1Image` objects
                list of realigned 3D vols

            And if output_dir is not None, output will also have the
            following items:
            realigned_images: list of strings
                full paths of the realigned files

            realignment_parameters_: string
                full patsh of text file containing realignment parameters
        """
        ...
    

