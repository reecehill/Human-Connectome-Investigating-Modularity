import modules.globals as g
from modules.hcp_data_manager.downloader import getFile
import config
from pathlib import Path
from modules.subprocess_caller.call import *

def createTimingFiles(subjectId: str):
  g.logger.info("Ensuring timing files for functional data exists -- Run 1 (Right-Left Phase Encoding)")
  _ = [getFile(localPath=Path(config.DATA_DIR / 'subjects' / subjectId / 'unprocessed' / ('7T' if config.USE_7T_DIFFUSION else '3T') / 'tfMRI_MOTOR_RL' / 'LINKED_DATA' / 'EPRIME' / 'EVs' / f"{fmriTask}.txt")) for fmriTask in config.ALL_FMRI_TASKS]

  g.logger.info("Ensuring timing files for functional data exists -- Run 2 (Left-Right Phase Encoding)")
  _ = [getFile(localPath=Path(config.DATA_DIR / 'subjects' / subjectId / 'unprocessed' / ('7T' if config.USE_7T_DIFFUSION else '3T') / 'tfMRI_MOTOR_LR' / 'LINKED_DATA' / 'EPRIME' / 'EVs' / f"{fmriTask}.txt")) for fmriTask in config.ALL_FMRI_TASKS]

def runSpm(subjectId: str) -> bool:
  return call(cmdLabel="MATLAB",
              cmd=[
                      config.MATLAB,
                      f'-batch "RunPreproc_1stLevel_job {config.matLabDriveAndPathToSubjects} {subjectId}"',
                      ],
              cwd=config.matlabScriptsFolder)

def matlabProcessFunctional(subjectId: str):
  createTimingFiles(subjectId=subjectId)
  # runSpm() is not needed if we intend to use the processed data.
  # runSpm(subjectId=subjectId)
  


