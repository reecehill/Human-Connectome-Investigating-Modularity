import modules.globals as g
import datalad.api
import config


def getInitialDataset():
    buildDataDirectory()


def buildDataDirectory() -> None:
    g.logger.info("Building dataset")
    if not (config.DATA_DIR / "ds002685").exists():
        datalad.api.install(source="https://github.com/OpenNeuroDatasets/ds002685.git", recursive=True, path=config.DATA_DIR / "ds002685", return_type="list-or-list")  # type: ignore
    else:
        g.logger.warn(
            "The data tree was not rebuilt as it already exists. Consider wiping this."
        )


def downloadFile(filePath: str) -> None:
    g.logger.info("Downloading: " + filePath)
    datalad.api.get(filePath, get_data=True, recursive=True)  # type: ignore
    g.logger.info("Unlocking: " + filePath)
    datalad.api.unlock(path=filePath)  # type: ignore


def clean() -> None:
    datalad.api.clean()  # type: ignore
