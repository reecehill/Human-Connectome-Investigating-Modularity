from modules.subprocess_caller.call import *
import config
from modules.file_directory.file_directory import createDirectories
from modules.utils import prepStep

def runMatlab(subjectId: str) -> bool:
        downsample = config.DOWNSAMPLE_SURFACE
        conditions = config.ALL_FMRI_TASKS
        createDirectories([config.SUBJECT_DIR / 'exported_modules'], createParents=True, throwErrorIfExists=False)
        cmds = [
                call(cmdLabel="MATLAB",
                cmd=[
                        config.MATLAB,
                        f'-batch "exportStrucModulesToCsv {config.SUBJECT_DIR} {subjectId} {downsample}"',
                        ],
                cwd=config.matlabScriptsFolder),
                
                call(cmdLabel="MATLAB",
                cmd=[
                        config.MATLAB,
                        f'-batch "exportFuncModulesToCsv {config.SUBJECT_DIR} {subjectId} {downsample} {conditions}"',
                        ],
                cwd=config.matlabScriptsFolder),
        ]
        
        return all(cmds)

def processMapping(subjectId: str) -> bool:
        prepStep(subjectId)
        return runMatlab(subjectId)