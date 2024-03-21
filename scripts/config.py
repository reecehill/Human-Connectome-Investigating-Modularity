# ----------
# CONFIGURATION FILE.
# ----------

import multiprocessing
from typing import Optional
from includes.automated import *
# import includes.all_subjects


CPU_THREADS = multiprocessing.cpu_count()
#CPU_THREADS = 5

USE_7T_DIFFUSION = False # Bool, either True = use 7T or False = use 3T.
NORMALISE_TO_MNI152 = True # Bool, either True = coregister data to MNI152 space first. 

# ----------
# [START] DSI STUDIO PARAMETERS
# ----------
"""
0:DSI, 1:DTI, 2:Funk-Randon QBI, 3:Spherical Harmonic QBI, 4:GQI 6: Convert to HARDI 7:QSDR. For detail, please refer to the reconstruction page. 
"""
DSI_STUDIO_RECONSTRUCTION_METHOD = 4 #was 7

"""
0:streamline (default), 1:rk4 
"""
DSI_STUDIO_TRACKING_METHOD = 0

DSI_STUDIO_FIBRE_COUNT = 10000000
#DSI_STUDIO_FIBRE_COUNT = 1000
DSI_STUDIO_USE_RECONST = True # True: Use DSI Studio's reconstruction algorithm. False: Convert bedpostX file to DSI Studio format.
DSI_STUDIO_SEED_COUNT = 1e9 # A large number to prevent DSI Studio from running forever in case no more fibres are found.
DSI_STUDIO_FA_THRESH = 0
DSI_STUDIO_OTSU_THRESH = 0.6
DSI_STUDIO_INITIAL_DIREC = 0 # initial propagation direction 0:primary fiber, 1:random, 2:all fiber orientations
DSI_STUDIO_SEED_PLAN = 0 # specify the seeding strategy 0:subvoxel random, 1:voxelwise center
DSI_STUDIO_INTERPOLATION = 0 #interpolation methods (0:trilinear, 1:gaussian radial, 2:nearest neighbor)
DSI_STUDIO_RANDOM_SEED = 0 # specify whether a timer is used for generating seed points. Setting it on (--random_seed=1) will make tracking random. The default is off. 
DSI_STUDIO_STEP_SIZE = 0.625
DSI_STUDIO_TURNING_ANGLE = 60
DSI_STUDIO_SMOOTHING = 0
DSI_STUDIO_MIN_LENGTH = 10
DSI_STUDIO_MAX_LENGTH = 300
DSI_STUDIO_REF_IMG = "T1w_restore_brain.nii.gz" # was aparc+aseg.nii.gz image. Relative from T1w/ folder.
#DSI_STUDIO_REF_IMG = "aparc+aseg.nii.gz" # was aparc+aseg.nii.gz image. Relative from T1w/ folder.
DSI_STUDIO_ANNOTATED_IMG = "aparc+aseg.nii.gz"
DSI_STUDIO_USE_ROI = False
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
RUN_MATLAB_DIFFUSION = True
RUN_MATLAB_FUNCTIONAL = True
RUN_MATLAB_MAPPING = False
MATLAB_CALCULATE_STATS = False
# ----------
# [END] PIPELINE PARAMETERS
# ----------

