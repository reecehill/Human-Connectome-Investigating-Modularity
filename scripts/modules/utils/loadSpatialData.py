import pandas as pd
from pathlib import Path 
from h5py import File # type:ignore
import config
import numpy.typing as npt
import numpy as np

def loadRoiIds() -> "npt.NDArray[np.int64]":
  roiIds: pd.DataFrame = pd.read_csv((config.SUBJECT_DIR / f'{config.CURRENT_HEMISPHERE}_ROIids.csv').absolute(
  ).__str__(), sep=',', header=None, keep_default_na=True).T
  return roiIds.to_numpy().flatten()

def loadVertices(faces: pd.DataFrame) -> pd.DataFrame:
  pathToVertices: Path = config.SUBJECT_DIR / 'labelSRF.mat'
  with File(pathToVertices, 'r') as f:
    vertices = pd.DataFrame(f[f'lo_g{config.CURRENT_HEMISPHERE[0].lower()}pvertex'][:]).T

  nodeIdsRequired = faces.values.reshape(-1, 1).flatten().tolist()
  # return vertices.iloc[nodeIdsRequired]
  return vertices


def loadFaces() -> pd.DataFrame:
    pathToFaces = config.SUBJECT_DIR / 'labelSRF.mat'
    with File(pathToFaces, 'r') as f:
      # faces_L = pd.DataFrame(f[f'lo_glpfaces'][:]).T
      # faces_R = pd.DataFrame(f[f'lo_grpfaces'][:]).T
      # faces = pd.concat([faces_L, faces_R], ignore_index=True)
      faces = pd.DataFrame(f[f'lo_g{config.CURRENT_HEMISPHERE[0].lower()}pfaces'][:]).T -1 # We minus one as Python indexes from zero


    roiIds = loadRoiIds().tolist()
    return faces.iloc[roiIds]

def loadFacesAndVertices():
  faces = loadFaces()
  vertices = loadVertices(faces)
  return faces, vertices