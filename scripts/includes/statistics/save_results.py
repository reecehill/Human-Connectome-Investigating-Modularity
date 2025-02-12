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


def hash_dict(d: dict[str, Any]):
    import hashlib
    import json

    """Recursively hashes a dictionary, including nested dictionaries."""
    encoded = json.dumps(
        d, sort_keys=True, default=str
    ).encode()  # Ensure consistent ordering
    return hashlib.sha256(encoded).hexdigest()


def save_modules(x: "pd.Series[Any]", y: "pd.Series[Any]", title: str) -> None:
    import modules.globals as g

    filepath = Path(
        config.SUBJECT_STAT_DIR
        / f"{config.CURRENT_HEMISPHERE}_hemisphere"
        / "datasets"
        / f"{config.CURRENT_TASK}"
        / "dataset_name"
        / f"{x.attrs['dataset_descriptors']['dataset_name']}"
        / "data_type"
        / f"{x.attrs['dataset_descriptors']['data_type']}",
        *[
            str(handler["name"])
            for handler in x.attrs.get("applied_handlers", [])
            if handler["name"] not in ["save"]
        ],  # Append only allowed handlers
        *[
            str(item)
            for kv in x.attrs["dataset_descriptors"].items()
            if kv[0] not in {"subject_id", "task", "hemisphere", "dataset_name", "data_type"}
            for item in kv
        ],
    )

    createDirectories([filepath], createParents=True, throwErrorIfExists=False)

    xFilename, yFilename = (
        f"{hash_dict(x.attrs['dataset_descriptors'])}",
        f"{hash_dict(y.attrs['dataset_descriptors'])}",
    )
    xPath = (
        filepath
        / f"s-{len(x)}of{x.attrs['applied_handlers'][-1]['metadata']['pre_handler_length']}-{xFilename}.csv"
    )
    yPath = (
        filepath
        / f"f-{len(y)}of{y.attrs['applied_handlers'][-1]['metadata']['pre_handler_length']}-{yFilename}.csv"
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
