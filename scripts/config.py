# ----------
# CONFIGURATION FILE.
# ----------

from multiprocessing import cpu_count
from typing import Literal, Optional, Union
from includes.automated import *
from includes.all_subjects import all_healthy_young_adults
import modules.globals as g

CPU_THREADS: int = cpu_count() - 2

FORCE_RUN: bool = (
    False  # By enabling this feature, steps will proceed even if their previous steps do not have a "success" status.
)
USE_PARALLEL_PROCESSING: bool = True
COMPRESS_FILE: bool = (
    True  # Compress files on-the-fly where possible. Recommended to only disable this for debugging.
)
# CPU_THREADS = 10

USE_7T_DIFFUSION: bool = False  # Bool, either True = use 7T or False = use 3T.
# Bool, either True = coregister data to MNI152 space first.
NORMALISE_TO_MNI152: bool = True

# ----------
# [START] DSI STUDIO PARAMETERS
# ----------
"""
0:DSI, 1:DTI, 2:Funk-Randon QBI, 3:Spherical Harmonic QBI, 4:GQI 6: Convert to HARDI 7:QSDR. For detail, please refer to the reconstruction page. 
"""
DSI_STUDIO_RECONSTRUCTION_METHOD: int = 4  # was 7
DSI_STUDIO_TRACKING_METHOD: int = 0  # 0:streamline (default), 1:rk4
# int: number of times dsi studio is ran to track fibres (thus total fibres = DSI_STUDIO_ITERATION_COUNT * DSI_STUDIO_FIBRE_COUNT)
DSI_STUDIO_ITERATION_COUNT: int = 1
DSI_STUDIO_FIBRE_COUNT: int = 500000
# DSI_STUDIO_FIBRE_COUNT = 1000
# True: Use DSI Studio's reconstruction algorithm. False: Convert bedpostX file to DSI Studio format.
DSI_STUDIO_USE_RECONST: bool = False
# A large number to prevent DSI Studio from running forever in case no more fibres are found.
DSI_STUDIO_SEED_COUNT: float = 1e9
DSI_STUDIO_FA_THRESH: int = 0
DSI_STUDIO_CHECK_ENDING: int = 1
DSI_STUDIO_OTSU_THRESH: float = 0.6
# initial propagation direction 0:primary fiber, 1:random, 2:all fiber orientations
DSI_STUDIO_INITIAL_DIREC: int = 0
# specify the seeding strategy 0:subvoxel random, 1:voxelwise center
DSI_STUDIO_SEED_PLAN: int = 0
# interpolation methods (0:trilinear, 1:gaussian radial, 2:nearest neighbor)
DSI_STUDIO_INTERPOLATION: int = 0
# specify whether a timer is used for generating seed points. Setting it on (--random_seed=1) will make tracking random. The default is off.
DSI_STUDIO_RANDOM_SEED: int = 0
DSI_STUDIO_STEP_SIZE: float = 0.625
DSI_STUDIO_TURNING_ANGLE: int = 60
DSI_STUDIO_SMOOTHING: int = 0
DSI_STUDIO_MIN_LENGTH: int = 10
DSI_STUDIO_MAX_LENGTH: int = 300
# was aparc+aseg.nii.gz image. Relative from T1w/ folder.
DSI_STUDIO_REF_IMG: str = "T1w_restore_brain.nii.gz"
# DSI_STUDIO_REF_IMG = "aparc+aseg.nii.gz" # was aparc+aseg.nii.gz image. Relative from T1w/ folder.
DSI_STUDIO_ANNOTATED_IMG: str = "aparc+aseg.nii.gz"
DSI_STUDIO_USE_ROI: bool = True
# ----------
# [END] DSI STUDIO PARAMETERS
# ----------

# ----------
# [START] NETWORKX PARAMETERS
# ----------
# louvain_communities, leiden_communities, scan, frc_fgsn, fast_label_propagation_communities, girvan_newman, k_clique_communities, greedy_modularity_communities
NETWORKX_ALGORITHM: str = "leiden_communities"
NETWORKX_GAMMA_START = 0.2
NETWORKX_GAMMA_END = 1.2
NETWORKX_GAMMA_STEP = 0.2
NETWORKX_ITERATION_COUNT = 2
NETWORKX_MAX_LEVEL: "Union[int,None]" = 5
NETWORKX_FLUID_K: int = 3
# ----------
# [END] NETWORKX PARAMETERS
# ----------

