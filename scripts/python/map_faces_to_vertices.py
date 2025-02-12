from nibabel.loadsave import load, save
from nibabel.gifti.gifti import GiftiDataArray, GiftiImage
import numpy as np
from pathlib import Path
import pandas as pd
from scipy.stats import mode

# Define relative paths
base_path = Path(__file__).parent  # Directory of the current script
scalar_file = (
    base_path.parent.parent
    / "data"
    / "subjects"
    / "100408"
    / "exported_modules"
    / "left_structural_modules.csv"
).resolve(strict=True)

# scalar_file = (
#     base_path.parent.parent
#     / "data"
#     / "subjects"
#     / "100408"
#     / "statistics"
#     / "right_hemisphere"
#     / "datasets"
#     / "cleaned_mapped_left_structural_modules.csv"
# ).resolve(strict=True)

scalar_file_is_processed = True if "_cleaned" in scalar_file.name else False

hemisphere_face_ids_L = (
    base_path.parent.parent
    / "data"
    / "subjects"
    / "100408"
    / "exported_modules"
    / "all_left_structural_modules.csv"
).resolve(strict=True)
hemisphere_face_ids_R = (
    base_path.parent.parent
    / "data"
    / "subjects"
    / "100408"
    / "exported_modules"
    / "all_right_structural_modules.csv"
).resolve(strict=True)
roi_face_ids_L = (
    base_path.parent.parent
    / "data"
    / "subjects"
    / "100408"
    / "exported_modules"
    / "lh.L_precentral_L_faceIds.csv"
).resolve(strict=True)
surface_file = (
    base_path.parent.parent
    / "data"
    / "subjects"
    / "100408"
    / "MNINonLinear"
    / "fsaverage_LR32k"
    / "100408.L.pial_MSMAll.32k_fs_LR.surf.gii"
).resolve(strict=True)
output_file = (
    base_path.parent.parent
    / "data"
    / "subjects"
    / "100408"
    / "MNINonLinear"
    / "Results"
    / "tfMRI_MOTOR"
    / "tfMRI_MOTOR_hp200_s2_level2_MSMAll.feat"
    / f"{scalar_file.name}.func.gii"
)

# Load surface
surf = load(surface_file)
vertices = surf.darrays[0].data
faces_R = surf.darrays[1].data - 1
faces_R = faces_R.astype(int)  # Ensure indices are integers

# Constrain faces to ROI
left_hemi_faces = pd.read_csv(
    hemisphere_face_ids_L, sep=",", header=None, keep_default_na=True
).T.to_numpy(dtype=np.int32)
right_hemi_faces = pd.read_csv(
    hemisphere_face_ids_R, sep=",", header=None, keep_default_na=True
).T.to_numpy(dtype=np.int32)
right_scalars = np.ones(right_hemi_faces.size) * -1

roi_faces = pd.read_csv(
    roi_face_ids_L, sep=",", header=None, keep_default_na=True
).T.to_numpy(dtype=np.int32)

# Load scalar data
face_scalars = pd.read_csv(
    scalar_file, sep=",", header=None, keep_default_na=True
).T.to_numpy(dtype=np.int32)

if scalar_file_is_processed:
    ids = face_scalars[0, :]
    face_scalars = face_scalars[1, :]
    faces_R = faces_R[roi_faces - len(left_hemi_faces)]
    faces_R = faces_R[ids, :]
else:
    faces_R = faces_R[roi_faces - len(left_hemi_faces)]


# Create vertex scalars by assigning each face's scalar to its vertices
vertex_face_values = [
    [] for _ in range(len(vertices))
]  # List to store values per vertex
for i, face in enumerate(faces_R):
    for v in face[0]:
        vertex_face_values[v].append(face_scalars[i])

# Compute the mode for each vertex
vertex_scalars = np.zeros(len(vertices), dtype=np.int32)
for i, values in enumerate(vertex_face_values):
    if values:  # Check if there are values attached to the vertex
        vertex_scalars[i] = mode(values, axis=None)[0]  # Get the mode
    else:
        vertex_scalars[i] = -1  # Default value for vertices with no attached faces

# Save as a GIFTI functional file
gifti_image = GiftiImage(
    darrays=[GiftiDataArray(vertex_scalars, intent="NIFTI_INTENT_LABEL")]
)
save(gifti_image, output_file)

print(f"Output saved to {output_file}")
