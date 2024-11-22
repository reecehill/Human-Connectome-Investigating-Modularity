import pandas as pd
import pyvista as pv
import numpy as np
from modules.utils.loadSpatialData import loadFacesAndVertices


def plotRoiRegion() -> None:
    """
    Load the vertex and face data and plot a region of interest (ROI) on a 3D mesh.
    """
    xy_vertices: pd.DataFrame  # shape (m x 3)
    xy_faces: pd.DataFrame  # shape (n x 3)
    xy_faces, xy_vertices = loadFacesAndVertices()

    faces = np.hstack([[3, *face] for face in xy_faces.to_numpy()]).astype(int)

    mesh = pv.PolyData(xy_vertices.to_numpy(), faces)
    plotter = pv.Plotter()
    plotter.add_mesh(
        mesh,
        color="cyan",
        show_edges=True,
        edge_color="black",
        opacity=0.8,
        smooth_shading=True,
    )
    light = pv.Light(position=(5, 5, 5), focal_point=(0, 0, 0), color="white")
    light.intensity = 1.0  # Adjust intensity as needed
    plotter.enable_shadows()  # type:ignore
    plotter.add_light(light)
    plotter.enable_anti_aliasing()
    # plotter.show_grid()
    # plotter.enable_depth_of_field()
    # plotter.camera.focal_point = (0, 0, 0)  # Set focal point on the mesh
    # plotter.camera.position = (0, , 5)     # Adjust the camera position as needed
    plotter.show()
