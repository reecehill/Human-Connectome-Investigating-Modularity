from typing import Dict, Union
from includes.statistics.nan_handlers import (
    mask,
    ffill,
    smoothed,
    filter_by_parent,
    white_noise,
)
import pandas as pd
import numpy as np
import numpy.typing as npt
import modules.globals as g

# Cleaning data to exclude NaN values


def clean_data(
    nan_handler: str,
    x: "pd.Series[int]",
    y: "pd.Series[int]",
    **kwargs: "pd.Series[int]",
) -> (
    "tuple[Union[pd.Series[int], pd.Series[str]],Union[pd.Series[int], pd.Series[str]]]"
):
    x_out: "Union[pd.Series[int], pd.Series[str]]"
    y_out: "Union[pd.Series[int], pd.Series[str]]"
    if nan_handler == "mask":
        x_out, y_out = mask(x, y)
    elif nan_handler == "ffill":
        x_out, y_out = ffill(x, y)
    elif nan_handler == "smoothed":
        x_out, y_out = smoothed(x, y)
    elif nan_handler == "filter_by_parent":
        x_out, y_out = filter_by_parent(x, y)
    elif nan_handler == "white_noise":
        x_out, y_out = white_noise(x, y, **kwargs)
    else:
        raise ValueError(
            f'Invalid nan_handler: {nan_handler}. Expected "mask", "ffill", "smoothed", or "filter_by_parent".'
        )

    diffInStrucAndFnModules: int = len(x_out.unique()) - len(y_out.unique())
    g.logger.info(
        f"Struc. modules: #{len(x.unique())} -> #{len(x_out.unique())} | Fn modules: #{len(y.unique())} -> #{len(y_out.unique())} (post-{nan_handler}) ["
        + "{0:{1}}".format(
            diffInStrucAndFnModules, "+" if diffInStrucAndFnModules else ""
        )
        + "]"
    )

    makeLabelsSymmetric = False
    if makeLabelsSymmetric:
        x_out = pd.Series(np.append(x_out, np.flip(x_out.to_numpy().copy())).tolist())
        y_out = pd.Series(np.append(y_out, np.flip(y_out.to_numpy().copy())).tolist())

    return x_out, y_out
