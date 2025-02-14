from typing import Any, Dict
from includes.visualisation.graphs import plotRoiRegion, plotTimelines
from modules.pipeline.stepper import prepStep
from modules.visualisation.includes.filter_data.functions import (
    separate_missing_modules
)
from modules.visualisation.includes.wrappers import (
    make_boxplots,
    make_scatterplots,
    make_violinplots,
    make_corrplots,
)

if __name__ == "__main__":
    raise Exception("This file is not meant to be run directly.")
else:

    def run() -> None:
        from traceback import format_exc

        try:
            from typing import List, Literal
            from modules.logger.logger import stop_root_logger
            from modules.file_directory.file_directory import createDirectories
            from pathlib import Path
            from pandas import DataFrame
            import modules.globals as g
            from modules.logger.logger import LoggerClass, config_root_logger
            from modules.visualisation.includes.io import read_csv
            from modules.pipeline.stepper import stepFnType

            # ------------------------------------------------------------
            # [START] Load and run the global logger.
            # ------------------------------------------------------------
            import config

            g.logger = LoggerClass()
            g.logger, g.log_queue = g.logger.run()
            # Start the queue listener in a separate thread
            g.queue_listener = config_root_logger(log_queue=g.log_queue)
            g.queue_listener.start()
            g.logger.info("Logger is running for VISUALISATION.")

            g.logger.info(
                "You must ensure the .csv files are copied to <project_root>/data_processed/allSubjects.csv and <project_root>/data_processed/allModules.csv"
            )
            createDirectories(
                [config.BASE_DIR / "data_processed" / "figures"],
                createParents=True,
                throwErrorIfExists=False,
            )
            pathTo: dict[str, Path] = {
                "subjects": Path(
                    config.BASE_DIR / "data_processed" / "allSubjects.csv.gz"
                ).resolve(strict=True),
                "modules": Path(
                    config.BASE_DIR / "data_processed" / "allModules.csv.gz"
                ).resolve(strict=True),
                "figures": Path(config.BASE_DIR / "data_processed" / "figures").resolve(
                    strict=True
                ),
            }
            allSubjects: DataFrame = read_csv(pathTo["subjects"])
            allModules_raw: DataFrame = read_csv(pathTo["modules"])

            # ----
            # We first clean the statistics by removing module pairs where one or more module contains the word "missing"
            # ----
            allModules = separate_missing_modules(allModules_raw, pathTo)

            allStats: List[str] = [
                "Levenshtein Distance - X as Truth",
                "Normalised Levenshtein Distance - X as Truth",
                "Mutual Information Score - X as Truth",
                "Normalized Mutual Information - X as Truth",
                "Adjusted Mutual Information - X as Truth",
                "V-measure Cluster Labeling - X as Truth",
                "Homogeneity Score - X as Truth",
                "Adjusted Random Score - X as Truth",
                "Fowlkes-Mallows Index - X as Truth",
                "Levenshtein Distance - Y as Truth",
                "Normalised Levenshtein Distance - Y as Truth",
                "Mutual Information Score - Y as Truth",
                "Normalized Mutual Information - Y as Truth",
                "Adjusted Mutual Information - Y as Truth",
                "V-measure Cluster Labeling - Y as Truth",
                "Homogeneity Score - Y as Truth",
                "Adjusted Random Score - Y as Truth",
                "Fowlkes-Mallows Index - Y as Truth",
            ]
            allTasks: List[Literal["lf", "rf", "rh", "lh", "t"]] = [
                "lf",
                "rf",
                "lh",
                "rh",
                "t",
            ]
            allHemispheres: List[Literal["left", "right"]] = ["left", "right"]
            subjectSample: List[str] = config.ALL_SUBJECTS[26:31]

            # We now mimic the prepStep setup just to get a figure
            allSteps: "Dict[Any, bool]" = {
                plotRoiRegion: True
            }
            g.allSteps = allSteps
            subjectSample = ['106824']
            for subjectId in subjectSample:
                prepStep(subjectId, "plotRoiRegion", hemisphere="left", task="lh")
                plotRoiRegion(subjectId, pathTo=pathTo)
                plotTimelines(subjectId, pathTo=pathTo)
            subjectSample: List[str] = config.ALL_SUBJECTS[26:31]
            # Wrapper function to combine filtering and plotting
            make_boxplots(
                pathTo,
                allSubjects,
                allModules,
                allHemispheres,
                allStats,
                allTasks,
                subjectSample,
            )

            make_violinplots(
                pathTo,
                allSubjects,
                allModules,
                allHemispheres,
                allStats,
                allTasks,
                subjectSample,
            )

            make_corrplots(
                pathTo,
                allSubjects,
                allModules,
                allHemispheres,
                allStats,
                allTasks,
                subjectSample,
            )

            make_scatterplots(
                pathTo,
                allSubjects,
                allModules,
                allHemispheres,
                allStats,
                allTasks,
                subjectSample,
            )

            g.logger.info("Powering down the logger...")
            stop_root_logger(g.queue_listener)
            # ------------------------------------------------------------
            # [END] Global logger now unavailable.
            # ------------------------------------------------------------
        except Exception as e:
            print("There was an error instantiating the logger.")
            print(e)
            print(format_exc())
            exit()
        finally:
            print("Process is complete.")
