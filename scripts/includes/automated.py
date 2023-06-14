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
from typing import Optional


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
# ----------
# [END] DIRECTORY STRUCTURE PARAMETERS
# ----------


# ----------
# [START] EXECUTABLE PATHS
# ----------
def getPathOfExecutable(executable: str, executableAlias: Optional[str] = None, userSubmitted: Optional[str] = None) -> Path:
  if(userSubmitted is None or userSubmitted is ""):
    pathToExecutable =  getoutput(f"which {executable}") or \
      getoutput(f"find $HOME -wholename '*/{executable}/*' -name '{executable}' -type f -executable") or \
      getoutput(f"find $HOME -wholename '*/{executable}/*' -name '{executableAlias}' -type f -executable")
    if (pathToExecutable == ""):
      message = f"Cannot find the executable: {executable}. Please manually specify its location in config.py"
      raise BaseException(message)
    return Path(pathToExecutable).resolve(strict=True)
  else:
    try:
      return Path(userSubmitted).resolve(strict=True)
    except Exception:
      print(f"The location you specified for {executable} (at: {userSubmitted}) could not be found.")
      raise
      

def getSpmDir(userSubmitted: str = "") -> Path:
  if (userSubmitted is ""):
    try:
      return (Path.home() / "spm12").resolve(strict=True)
    except Exception:
      print("The installation to SPM is not where it is expected. Please specify the folder in which SPM was installed.")
      raise
  else:
    try:
      return Path(userSubmitted).resolve(strict=True)
    except Exception:
      print("The SPM12 installation directory provided could not be found. Try again, providing an absolute path from root.")
      raise

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
