import os
from subprocess import getoutput
from typing import Optional
from shutil import which
try:
    from pathlib import Path
    from time import strftime
except ImportError as e:
    print(e)
    exit()

# ----------
# These configuration parameters are:
# 1) Not intended to be edited by the user.
# 2) Generally used throughout the program.
# 3) Therefore, automatically assigned.
# ----------


def findAndInject(find: str, replace: str, string: str) -> str:
    return string.replace(find, replace)


def getLogDirectoryPath(userSubmitted: str) -> Path:
    LOGS_DIR: Path = (BASE_DIR / userSubmitted /
                      TIMESTAMP_OF_SCRIPT).resolve(strict=False)
    return LOGS_DIR


def getDiffusionFolder(use7TDiffusion: bool = False):
    append = ""
    if (use7TDiffusion):
        append = "_7T"
    return f'Diffusion{append}'


TIMESTAMP_OF_SCRIPT = strftime("%d%m%Y-%H%M%S")
START_A_FRESH = False


# ----------
# [START] DIRECTORY STRUCTURE PARAMETERS
# ----------
BASE_DIR: Path = Path(__file__).parent.parent.parent.resolve(strict=True)
SCRIPTS_DIR: Path = (BASE_DIR / "scripts").resolve(strict=True)
INCLUDES_DIR: Path = (SCRIPTS_DIR / "includes").resolve(strict=True)
DATA_DIR: Path = (BASE_DIR / "data").resolve(strict=True)
SUBJECTS_DIR: Path = (DATA_DIR / "subjects").resolve(strict=True)
UPLOADS_DIR: Path = (BASE_DIR / "uploads" /
                     TIMESTAMP_OF_SCRIPT).resolve(strict=False)

SUBJECT_DIR: Path = Path()
PIPELINE_SUCCESS_FILE: Path = Path()
BATCH_SUCCESS_FILE: Path = Path()
SUBJECT_STAT_DIR: Path = Path()

STAT_FILE_BY_SUBJECT: Path = DATA_DIR / f'allSubjects-{TIMESTAMP_OF_SCRIPT}.csv'
STAT_FILE_BY_MODULE: Path = DATA_DIR / f'allModules-{TIMESTAMP_OF_SCRIPT}.csv'
# [END] DIRECTORY STRUCTURE PARAMETERS
# ----------

# ----------
# [START] SUBJECT-SPECIFIC PARAMETERS
# These get continuously overwritten by any step of the pipeline to share loop information.
# ----------
CURRENT_STEP: str = ""
CURRENT_SUBJECT: str = ""
CURRENT_HEMISPHERE: str = ""
CURRENT_TASK: str = ""
CURRENT_BATCH: str = ""
# ----------
# [END] SUBJECT-SPECIFIC PARAMETERS
# ----------
# If an error occurs at any step whilst processing a subject, this is set to False. This is only set to True upon finishing a step. Thus, "None" indicates termination mid-step.
SUBJECT_PIPELINE_SUCCESS: "Optional[bool]" = None
# If an error occurs during the step whilst processing a subject, this is set to 1.
SUBJECT_STEP_SUCCESS: "Optional[bool]" = None

# ----------


def splitIntoBatches(data: "list[str]", numBatches: int) -> "list[list[str]]":
    """
    Split a list of strings into no more than `numBatches` total batches.

    Parameters:
    - data: The list of strings to split.
    - numBatches: The maximum number of batches to split the list into.

    Returns:
    - A list of batches (list of lists).
    """
    # Calculate the approximate size of each batch
    batchSize = len(data) // numBatches + (1 if len(data) %
                                           numBatches != 0 else 0)

    # Split the list into batches
    batches = [data[i:i + batchSize] for i in range(0, len(data), batchSize)]

    return batches


# ----------
# [START] EXECUTABLE PATHS
# ----------
def getPathOfExecutable(executable: str, executableAlias: "Optional[str]" = None, userSubmitted: "Optional[str]" = None) -> Path:
    if (userSubmitted is None or userSubmitted == ""):
        pathToExecutable =  \
            which(executable) or \
            getoutput(f"find $HOME -wholename '*/{executable}/*' -name '{executableAlias}' -type f -executable") or \
            getoutput(f"find $HOME -wholename '*/{executable}/*' -name '{executableAlias}' -type f -executable") or \
            getoutput(f"find $HOME -wholename '*/{executable}/*' -name '{executable}' -type f -executable") or \
            getoutput(
                f"find $HOME -wholename '*/{executableAlias}/*' -name '{executable}' -type f -executable")
        # If the pathToExecutable is a string and contains data after being stripped of white space.
        if (isinstance(pathToExecutable, str) and pathToExecutable.strip()):  # type: ignore #
            print(f'Path to {executable} is {pathToExecutable}')
            return Path(pathToExecutable).resolve(strict=True)
        else:
            message = f"Cannot find the executable: {executable}. Please specify or correct the location in config.py"
            raise BaseException(message)
    else:
        if (Path(userSubmitted).exists()):
            return Path(userSubmitted).resolve(strict=True)
        else:
            print(
                f"The location you specified for {executable} (at: {userSubmitted}) could not be found.")
            print(
                f"Parent contents ({userSubmitted}/../) [ls -la {userSubmitted}/../]:")
            print(getoutput(f"ls -la {userSubmitted}/../"))
            print(f"Attempting to find {executable} using default settings...")
            return getPathOfExecutable(executable=executable, executableAlias=executableAlias, userSubmitted="")


def getSpmDir(userSubmitted: str = "") -> Path:
    if (userSubmitted == ""):
        try:
            return (Path.home() / "spm12").resolve(strict=True)
        except Exception:
            print("The installation to SPM is not where it is expected. Please specify or re-check the folder in which SPM was installed.")
            raise
    else:
        try:
            #  Retry using default settings ("") if not user specified path doesn't exist.
            return Path(userSubmitted).resolve(strict=True) if Path(userSubmitted).exists() else getSpmDir(userSubmitted="")
        except Exception:
            print("The SPM12 installation directory provided could not be found. Try again, providing an absolute path from root.")
            raise


def getNativeOrMni152Folder(isMni152: bool) -> str:
    return "MNINonLinear" if (isMni152) else "T1w"

# ----------
# [END] EXECUTABLE PATHS
# ----------


# ----------
# [START] SETTING ENVIRONMENT VARIABLES
# ----------
os.environ["SUBJECTS_DIR"] = str(SUBJECTS_DIR)
# ----------
# [END] SETTING ENVIRONMENT VARIABLES
# ----------

matLabDriveAndPathToSubjects = str((
    DATA_DIR / 'subjects').resolve(strict=True))+"/"
matlabScriptsFolder = str((SCRIPTS_DIR / "matlab").resolve(strict=True))
