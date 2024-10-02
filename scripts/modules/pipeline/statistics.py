from python.non_spatial_stats import runTests
from pathlib import Path
import config
from modules.file_directory.file_directory import createDirectories
from modules.utils import prepStep
from modules.subprocess_caller.call import *

def runStatistics(subjectId: str) -> bool:
  prepStep(subjectId)
  statDir = config.SUBJECT_DIR / 'statistics'

  return runDeprecatedStats(subjectId)
  
  for hemisphere in config.HEMISPHERES:
    createDirectories(directoryPaths=[statDir / f'{hemisphere}_hemisphere' ], createParents=True, throwErrorIfExists=False)
  config.setStatDir(statDir.resolve(strict=True))

  
  return nonSpatialStatsPerTask(subjectId=subjectId)
def nonSpatialStatsPerTask(subjectId: str) -> bool:  
  statSuccess: "list[bool]" = [False for _ in range(len(config.ALL_FMRI_TASKS) * len(config.HEMISPHERES))]
  for hemisphere in config.HEMISPHERES:  
    for task in config.ALL_FMRI_TASKS:
      pathToXCsv: Path = (config.SUBJECT_DIR / 'exported_modules' / f'{hemisphere}_structural_modules.csv').resolve(strict = True)
      pathToYCsv: Path = (config.SUBJECT_DIR / 'exported_modules' / f'{hemisphere}_{task}_functional_modules.csv').resolve(strict = True)
      pathToOutputtedXlsx: Path = (config.SUBJECT_STAT_DIR / f'{hemisphere}_hemisphere' / f'nonspatial_tests_hemi_{hemisphere}_task_{task}.xlsx').resolve(strict=False)
      runTests(subjectId, pathToXCsv, pathToYCsv, pathToOutputtedXlsx)
      statSuccess.append(pathToOutputtedXlsx.exists())
  return all(statSuccess)

def runDeprecatedStats(subjectId):
  conditions = config.ALL_FMRI_TASKS
  visualiseData = 0
  
  cmds = [
    # call(cmdLabel="MATLAB",
    #           cmd=[
    #                   config.MATLAB,
    #                   f'-batch "mapDwiAndFmriToFaces {config.SUBJECT_DIR} {subjectId} {conditions} {visualiseData}"',
    #                   ],
    #           cwd=config.matlabScriptsFolder),
    call(cmdLabel="MATLAB",
              cmd=[
                      config.MATLAB,
                      f'-batch "calculateOverlap {config.SUBJECT_DIR} {subjectId} {conditions} {visualiseData}"',
                      ],
              cwd=config.matlabScriptsFolder)
  ]
  return all(cmds)