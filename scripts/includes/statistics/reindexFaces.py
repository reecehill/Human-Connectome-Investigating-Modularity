from typing import Any, Tuple
import h5py
import pandas as pd
import numpy as np
import scipy.sparse as sp
from scipy.sparse.csgraph import reverse_cuthill_mckee  # type: ignore
import config


def reindexFacesToEnsureAdjacency(
    x: "pd.Series[Any]", y: "pd.Series[Any]", centroid_coords: "pd.DataFrame"
) -> "Tuple[pd.Series[Any],pd.Series[Any],pd.DataFrame]":
    if config.CURRENT_HEMISPHERE == "left":
        originalIndicesFile = "lh.L_precentral_L_faceIds.csv"
    elif config.CURRENT_HEMISPHERE == "right":
        originalIndicesFile = "rh.R_precentral_R_faceIds.csv"
    else:
        raise ValueError(f"Invalid hemisphere: {config.CURRENT_HEMISPHERE}")

    original_indices = pd.read_csv(
        config.SUBJECT_DIR / "exported_modules" / originalIndicesFile,
        header=None,
    ).T[0]

    mat_file_path = config.SUBJECT_DIR / "edgeList.mat"
    with h5py.File(mat_file_path, "r") as f:  # type: ignore
        edge_list_local = f["edgeListLocal"][:]

    # Transpose to get (m-by-2) format
    edge_list_df = pd.DataFrame(
        edge_list_local.T, columns=["Face_ID", "Connected_Face_ID"]
    )
    del edge_list_local

    # Step 1: Sort faces by Z-Coordinate
    sorted_face_indices = np.lexsort(
        [
            centroid_coords.iloc[1, :],
            centroid_coords.iloc[0, :],
            centroid_coords.iloc[2, :],
        ]
    )  # Sorting by Z-coordinate

    x_sorted = x.iloc[sorted_face_indices].reset_index(drop=True)
    y_sorted = y.iloc[sorted_face_indices].reset_index(drop=True)
    centroids_sorted = centroid_coords.iloc[:,sorted_face_indices].reset_index(drop=True)

    # Step 3: Compute adjacency-preserving order using RCM
    face_id_to_index = {face: i for i, face in enumerate(original_indices)}
    # index_to_face_id = {i: face for face, i in face_id_to_index.items()}

    # Step 2: Ensure edges are correctly mapped
    edge_list_mapped = edge_list_df[
        edge_list_df["Face_ID"].isin(original_indices)
        & edge_list_df["Connected_Face_ID"].isin(original_indices)
    ].copy()

    # Step 3: Replace the original Face_IDs with new indexed ones
    edge_list_mapped["Face_ID"] = edge_list_mapped["Face_ID"].map(face_id_to_index)
    edge_list_mapped["Connected_Face_ID"] = edge_list_mapped["Connected_Face_ID"].map(
        face_id_to_index
    )

    # Step 4: Convert to adjacency matrix
    edges_mapped = edge_list_mapped.to_numpy()
    num_faces = len(original_indices)  # Should be 3892

    # Ensure no out-of-bounds indexing
    assert edges_mapped.max() < num_faces, "Mapped indices exceed allowed range!"

    # Step 5: Construct Sparse Matrix
    adj_matrix = sp.csr_matrix(
        (np.ones(len(edges_mapped)), (edges_mapped[:, 0], edges_mapped[:, 1])),
        shape=(num_faces, num_faces),
    )

    # Compute the new adjacency-preserving order
    new_order = reverse_cuthill_mckee(adj_matrix, True)

    # Reorder x based on these new indices
    x_reordered: pd.Series[Any] = x_sorted[np.argsort(new_order)].reset_index(drop=True)
    y_reordered: pd.Series[Any] = y_sorted[np.argsort(new_order)].reset_index(drop=True)
    centroids_reordered: pd.DataFrame = centroids_sorted.T.iloc[new_order].T.reset_index(drop=True)

    # Update the attributes of the reindexed series with the attributes of the original series
    for xory in [x_reordered, y_reordered]:
        xory.attrs.update(
            {
                "dataset_descriptors": {
                    **xory.attrs.get("dataset_descriptors", {}),
                },
                "applied_handlers": xory.attrs["applied_handlers"]
                + [
                    {
                        "name": "reindexedFaces",
                        "metadata": {"mapping": new_order},
                    }
                ],
            }
        )
    return x_reordered, y_reordered, centroids_reordered
