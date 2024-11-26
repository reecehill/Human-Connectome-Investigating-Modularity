from pathlib import Path
from matplotlib import cm
from numpy._typing._array_like import NDArray
import pandas as pd
import pyvista as pv
import numpy as np
import numpy.typing as npt
from sklearn.cluster import KMeans
from modules.utils.loadSpatialData import loadFacesAndVertices, loadRoiIds
from modules.visualisation.includes.io.save_pickled_object import save_fig_as_pickle


def plotRoiRegion(subjectId: str, pathTo: dict[str, Path]) -> bool:
    import config

    """
    Load the vertex and face data and plot a region of interest (ROI) on a 3D mesh.
    """
    xy_vertices: pd.DataFrame  # shape (m x 3)
    xy_faces: pd.DataFrame  # shape (n x 3)
    xy_faces, xy_vertices = loadFacesAndVertices(onlyRoi=False)

    faces = np.hstack([[3, *face] for face in xy_faces.to_numpy()]).astype(int)

    pathToXCsv: Path = (
        config.SUBJECT_DIR
        / "exported_modules"
        / f"{config.CURRENT_HEMISPHERE}_structural_modules.csv"
    ).resolve(strict=True)
    pathToYCsv: Path = (
        config.SUBJECT_DIR
        / "exported_modules"
        / f"{config.CURRENT_HEMISPHERE}_{config.CURRENT_TASK}_functional_modules.csv"
    ).resolve(strict=True)
    roiIds: npt.NDArray = loadRoiIds()

    x_raw: pd.DataFrame = pd.read_csv(
        pathToXCsv, sep=",", header=None, keep_default_na=True
    ).T
    y_raw: pd.DataFrame = pd.read_csv(
        pathToYCsv, sep=",", header=None, keep_default_na=True
    ).T

    mesh = pv.PolyData(xy_vertices.to_numpy(), faces)
    # Define face scalars (e.g., color indices for each face)
    x_unique_labels = np.unique(
        x_raw.to_numpy(dtype=str)
    ).tolist()  # Find unique labels
    x_face_labels = x_raw.to_numpy(dtype=str).flatten()
    x_cmap = cm.get_cmap("tab10", len(x_unique_labels))  # Use a colormap

    x_label_to_color: dict[str, tuple[float, float, float, float]] = {label: ((*x_cmap(i)[:3], 1.0)) for i, label in enumerate(x_unique_labels)}
    x_face_colors = np.full(shape=(xy_faces.shape[0], 4), fill_value=(0.5, 0, 0, 0.1))
    x_face_colors[roiIds] = np.array(
        [x_label_to_color[label] for label in x_face_labels]
    )

    y_unique_labels = np.unique(
        y_raw.to_numpy(dtype=str)
    ).tolist()  # Find unique labels
    y_face_labels = y_raw.to_numpy(dtype=str).flatten()
    y_cmap = cm.get_cmap("tab10", len(y_unique_labels))  # Use a colormap
    y_label_to_color = {
        label: ((*y_cmap(i)[:3], 1.0)) for i, label in enumerate(y_unique_labels)
    }
    y_face_colors = np.full(shape=(xy_faces.shape[0], 4), fill_value=(0.5, 0, 0, 0.1))
    y_face_colors[roiIds] = np.array(
        [y_label_to_color[label] for label in y_face_labels]
    )
    # Apply texture to the mesh
    # plotter = pv.Plotter()
    # Add scalars to the mesh
    mesh.cell_data["x_face_colors_rgb"] = x_face_colors
    mesh.cell_data["y_face_colors_rgb"] = y_face_colors

    plotter = pv.Plotter(
        shape=(
            1,
            2,
        ),
        window_size=(1000, 1000),
        title=f"ROI Region for Subject {subjectId}",
        off_screen=True,
    )
    light = pv.Light(position=(5, 5, 5), focal_point=(0, 0, 0), color="white", intensity=1.0, light_type="cameralight")
    # light.intensity = 1.0  # Adjust intensity as needed
    # plotter.enable_shadows()  # type:ignore
    plotter.add_light(light)

    plotter.subplot(0, 0)
    x_legend_entries = [[f"Module #{label}", tuple(color), "triangle"] for label, color in x_label_to_color.items()]
    plotter.add_legend(x_legend_entries[20:25], bcolor="white", loc="lower right") # type: ignore
    plotter.add_mesh(
        mesh=mesh.copy(),
        show_edges=True,
        edge_color="black",
        # smooth_shading=True,
        scalars="x_face_colors_rgb",
        rgb=True,
        categories=True,
    )
    plotter.add_text("x_raw Scalars", position="upper_left")

    plotter.subplot(0, 1)
    plotter.add_mesh(
        mesh=mesh.copy(),
        show_edges=True,
        edge_color="black",
        opacity=1,
        smooth_shading=True,
        scalars="y_face_colors_rgb",
        rgb=True,
        categories=True,
    )
    y_legend_entries = [
        [f"Module #{label}", tuple(color), "triangle"] for label, color in y_label_to_color.items()
    ]
    plotter.add_legend(y_legend_entries, bcolor="white", loc="lower left")  # type: ignore
    plotter.add_text("y_raw Scalars", position="upper_left")

    plotter.link_views()

    plotter.save_graphic(pathTo["figures"] / 'module_mesh.svg')


    plotter.close()
    print(f"Mesh figure saved as '{str(pathTo['figures'] / 'module_mesh.svg')}'.")
    return True
