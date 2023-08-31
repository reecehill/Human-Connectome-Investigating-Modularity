from modules.subprocess_caller.call import *
import config

def runMatlab(subjectId: str, conditionIndex: int =1, visualiseData: bool =False) -> bool:
    return call(cmdLabel="MATLAB",
              cmd=[
                      config.MATLAB,
                      f'-batch "mapDwiAndFmriToFaces {config.matLabDriveAndPathToSubjects} {subjectId} {conditionIndex} {visualiseData}"',
                      ],
              cwd=config.matlabScriptsFolder)

def matlabProcessMapping(subjectId: str) -> bool:
  return runMatlab(subjectId)