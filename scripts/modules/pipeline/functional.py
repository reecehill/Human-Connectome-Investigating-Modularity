import modules.globals as g
from modules.hcp_data_manager.downloader import getFile
import config
from pathlib import Path
from modules.subprocess_caller.call import *
from ..file_directory.file_directory import createDirectories

def createTimingFiles(subjectId: str) -> bool:
  # Function not used when using fMRI pre-processed data in HCP dataset.
  g.logger.info("Ensuring timing files for functional data exists -- Run 1 (Right-Left Phase Encoding)")
  _ = [getFile(localPath=Path(config.DATA_DIR / 'subjects' / subjectId / 'unprocessed' / ('7T' if config.USE_7T_DIFFUSION else '3T') / 'tfMRI_MOTOR_RL' / 'LINKED_DATA' / 'EPRIME' / 'EVs' / f"{fmriTask}.txt")) for fmriTask in config.ALL_FMRI_TASKS]

  g.logger.info("Ensuring timing files for functional data exists -- Run 2 (Left-Right Phase Encoding)")
  _ = [getFile(localPath=Path(config.DATA_DIR / 'subjects' / subjectId / 'unprocessed' / ('7T' if config.USE_7T_DIFFUSION else '3T') / 'tfMRI_MOTOR_LR' / 'LINKED_DATA' / 'EPRIME' / 'EVs' / f"{fmriTask}.txt")) for fmriTask in config.ALL_FMRI_TASKS]
  return True

def getFmriData(subjectId: str) -> bool:
  # Function not used when using fMRI pre-processed data in HCP dataset.
  g.logger.info("Ensuring functional data results exist")
  subjectDir = config.SUBJECTS_DIR / subjectId / "MNINonLinear"
  filesToExist = [
                    (subjectDir / 'Results' / 'tfMRI_MOTOR' /'tfMRI_MOTOR_hp200_s2_level2.feat' /f'{subjectId}_tfMRI_MOTOR_level2_hp200_s2.dscalar.nii'),
                    ]
  _ = [getFile(localPath=fileToExist) for fileToExist in filesToExist]

  g.logger.info("Ensuring surface files exist")
  filesToExist = [
                    (subjectDir / 'fsaverage_LR32k' / f'{subjectId}.L.pial.32k_fs_LR.surf.gii'),
                    (subjectDir / 'fsaverage_LR32k' / f'{subjectId}.R.pial.32k_fs_LR.surf.gii'),
                    ]
  _ = [getFile(localPath=fileToExist) for fileToExist in filesToExist]
  return True

def runSpm(subjectId: str) -> bool:
  # Function not used when using fMRI pre-processed data in HCP dataset.
  return call(cmdLabel="MATLAB",
              cmd=[
                      config.MATLAB,
                      f'-batch "RunPreproc_1stLevel_job {config.matLabDriveAndPathToSubjects} {subjectId}"',
                      ],
              cwd=config.matlabScriptsFolder)

def matlabSortFmriVoxelsIntoModules(subjectId: str, binaryThreshold: float) -> bool:
  # Function not used when using fMRI pre-processed data in HCP dataset.
  # TODO: NOT USED.
  return call(cmdLabel="MATLAB",
              cmd=[
                      config.MATLAB,
                      f'-batch "convertIntensityToCoordinates {config.matLabDriveAndPathToSubjects} {subjectId} {binaryThreshold}"',
                      ],
              cwd=config.matlabScriptsFolder)  

def matlabMapLowToHighResFmriData(subjectId: str) -> bool:
  subjectFolder = config.SUBJECTS_DIR / subjectId

  fMriScalarPath = subjectFolder / config.IMAGES["FMRI"]["LOW_RES"]["DATA"]["FOLDER"] / (config.IMAGES["FMRI"]["LOW_RES"]["DATA"]["PATH"].replace("$subjectId$",subjectId))
  fMriAsModulesPath = subjectFolder / config.IMAGES["FMRI"]["LOW_RES"]["DATA"]["FOLDER"] / (config.IMAGES["FMRI"]["LOW_RES"]["DATA"]["PATH"].replace("$subjectId$",subjectId).replace(".dscalar.nii",".clusters.dscalar.nii"))
  
  subjectLowResSurfacePath_left = subjectFolder / config.IMAGES["FMRI"]["LOW_RES"]["SURFACE"]["FOLDER"] / config.IMAGES["FMRI"]["LOW_RES"]["SURFACE"]["L_HEMISPHERE_PATH"].replace("$subjectId$",subjectId)
  subjectLowResSurfacePath_right = subjectFolder / config.IMAGES["FMRI"]["LOW_RES"]["SURFACE"]["FOLDER"] / config.IMAGES["FMRI"]["LOW_RES"]["SURFACE"]["R_HEMISPHERE_PATH"].replace("$subjectId$",subjectId)                                                                                  
  
  remoteFilesToExist: "list[Path]" = [
                    fMriScalarPath,
                    subjectLowResSurfacePath_left,
                    subjectLowResSurfacePath_right
                    ]
  localFilesToExist: "list[Path]" = [
                    fMriAsModulesPath
                    ]
  _ = [getFile(localPath=fileToExist) for fileToExist in remoteFilesToExist]
  _ = [getFile(localPath=fileToExist, localOnly=True) for fileToExist in localFilesToExist]
  createDirectories(directoryPaths=[subjectFolder / config.IMAGES["FMRI"]["HIGH_RES"]["DATA"]["FOLDER"]], createParents=True, throwErrorIfExists=False)

  return call(cmdLabel="MATLAB",
              cmd=[
                      config.MATLAB,
                      f'-batch "mapFmriToHighResSurf {config.matLabDriveAndPathToSubjects} {subjectId} {config.DOWNSAMPLE_SURFACE} {config.PIAL_SURFACE_TYPE} \'{(subjectFolder / config.IMAGES["FMRI"]["HIGH_RES"]["DATA"]["FOLDER"]).resolve(strict=False)}\' \'{fMriScalarPath}\' \'{fMriAsModulesPath}\' \'{subjectLowResSurfacePath_left}\' \'{subjectLowResSurfacePath_right}\'"',
                      ],
              cwd=config.matlabScriptsFolder)   

