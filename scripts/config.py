# ----------
# CONFIGURATION FILE.
# ----------

from typing import Optional
from includes.automated import *

# ----------
# [START] SYSTEM PARAMETERS
# ----------

# ----------
# [END] SYSTEM PARAMETERS
# ----------

# ----------
# [START] PARTICIPANT PARAMETERS
# ----------
PARTICIPANTS = ['sub-01', 'sub-02', 'sub-04', 'sub-05', 'sub-06', 'sub-07', 'sub-08', 'sub-09', 'sub-11', 'sub-12', 'sub-13', 'sub-14', 'sub-15']

# ----------
# [END] PARTICIPANT PARAMETERS
# ----------

# ----------
# [START] LOGGING PARAMETERS
# ----------
logDirectoryPath: str = "logs" # Relative to the uploads folder of the project, should NOT begin with /.
spmDirectoryPath: str = "" # From root, resolvable by Path.resolve(). If empty, a default is used.


EXPORT_FILES: "list[Optional[str]]" = [] #Additional files to save upon code completion.

# ----------
# [END] LOGGING PARAMETERS
# ----------


# DO NOT EDIT BELOW THIS LINE
LOGS_DIR: Path = getLogDirectoryPath(logDirectoryPath)
SPM_DIR: Path = getSpmDir(spmDirectoryPath)