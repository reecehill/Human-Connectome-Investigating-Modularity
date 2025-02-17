from typing import Any, Dict, Literal, Optional, Tuple, Union, cast
from includes.statistics.nan_handlers import (
    mask_removeMissing,
    ffill,
    smoothed,
    filter_by_parent,
    white_noise,
    get_main_fn_module_by_topology,
)
import pandas as pd
import numpy as np
from includes.statistics.save_results import save_modules
from includes.statistics.utils import populateModuleMetrics
import modules.globals as g

# Cleaning data to exclude NaN values


def clean_data(
    nan_handlers: "list[Literal['mask_removeMissing','ffill','smoothed','filter_by_parent','type_consistency','drop_na','white_noise','get_main_fn_module_by_topology','save']]",
    x: "Union[pd.Series[str],pd.Series[int]]",
    y: "Union[pd.Series[str],pd.Series[int]]",
    title: Optional[str] = "",
    dataset_name: Optional[str] = None,
    **kwargs: Any,
) -> "tuple[pd.Series[Any],pd.Series[Any]]":
    """
    Cleans the input data series `x` and `y` based on the specified `nan_handler` method.

    Parameters:
    - nan_handler (str): The method to handle NaN values. Options are "mask", "ffill", "smoothed", "filter_by_parent", "white_noise", or "none".
    - x (pd.Series[int]): The input series representing structural modules.
    - y (pd.Series[int]): The input series representing functional modules.
    - **kwargs (pd.Series[int]): Additional parameters for specific NaN handling methods.

    Returns:
    - tuple[Union[pd.Series[int], pd.Series[str]], Union[pd.Series[int], pd.Series[str]]]: A tuple containing the cleaned `x` and `y` series.

    Raises:
    - ValueError: If an invalid `nan_handler` is provided.

    Notes:
    - Logs the number of unique elements in `x` and `y` before and after cleaning.
    - Optionally makes the labels symmetric if `makeLabelsSymmetric` is set to True.
    """
    x_out: "pd.Series[Any]"
    y_out: "pd.Series[Any]"

    if len(nan_handlers) != 1:
        x_temp, y_temp = x.copy(), y.copy()  # start with unmodified series
        for nan_handler in nan_handlers:
            # Build the title with the current nan_handler in bold
            title = title if title else None
            x_temp, y_temp = clean_data(
                [nan_handler],
                x_temp,
                y_temp,
                title=title,
                dataset_name=dataset_name,
                **kwargs,
            )
        x_out, y_out = (
            x_temp,
            y_temp,
        )  # end with cleaned series if multiple handlers specified

    elif len(nan_handlers) == 1:  # single handler specified
        nan_handler = nan_handlers[0]
        if nan_handler == "mask_removeMissing":
            x_out, y_out = mask_removeMissing(x, y)
        elif nan_handler == "ffill":
            x_out, y_out = ffill(x, y)
        elif nan_handler == "smoothed":
            x_out, y_out = smoothed(x, y)
        elif nan_handler == "filter_by_parent":
            filter_by_parent_kwargs: "pd.Series[int]" = cast("pd.Series[int]", kwargs)
            x_out, y_out = filter_by_parent(x, y, **filter_by_parent_kwargs)
        elif nan_handler == "white_noise":
            white_noise_kwargs: "pd.Series[int]" = cast("pd.Series[int]", kwargs)
            x_out, y_out = white_noise(x, y, **white_noise_kwargs)
        elif nan_handler == "get_main_fn_module_by_topology":
            topology_kwargs: "pd.DataFrame" = cast("pd.DataFrame", kwargs)
            x_out, y_out = get_main_fn_module_by_topology(x, y, **topology_kwargs)  # type: ignore
        elif nan_handler == "drop_na":
            x_out, y_out = x.dropna(), y.dropna()
        elif nan_handler == "type_consistency":
            # Ensure same type for x and y
            if (
                x.dtype != y.dtype
                or x.attrs["dataset_descriptors"]["data_type"]
                != y.attrs["dataset_descriptors"]["data_type"]
            ):
                raise ValueError(
                    f"Data types of x and y should be the same. x: {x.dtype}, y: {y.dtype} | x: {x.attrs['dataset_descriptors']['data_type']}, y: {y.attrs['dataset_descriptors']['data_type']}"
                )

            # Ensure same length for x and y
            if len(x) != len(y):
                raise ValueError(
                    f"Length of x and y should be the same. x: {len(x)}, y: {len(y)}"
                )

            x_out, y_out = x.copy(), y.copy()

            # Convert np.nan and -1 to "missing-B" for words of data type
            if x.attrs["dataset_descriptors"]["data_type"] == "words":
                x_out.replace([np.nan, -1, "nan"], "missing-B", inplace=True)
                y_out.replace([np.nan, -1, "nan"], "missing-B", inplace=True)

            # Convert any string containing "missing" and np.nan to -1 (int) for integers of data type
            if x.attrs["dataset_descriptors"]["data_type"] == "int":
                x_out.replace(
                    [r".*missing.*", np.nan, "nan"], -1, regex=True, inplace=True
                )
                y_out.replace(
                    [r".*missing.*", np.nan, "nan"], -1, regex=True, inplace=True
                )

        elif nan_handler == "save":
            # Purpose of running clean_data is just to save the data.
            x_out, y_out = (
                x.copy(),
                y.copy(),
            )  # no modification needed for "none" handler
        else:
            raise ValueError(
                f'Invalid nan_handler: {nan_handler}. Options are "mask_removeMissing", "ffill", "smoothed", "filter_by_parent", "white_noise", "drop_na", "get_main_fn_module_by_topology", or "save".'
            )

        for preHandlerSize, out in [(x.size, x_out), (y.size, y_out)]:
            out.attrs.update(
                {
                    "dataset_descriptors": (
                        {
                            **out.attrs.get("dataset_descriptors", {}),
                            "dataset_name": (
                                dataset_name
                                if dataset_name
                                else (
                                    out.attrs["dataset_descriptors"]["dataset_name"]
                                    if "cleaned"
                                    in out.attrs["dataset_descriptors"]["dataset_name"]
                                    or nan_handler == "save"
                                    else f"{out.attrs['dataset_descriptors']['dataset_name']}_cleaned"
                                )
                            ),
                        }
                    ),
                    "applied_handlers": out.attrs.get("applied_handlers", []).append(
                        {
                            "name": nan_handler,
                            "metadata": {"pre_handler_length": preHandlerSize},
                        }
                    ),
                    "metrics": {
                        "distances_from_rois": populateModuleMetrics(
                            out, out.attrs["centroid_coords"]
                        ),
                    },
                }
            )

        title = title if title else "View path for applied nan handlers"
        save_modules(x_out, y_out, title=f"{title}")

        diffInStrucAndFnModules: int = len(x_out.unique()) - len(y_out.unique())
        g.logger.info(
            f"Struc. modules: #{len(x.unique())} -> #{len(x_out.unique())} | Fn modules: #{len(y.unique())} -> #{len(y_out.unique())} (post-{nan_handler}) ["
            + "{0:{1}}".format(
                diffInStrucAndFnModules, "+" if diffInStrucAndFnModules else ""
            )
            + "]"
        )

        # plot_timeline(x_out, y_out, title=title)

        makeLabelsSymmetric = False
        if makeLabelsSymmetric:
            x_out = pd.Series(
                np.append(x_out, np.flip(x_out.to_numpy().copy())).tolist()
            )
            y_out = pd.Series(
                np.append(y_out, np.flip(y_out.to_numpy().copy())).tolist()
            )

    else:
        raise ValueError(
            "nan_handlers should be a list with exactly one or more elements."
        )
    return x_out, y_out
