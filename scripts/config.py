# ----------
# CONFIGURATION FILE.
# ----------

import multiprocessing
from typing import Optional
from includes.automated import *
import includes.all_subjects


CPU_THREADS = multiprocessing.cpu_count()
#CPU_THREADS = 5

# ----------
# [START] DSI STUDIO PARAMETERS
# ----------
"""
0:DSI, 1:DTI, 2:Funk-Randon QBI, 3:Spherical Harmonic QBI, 4:GQI 6: Convert to HARDI 7:QSDR. For detail, please refer to the reconstruction page. 
"""
DSI_STUDIO_RECONSTRUCTION_METHOD = 4

"""
0:streamline (default), 1:rk4 
"""
DSI_STUDIO_TRACKING_METHOD = 1

DSI_STUDIO_FIBRE_COUNT = 10000000
DSI_STUDIO_SEED_COUNT = 1e9 # A large number to prevent DSI Studio from running forever in case no more fibres are found.
DSI_STUDIO_FA_THRESH = 0
DSI_STUDIO_OTSU_THRESH = 0.6
DSI_STUDIO_INITIAL_DIREC = 0 # initial propagation direction 0:primary fiber, 1:random, 2:all fiber orientations
DSI_STUDIO_SEED_PLAN = 0 # specify the seeding strategy 0:subvoxel random, 1:voxelwise center
DSI_STUDIO_INTERPOLATION = 0 #interpolation methods (0:trilinear, 1:gaussian radial, 2:nearest neighbor)
DSI_STUDIO_RANDOM_SEED = 0 # specify whether a timer is used for generating seed points. Setting it on (--random_seed=1) will make tracking random. The default is off. 
DSI_STUDIO_STEP_SIZE = 0.625
DSI_STUDIO_TURNING_ANGLE = 60
DSI_STUDIO_SMOOTHING =0
DSI_STUDIO_MIN_LENGTH = 10
DSI_STUDIO_MAX_LENGTH = 300
DSI_STUDIO_REF_IMG = "" # was aparc+aseg.nii.gz image.

# ----------
# [END] DSI STUDIO PARAMETERS
# ----------

# ----------
# [START] PIPELINE PARAMETERS
# ----------
PREPROCESS = False # Not implemented
EAGER_LOAD_DATA = False # Not implemented
GENERATE_LABELS = True
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
dsiStudioPath: str = "" # From root, resolvable by Path.resolve(). REQUIRED.
matlabPath: str = "" # From root, resolvable by Path.resolve(). Enter here to override automatic finding.
freesurferPath: str = "" # NOT IMPLEMENTED.

EXPORT_FILES: "list[Optional[str]]" = [] #Additional files to save upon code completion.

# ----------
# [END] LOGGING PARAMETERS
# ----------


# DO NOT EDIT BELOW THIS LINE
LOGS_DIR: Path = getLogDirectoryPath(logDirectoryPath)
SPM_DIR: Path = getSpmDir(spmDirectoryPath)

DIFFUSION_FOLDER = getDiffusionFolder(USE_7T_DIFFUSION)
DSI_STUDIO = getPathOfExecutable(executable="dsistudio", executableAlias="dsi_studio", userSubmitted=dsiStudioPath)
MATLAB = getPathOfExecutable(executable="matlab", userSubmitted=matlabPath)
FREESURFER = getPathOfExecutable(executable="freesurfer", userSubmitted=freesurferPath)