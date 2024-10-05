import itertools
from modules.pipeline.stepper import finishStep
from python.non_spatial_stats import runTests
from pathlib import Path
import config
from modules.file_directory.file_directory import createDirectories
from modules.subprocess_caller.call import *
from modules.hcp_data_manager.downloader import getFile

def runStatistics(subjectId: str) -> bool:
  statDir = config.SUBJECT_DIR / 'statistics'
  for hemisphere in config.HEMISPHERES:
    createDirectories(directoryPaths=[statDir / f'{hemisphere}_hemisphere' ], createParents=True, throwErrorIfExists=False)
  config.setStatDir(statDir.resolve(strict=True))

  return nonSpatialStatsPerTask(subjectId) and \
    runDeprecatedStats(subjectId)
  
def nonSpatialStatsPerTask(subjectId: str) -> bool:  
  allIterations = list(itertools.product(config.HEMISPHERES, config.ALL_FMRI_TASKS))
  statSuccess: "list[bool]" = [False for _ in range(len(allIterations))]
  for iterationI, iteration in enumerate(allIterations):
    hemisphere = iteration[0]
    task = iteration[1]
    config.setCurrentHemisphere(hemisphere)
    config.setCurrentTask(task)
    
    pathToXCsv: Path = (config.SUBJECT_DIR / 'exported_modules' / f'{hemisphere}_structural_modules.csv').resolve(strict = True)
    pathToYCsv: Path = (config.SUBJECT_DIR / 'exported_modules' / f'{hemisphere}_{task}_functional_modules.csv').resolve(strict = True)
    _ = [getFile(localPath=localFileToExist, localOnly=True) for localFileToExist in [pathToXCsv, pathToYCsv]]
    pathToOutputtedXlsx: Path = (config.SUBJECT_STAT_DIR / f'{hemisphere}_hemisphere' / f'nonspatial_tests_hemi_{hemisphere}_task_{task}.xlsx').resolve(strict=False)

    runTests(subjectId, pathToXCsv, pathToYCsv, pathToOutputtedXlsx)
    
    statSuccess[iterationI] = pathToOutputtedXlsx.exists()
  return all(statSuccess)

def runDeprecatedStats(subjectId: str) -> bool:
  if config.CALC_DEPRECATED_STATS == False:
    return True
  conditions = config.ALL_FMRI_TASKS
  visualiseData = 0
  
  cmds = [
    call(cmdLabel="MATLAB",
              cmd=[
                      config.MATLAB,
                      f'-batch "mapDwiAndFmriToFaces {config.SUBJECT_DIR} {subjectId} {conditions} {visualiseData}"',
                      ],
              cwd=config.matlabScriptsFolder),
    call(cmdLabel="MATLAB",
              cmd=[
                      config.MATLAB,
                      f'-batch "calculateOverlap {config.SUBJECT_DIR} {subjectId} {conditions} {visualiseData}"',
                      ],
              cwd=config.matlabScriptsFolder)
  ]
  return all(cmds)