# ----------
# [START] PROCESSING PARAMETERS
# ----------
#NUMBER_OF_TRACTS = 10000000
NUMBER_OF_TRACTS = 1000 # Not implemented.
NUMBER_OF_NODES = 59 # per hemisphere (32, 59, 164). NOTE: Only 59k is supported for now.
PIAL_SURFACE_TYPE = 1 # NOTE: Anything other than 2 (int) is unsupported.
DOWNSAMPLE_SURFACE = 'yes' # NOTE: Anything other than 'yes' (str) is unsupported.
DOWNSAMPLE_RATE = 0.1 # NOTE: Default should be 0.1 (float). 
USE_PRESET_DOWNSAMPLED_MESH = 1 # (int) If 1, the below downsamples meshes will be imported as a low-res mesh. If 0 (false), they will be created by the downsample_rate of the pial surface.
# IMPORTANT: Filenames may use the $subjectId$ placeholder to dynamically insert subject's id.
LOW_RES_SURFACE_FOLDER = "MNINonLinear/fsaverage_LR32k" # (string) Relative to the main (root) folder of each subject
LOW_RES_SURFACE_LEFT_HEMISPHERE_FILENAME: str = '$subjectId$.L.pial.32k_fs_LR.surf.gii' # (string) Filename of low-resolution surface of left-hemisphere.
LOW_RES_SURFACE_RIGHT_HEMISPHERE_FILENAME: str = '$subjectId$.R.pial.32k_fs_LR.surf.gii' # (string) Filename to low-resolution surface of right-hemisphere. .surf.gii
HIGH_RES_SURFACE_FOLDER: str = 'MNINonLinear' # (string) Relative to the main (root) folder of each subject
HIGH_RES_SURFACE_LEFT_HEMISPHERE_FILENAME: str = '$subjectId$.L.pial_MSMAll.164k_fs_LR.surf.gii' # NOTE: '{subjectId}.' will be prepended.
HIGH_RES_SURFACE_RIGHT_HEMISPHERE_FILENAME: str = '$subjectId$.R.pial_MSMAll.164k_fs_LR.surf.gii' # NOTE: '{subjectId}.' will be prepended.
FMRI_DATA_FOLDER: str = "MNINonLinear/Results/tfMRI_MOTOR/tfMRI_MOTOR_hp200_s2_level2_MSMAll.feat" # (string) Relative to the main (root) folder of each subject
FMRI_DATA_FILENAME: str = "$subjectId$_tfMRI_MOTOR_level2_hp200_s2_MSMAll.dscalar.nii" # (string) Is a dscalar.nii (cifti) format, and must have same number of faces/nodes (i.e., be compatible with) the surface defined in LOW_RES_SURFACE_LEFT_HEMISPHERE_FILENAME. 
FMRI_THRESHOLD_TO_BINARISE = 1.0 # NOTE: fMRI activations above (>) this value will become "1", otherwise "0". 

# ----------
# [END] PROCESSING PARAMETERS
# ----------


# ----------
# [START] PARTICIPANT PARAMETERS
# ----------
#ALL_SUBJECTS: "list[str]" = includes.all_subjects.all_subjects
ALL_SUBJECTS: "list[str]" = ["100610"]
# ALL_FMRI_TASKS must have a corresponding timing file (.txt) of the same name.
ALL_FMRI_TASKS: "list[str]" = ["lf","rf","lh","rh","t"] # lf=left foot; rf=right foot; lh=left hand; rh=right hand; t=tongue;
# ----------
# [END] PARTICIPANT PARAMETERS
# ----------

# ----------
# [START] LOGGING PARAMETERS
# ----------
logDirectoryPath: str = "logs" # Relative to the uploads folder of the project, should NOT begin with /.
spmDirectoryPath: str = "/gpfs01/software/spm12" # From root, resolvable by Path.resolve(). If empty, a default is used.
dsiStudioPath: str = "/gpfs01/software/imaging/dsi-studio/20221110/bin/dsi_studio" # From root, to the executable file, resolvable by Path.resolve(). REQUIRED.
#matlabPath: str = "/gpfs01/software/matlab_r2021a" # From root, resolvable by Path.resolve(). Enter here to override automatic finding.
matlabPath: str = "" # From root, resolvable by Path.resolve(). Enter here to override automatic finding.
# freesurferPath: str = "/gpfs01/software/freesurfer-v6.0.0" # NOT IMPLEMENTED.

EXPORT_FILES: "list[Optional[str]]" = [] #Additional files to save upon code completion.

# ----------
# [END] LOGGING PARAMETERS
# ----------


# DO NOT EDIT BELOW THIS LINE
LOGS_DIR: Path = getLogDirectoryPath(logDirectoryPath)
SPM_DIR: Path = getSpmDir(spmDirectoryPath)
NATIVEORMNI152FOLDER: str = getNativeOrMni152Folder(NORMALISE_TO_MNI152)
DIFFUSION_FOLDER = getDiffusionFolder(USE_7T_DIFFUSION)
DSI_STUDIO = getPathOfExecutable(executable="dsi_studio", executableAlias="dsi-studio", userSubmitted=dsiStudioPath)
MATLAB = getPathOfExecutable(executable="matlab", userSubmitted=matlabPath)
# FREESURFER = getPathOfExecutable(executable="freesurfer", userSubmitted=freesurferPath)