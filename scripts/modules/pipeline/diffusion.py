from pathlib import Path
import modules.globals as g
import config
from modules.hcp_data_manager.downloader import getFile
from ..file_directory.file_directory import createDirectories
from modules.subprocess_caller.call import *
import includes.anatomicalLabels as anatomicalLabels

def processDiffusionTracts(subjectId: str) -> bool:
  # Downsampled surface files (e.g., 32k)
  subjectDownsampledFolder = config.SUBJECT_DIR / config.IMAGES["FMRI"]["LOW_RES"]["SURFACE"]["FOLDER"]
  subjectLowResSurfacePath_left = config.SUBJECT_DIR / config.IMAGES["FMRI"]["LOW_RES"]["SURFACE"]["FOLDER"] / config.IMAGES["FMRI"]["LOW_RES"]["SURFACE"]["L_HEMISPHERE_PATH"].replace("$subjectId$",subjectId)
  subjectLowResSurfacePath_right = config.SUBJECT_DIR / config.IMAGES["FMRI"]["LOW_RES"]["SURFACE"]["FOLDER"] / config.IMAGES["FMRI"]["LOW_RES"]["SURFACE"]["R_HEMISPHERE_PATH"].replace("$subjectId$",subjectId)

  # Original/high-resolution surface files (e.g., native or 164k).
  subjectHiResSurfaceFolder = config.SUBJECT_DIR / config.IMAGES["FMRI"]["HIGH_RES"]["SURFACE"]["FOLDER"] 
  subjectHiResSurface_left = subjectHiResSurfaceFolder / config.IMAGES["FMRI"]["HIGH_RES"]["SURFACE"]["L_HEMISPHERE_PATH"].replace("$subjectId$",subjectId)
  subjectHiResSurface_right = subjectHiResSurfaceFolder / config.IMAGES["FMRI"]["HIGH_RES"]["SURFACE"]["R_HEMISPHERE_PATH"].replace("$subjectId$",subjectId)

  
  # Ensure necessary files exist from previous steps.
  anatomicalLabelsToExist: "list[str]" = anatomicalLabels.anatomicalLabelsToExist
  remoteFilesToExist: "list[Path]" = [
                  (config.SUBJECT_DIR / config.NATIVEORMNI152FOLDER / 'aparc+aseg.nii.gz'),
                  (config.SUBJECT_DIR / 'T1w' / subjectId / 'mri' / 'transforms' / 'talairach.xfm'),
                  subjectHiResSurface_left,
                  subjectHiResSurface_right,
                  ]
  
  localFilesToExist: "list[Path]" = [\
    (config.SUBJECT_DIR / 'T1w' / config.DIFFUSION_FOLDER / ('1m'+str(currentIteration)+'.trk')) for currentIteration in range(0, config.DSI_STUDIO_ITERATION_COUNT, 1)] + [\
      (config.SUBJECT_DIR / config.NATIVEORMNI152FOLDER / subjectId / 'label' / 'label_type2' / label) for label in anatomicalLabelsToExist]

  # Ensure, if required, the downsampled meshes already exist.
  if(config.USE_PRESET_DOWNSAMPLED_MESH):
    remoteFilesToExist.append(subjectLowResSurfacePath_left)
    remoteFilesToExist.append(subjectLowResSurfacePath_right)
  else:
    # We will create our own downsampled surfaces, so ensure the folder exists. 
    createDirectories(directoryPaths=[subjectDownsampledFolder], createParents=True, throwErrorIfExists=False)
  
  _ = [getFile(localPath=fileToExist) for fileToExist in remoteFilesToExist]
  _ = [getFile(localPath=fileToExist, localOnly=True) for fileToExist in localFilesToExist]

  subjectDownsampledFolder.resolve(strict=True)
  return call(cmdLabel="MATLAB",
              cmd=[
                      config.MATLAB,
                      f'-batch "batch_process \'{config.matLabDriveAndPathToSubjects}\' \'{subjectId}\' {config.PIAL_SURFACE_TYPE} \'{config.DOWNSAMPLE_SURFACE}\' \'{config.DOWNSAMPLE_RATE}\' \'{config.DSI_STUDIO_ITERATION_COUNT}\' \'{config.USE_PRESET_DOWNSAMPLED_MESH}\' \'{subjectLowResSurfacePath_left.resolve(strict=False)}\' \'{subjectLowResSurfacePath_right.resolve(strict=False)}\'"',
                      ],
              cwd=config.matlabScriptsFolder)