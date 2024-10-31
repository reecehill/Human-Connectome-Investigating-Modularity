import pandas as pd
import numpy as np
from includes.statistics.utils import append_result_to_csv
from pathlib import Path


def save_results(
        dfXTruth: pd.DataFrame,
        dfYTruth: pd.DataFrame,
        pathToOutputtedCsv: Path):

    append_result_to_csv(df=dfXTruth, filename=pathToOutputtedCsv)
    append_result_to_csv(df=dfYTruth, filename=pathToOutputtedCsv)

    # # Write results also to numpy file
    # np.savez_compressed(
    #     file=str(pathToOutputtedCsv.resolve()).replace('.xlsx', '.npz'),
    #     dfXTruth=dfXTruth,
    #     dfYTruth=dfYTruth,
    # )
