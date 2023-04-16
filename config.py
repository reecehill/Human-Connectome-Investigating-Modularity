# ----------
# CONFIGURATION FILE.
# ----------
from parameters.automated import *

# ----------
# [START] SYSTEM PARAMETERS
# ----------

# ----------
# [END] SYSTEM PARAMETERS
# ----------

# ----------
# [START] LOGGING PARAMETERS
# ----------
logDirectoryPath: str = "/" + "logs" #Must always be preceded by "/", to indicate root of project.
# ----------
# [END] LOGGING PARAMETERS
# ----------


# DO NOT EDIT BELOW THIS LINE
logDirectoryPath: str = getLogDirectoryPath(logDirectoryPath)