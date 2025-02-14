import hashlib
from typing import Any
import pandas as pd
from pathlib import Path
from h5py import File  # type:ignore
import config
import numpy.typing as npt
import numpy as np
import modules.globals as g
from types import ModuleType
def loadRoiIds() -> "npt.NDArray[np.int64]":
    roiIds: pd.DataFrame = pd.read_csv(
        (config.SUBJECT_DIR / f"{config.CURRENT_HEMISPHERE}_ROIids.csv")
        .absolute()
        .__str__(),
        sep=",",
        header=None,
        keep_default_na=True,
    ).T
    return roiIds.to_numpy().flatten()


def loadVertices(faces: pd.DataFrame) -> pd.DataFrame:
    pathToVertices: Path = config.SUBJECT_DIR / "labelSRF.mat"
    cacheLabel = f"{str(pathToVertices)}{hash_vars(config)}-vertices"

    if cacheLabel in globals():
        g.logger.info(f"{cacheLabel} in globals()")
        return globals()[cacheLabel]
    else:
        with File(pathToVertices, "r") as f:
            vertices = pd.DataFrame(
                f[f"lo_g{config.CURRENT_HEMISPHERE[0].lower()}pvertex"][:]
            ).T

        nodeIdsRequired = faces.values.reshape(-1, 1).flatten().tolist()
        # return vertices.iloc[nodeIdsRequired]
        globals()[cacheLabel] = vertices
        return vertices


def hash_vars(module: ModuleType) -> str:
    """
    Hashes only user-defined variables from an imported module.
    
    Parameters:
        module (types.ModuleType): The module to process.

    Returns:
        str: SHA-256 hash of the module's user-defined variables.
    """
    user_vars: dict[str, Any] = {
        k: v for k, v in vars(module).items()
        if not k.startswith("__") and not callable(v) and not isinstance(v, type)
    }

    # Convert dictionary to a sorted tuple for consistent hashing
    return hashlib.sha256(str(sorted(user_vars.items())).encode()).hexdigest()

def loadFaces(onlyRoi: bool = True) -> pd.DataFrame:
    pathToFaces = config.SUBJECT_DIR / "labelSRF.mat"

    cacheLabel = f"{str(pathToFaces)}{hash_vars(config)}-faces"
    if cacheLabel in globals():
        g.logger.info(f"{cacheLabel} in globals()")

        return globals()[cacheLabel]
    else:
        with File(pathToFaces, "r") as f:
            # faces_L = pd.DataFrame(f[f'lo_glpfaces'][:]).T
            # faces_R = pd.DataFrame(f[f'lo_grpfaces'][:]).T
            # faces = pd.concat([faces_L, faces_R], ignore_index=True)
            faces = (
                pd.DataFrame(f[f"lo_g{config.CURRENT_HEMISPHERE[0].lower()}pfaces"][:]).T
                - 1
            )  # We minus one as Python indexes from zero

        # TODO: Should not have 64980 hardcoded.
        
        if onlyRoi:
            roiIds = loadRoiIds().tolist()
            if config.CURRENT_HEMISPHERE == "right":
                roiIds = (np.array(roiIds)-64980).tolist()    
            faces =  faces.iloc[roiIds]
        globals()[cacheLabel] = faces
        return faces


def loadFacesAndVertices(onlyRoi: bool = True) -> tuple[pd.DataFrame, pd.DataFrame]:
    faces = loadFaces(onlyRoi=onlyRoi)
    vertices = loadVertices(faces)
    return faces, vertices
