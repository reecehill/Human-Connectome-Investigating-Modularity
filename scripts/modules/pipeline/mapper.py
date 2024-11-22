from modules.subprocess_caller.call import *
import config
from modules.file_directory.file_directory import createDirectories


def runMatlab(subjectId: str) -> bool:
    downsample = config.DOWNSAMPLE_SURFACE
    conditions: "list[str]" = config.ALL_FMRI_TASKS
    neededDirectories: "list[Path]" = [
        config.SUBJECT_DIR / "exported_modules",
        config.SUBJECT_DIR / "face_surface_areas",
    ]
    createDirectories(neededDirectories, createParents=True, throwErrorIfExists=False)

    cmds = [
        call(
            cmdLabel="MATLAB",
            cmd=[
                config.MATLAB,
                f'-batch "exportRoiIds {config.SUBJECT_DIR} {downsample}"',
            ],
            cwd=config.matlabScriptsFolder,
        ),
        call(
            cmdLabel="MATLAB",
            cmd=[
                config.MATLAB,
                f'-batch "exportFaceSurfaceAreas {config.SUBJECT_DIR} {downsample}"',
            ],
            cwd=config.matlabScriptsFolder,
        ),
        call(
            cmdLabel="MATLAB",
            cmd=[
                config.MATLAB,
                f'-batch "exportStrucModulesToCsv {config.SUBJECT_DIR} {subjectId} {downsample}"',
            ],
            cwd=config.matlabScriptsFolder,
        ),
        call(
            cmdLabel="MATLAB",
            cmd=[
                config.MATLAB,
                f'-batch "exportFuncModulesToCsv {config.SUBJECT_DIR} {subjectId} {downsample} {conditions}"',
            ],
            cwd=config.matlabScriptsFolder,
        ),
    ]

    return all(cmds)


def processMapping(subjectId: str) -> bool:
    return runMatlab(subjectId=subjectId)
