import config
from modules.pipeline import data, structural, tractography, diffusion, functional, modularity, mapper, statistics

def runPipeline() -> None:
  # (1) RETRIEVE BRAIN SCAN TREE DIRECTORY.
  if (config.EAGER_LOAD_DATA): data.getData()

  # (2) PREPROCESSING DATA
  if (config.PREPROCESS): data.preprocessData()

  # (2B) RUN FREESURFER: Annotate pial surface with labels
  if(config.GENERATE_LABELS): [structural.generateLabels(subjectId) for subjectId in config.ALL_SUBJECTS]
  if(config.GENERATE_LABELS): [structural.generateMni152Labels(subjectId) for subjectId in config.ALL_SUBJECTS]

  # (3) RUN DSI STUDIO
  if(config.RUN_DSI_STUDIO): [tractography.runDsiStudio(subjectId) for subjectId in config.ALL_SUBJECTS]

  # (4) RUN MATLAB: Process diffusion tracks, projecting them to nearest face and into adjacency matrices
  if(config.RUN_PROCESS_TRACTOGRAPHY): [diffusion.processDiffusionTracts(subjectId) for subjectId in config.ALL_SUBJECTS]

  # (5) RUN MATLAB: Calculate functional data, convert fMRI images to clusters
  if(config.RUN_CALC_FUNC_MODULARITY): [functional.prepareFunctionalSurfacesForModularity(subjectId) for subjectId in config.ALL_SUBJECTS]

  # (6) RUN NetworkX: Calculate structural modularity, run NETWORKX
  if(config.RUN_CALC_STRUC_MODULARITY): [modularity.calculateModularity(subjectId) for subjectId in config.ALL_SUBJECTS]

  # (7) RUN EXPORT MAPPING: Yield from previous operations .csv files: []
  if(config.RUN_MAPPING): [mapper.processMapping(subjectId) for subjectId in config.ALL_SUBJECTS]

  # (7) GET STATISTICS
  if(config.RUN_STATS): [statistics.runStatistics(subjectId) for subjectId in config.ALL_SUBJECTS]
  pass