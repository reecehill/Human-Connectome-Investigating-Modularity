"""
This type stub file was generated by pyright.
"""

from nilearn import _utils
from nilearn.maskers.base_masker import BaseMasker

"""
Transformer for computing ROI signals.
"""
class _ExtractionFunctor:
    func_name = ...
    def __init__(self, _resampled_labels_img_, background_label, strategy, mask_img) -> None:
        ...
    
    def __call__(self, imgs): # -> tuple[ndarray[Unknown, Unknown], list[Unknown]]:
        ...
    


@_utils.fill_doc
class NiftiLabelsMasker(BaseMasker, _utils.CacheMixin):
    """Class for masking of Niimg-like objects.

    NiftiLabelsMasker is useful when data from non-overlapping volumes should
    be extracted (contrarily to :class:`nilearn.maskers.NiftiMapsMasker`).
    Use case: Summarize brain signals from clusters that were obtained by prior
    K-means or Ward clustering.

    Parameters
    ----------
    labels_img : Niimg-like object
        See :ref:`extracting_data`.
        Region definitions, as one image of labels.

    labels : :obj:`list` of :obj:`str`, optional
        Full labels corresponding to the labels image. This is used
        to improve reporting quality if provided.
        Warning: The labels must be consistent with the label
        values provided through `labels_img`.

    background_label : :obj:`int` or :obj:`float`, optional
        Label used in labels_img to represent background.
        Warning: This value must be consistent with label values and
        image provided.
        Default=0.

    mask_img : Niimg-like object, optional
        See :ref:`extracting_data`.
        Mask to apply to regions before extracting signals.
    %(smoothing_fwhm)s
    standardize : {False, True, 'zscore', 'psc'}, optional
        Strategy to standardize the signal.
        'zscore': the signal is z-scored. Timeseries are shifted
        to zero mean and scaled to unit variance.
        'psc':  Timeseries are shifted to zero mean value and scaled
        to percent signal change (as compared to original mean signal).
        True : the signal is z-scored. Timeseries are shifted
        to zero mean and scaled to unit variance.
        False : Do not standardize the data.
        Default=False.

    standardize_confounds : :obj:`bool`, optional
        If standardize_confounds is True, the confounds are z-scored:
        their mean is put to 0 and their variance to 1 in the time dimension.
        Default=True.

    high_variance_confounds : :obj:`bool`, optional
        If True, high variance confounds are computed on provided image with
        :func:`nilearn.image.high_variance_confounds` and default parameters
        and regressed out. Default=False.

    detrend : :obj:`bool`, optional
        This parameter is passed to signal.clean. Please see the related
        documentation for details. Default=False.

    low_pass : None or :obj:`float`, optional
        This parameter is passed to signal.clean. Please see the related
        documentation for details

    high_pass : None or :obj:`float`, optional
        This parameter is passed to signal.clean. Please see the related
        documentation for details

    t_r : :obj:`float`, optional
        This parameter is passed to signal.clean. Please see the related
        documentation for details

    dtype : {dtype, "auto"}, optional
        Data type toward which the data should be converted. If "auto", the
        data will be converted to int32 if dtype is discrete and float32 if it
        is continuous.

    resampling_target : {"data", "labels", None}, optional
        Gives which image gives the final shape/size. For example, if
        `resampling_target` is "data", the atlas is resampled to the
        shape of the data if needed. If it is "labels" then mask_img
        and images provided to fit() are resampled to the shape and
        affine of maps_img. "None" means no resampling: if shapes and
        affines do not match, a ValueError is raised. Default="data".

    memory : :obj:`joblib.Memory` or :obj:`str`, optional
        Used to cache the region extraction process.
        By default, no caching is done. If a string is given, it is the
        path to the caching directory.

    memory_level : :obj:`int`, optional
        Aggressiveness of memory caching. The higher the number, the higher
        the number of functions that will be cached. Zero means no caching.
        Default=1.

    verbose : :obj:`int`, optional
        Indicate the level of verbosity. By default, nothing is printed
        Default=0.

    strategy : :obj:`str`, optional
        The name of a valid function to reduce the region with.
        Must be one of: sum, mean, median, minimum, maximum, variance,
        standard_deviation. Default='mean'.

    reports : :obj:`bool`, optional
        If set to True, data is saved in order to produce a report.
        Default=True.

    Attributes
    ----------
    mask_img_ : :obj:`nibabel.nifti1.Nifti1Image`
        The mask of the data, or the computed one.

    labels_img_ : :obj:`nibabel.nifti1.Nifti1Image`
        The labels image.

    n_elements_ : :obj:`int`
        The number of discrete values in the mask.
        This is equivalent to the number of unique values in the mask image,
        ignoring the background value.

        .. versionadded:: 0.9.2

    See also
    --------
    nilearn.maskers.NiftiMasker

    """
    def __init__(self, labels_img, labels=..., background_label=..., mask_img=..., smoothing_fwhm=..., standardize=..., standardize_confounds=..., high_variance_confounds=..., detrend=..., low_pass=..., high_pass=..., t_r=..., dtype=..., resampling_target=..., memory=..., memory_level=..., verbose=..., strategy=..., reports=...) -> None:
        ...
    
    def generate_report(self): # -> HTMLReport:
        ...
    
    def fit(self, imgs=..., y=...): # -> Self@NiftiLabelsMasker:
        """Prepare signal extraction from regions.

        All parameters are unused, they are for scikit-learn compatibility.

        """
        ...
    
    def fit_transform(self, imgs, confounds=..., sample_mask=...):
        """Prepare and perform signal extraction from regions.

        Parameters
        ----------
        imgs : 3D/4D Niimg-like object
            See :ref:`extracting_data`.
            Images to process.
            If a 3D niimg is provided, a singleton dimension will be added to
            the output to represent the single scan in the niimg.

        confounds : CSV file or array-like or :obj:`pandas.DataFrame`, optional
            This parameter is passed to signal.clean. Please see the related
            documentation for details.
            shape: (number of scans, number of confounds)

        sample_mask : Any type compatible with numpy-array indexing, optional
            shape: (number of scans - number of volumes removed, )
            Masks the niimgs along time/fourth dimension to perform scrubbing
            (remove volumes with high motion) and/or non-steady-state volumes.
            This parameter is passed to signal.clean.

                .. versionadded:: 0.8.0

        Returns
        -------
        region_signals : 2D :obj:`numpy.ndarray`
            Signal for each label.
            shape: (number of scans, number of labels)

        """
        ...
    
    def transform_single_imgs(self, imgs, confounds=..., sample_mask=...): # -> Any:
        """Extract signals from a single 4D niimg.

        Parameters
        ----------
        imgs : 3D/4D Niimg-like object
            See :ref:`extracting_data`.
            Images to process.
            If a 3D niimg is provided, a singleton dimension will be added to
            the output to represent the single scan in the niimg.

        confounds : CSV file or array-like or :obj:`pandas.DataFrame`, optional
            This parameter is passed to signal.clean. Please see the related
            documentation for details.
            shape: (number of scans, number of confounds)

        sample_mask : Any type compatible with numpy-array indexing, optional
            shape: (number of scans - number of volumes removed, )
            Masks the niimgs along time/fourth dimension to perform scrubbing
            (remove volumes with high motion) and/or non-steady-state volumes.
            This parameter is passed to signal.clean.

                .. versionadded:: 0.8.0

        Returns
        -------
        region_signals : 2D numpy.ndarray
            Signal for each label.
            shape: (number of scans, number of labels)

        Warns
        -----
        DeprecationWarning
            If a 3D niimg input is provided, the current behavior
            (adding a singleton dimension to produce a 2D array) is deprecated.
            Starting in version 0.12, a 1D array will be returned for 3D
            inputs.

        """
        ...
    
    def inverse_transform(self, signals): # -> Nifti1Image | FileBasedImage:
        """Compute voxel signals from region signals

        Any mask given at initialization is taken into account.

        .. versionchanged:: 0.9.2

            This method now supports 1D arrays, which will produce 3D images.

        Parameters
        ----------
        signals : 1D/2D :obj:`numpy.ndarray`
            Signal for each region.
            If a 1D array is provided, then the shape should be
            (number of elements,), and a 3D img will be returned.
            If a 2D array is provided, then the shape should be
            (number of scans, number of elements), and a 4D img will be
            returned.

        Returns
        -------
        img : :obj:`nibabel.nifti1.Nifti1Image`
            Signal for each voxel
            shape: (X, Y, Z, number of scans)

        """
        ...
    

