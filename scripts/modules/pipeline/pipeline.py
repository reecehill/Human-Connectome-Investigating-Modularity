from types import FunctionType
from typing import Callable, Dict, List
import config
from includes.stepper.functions import updateBatchStatus
from modules.hcp_data_manager.deleter import deleteFilesByExtensions
from modules.pipeline import data, structural, tractography, diffusion, functional, modularity, mapper, statistics
from modules.pipeline.stepper import processStep
import modules.globals as g

allSteps: Dict[Callable[[str], bool], bool] = {
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
  for stepFn, runStep in allSteps.items():
    if(runStep):
      for subjectId in config.ALL_SUBJECTS:
        processStep(step=stepFn, subjectId=subjectId)
        # Once all subjects are processed for that step, update the batch status.
        updateBatchStatus() # TODO: optimisation -> avoid unnecessary IO.  
    g.logger.info(f'Completed {stepFn.__name__} for all subjects')
  g.logger.info(f'Now deleting data that was downloaded for batch: {config.ALL_SUBJECTS[0]}-{config.ALL_SUBJECTS[-1]}')
  deleteFilesByExtensions(directory=config.SUBJECTS_DIR / '100206', extensions=[
    '*.nii', '*.nii.gz','*.gii','*.gii.nz', '*.label', '*.annot', '*.pial','*.dlabel','*.trk','*.mat','*.fib'], recursive=True, depth=-1)