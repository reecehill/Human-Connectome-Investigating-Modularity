"""
This type stub file was generated by pyright.
"""

"""Utilities for probabilistic error control at voxel- and
cluster-level in brain imaging: cluster-level thresholding, false
discovery rate control, false discovery proportion in clusters.

Author: Bertrand Thirion, 2015 -- 2019

"""
def fdr_threshold(z_vals, alpha): # -> Any | float:
    """Return the Benjamini-Hochberg FDR threshold for the input z_vals

    Parameters
    ----------
    z_vals : array
        A set of z-variates from which the FDR is computed.

    alpha : float
        The desired FDR control.

    Returns
    -------
    threshold : float
        FDR-controling threshold from the Benjamini-Hochberg procedure.

    """
    ...

def cluster_level_inference(stat_img, mask_img=..., threshold=..., alpha=..., verbose=...): # -> Any | None:
    """ Report the proportion of active voxels for all clusters
    defined by the input threshold.

    This implements the method described in :footcite:`Rosenblatt2018`.

    Parameters
    ----------
    stat_img : Niimg-like object or None, optional
       statistical image (presumably in z scale)

    mask_img : Niimg-like object, optional,
        mask image

    threshold : list of floats, optional
       Cluster-forming threshold in z-scale. Default=3.0.

    alpha : float or list, optional
        Level of control on the true positive rate, aka true dsicovery
        proportion. Default=0.05.

    verbose : bool, optional
        Verbosity mode. Default=False.

    Returns
    -------
    proportion_true_discoveries_img : Nifti1Image
        The statistical map that gives the true positive.

    References
    ----------
    .. footbibliography::

    """
    ...

def threshold_stats_img(stat_img=..., mask_img=..., alpha=..., threshold=..., height_control=..., cluster_threshold=..., two_sided=...): # -> tuple[None, ndarray[Any, dtype[Any]] | float] | tuple[Nifti1Image | FileBasedImage | Unknown, Any | float | ndarray[Any, dtype[Any]]]:
    """ Compute the required threshold level and return the thresholded map

    Parameters
    ----------
    stat_img : Niimg-like object or None, optional
       Statistical image (presumably in z scale) whenever height_control
       is 'fpr' or None, stat_img=None is acceptable.
       If it is 'fdr' or 'bonferroni', an error is raised if stat_img is None.

    mask_img : Niimg-like object, optional,
        Mask image

    alpha : float or list, optional
        Number controlling the thresholding (either a p-value or q-value).
        Its actual meaning depends on the height_control parameter.
        This function translates alpha to a z-scale threshold.
        Default=0.001.

    threshold : float, optional
       Desired threshold in z-scale.
       This is used only if height_control is None. Default=3.0.

    height_control : string, or None optional
        False positive control meaning of cluster forming
        threshold: None|'fpr'|'fdr'|'bonferroni'
        Default='fpr'.

    cluster_threshold : float, optional
        cluster size threshold. In the returned thresholded map,
        sets of connected voxels (`clusters`) with size smaller
        than this number will be removed. Default=0.

    two_sided : Bool, optional
        Whether the thresholding should yield both positive and negative
        part of the maps.
        In that case, alpha is corrected by a factor of 2.
        Default=True.

    Returns
    -------
    thresholded_map : Nifti1Image,
        The stat_map thresholded at the prescribed voxel- and cluster-level.

    threshold : float
        The voxel-level threshold used actually.

    Notes
    -----
    If the input image is not z-scaled (i.e. some z-transformed statistic)
    the computed threshold is not rigorous and likely meaningless

    See also
    --------
    nilearn.image.threshold_img :
        Apply an explicit voxel-level (and optionally cluster-level) threshold
        without correction.

    """
    ...
