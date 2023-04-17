# ----------
# These configuration parameters are:
# 1) Not intended to be edited by the user.
# 2) Generally used throughout the program.
# 3) Therefore, automatically assigned.
# ----------
try:
  from pathlib import Path
except Exception as e:
  print(e)
  exit()

# ----------
# [START] DIRECTORY STRUCTURE PARAMETERS
# ----------
SCRIPTS_DIR: Path = Path(__file__).parent.parent.resolve(strict=True)
UPLOADS_DIR: Path = SCRIPTS_DIR.parent / "uploaded"
#base_dir: str = abspath(join(dirname(__file__) + "/../"))

# ----------
# [END] DIRECTORY STRUCTURE PARAMETERS
# ----------


# ----------
# [START] LOGGING PARAMETERS
# ----------


def getLogDirectoryPath(userSubmitted: str) -> Path:
  LOGS_DIR: Path = (UPLOADS_DIR / userSubmitted).resolve(strict=False)
  return LOGS_DIR

# ----------
# [END] LOGGING PARAMETERS
# ----------