# Reload the necessary libraries after execution state reset
import h5py
from pathlib import Path
import pandas as pd
import numpy as np
import scipy.sparse as sp
from scipy.sparse.csgraph import reverse_cuthill_mckee  # type: ignore
import networkx as nx
from scipy.sparse import coo_matrix, csr_matrix
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

originalIndicesFile = "lh.L_precentral_L_faceIds.csv"
original_indices = pd.read_csv(
    Path("./data/subjects/100408/exported_modules") / originalIndicesFile,
    header=None,
).T[0]


pathToXCsv = Path("./data/subjects/100408/exported_modules/left_structural_modules.csv")
x_raw: pd.DataFrame = pd.read_csv(
    pathToXCsv.absolute().__str__(), sep=",", header=None, keep_default_na=True
).T
x = x_raw[0]

pathToCentroids = Path("./data/subjects/100408/left_centroidCoordinatesByROIId.csv")
centroids_raw: pd.DataFrame = pd.read_csv(
    pathToCentroids.absolute().__str__(), sep=",", header=None, keep_default_na=True
)
centroids = centroids_raw
# Load the MATLAB v7.3 (HDF5) file again

mat_file_path = "./data/subjects/100408/edgeList.mat"
with h5py.File(mat_file_path, "r") as f:  # type: ignore
    edge_list_local = f["edgeListLocal"][:]

# Transpose to get (m-by-2) format
edge_list_df = pd.DataFrame(edge_list_local.T, columns=["Face_ID", "Connected_Face_ID"])
# Ensure face indices are mapped to a compact 0-based index
edge_list_df["Face_ID"], face_id_unique = pd.factorize(edge_list_df["Face_ID"])
edge_list_df["Connected_Face_ID"] = pd.Categorical(
    edge_list_df["Connected_Face_ID"], categories=face_id_unique
).codes

# Step 1: Sort faces by Z-Coordinate
sorted_face_indices = np.lexsort(
    [
        centroids.iloc[:, 1],
        centroids.iloc[:, 0],
        centroids.iloc[:, 2]
        ]
)  # Sorting by Z-coordinate


x_sorted = x.iloc[sorted_face_indices].reset_index(drop=True)
centroids_sorted = centroids.iloc[sorted_face_indices].reset_index(drop=True)


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
adj_matrix = csr_matrix(
    (np.ones(len(edges_mapped)), (edges_mapped[:, 0], edges_mapped[:, 1])),
    shape=(num_faces, num_faces),
)

# Compute the new adjacency-preserving order
new_order = reverse_cuthill_mckee(adj_matrix)

# Reorder x based on these new indices
x_reordered = x_sorted.iloc[np.argsort(new_order)].reset_index(drop=True)
# y_reordered = y_sorted.iloc[new_order].reset_index(drop=True)
centroids_reordered = centroids_sorted.iloc[np.argsort(new_order), :].reset_index(
    drop=True
)


# Create a color gradient based on the order
face_indices = np.arange(len(centroids_reordered))

# 3D Scatter Plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection="3d")

sc = ax.scatter(
    centroids_reordered.iloc[:, 0],
    centroids_reordered.iloc[:, 1],
    centroids_reordered.iloc[:, 2],
    c=face_indices,
    cmap="viridis",
    s=10,  # type: ignore
)
plt.colorbar(sc, label="Face Order (x_reordered)")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")  # type: ignore
plt.title("3D Visualization of x_reordered (Color Indicates Order)")

# Compute distances between consecutive reordered faces
distances = np.linalg.norm(np.diff(centroids_reordered, axis=0), axis=1)

plt.figure(figsize=(10, 5))
plt.plot(distances, marker="o", linestyle="-")
plt.xlabel("Face Index in x_reordered")
plt.ylabel("Distance to Next Face")
plt.title("Distance Between Consecutive Faces in x_reordered")
plt.show()

exit()
