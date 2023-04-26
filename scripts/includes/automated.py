# ----------
# These configuration parameters are:
# 1) Not intended to be edited by the user.
# 2) Generally used throughout the program.
# 3) Therefore, automatically assigned.
# ----------
try:
  from time import strftime
  from pathlib import Path
except Exception as e:
  print(e)
  exit()

def getLogDirectoryPath(userSubmitted: str) -> Path:
  LOGS_DIR: Path = (BASE_DIR / userSubmitted / TIMESTAMP_OF_SCRIPT).resolve(strict=False)
  return LOGS_DIR
def getSpmDir(userSubmitted: str = "") -> Path:
  if (userSubmitted is ""):
    try:
      return (Path.home() / "spm12").resolve(strict=True)
    except Exception as e:
      print("The installation to SPM is not where it is expected. Please specify the folder in which SPM was installed.")
      raise
  else:
    try:
      return Path(userSubmitted).resolve(strict=True)
    except Exception as e:
      print("The SPM12 installation directory provided could not be found. Try again, providing an absolute path from root.")
      raise

TIMESTAMP_OF_SCRIPT = strftime("%d%m%Y-%H%M%S")
START_A_FRESH = False

# ----------
# [START] DIRECTORY STRUCTURE PARAMETERS
# ----------
BASE_DIR: Path = Path(__file__).parent.parent.parent.resolve(strict=True)
SCRIPTS_DIR: Path = (BASE_DIR / "scripts").resolve(strict=True)
INCLUDES_DIR: Path = (SCRIPTS_DIR / "includes").resolve(strict=True)
DATA_DIR: Path = (BASE_DIR / "data").resolve(strict=True)
UPLOADS_DIR: Path = (BASE_DIR / "uploads" / TIMESTAMP_OF_SCRIPT).resolve(strict=False)


# ----------
# [END] DIRECTORY STRUCTURE PARAMETERS
# ----------


# ----------
# [START] LOGGING PARAMETERS
# ----------



# ----------
# [END] LOGGING PARAMETERS
# ----------