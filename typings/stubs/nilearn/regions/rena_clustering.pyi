"""
This type stub file was generated by pyright.
"""

from sklearn.base import BaseEstimator, ClusterMixin, TransformerMixin
from nilearn._utils import fill_doc

"""Recursive Neighbor Agglomeration (ReNA):
fastclustering for approximation of structured signals
"""
def recursive_neighbor_agglomeration(X, mask_img, n_clusters, n_iter=..., threshold=..., verbose=...): # -> tuple[Unknown, Any | Unknown]:
    """Recursive neighbor agglomeration (:term:`ReNA`): it performs
    iteratively the nearest neighbor grouping.
    See :footcite:`Hoyos2019`.

    Parameters
    ----------
    X : :class:`numpy.ndarray`
        Training data. shape = [n_samples, n_features]

    mask_img : Niimg-like object
        Object used for masking the data.

    n_clusters : :obj:`int`
        The number of clusters to find.

    n_iter : :obj:`int`, optional
        Number of iterations. Default=10.

    threshold : :obj:`float` in the close interval [0, 1], optional
        The threshold is set to handle eccentricities.
        Default=1e-7.

    verbose : :obj:`int`, optional
        Verbosity level. Default=0.

    Returns
    -------
    n_components : :obj:`int`
        Number of clusters.

    labels : :class:`numpy.ndarray`
        Cluster assignation. shape = [n_features]

    References
    ----------
    .. footbibliography::

    """
    ...

@fill_doc
class ReNA(BaseEstimator, ClusterMixin, TransformerMixin):
    """Recursive Neighbor Agglomeration (:term:`ReNA`):
    Recursively merges the pair of clusters according to 1-nearest neighbors
    criterion.
    See :footcite:`Hoyos2019`.

    Parameters
    ----------
    %(mask_img)s
    n_clusters : :obj:`int`, optional
        The number of clusters to find. Default=2.

    scaling : :obj:`bool`, optional
        If scaling is True, each cluster is scaled by the square root of its
        size, preserving the l2-norm of the image. Default=False.

    n_iter : :obj:`int`, optional
        Number of iterations of the recursive neighbor agglomeration.
        Default=10.

    threshold : :obj:`float` in the open interval (0., 1.), optional
        Threshold used to handle eccentricities.
        Default=1e-7.
    %(memory)s
    %(memory_level1)s
    %(verbose0)s

    Attributes
    ----------
    `labels_ ` : :class:`numpy.ndarray`, shape = [n_features]
        Cluster labels for each feature.

    `n_clusters_` : :obj:`int`
        Number of clusters.

    `sizes_` : :class:`numpy.ndarray`, shape = [n_features]
        It contains the size of each cluster.

    References
    ----------
    .. footbibliography::

    """
    def __init__(self, mask_img, n_clusters=..., scaling=..., n_iter=..., threshold=..., memory=..., memory_level=..., verbose=...) -> None:
        ...
    
    def fit(self, X, y=...): # -> Self@ReNA:
        """Compute clustering of the data.

        Parameters
        ----------
        X : :class:`numpy.ndarray`, shape = [n_samples, n_features]
            Training data.

        y : Ignored

        Returns
        -------
        self : `ReNA` object

        """
        ...
    
    def transform(self, X, y=...): # -> NDArray[bool_] | NDArray[Unknown]:
        """Apply clustering, reduce the dimensionality of the data.

        Parameters
        ----------
        X : :class:`numpy.ndarray`, shape = [n_samples, n_features]
            Data to transform with the fitted clustering.

        Returns
        -------
        X_red : :class:`numpy.ndarray`, shape = [n_samples, n_clusters]
            Data reduced with agglomerated signal for each cluster.

        """
        ...
    
    def inverse_transform(self, X_red):
        """Send the reduced 2D data matrix back to the original feature
        space (:term:`voxels<voxel>`).

        Parameters
        ----------
        X_red : :class:`numpy.ndarray`, shape = [n_samples, n_clusters]
            Data reduced with agglomerated signal for each cluster.

        Returns
        -------
        X_inv : :class:`numpy.ndarray`, shape = [n_samples, n_features]
            Data reduced expanded to the original feature space.

        """
        ...
    

