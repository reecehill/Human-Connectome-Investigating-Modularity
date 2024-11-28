import itertools
from modules.pipeline.stepper import finishStep
from includes.statistics.non_spatial_stats import runTests
from pathlib import Path
import config
from modules.file_directory.file_directory import createDirectories
from modules.subprocess_caller.call import *
from modules.hcp_data_manager.downloader import getFile


def runStatistics(subjectId: str) -> bool:
    statDir = config.SUBJECT_DIR / "statistics"
    for hemisphere in config.HEMISPHERES:
        createDirectories(
            directoryPaths=[statDir / f"{hemisphere}_hemisphere"],
            createParents=True,
            throwErrorIfExists=False,
        )
    config.setStatDir(statDir.resolve(strict=True))

    cmds = []
    allIterations = list(itertools.product(config.HEMISPHERES, config.ALL_FMRI_TASKS))
    for iterationI, iteration in enumerate(allIterations):
        hemisphere = iteration[0]
        task = iteration[1]
        config.setCurrentHemisphere(hemisphere)
        config.setCurrentTask(task)
        cmds.append(nonSpatialStatsPerTask(subjectId))

    return all(cmds) and runDeprecatedStats(subjectId)


def nonSpatialStatsPerTask(subjectId: str) -> bool:
    pathToXCsv: Path = (
        config.SUBJECT_DIR
        / "exported_modules"
        / f"{config.CURRENT_HEMISPHERE}_structural_modules.csv"
    ).resolve(strict=True)
    pathToYCsv: Path = (
        config.SUBJECT_DIR
        / "exported_modules"
        / f"{config.CURRENT_HEMISPHERE}_{config.CURRENT_TASK}_functional_modules.csv"
    ).resolve(strict=True)
    pathToXYSurfaceAreas: Path = (
        config.SUBJECT_DIR
        / "face_surface_areas"
        / f"{config.CURRENT_HEMISPHERE}_sa_by_face.csv"
    ).resolve(strict=True)

    pathToCentroidCoords: Path = (
        config.SUBJECT_DIR
        / f"{config.CURRENT_HEMISPHERE}_centroidCoordinatesByROIId.csv"
    ).resolve(strict=True)

    _ = [
        getFile(localPath=localFileToExist, localOnly=True)
        for localFileToExist in [
            pathToXCsv,
            pathToYCsv,
            pathToXYSurfaceAreas,
            pathToCentroidCoords,
        ]
    ]

    return runTests(
        subjectId, pathToXCsv, pathToYCsv, pathToXYSurfaceAreas, pathToCentroidCoords
    )


def runDeprecatedStats(subjectId: str) -> bool:
    if config.CALC_DEPRECATED_STATS == False:
        return True
    conditions = config.ALL_FMRI_TASKS
    visualiseData = 0

    cmds = [
        call(
            cmdLabel="MATLAB",
            cmd=[
                config.MATLAB,
                f'-batch "mapDwiAndFmriToFaces {config.SUBJECT_DIR} {subjectId} {conditions} {visualiseData}"',
            ],
            cwd=config.matlabScriptsFolder,
        ),
        call(
            cmdLabel="MATLAB",
            cmd=[
                config.MATLAB,
                f'-batch "calculateOverlap {config.SUBJECT_DIR} {subjectId} {conditions} {visualiseData}"',
            ],
            cwd=config.matlabScriptsFolder,
        ),
    ]
    return all(cmds)
