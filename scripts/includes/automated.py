# ----------
# These configuration parameters are:
# 1) Not intended to be edited by the user.
# 2) Generally used throughout the program.
# 3) Therefore, automatically assigned.
# ----------
try:
  from pathlib import Path
  from time import strftime
except Exception as e:
  print(e)
  exit()
import os
from subprocess import getoutput
from typing import Callable, Dict, List, Optional, Union

# from modules.file_directory.shutil_ported import which
from shutil import which

import config

def findAndInject(find: str, replace: str, string: str) -> str:
  return string.replace(find, replace)

def getLogDirectoryPath(userSubmitted: str) -> Path:
  LOGS_DIR: Path = (BASE_DIR / userSubmitted / TIMESTAMP_OF_SCRIPT).resolve(strict=False)
  return LOGS_DIR


def getDiffusionFolder(use7TDiffusion: bool = False):
  append = ""
  if(use7TDiffusion): append = "_7T"
  return f'Diffusion{append}' 

TIMESTAMP_OF_SCRIPT = strftime("%d%m%Y-%H%M%S")
START_A_FRESH = False


# ----------
# [START] DIRECTORY STRUCTURE PARAMETERS
# ----------
BASE_DIR: Path = Path(__file__).parent.parent.parent.resolve(strict=True)
SCRIPTS_DIR: Path = (BASE_DIR / "scripts").resolve(strict=True)
INCLUDES_DIR: Path = (SCRIPTS_DIR / "includes").resolve(strict=True)
DATA_DIR: Path = (BASE_DIR / "data").resolve(strict=True)
SUBJECTS_DIR: Path = (DATA_DIR / "subjects").resolve(strict=True)
UPLOADS_DIR: Path = (BASE_DIR / "uploads" / TIMESTAMP_OF_SCRIPT).resolve(strict=False)

SUBJECT_DIR: Path = Path()
PIPELINE_SUCCESS_FILE: Path = Path()
SUBJECT_STAT_DIR: Path = Path()

STAT_FILE: Path = DATA_DIR / 'allSubjects.csv'
# [END] DIRECTORY STRUCTURE PARAMETERS
# ----------

# ----------
# [START] SUBJECT-SPECIFIC PARAMETERS
# These get continuously overwritten by any step of the pipeline to share loop information.
# ----------
CURRENT_STEP: str = ""
CURRENT_SUBJECT: str = ""
CURRENT_HEMISPHERE: str = ""
CURRENT_TASK: str = ""
# ----------
# [END] SUBJECT-SPECIFIC PARAMETERS
# ----------

SUBJECT_PIPELINE_SUCCESS: Optional[bool] = None # If an error occurs at any step whilst processing a subject, this is set to False. This is only set to True upon finishing a step. Thus, "None" indicates termination mid-step.
SUBJECT_STEP_SUCCESS: Optional[bool] = None # If an error occurs during the step whilst processing a subject, this is set to 1.

# ----------


# ----------
# [START] EXECUTABLE PATHS
# ----------
def getPathOfExecutable(executable: str, executableAlias: Optional[str] = None, userSubmitted: Optional[str] = None) -> Path:
  if(userSubmitted == None or userSubmitted == ""):
    pathToExecutable =  \
      which(executable) or \
      getoutput(f"find $HOME -wholename '*/{executable}/*' -name '{executableAlias}' -type f -executable") or \
      getoutput(f"find $HOME -wholename '*/{executable}/*' -name '{executableAlias}' -type f -executable") or \
      getoutput(f"find $HOME -wholename '*/{executable}/*' -name '{executable}' -type f -executable") or \
      getoutput(f"find $HOME -wholename '*/{executableAlias}/*' -name '{executable}' -type f -executable") 
    # If the pathToExecutable is a string and contains data after being stripped of white space. 
    if (isinstance(pathToExecutable, str) and pathToExecutable.strip()): # type: ignore # 
      print(f'Path to {executable} is {pathToExecutable}')
      return Path(pathToExecutable).resolve(strict=True)
    else:
      message = f"Cannot find the executable: {executable}. Please specify or correct the location in config.py"
      raise BaseException(message)
  else:
    if(Path(userSubmitted).exists()):
      return Path(userSubmitted).resolve(strict=True)
    else:
      print(f"The location you specified for {executable} (at: {userSubmitted}) could not be found.");
      print(f"Parent contents ({userSubmitted}/../) [ls -la {userSubmitted}/../]:");
      print(getoutput(f"ls -la {userSubmitted}/../"));
      print(f"Attempting to find {executable} using default settings...");
      return getPathOfExecutable(executable=executable, executableAlias=executableAlias, userSubmitted="")


def getSpmDir(userSubmitted: str = "") -> Path:
  if (userSubmitted == ""):
    try:
      return (Path.home() / "spm12").resolve(strict=True)
    except Exception:
      print("The installation to SPM is not where it is expected. Please specify or re-check the folder in which SPM was installed.")
      raise
  else:
    try:
      #  Retry using default settings ("") if not user specified path doesn't exist. 
      return Path(userSubmitted).resolve(strict=True) if Path(userSubmitted).exists() else getSpmDir(userSubmitted="")
    except Exception:
      print("The SPM12 installation directory provided could not be found. Try again, providing an absolute path from root.")
      raise

def getNativeOrMni152Folder(isMni152: bool) -> str:
  return "MNINonLinear" if (isMni152) else "T1w"

# ----------
# [END] EXECUTABLE PATHS
# ----------

# ----------
# [START] SETTING ENVIRONMENT VARIABLES
# ----------
os.environ["SUBJECTS_DIR"] = SUBJECTS_DIR.__str__()
# ----------
# [END] SETTING ENVIRONMENT VARIABLES
# ----------

matLabDriveAndPathToSubjects = (DATA_DIR / 'subjects').resolve(strict=True).__str__()+"/"
matlabScriptsFolder = (SCRIPTS_DIR / "matlab" ).resolve(strict=True).__str__()