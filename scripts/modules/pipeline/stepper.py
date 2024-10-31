import logging
from typing import Any, Callable, List, Literal, Optional, Tuple, Union
import config
from includes.stepper.functions import updateStepSuccessStatus, prevStepWasSuccessful
import modules.globals as g
import pandas as pd

from modules.hcp_data_manager.deleter import deleteFilesByExtensions


def prepStep(subjectId: str, stepName: str, hemisphere: "Optional[Literal['left', 'right']]" = None, task: "Optional[str]" = None) -> bool:
    # Called at every new step in pipeline.
    config.setCurrentStep(currentStep=stepName)
    subjectDir = config.SUBJECTS_DIR / subjectId
    config.setSubjectDir(subjectDir)
    config.setSubjectStepSuccess(subjectStepSuccess=None, reset=True)
    config.setCurrentSubject(subjectId)

    if (hemisphere):
        config.setCurrentHemisphere(hemisphere)
    if (task):
        config.setCurrentTask(task)

    if (prevStepWasSuccessful() is False and config.FORCE_RUN is False):
        g.logger.warning(
            f'Skipping {stepName} for subject {subjectId} as previous step failed')
        return False
    else:
        return True


def finishStep(result: bool):
    # Called at the end of every step in pipeline.
    config.setSubjectStepSuccess(subjectStepSuccess=result)

    if (prevStepWasSuccessful() is False and config.FORCE_RUN is False):
        pass
    else:
        updateStepSuccessStatus()
        g.logger.info(
            f'Completed {config.CURRENT_STEP} ({"successfully" if config.SUBJECT_STEP_SUCCESS else "failed"}) for subject {config.CURRENT_SUBJECT}')

    config.setCurrentStep(currentStep="")


stepFnType = Callable[[str], bool]


def processStepFn(step: stepFnType, subjectId: str):
    result: bool = False
    try:
        g.logger.info(f'Running {step.__name__} for subject {subjectId}')
        stepWillRun: bool = prepStep(
            subjectId=subjectId, stepName=step.__name__)
        # Call processStep
        result = step(subjectId) if stepWillRun else False
    except Exception as e:
        result = False
        g.logger.error(f"Error running step: {e}")
    finally:
        finishStep(result=result)
        return config.SUBJECT_STEP_SUCCESS


def cleanDirOfBatch(subjectBatch: List[str]):
    g.logger.info(
        f'Now deleting data that was downloaded for batch: {config.ALL_SUBJECTS[0]}-{config.ALL_SUBJECTS[-1]}')
    directoriesUsed: "List[config.Path]" = [
        config.SUBJECTS_DIR / subjectId for subjectId in subjectBatch]
    deleteFilesByExtensions(directories=directoriesUsed, extensions=[
                            '*'], recursive=True, depth=-1)
