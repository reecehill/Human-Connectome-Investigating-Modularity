from multiprocessing import current_process
from typing import Tuple
from modules.pipeline.stepper import stepFnType


def processSubject(stepFn: stepFnType, subjectId: str) -> "Tuple[str,bool]":
    from modules.pipeline.stepper import processStepFn

    try:
        current_process().name = f"Process|Sbj-{subjectId}|Fn-{stepFn.__name__}"
        step_result: bool = processStepFn(step=stepFn, subjectId=subjectId)
        return stepFn.__name__, step_result
    except Exception as e:
        import globals as g

        g.logger.error(
            f"Error in processing subject {subjectId} with {stepFn.__name__}: {e}"
        )
        raise e
