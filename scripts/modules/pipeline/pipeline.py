from types import FunctionType
from typing import Callable, Dict, List
import config
from includes.stepper.functions import updateBatchStatus
from modules.hcp_data_manager.deleter import deleteFilesByExtensions
from modules.pipeline import data, structural, tractography, diffusion, functional, modularity, mapper, statistics
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
    statistics.runStatistics: config.RUN_STATS,
}


def runPipeline() -> None:
    g.allSteps = allSteps
    for subjectBatch in config.BATCHED_SUBJECTS:
        for stepFn, runStep in allSteps.items():
            if (runStep):
                runSubjectBatchThroughStep(
                    stepFn=stepFn, subjectBatch=subjectBatch)
            else:
                g.logger.info(f'Skipping {stepFn.__name__} for all subjects')
        # TODO: optimisation -> avoid unnecessary IO.
        allSubjectsAllStepsSuccess = updateBatchStatus()
        if (allSubjectsAllStepsSuccess):
            cleanDirOfBatch(subjectBatch)
        g.logger.info(
            f"Completed batch for subjects {subjectBatch[0]}-{subjectBatch[-1]}")

    g.logger.info('Pipeline run completed.')


def runSubjectBatchThroughStep(stepFn: stepFnType, subjectBatch: List[str]) -> None:
    if (config.USE_PARALLEL_PROCESSING):
        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = [executor.submit(processSubject, stepFn, subjectId)
                       for subjectId in subjectBatch]
            for future in concurrent.futures.as_completed(futures):
                step_name: str = future.result()
                g.logger.info(f"Completed processing for {step_name}")

        # Once all subjects are processed for that step, update the batch status.
        updateBatchStatus()  # TODO: optimisation -> avoid unnecessary IO.
        g.logger.info(f"Completed batch for {stepFn.__name__}")
    else:
        for subjectId in subjectBatch:
            processSubject(stepFn=stepFn, subjectId=subjectId)
            # Once all subjects are processed for that step, update the batch status.
        g.logger.info(f"Completed batch for {stepFn.__name__}")


def processSubject(stepFn: stepFnType, subjectId: str) -> str:
    processStepFn(step=stepFn, subjectId=subjectId)
    # Return the step name for logging purposes
    return stepFn.__name__
