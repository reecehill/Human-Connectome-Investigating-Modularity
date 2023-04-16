# ----------
# These configuration parameters are:
# 1) Not intended to be edited by the user.
# 2) Generally used throughout the program.
# 3) Therefore, automatically assigned.
# ----------

from os.path import abspath, dirname, join
from typing import Optional

# ----------
# [START] DIRECTORY STRUCTURE PARAMETERS
# ----------
base_dir: str = abspath(dirname(__file__))

# This array is built, then populated by functions, then processed, then cleared. 
filesToExist: dict[str, bool | list[Optional[str]]] = {
  'processed': False,
  'items': []
}
# This array is built, then populated by functions, then processed, then cleared. 
foldersToExist: dict[str, bool | list[Optional[str]]] = {
  'processed': False,
  'items': []
}

def extendRequiredPaths(fileDirectories: list[Optional[str]] = [], filePaths: list[Optional[str]] = []):
  try: 
    foldersToExist["items"].extend(fileDirectories) # type: ignore
    filesToExist["items"].extend(filePaths) # type: ignore
    return True
  except:
    return False
    
# ----------
# [END] DIRECTORY STRUCTURE PARAMETERS
# ----------


# ----------
# [START] LOGGING PARAMETERS
# ----------
def getLogDirectoryPath(userSubmitted: str) -> str:
  logDirectoryPath = join(base_dir + "../.." + userSubmitted)
  return logDirectoryPath

# ----------
# [END] LOGGING PARAMETERS
# ----------