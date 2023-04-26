# ----------
# CONFIGURATION FILE.
# ----------

from typing import Optional
from includes.automated import *
import includes.all_subjects

# ----------
# [START] PIPELINE PARAMETERS
# ----------
PREPROCESS = False # Not implemented
EAGER_LOAD_DATA = False # Not implemented
RUN_DSI_STUDIO = True
USE_7T_DIFFUSION = False # Bool, either True = use 7T or False = use 3T.
RUN_MATLAB_DIFFUSION = True
RUN_MATLAB_FUNCTIONAL = True
RUN_MATLAB_MAPPING = True
MATLAB_CALCULATE_STATS = True
# ----------
# [END] PIPELINE PARAMETERS
# ----------

# ----------
# [START] PROCESSING PARAMETERS
# ----------
NUMBER_OF_TRACTS = 10000000
PIAL_SURFACE_TYPE = 2 # NOTE: Anything other than 2 (int) is unsupported.
DOWNSAMPLE_SURFACE = 'yes' # NOTE: Anything other than 'yes' (str) is unsupported.
DOWNSAMPLE_RATE = 0.1 # NOTE: Default should be 0.1 (float). 
# ----------
# [END] PROCESSING PARAMETERS
# ----------


# ----------
# [START] PARTICIPANT PARAMETERS
# ----------
#ALL_SUBJECTS: "list[str]" = includes.all_subjects.all_subjects
ALL_SUBJECTS: "list[str]" = ["100610"]

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
DIFFUSION_FOLDER = getDiffusionFolder(USE_7T_DIFFUSION)