import config
from modules.pipeline import data, diffusion, functional, mapper, statistics

def runPipeline() -> None:
  # (1) RETRIEVE BRAIN SCAN TREE DIRECTORY.
  if (config.EAGER_LOAD_DATA): data.getData()

  # (2) PREPROCESSING DATA
  if (config.PREPROCESS): data.preprocessData()

  # (3) RUN DSI STUDIO
  # if(config.RUN_DSI_STUDIO): [diffusion.runDsiStudio(subjectId) for subjectId in config.ALL_SUBJECTS]

  # (4) RUN MATLAB: Process diffusion tracks
  if(config.RUN_MATLAB_DIFFUSION): [diffusion.matlabProcessDiffusion(subjectId) for subjectId in config.ALL_SUBJECTS]

  # (5) RUN MATLAB: Process functional data
  if(config.RUN_MATLAB_FUNCTIONAL): [functional.matlabProcessFunctional(subjectId) for subjectId in config.ALL_SUBJECTS]

  # (6) RUN MATLAB: Map functional and diffusion data
  if(config.RUN_MATLAB_MAPPING): [mapper.matlabProcessMapping(subjectId) for subjectId in config.ALL_SUBJECTS]

  # (7) GET STATISTICS
  if(config.MATLAB_CALCULATE_STATS): [statistics.matlabGetStatistics(subjectId) for subjectId in config.ALL_SUBJECTS]
  pass