# ----------
# [START] PIPELINE PARAMETERS
# ----------
PREPROCESS = False  # Not implemented
EAGER_LOAD_DATA = False  # Not implemented
GENERATE_LABELS = True
RUN_DSI_STUDIO = True
RUN_PROCESS_TRACTOGRAPHY = True
RUN_CALC_FUNC_MODULARITY = True
RUN_CALC_STRUC_MODULARITY = True
RUN_MAPPING = True
RUN_CLEAN_SUBJECT_DIR = True
RUN_STATS = True
# ----------
# [END] PIPELINE PARAMETERS
# ----------

# ----------
# [START] FINDING MODULARITY (NETWORKX) PARAMETERS
# ----------
L_MATRIX = "adj_matrix_wei_roiL"  # adj_matrix_wei_roiL, adj_matrix_bin_roiL
R_MATRIX = "adj_matrix_wei_roiR"  # adj_matrix_wei_roiR, adj_matrix_bin_roiR
# ----------
# [END] FINDING MODULARITY (NETWORKX) PARAMETERS
# ----------

# ----------
# [START] FMRI PARAMETERS
# ----------
DESIRED_FMRI_MAPS: "list[str]" = [
    "$subjectId$_tfMRI_MOTOR_level2_LF-AVG_hp200_s2_MSMAll",
    "$subjectId$_tfMRI_MOTOR_level2_RF-AVG_hp200_s2_MSMAll",
    "$subjectId$_tfMRI_MOTOR_level2_LH-AVG_hp200_s2_MSMAll",
    "$subjectId$_tfMRI_MOTOR_level2_RH-AVG_hp200_s2_MSMAll",
    "$subjectId$_tfMRI_MOTOR_level2_T-AVG_hp200_s2_MSMAll",
]  # See tfMRI_MOTOR_LR_hp200_s2_level1.fsf for outputted contrasts from FSL. This variable filters out unwanted contrasts (e.g., negative contrasts). Useful when using preprocessed data that contains more than needed.
# fMRI values above this percentile will indicate a cluster.
CLUSTER_THRESHOLD: float = 50
# fMRI values above this area (mm) will indicate a cluster.
CLUSTER_MIN_AREA: float = 5.0
# ----------
# [END] FMRI PARAMETERS
# ----------


