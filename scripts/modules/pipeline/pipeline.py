from multiprocessing import current_process
from typing import Dict, List, Tuple
import config
from includes.stepper.functions import updateBatchStatus
from modules.pipeline import (
    data,
    structural,
    tractography,
    diffusion,
    functional,
    modularity,
    mapper,
    statistics,
)
from modules.pipeline.stepper import cleanDirOfBatch, processStepFn, stepFnType
import modules.globals as g
import concurrent.futures

allSteps: "Dict[stepFnType, bool]" = {
    # data.getData: config.EAGER_LOAD_DATA,
    # data.preprocessData: config.PREPROCESS,
    structural.generateLabels: config.GENERATE_LABELS,
    structural.generateMni152Labels: config.GENERATE_LABELS,
    tractography.runDsiStudio: config.RUN_DSI_STUDIO,
    diffusion.processDiffusionTracts: config.RUN_PROCESS_TRACTOGRAPHY,
    functional.prepareFunctionalSurfacesForModularity: config.RUN_CALC_FUNC_MODULARITY,
    modularity.calculateModularity: config.RUN_CALC_STRUC_MODULARITY,
    mapper.processMapping: config.RUN_MAPPING,
    data.cleanSubjectDirectory: config.RUN_CLEAN_SUBJECT_DIR,
    statistics.runStatistics: config.RUN_STATS,
}


def runPipeline() -> None:
    g.allSteps = allSteps
    for subjectBatchIndex, batchSubjects in enumerate(config.BATCHED_SUBJECTS):
        config.setCurrentBatch(str(subjectBatchIndex))

        for stepFn, runStep in allSteps.items():
            if runStep:
                runSubjectBatchThroughStep(stepFn=stepFn, subjectBatch=batchSubjects)
            else:
                g.logger.info(f"Skipping {stepFn.__name__} for all subjects")

        try:
            # Delete subject batch once done.
            allSubjectsAllStepsSuccess: bool = updateBatchStatus(
                batchSubjects=batchSubjects
            )
        except Exception as e:
            g.logger.error(f"Error updating batch status: {e}")
            allSubjectsAllStepsSuccess = False

        if allSubjectsAllStepsSuccess:
            cleanDirOfBatch(batchSubjects)
        g.logger.info(
            f"Completed batch for subjects {batchSubjects[0]}-{batchSubjects[-1]}"
        )

    g.logger.info("Pipeline run completed.")


def runSubjectBatchThroughStep(stepFn: stepFnType, subjectBatch: List[str]) -> None:
    if config.USE_PARALLEL_PROCESSING:
        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = [
                executor.submit(processSubject, stepFn, subjectId)
                for subjectId in subjectBatch
            ]
            try:
                for future in concurrent.futures.as_completed(
                    fs=futures, timeout=60 * 60 * 2
                ):  # Max 2 hours for a single subject (typical subject takes ~30min)
                    try:
                        step_name, step_result = future.result()
                        g.logger.info(f"Completed processing [{step_result}] for {step_name}")
                    except concurrent.futures.TimeoutError:
                        g.logger.error("A process timed out.")
                    except Exception as e:
                        g.logger.error(f"An error occurred: {e}")
                        raise e
                    finally:
                        g.logger.info("Future completed.")
            except Exception as e:
                g.logger.error(f"Error during parallel processing: {e}")
                raise e
            finally:
                g.logger.info("Shutting down executor.")
                executor.shutdown(wait=True)
    else:
        for subjectId in subjectBatch:
            step_name, step_result = processSubject(stepFn=stepFn, subjectId=subjectId)
            g.logger.info(f"Completed processing [{step_result}] for {step_name}")
    g.logger.info(f"Completed batch for {stepFn.__name__}")


def processSubject(stepFn: stepFnType, subjectId: str) -> "Tuple[str,bool]":
    try:
        current_process().name = f"Process|Sbj-{subjectId}|Fn-{stepFn.__name__}"
        step_result: bool = processStepFn(step=stepFn, subjectId=subjectId)
        return stepFn.__name__, step_result
    except Exception as e:
        g.logger.error(
            f"Error in processing subject {subjectId} with {stepFn.__name__}: {e}"
        )
        raise e
