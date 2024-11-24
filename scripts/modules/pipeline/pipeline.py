from multiprocessing import current_process, log_to_stderr
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
import logging

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
    log_to_stderr(
        logging.DEBUG,
    )

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
        with concurrent.futures.ProcessPoolExecutor(
            max_workers=config.CPU_THREADS
        ) as executor:
            futures: List[concurrent.futures.Future[Tuple[str, bool]]] = []
            for subjectId in subjectBatch:
                futures.append(executor.submit(processSubject, stepFn, subjectId))
                
            try:
                for future in concurrent.futures.as_completed(
                    fs=futures
                ):  # Max 2 hours wait between a successful step completion by any subject.
                    try:
                        step_name, step_result = future.result(timeout=60 * 60 * 1)
                        g.logger.info(
                            f"Completed processing [{step_result}] for {step_name}"
                        )
                    except concurrent.futures.TimeoutError as e:
                        g.logger.error(f"A process timed out: {e}")
                    except Exception as e:
                        g.logger.error(f"An error occurred: {e}")
                        raise e
                    finally:
                        g.logger.info(
                            f"Future [done: {future.done()}] [cancelled: {future.cancelled()}]"
                        )
                        if not future.done():
                            g.logger.info(f"Future unfinished:")
                            g.logger.info(future)
                        g.logger.info("Future completed.")
            except Exception as e:
                g.logger.error(f"Error during parallel processing: {e}")
                raise e
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
