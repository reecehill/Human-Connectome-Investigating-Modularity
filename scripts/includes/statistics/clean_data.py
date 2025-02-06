from typing import Any, Optional, Union, cast
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
from includes.visualisation.plot_timeline import plot_timeline
import modules.globals as g

# Cleaning data to exclude NaN values


def clean_data(
    nan_handlers: "Union[str,list[str]]",
    x: "Union[pd.Series[str],pd.Series[int]]",
    y: "Union[pd.Series[str],pd.Series[int]]",
    title: Optional[str] = "",
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

    if isinstance(nan_handlers, list):
        x_temp, y_temp = x.copy(), y.copy()  # start with unmodified series
        for nan_handler in nan_handlers:
            # Build the title with the current nan_handler in bold
            title = title if title else "-".join(
                [
                    handler.upper() if handler == nan_handler else handler.lower()
                    for handler in nan_handlers
                ]
            )
            x_temp, y_temp = clean_data(
                nan_handler, x_temp, y_temp, title=title, **kwargs
            )
        x_out, y_out = (
            x_temp,
            y_temp,
        )  # end with cleaned series if multiple handlers specified

    else:  # single handler specified
        nan_handler = nan_handlers
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
            x_out, y_out = get_main_fn_module_by_topology(x, y, **topology_kwargs) # type: ignore
        elif nan_handler == "none":
            x_out, y_out = (
                x.copy(),
                y.copy(),
            )  # no modification needed for "none" handler
        else:
            raise ValueError(
                f'Invalid nan_handler: {nan_handler}. Expected "mask", "ffill", "smoothed", or "filter_by_parent".'
            )

        x_out.attrs.update(
            {
                "dataset_descriptors": {
                    **x_out.attrs.get("dataset_descriptors", {}),
                    "dataset_name": (
                        x_out.attrs["dataset_descriptors"]["dataset_name"]
                        if "cleaned"
                        in x_out.attrs["dataset_descriptors"]["dataset_name"]
                        else f"{x_out.attrs['dataset_descriptors']['dataset_name']}_cleaned"
                    ),
                },
                "applied_handlers": x_out.attrs["applied_handlers"]
                + [{"name": nan_handler, "metadata": {"pre_handler_length": x.size}}],
            }
        )
        y_out.attrs.update(
            {
                "dataset_descriptors": {
                    **y_out.attrs.get("dataset_descriptors", {}),
                    "dataset_name": (
                        y_out.attrs["dataset_descriptors"]["dataset_name"]
                        if "cleaned"
                        in y_out.attrs["dataset_descriptors"]["dataset_name"]
                        else f"{y_out.attrs['dataset_descriptors']['dataset_name']}_cleaned"
                    ),
                },
                "applied_handlers": y_out.attrs["applied_handlers"]
                + [{"name": nan_handler, "metadata": {"pre_handler_length": y.size}}],
            }
        )

        diffInStrucAndFnModules: int = len(x_out.unique()) - len(y_out.unique())
        g.logger.info(
            f"Struc. modules: #{len(x.unique())} -> #{len(x_out.unique())} | Fn modules: #{len(y.unique())} -> #{len(y_out.unique())} (post-{nan_handler}) ["
            + "{0:{1}}".format(
                diffInStrucAndFnModules, "+" if diffInStrucAndFnModules else ""
            )
            + "]"
        )

        title = title if title else f"{nan_handler}"
        plot_timeline(x_out, y_out, title=title)

    makeLabelsSymmetric = False
    if makeLabelsSymmetric:
        x_out = pd.Series(np.append(x_out, np.flip(x_out.to_numpy().copy())).tolist())
        y_out = pd.Series(np.append(y_out, np.flip(y_out.to_numpy().copy())).tolist())

    return x_out, y_out
