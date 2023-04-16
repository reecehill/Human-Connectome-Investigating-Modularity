# ----------
# These configuration parameters are:
# 1) Not intended to be edited by the user.
# 2) Generally used throughout the program.
# 3) Therefore, automatically assigned.
# ----------
try:
  from os.path import abspath, dirname, join
except Exception as e:
  print(e)
  exit()
# ----------
# [START] DIRECTORY STRUCTURE PARAMETERS
# ----------
base_dir: str = abspath(dirname(__file__))

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