# ----------
# [START] PROCESSING PARAMETERS
# ----------
HEMISPHERES: "list[Literal['left','right']]" = ["left", "right"]
# per hemisphere (32, 59, 164). NOTE: Only 59k is supported for now.
NUMBER_OF_NODES = 59
PIAL_SURFACE_TYPE = 1  # NOTE: Anything other than 1 or 2 (int) is unsupported.
# NOTE: Anything other than 'yes' (str) is unsupported.
DOWNSAMPLE_SURFACE = "yes"
DOWNSAMPLE_RATE = 0.1  # NOTE: Default should be 0.1 (float).
# (int) If 1, the below downsamples meshes will be imported as a low-res mesh. If 0 (false), they will be created by the downsample_rate of the pial surface.
USE_PRESET_DOWNSAMPLED_MESH = 1
# IMPORTANT: Filenames may use the $subjectId$ placeholder to dynamically insert subject's id.
IMAGES: dict[str, dict[str, dict[str, dict[str, str]]]] = {
    "FMRI": {
        "LOW_RES": {
            "SURFACE": {
                # (string) Relative to the main (root) folder of each subject
                "FOLDER": "MNINonLinear/fsaverage_LR32k",
                # Relative to IMAGES["FMRI"]["LOW_RES"]["SURFACE"]["FOLDER"]
                "L_HEMISPHERE_PATH": "$subjectId$.L.pial_MSMAll.32k_fs_LR.surf.gii",
                # Relative to IMAGES["FMRI"]["LOW_RES"]["SURFACE"]["FOLDER"]
                "R_HEMISPHERE_PATH": "$subjectId$.R.pial_MSMAll.32k_fs_LR.surf.gii",
            },
            "DATA": {
                # (string) Relative to the main (root) folder of each subject
                "FOLDER": "MNINonLinear/Results/tfMRI_MOTOR/tfMRI_MOTOR_hp200_s2_level2_MSMAll.feat",
                # (string) .dscalar.nii (cifti) format with same number of faces/nodes (i.e., be compatible with) the low_res surface. Path relative to IMAGES["FMRI"]["LOW_RES"]["DATA"]["FOLDER"].
                "PATH": "$subjectId$_tfMRI_MOTOR_level2_hp200_s2_MSMAll.dscalar.nii",
            },
            "LABEL": {
                "FOLDER": "MNINonLinear/fsaverage_LR32k/",
                "L_PATH": "$subjectId$.L.aparc.32k_fs_LR.label.gii",
                "R_PATH": "$subjectId$.R.aparc.32k_fs_LR.label.gii",
                "CIFTI_PATH": "$subjectId$.aparc.32k_fs_LR.dlabel.nii",
                "L_SHAPE": "$subjectId$.L.shape.gii",
                "R_SHAPE": "$subjectId$.R.shape.gii",
                # When selecting a label, this is the name of the resulting mask file.
                "L_MASK": "L.precentral.dscalar.nii",
                # When selecting a label, this is the name of the resulting mask file.
                "R_MASK": "R.precentral.dscalar.nii",
                # When selecting a label, this is the name of the resulting mask file.
                "LR_MASK": "LR.precentral.dscalar.nii",
            },
        },
        "HIGH_RES": {
            "SURFACE": {
                # (string) Relative to the main (root) folder of each subject
                "FOLDER": "MNINonLinear/",
                # Relative to IMAGES["FMRI"]["HIGH_RES"]["SURFACE"]["FOLDER"]
                "L_HEMISPHERE_PATH": "$subjectId$.L.pial_MSMAll.164k_fs_LR.surf.gii",
                # Relative to IMAGES["FMRI"]["HIGH_RES"]["SURFACE"]["FOLDER"]
                "R_HEMISPHERE_PATH": "$subjectId$.R.pial_MSMAll.164k_fs_LR.surf.gii",
            },
            "DATA": {
                # (string) Relative to the main (root) folder of each subject. Will be created at runtime.
                "FOLDER": "MNINonLinear/Results/HiResAutoGenerated_tfMRI_MOTOR",
                # (string) .dscalar.nii (cifti) format with same number of faces/nodes (i.e., be compatible with) the high_res surface. Path relative to IMAGES["FMRI"]["HIGH_RES"]["DATA"]["FOLDER"].
                "PATH": "$subjectId$_tfMRI_MOTOR_level2_hp200_s2_MSMAll.dscalar.nii",
            },
        },
        "COMMON_RES": {  # For a mesh that is common to all imaging modalities, based on structural data.
            "SURFACE": {
                # (string) Relative to the main (root) folder of each subject
                "FOLDER": "T1w/",
                # Relative to IMAGES["FMRI"]["COMMON_RES"]["SURFACE"]["FOLDER"]
                "L_HEMISPHERE_PATH": "automated.L.pial.variableNodes.surf.gii",
                # Relative to IMAGES["FMRI"]["COMMON_RES"]["SURFACE"]["FOLDER"]
                "R_HEMISPHERE_PATH": "automated.R.pial.variableNodes.surf.gii",
            },
            "DATA": {
                # (string) Relative to the main (root) folder of each subject. Will be created at runtime.
                "FOLDER": "T1w/Results/tfMRI_MOTOR/tfMRI_MOTOR_hp200_s2_level2_MSMAll.feat/",
                # (string) .dscalar.nii (cifti) format with same number of faces/nodes (i.e., be compatible with) as COMMON_RES surface. Path relative to IMAGES["FMRI"]["COMMON_RES"]["DATA"]["FOLDER"].
                "SCALAR_FOLDER": "scalar/",
                # (string) .dscalar.nii (cifti) format with same number of faces/nodes (i.e., be compatible with) the COMMON_RES surface. Path relative to IMAGES["FMRI"]["COMMON_RES"]["DATA"]["FOLDER"].
                "MODULES_FOLDER": "clusters/",
            },
        },
    },
    "DIFFUSION": {
        "STANDARD_RES": {
            "DATA": {"FOLDER": "", "PATH": ""},
            "NODIF_BRAIN_MASK": {
                "FOLDER": "T1w/Diffusion/",
                # This is just used to get an image of same dimensions as diffusion data (its filesize is KB)!
                "PATH": "nodif_brain_mask.nii.gz",
            },
        }
    },
    "T1w": {
        "STANDARD_RES": {
            "MASKS": {
                "ALL_LABELS": "aparc+aseg.nii.gz",
                "LEFT": "lh_precentral.mask.nii.gz",
                "RIGHT": "rh_precentral.mask.nii.gz",
                "LEFT_INVERSED": "inversed_lh_precentral.mask.nii.gz",
                "RIGHT_INVERSED": "inversed_rh_precentral.mask.nii.gz",
                "ROI_INVERSED": "none_roi.mask.nii.gz",
            }
        }
    },
}
TRANSFORMS: dict[str, dict[str, str]] = {
    "INTRA_SUBJECT": {
        # (string) Relative to the main (root) folder of each subject
        "FOLDER": "MNINonLinear/xfms",
        "ACPC_DC2STANDARD": "acpc_dc2standard.nii.gz",  # Nifti file format
        "STANDARD2ACPC_DC": "standard2acpc_dc.nii.gz",  # Nifti file format
    }
}

