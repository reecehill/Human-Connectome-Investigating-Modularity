# ----------
# CONFIGURATION FILE.
# ----------
from typing import Optional
from parameters.automated import *

# ----------
# [START] SYSTEM PARAMETERS
# ----------

# EMPTY

# ----------
# [END] SYSTEM PARAMETERS
# ----------

# ----------
# [START] LOGGING PARAMETERS
# ----------
logDirectoryPath: str = "/" + "logs" #Must always be preceded by "/", to indicate root of project.

exportFiles: list[Optional[str]] = [] #Additional files to save upon code completion.

# ----------
# [END] LOGGING PARAMETERS
# ----------


# DO NOT EDIT BELOW THIS LINE
logDirectoryPath: str = getLogDirectoryPath(logDirectoryPath)