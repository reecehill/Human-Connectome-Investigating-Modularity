from includes.stepper.functions import allStepsAreSuccessful
from modules.pipeline.stepper import cleanDirOfBatch


def getData() -> None:
  from modules.ibc_data_manager.downloader import buildDataDirectory
  buildDataDirectory()

def preprocessData() -> None:
    pass

def cleanSubjectDirectory(subjectId: str) -> bool:
  # Delete all big data for a subject.
  # NB: This function was designed for batches, but per subject seems much better.
    # Delete subject batch once done.
  if (allStepsAreSuccessful):
    cleanDirOfBatch(subjectBatch=[subjectId])
  return True