# NOTE: fMRI activations above (>) this value will become "1", otherwise "0".
FMRI_THRESHOLD_TO_BINARISE = 1.0

# ----------
# [END] PROCESSING PARAMETERS
# ----------


# ----------
# [START] PARTICIPANT PARAMETERS
# ----------
ALL_SUBJECTS: "list[str]" = all_healthy_young_adults[:200]
# ALL_SUBJECTS: "list[str]" = [all_healthy_young_adults[2]]
# ALL_SUBJECTS: "list[str]" = ["100408"]
SUBJECTS_INTO_N_BATCHES: int = 25  # Number of batches

# ALL_FMRI_TASKS must have a corresponding timing file (.txt) of the same name.
# lf=left foot; rf=right foot; lh=left hand; rh=right hand; t=tongue;
ALL_FMRI_TASKS: "list[str]" = ["lf", "rf", "lh", "rh", "t"]
# ----------
# [END] PARTICIPANT PARAMETERS
# ----------

# ----------
# [START] LOGGING PARAMETERS
# ----------

# In a scenario where the cmd prompt is not easily accessible (e.g., a colleague running code on your behalf), it can be useful to upload the logs as they occur (and upon failure) to a remote system that you do have access to. This is disabled by default. See .env for SSH credentials.
logUsingSSH: bool = False
# Relative to the uploads folder of the project, should NOT begin with /.
logDirectoryPath: str = "logs"
# From root, resolvable by Path.resolve(). If empty, a default is used.
spmDirectoryPath: str = "/gpfs01/software/imaging/spm12"
# From root, to the executable file, resolvable by Path.resolve(). REQUIRED.
dsiStudioPath: str = "/software/imaging/dsi-studio/20240424/bin/dsi_studio"
# From root, resolvable by Path.resolve(). Enter here to override automatic finding.
matlabPath: str = "/gpfs01/software/matlab_r2022a/bin/matlab"
# matlabPath: str = "" # From root, resolvable by Path.resolve(). Enter here to override automatic finding.
# From root, resolvable by Path.resolve(). Enter here to override automatic finding.
wbCommandPath: str = (
    "/gpfs01/software/imaging/workbench/workbench-1.5.0/bin_rh_linux64/wb_command"
)
# wbCommandPath: str = "" # From root, resolvable by Path.resolve(). Enter here to override automatic finding.
# freesurferPath: str = "/gpfs01/software/freesurfer-v6.0.0" # NOT IMPLEMENTED.


# Additional files to save upon code completion.
EXPORT_FILES: "list[Optional[str]]" = []

# ----------
# [END] LOGGING PARAMETERS
# ----------

# ----------
# [START] STATISTICS PARAMETERS
# ----------
CALC_DEPRECATED_STATS: bool = False
# ----------
# [END] STATISTICS PARAMETERS
# ----------


# DO NOT EDIT BELOW THIS LINE
BATCHED_SUBJECTS: "list[list[str]]" = splitIntoBatches(
    ALL_SUBJECTS, SUBJECTS_INTO_N_BATCHES
)
LOGS_DIR: Path = getLogDirectoryPath(logDirectoryPath)
logDirectoryPath = str(LOGS_DIR)

