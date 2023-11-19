import modules.globals as g
from modules.hcp_data_manager.downloader import getFile
import config
from pathlib import Path
from modules.subprocess_caller.call import *
from ..file_directory.file_directory import createDirectories

def createTimingFiles(subjectId: str) -> bool:
  g.logger.info("Ensuring timing files for functional data exists -- Run 1 (Right-Left Phase Encoding)")
  _ = [getFile(localPath=Path(config.DATA_DIR / 'subjects' / subjectId / 'unprocessed' / ('7T' if config.USE_7T_DIFFUSION else '3T') / 'tfMRI_MOTOR_RL' / 'LINKED_DATA' / 'EPRIME' / 'EVs' / f"{fmriTask}.txt")) for fmriTask in config.ALL_FMRI_TASKS]

  g.logger.info("Ensuring timing files for functional data exists -- Run 2 (Left-Right Phase Encoding)")
  _ = [getFile(localPath=Path(config.DATA_DIR / 'subjects' / subjectId / 'unprocessed' / ('7T' if config.USE_7T_DIFFUSION else '3T') / 'tfMRI_MOTOR_LR' / 'LINKED_DATA' / 'EPRIME' / 'EVs' / f"{fmriTask}.txt")) for fmriTask in config.ALL_FMRI_TASKS]
  return True

def getFmriData(subjectId: str) -> bool:
  g.logger.info("Ensuring functional data results exist")
  subjectDir = config.SUBJECTS_DIR / subjectId / "MNINonLinear"
  filesToExist = [
                    (subjectDir / 'Results' / 'tfMRI_MOTOR' /'tfMRI_MOTOR_hp200_s2_level2.feat' /f'{subjectId}_tfMRI_MOTOR_level2_hp200_s2.dscalar.nii'),
                    ]
  _ = [getFile(localPath=fileToExist) for fileToExist in filesToExist]

  g.logger.info("Ensuring surface files exist")
  filesToExist = [
                    (subjectDir / 'fsaverage_LR59k' / f'{subjectId}.L.pial.59k_fs_LR.surf.gii'),
                    (subjectDir / 'fsaverage_LR59k' / f'{subjectId}.R.pial.59k_fs_LR.surf.gii'),
                    ]
  _ = [getFile(localPath=fileToExist) for fileToExist in filesToExist]
  return True

def runSpm(subjectId: str) -> bool:
  return call(cmdLabel="MATLAB",
              cmd=[
                      config.MATLAB,
                      f'-batch "RunPreproc_1stLevel_job {config.matLabDriveAndPathToSubjects} {subjectId}"',
                      ],
              cwd=config.matlabScriptsFolder)

def matlabSortFmriVoxelsIntoModules(subjectId: str, binaryThreshold: float) -> bool:
  return call(cmdLabel="MATLAB",
              cmd=[
                      config.MATLAB,
                      f'-batch "convertIntensityToCoordinates {config.matLabDriveAndPathToSubjects} {subjectId} {binaryThreshold}"',
                      ],
              cwd=config.matlabScriptsFolder)  

def matlabProcessFunctional(subjectId: str) -> bool:
  # TODO: Folder naming scheme is remnant of SPM.
  firstLevelFolder =  config.SUBJECTS_DIR / subjectId / "1stlevel"
  createDirectories(directoryPaths=[firstLevelFolder], createParents=True, throwErrorIfExists=False)
    
  return (
    createTimingFiles(subjectId=subjectId) and
    getFmriData(subjectId=subjectId) and
    matlabSortFmriVoxelsIntoModules(subjectId=subjectId, binaryThreshold=config.FMRI_THRESHOLD_TO_BINARISE)
    )
  # runSpm() is not needed if we intend to use the processed data.
  # runSpm(subjectId=subjectId)
  


