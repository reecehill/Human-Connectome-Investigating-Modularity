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
# [START] LOGGING PARAMETERS
# ----------
logDirectoryPath: str = "logs" # Relative to the uploads folder of the project, should NOT begin with /.

EXPORT_FILES: "list[Optional[str]]" = [] #Additional files to save upon code completion.

# ----------
# [END] LOGGING PARAMETERS
# ----------


# DO NOT EDIT BELOW THIS LINE
LOGS_DIR: Path = getLogDirectoryPath(logDirectoryPath)