SPM_DIR: Path = getSpmDir(spmDirectoryPath)
spmDirectoryPath = str(SPM_DIR)

NATIVEORMNI152FOLDER: str = getNativeOrMni152Folder(NORMALISE_TO_MNI152)
DIFFUSION_FOLDER: str = getDiffusionFolder(USE_7T_DIFFUSION)

DSI_STUDIO: Path = getPathOfExecutable(
    executable="dsi_studio",
    executableAlias="dsi-studio",
    userSubmitted=dsiStudioPath,
    shouldFind=RUN_DSI_STUDIO,
)
dsiStudioPath = str(DSI_STUDIO)

MATLAB: Path = getPathOfExecutable(executable="matlab", userSubmitted=matlabPath)
matlabPath = str(MATLAB)

WB_COMMAND: Path = getPathOfExecutable(
    executable="wb_command", userSubmitted=wbCommandPath
)
wbCommandPath = str(WB_COMMAND)

# COMPOSITE PATHS DEPENDANT ON PREV PATHS
FMRI_SCALAR_PATH_CORTICAL: str = str(
    Path(IMAGES["FMRI"]["LOW_RES"]["DATA"]["FOLDER"])
    / IMAGES["FMRI"]["LOW_RES"]["DATA"]["PATH"]
).replace(".dscalar.nii", "_ROI.dscalar.nii")
# FREESURFER = getPathOfExecutable(executable="freesurfer", userSubmitted=freesurferPath)


def setCurrentBatch(currentBatch: str) -> None:
    global CURRENT_BATCH
    global BATCH_SUCCESS_FILE
    CURRENT_BATCH = currentBatch
    BATCH_SUCCESS_FILE = (
        DATA_DIR / f"batchSuccess-{CURRENT_BATCH}-{TIMESTAMP_OF_SCRIPT}.csv"
    )


def setSubjectDir(subjectDir: Path = Path("/path-not-given")):
    global SUBJECT_DIR
    global PIPELINE_SUCCESS_FILE
    SUBJECT_DIR = subjectDir
    PIPELINE_SUCCESS_FILE = subjectDir / "pipeline_success.csv"


def setStatDir(statDir: Path = Path("/path-not-given")) -> None:
    global SUBJECT_STAT_DIR
    SUBJECT_STAT_DIR = statDir


def setCurrentStep(currentStep: str) -> None:
    global CURRENT_STEP
    CURRENT_STEP = currentStep


def updateLoggerExtra():
    g.logger.extra = {  # type: ignore
        "ADDITIONAL": f"[s-{CURRENT_SUBJECT}:h-{CURRENT_HEMISPHERE}:t-{CURRENT_TASK}]"
    }


def setCurrentSubject(subjectId: str):
    global CURRENT_SUBJECT
    CURRENT_SUBJECT = subjectId
    updateLoggerExtra()


def setCurrentHemisphere(hemisphere: str) -> None:
    global CURRENT_HEMISPHERE
    CURRENT_HEMISPHERE = hemisphere if hemisphere else ""
    updateLoggerExtra()


def setCurrentTask(task: str) -> None:
    global CURRENT_TASK
    CURRENT_TASK = task if task else ""
    updateLoggerExtra()


def setSubjectStepSuccess(
    subjectStepSuccess: Optional[bool], reset: bool = False
) -> None:
    global SUBJECT_STEP_SUCCESS
    if SUBJECT_STEP_SUCCESS == None:
        # Variable has been initialised for the step, and the step is mid-run.
        SUBJECT_STEP_SUCCESS = subjectStepSuccess

    elif SUBJECT_STEP_SUCCESS == False:
        # Step has failed already.
        if reset:
            SUBJECT_STEP_SUCCESS = subjectStepSuccess
        else:
            raise ValueError(
                "Trying to overwrite SUBJECT_STEP_SUCCESS variable in non-overwrite context."
            )

    elif SUBJECT_STEP_SUCCESS == True:
        if reset:
            SUBJECT_STEP_SUCCESS = subjectStepSuccess
        else:
            raise ValueError(
                "Trying to overwrite SUBJECT_STEP_SUCCESS variable in non-overwrite context."
            )
    else:
        raise ValueError(
            "Invalid value for SUBJECT_STEP_SUCCESS. Expected bool, got {}.".format(
                type(SUBJECT_STEP_SUCCESS)
            )
        )
