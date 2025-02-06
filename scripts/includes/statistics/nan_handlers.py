import pandas as pd
import numpy as np
import numpy.typing as npt
from typing import Any, Dict, Optional, Union, cast
from includes.statistics.utils import enlarge_mask_with_mode_priority
import modules.globals as g


def mask_removeMissing(
    x: "Union[pd.Series[int],pd.Series[str]]",
    y: "Union[pd.Series[int],pd.Series[str]]",
) -> "tuple[Union[pd.Series[int],pd.Series[str]],Union[pd.Series[int],pd.Series[str]]]":

    # All structural modules begin counting from 1 onwards, functional from 2.
    x_str = x.astype(dtype=str)
    y_str = y.astype(dtype=str)

    x_out = x_str[
        (x_str != "-1") & (x_str != "0") & (~x_str.str.contains("missing", na=False))
    ]
    if "mapped" in y.attrs['dataset_descriptors']['dataset_name']:
        y_out = y_str[
            (y_str != "-1")
            & (y_str != "0")
            & (~y_str.str.contains("missing", na=False))
        ]
    else:
        y_out = y_str[
            (y_str != "-1")
            & (y_str != "0")
            & (y_str != "1")
            & (~y_str.str.contains("missing", na=False))
        ]

    if pd.api.types.is_integer_dtype(x):
        x_out = x_out.astype(int)
        y_out = y_out.astype(int)

    return x_out, y_out


def ffill(
    x: "Union[pd.Series[str],pd.Series[int]]", y: "Union[pd.Series[str],pd.Series[int]]"
) -> "tuple[Union[pd.Series[str],pd.Series[int]],Union[pd.Series[str],pd.Series[int]]]":
    x_filled: "Union[pd.Series[str],pd.Series[int]]" = (
        x.replace(-1, np.nan).ffill(limit=1).bfill(limit=1)
    )
    y_filled: "Union[pd.Series[str],pd.Series[int]]" = (
        y.replace(to_replace=[-1, 0, 1], value=np.nan)
        .ffill(limit=2, limit_area="inside")
        .bfill(limit=2, limit_area="inside")
    )  # type: ignore

    x_out, y_out = x_filled, y_filled
    return x_out, y_out


def smoothed(
    x: "Union[pd.Series[str],pd.Series[int]]", y: "Union[pd.Series[str],pd.Series[int]]"
) -> "tuple[Union[pd.Series[str],pd.Series[int]],Union[pd.Series[str],pd.Series[int]]]":
    x_filtered, y_filtered = mask_removeMissing(x, y)

    if pd.api.types.is_integer_dtype(x_filtered):
        raise ValueError("x_filtered must be an integer")
    if pd.api.types.is_integer_dtype(y_filtered):
        raise ValueError("y_filtered must be an integer")

    x_filtered = cast("pd.Series[int]", x_filtered)
    y_filtered = cast("pd.Series[int]", y_filtered)
    y_smoothed = y_filtered.fillna(value=int(-1), axis=0, inplace=False)
    y_smoothed = enlarge_mask_with_mode_priority(y_smoothed, n=0, mode_method="roi")
    y_smoothed = enlarge_mask_with_mode_priority(y_smoothed, n=1, mode_method="window")

    x_smoothed = x_filtered.fillna(value=int(-1), axis=0, inplace=False)
    x_smoothed = enlarge_mask_with_mode_priority(x_smoothed, n=0, mode_method="window")
    x_smoothed = enlarge_mask_with_mode_priority(x_smoothed, n=5, mode_method="roi")

    x_out, y_out = x_filtered, y_filtered
    return x_out, y_out


def white_noise(
    x: "Union[pd.Series[str],pd.Series[int]]",
    y: "Union[pd.Series[str],pd.Series[int]]",
    **kwargs: "Union[pd.Series[str],pd.Series[int]]",
) -> (
    "tuple[Union[pd.Series[int], pd.Series[str]],Union[pd.Series[int], pd.Series[str]]]"
):

    def replaceMissingValuesWithNan(
        xory: "Union[pd.Series[int],pd.Series[str]]", replace: "list[Union[int,str]]"
    ) -> "Union[pd.Series[int],pd.Series[str]]":
        return xory.replace(to_replace=replace, value=np.nan)

    def replaceNaNWithRandom(
        xory: "Union[pd.Series[int],pd.Series[str]]",
        sample_from: "Optional[Union[pd.Series[int], pd.Series[str]]]" = None,
    ) -> "Union[pd.Series[int],pd.Series[str]]":
        if sample_from is None:
            sample_from = xory

        xory[xory.isna()] = g.randomGen.choice(
            a=sample_from.unique(), size=xory[xory.isna()].size
        )
        return xory

    x_withnans: "Union[pd.Series[int],pd.Series[str]]" = replaceMissingValuesWithNan(
        xory=x, replace=[-1, 0, "missing"]
    )
    y_withnans: "Union[pd.Series[int],pd.Series[str]]" = replaceMissingValuesWithNan(
        y, [-1, 0, 1, "missing"]
    )

    sample_from_x: "Optional[Union[pd.Series[int], pd.Series[str]]]" = kwargs.get(
        "sample_from_x", None
    )
    sample_from_y: "Optional[Union[pd.Series[int], pd.Series[str]]]" = kwargs.get(
        "sample_from_y", None
    )

    x_randomised: "Union[pd.Series[int], pd.Series[str]]" = replaceNaNWithRandom(
        x_withnans, sample_from=sample_from_x
    )
    y_randomised: "Union[pd.Series[int], pd.Series[str]]" = replaceNaNWithRandom(
        y_withnans, sample_from=sample_from_y
    )

    return x_randomised, y_randomised