def convertFmriToClusters(subjectId: str) -> bool:
  # This function levies wb_command -cifti-find-clusters to detect fMRI clusters.
  # https://humanconnectome.org/software/workbench-command/-cifti-find-clusters
  g.logger.info("Finding clusters within functional data (scalar)")
  subjectFolder = config.SUBJECTS_DIR / subjectId

  fMriScalarPath = subjectFolder / config.IMAGES["FMRI"]["LOW_RES"]["DATA"]["FOLDER"] / (config.IMAGES["FMRI"]["LOW_RES"]["DATA"]["PATH"].replace("$subjectId$",subjectId))
  fMriAsModulesPath = subjectFolder / config.IMAGES["FMRI"]["LOW_RES"]["DATA"]["FOLDER"] / (config.IMAGES["FMRI"]["LOW_RES"]["DATA"]["PATH"].replace("$subjectId$",subjectId).replace(".dscalar.nii",".clusters.dscalar.nii"))
  subjectLowResSurfacePath_left = subjectFolder / config.IMAGES["FMRI"]["LOW_RES"]["SURFACE"]["FOLDER"] / config.IMAGES["FMRI"]["LOW_RES"]["SURFACE"]["L_HEMISPHERE_PATH"].replace("$subjectId$",subjectId)
  subjectLowResSurfacePath_right = subjectFolder / config.IMAGES["FMRI"]["LOW_RES"]["SURFACE"]["FOLDER"] / config.IMAGES["FMRI"]["LOW_RES"]["SURFACE"]["R_HEMISPHERE_PATH"].replace("$subjectId$",subjectId)
  
  g.logger.info("Ensuring files files exist")
  filesToExist = [
                    fMriScalarPath,
                    subjectLowResSurfacePath_left,
                    subjectLowResSurfacePath_right
                    ]
  _ = [getFile(localPath=fileToExist) for fileToExist in filesToExist]
  
  return call(cmdLabel="wb_command",
              cmd=[
                      config.WB_COMMAND,
                      '-cifti-find-clusters',
                      fMriScalarPath.resolve(),
                      '1.5',
                      '2',
                      'inf',
                      'inf',
                      'COLUMN',
                      fMriAsModulesPath.resolve(),
                      '-left-surface',
                      subjectLowResSurfacePath_left.resolve(),
                      '-right-surface',
                      subjectLowResSurfacePath_right.resolve(),
                      '-distance',
                      '20',
                      '-inf',
                      ])   

def matlabProcessFunctional(subjectId: str) -> bool:
  # This function takes fMRI data and returns a binarised surface.
  # TODO: Folder naming scheme is remnant of SPM.
  
  return (convertFmriToClusters(subjectId=subjectId) and
          matlabMapLowToHighResFmriData(subjectId=subjectId))
  return (matlabMapLowToHighResFmriData(subjectId=subjectId))
  firstLevelFolder =  config.SUBJECTS_DIR / subjectId / "1stlevel"
  createDirectories(directoryPaths=[firstLevelFolder], createParents=True, throwErrorIfExists=False)
    
  return (
    convertFmriToModules(subjectId=subjectId) and
    createTimingFiles(subjectId=subjectId) and
    getFmriData(subjectId=subjectId) and
    matlabSortFmriVoxelsIntoModules(subjectId=subjectId, binaryThreshold=config.FMRI_THRESHOLD_TO_BINARISE)
    )
  # runSpm() is not needed if we intend to use the processed data.
  # runSpm(subjectId=subjectId)
  


