from typing import Any
import pandas as pd
from includes.statistics.utils import append_result_to_csv
from pathlib import Path
import config
from modules.file_directory.file_directory import createDirectories


def append_results(
    dfXTruth: pd.DataFrame, dfYTruth: pd.DataFrame, pathToOutputtedCsv: Path
):

    append_result_to_csv(df=dfXTruth, filename=pathToOutputtedCsv)
    append_result_to_csv(df=dfYTruth, filename=pathToOutputtedCsv)

    # # Write results also to numpy file
    # np.savez_compressed(
    #     file=str(pathToOutputtedCsv.resolve()).replace('.xlsx', '.npz'),
    #     dfXTruth=dfXTruth,
    #     dfYTruth=dfYTruth,
    # )


def save_modules(x: "pd.Series[Any]", y: "pd.Series[Any]", title: str) -> None:
    import modules.globals as g

    filepath = Path(
        config.SUBJECT_STAT_DIR
        / f"{config.CURRENT_HEMISPHERE}_hemisphere"
        / "datasets"
        / f"{config.CURRENT_TASK}",
        *[
            str(item)
            for kv in x.attrs["dataset_descriptors"].items()
            if kv[0] not in {"subject_id", "task", "hemisphere"}
            for item in kv
        ],
    )
    createDirectories([filepath], createParents=True, throwErrorIfExists=False)

    xPath = (
        filepath
        / f"s_{title}-{len(x)}of{x.attrs['applied_handlers'][0]['metadata']['pre_handler_length']}.csv"
    )
    yPath = (
        filepath
        / f"f_{title}-{len(y)}of{y.attrs['applied_handlers'][0]['metadata']['pre_handler_length']}.csv"
    )

    for path, data in zip([xPath, yPath], [x, y]):
        data.to_csv(
            f"{path}{'.gz' if config.COMPRESS_FILE else ''}",
            index=True,
            header=False,
        )
        data.to_pickle(
            f"{str(path).replace('.csv','.pkl')}{'.gz' if config.COMPRESS_FILE else ''}",
        )
        g.logger.info(f"Written modules to file: {path}")