def get_main_fn_module_by_topology(
    x: "pd.Series[int]", y: "pd.Series[int]", **kwargs: "pd.DataFrame"
) -> "tuple[pd.Series[int],pd.Series[int]]":
    import config
    centroid_coords: "pd.DataFrame" = kwargs.get(
        "centroid_coords", pd.DataFrame([])
    )
    if centroid_coords.empty:
        raise ValueError("Centroid coordinates are required for this method.")

    unique_y_modules = y.unique()
    y_modules_centroids = np.full((len(unique_y_modules), 3), np.nan)

    for y_module_index, y_module_name in enumerate(unique_y_modules):
        y_indices = y[y == y_module_name].index
        y_modules_centroids[y_module_index] = centroid_coords[y_indices].mean(axis=1)
        pass

    reference_points = {
        "left": {
            "lf": np.array([-10, -20, 78]),
            "rf": np.array([-10, -20, 78]),  # from inspection
            "lh": np.array([-40, -26, 65]),
            "rh": np.array([-40, -26, 65]),  # from inspection
            "t": np.array([-60, 5, 34]),  # from inspection
        },
        "right": {
            "lf": np.array([10, -20, 78]),
            "rf": np.array([10, -20, 78]),  # from inspection
            "lh": np.array([40, -26, 65]),
            "rh": np.array([40, -26, 65]),  # from inspection
            "t": np.array([60, 5, 34]),  # from inspection
        },
    }

    expected_module_location = reference_points[config.CURRENT_HEMISPHERE][config.CURRENT_TASK]
    distances = np.linalg.norm(y_modules_centroids - expected_module_location, axis=1)

    # Find the y module with the minimum distance
    closest_module_index = np.argmin(distances)
    closest_module = unique_y_modules[closest_module_index]

    y_filtered = y[y == closest_module]
    x_filtered = x[y_filtered.index]
    return x_filtered, y_filtered


def filter_by_parent(
    x: "pd.Series[Any]", y: "pd.Series[Any]", **kwargs: Any
) -> "tuple[pd.Series[Any],pd.Series[Any]]":
    xRetrievalMethod = kwargs.get("xRetrievalMethod", "getMode")
    hardMask = kwargs.get("hardMask", False)
    orig_x: "pd.Series[Any]" = kwargs.get("orig_x", pd.Series())

    # As y may be smaller than x, by masking x with y we risk going from:
    # x = [ 1,1,1,1 ]
    # y = [ NaN, 1, 1, -1 ] (where NaN or -1 indicates a module not found)
    # TO
    # x_filtered = [1,1]
    # y_filtered = [1,1]
    # Statistically, it would appear the labels align perfectly. But this is not the case before filtering.
    # Instead, we will enlarge the y window (padded with -1) to match the x window.
    attrs = x.attrs
    if(not orig_x.empty):
        g.logger.info("Using orig_x in filter_by_parent as it is supplied.")
        x = orig_x

    x_final_modules: "pd.Series[Any]" = pd.Series(
        np.full(x.size, -1), index=x.index
    )

    x_final_modules.attrs = attrs

    y_final_modules: "pd.Series[Any]" = pd.Series(np.full(x.size, -1), index=x.index)
    y_final_modules.attrs = y.attrs

    for y_module_name in y.unique():
        # Get underlying X modules (may be >1)
        # Add x modules to final X.
        if xRetrievalMethod == "getAll":
            x_module_names: "npt.NDArray[Any]" = x[(y == y_module_name).index].unique()
            x_indices = x[x.isin(x_module_names)].index
            x_final_modules[x_indices] = x[x.isin(x_module_names)]
        elif xRetrievalMethod == "getMode":
            x_module_name: "Any" = x[(y == y_module_name).index].mode()[0]
            x_indices = x[x == x_module_name].index
            x_final_modules[x_indices] = x_module_name
        else:
            raise ValueError(f"Invalid xRetrievalMethod: {xRetrievalMethod}")

        # Add y modules to final Y.
        y_indices = y[y == y_module_name].index
        y_final_modules[y_indices] = y_module_name

    if hardMask:
        # Exclude faces from final list that do not have any corresponding module (i.e., not selected by functional or functional's parent structural module)) 
        idsOfNan = (x_final_modules == -1) & (y_final_modules == -1)
    else:
        idsOfNan = np.full(x.size, False)
        
    x_out: "pd.Series[Any]" = x_final_modules[~idsOfNan]
    y_out: "pd.Series[Any]" = y_final_modules[~idsOfNan]
    return x_out, y_out
