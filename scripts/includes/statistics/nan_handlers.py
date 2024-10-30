import pandas as pd
import numpy as np
import numpy.typing as npt
from typing import Any, Dict, Optional, Union, cast
from includes.statistics.utils import enlarge_mask_with_mode_priority
import modules.globals as g

def mask_removeMissing(x: "pd.Series[int]", y: "pd.Series[int]") -> "tuple[pd.Series[int],pd.Series[int]]":
    # All structural modules begin counting from 1 onwards, functional from 2.
    x_out = x[(x > 0)]
    y_out = y[(y > 1)]
    return x_out, y_out

def mask(x: "pd.Series[int]", y: "pd.Series[int]") -> "tuple[pd.Series[int],pd.Series[int]]":
    # All structural modules begin counting from 1 onwards, functional from 2.
    idsOfNonNan = (x > 0) & (y > 1)
    x_out = x[idsOfNonNan]
    y_out = y[idsOfNonNan]
    return x_out, y_out


def ffill(x: "pd.Series[int]", y: "pd.Series[int]") -> "tuple[pd.Series[int],pd.Series[int]]":

    x_filled: "pd.Series[int]" = x.replace(-1,
                                         np.nan).ffill(limit=1).bfill(limit=1)
    y_filled: "pd.Series[int]" = y.replace(to_replace=[-1, 0, 1], value=np.nan).ffill(
        limit=2, limit_area="inside").bfill(limit=2, limit_area="inside")  # type: ignore

    x_out, y_out = x_filled, y_filled
    return x_out, y_out


def smoothed(x: "pd.Series[int]", y: "pd.Series[int]") -> "tuple[pd.Series[int],pd.Series[int]]":
    x_filtered, y_filtered = mask(x, y)

    y_smoothed = y_filtered.fillna(
        value=int(-1), axis=0, inplace=False)
    y_smoothed = enlarge_mask_with_mode_priority(
        y_smoothed, n=0, mode_method='roi')
    y_smoothed = enlarge_mask_with_mode_priority(
        y_smoothed, n=1, mode_method='window')

    x_smoothed = x_filtered.fillna(
        value=int(-1), axis=0, inplace=False)
    x_smoothed = enlarge_mask_with_mode_priority(
        x_smoothed, n=0, mode_method='window')
    x_smoothed = enlarge_mask_with_mode_priority(
        x_smoothed, n=5, mode_method='roi')

    x_out, y_out = x_filtered, y_filtered
    return x_out, y_out


def white_noise(x: "Union[pd.Series[int],pd.Series[str]]", y: "Union[pd.Series[int], pd.Series[str]]", **kwargs: "Union[pd.Series[int], pd.Series[str]]") -> "tuple[Union[pd.Series[int],pd.Series[str]],Union[pd.Series[int],pd.Series[str]]]":
    
    def replaceMissingValuesWithNan(xory: "Union[pd.Series[int],pd.Series[str]]", replace: "list[Union[int,str]]") -> "Union[pd.Series[int],pd.Series[str]]":
        return xory.replace(to_replace=replace, value=np.nan)
    
    def replaceNaNWithRandom(xory: "Union[pd.Series[int],pd.Series[str]]", sample_from: "Optional[Union[pd.Series[int], pd.Series[str]]]" = None) -> "Union[pd.Series[int],pd.Series[str]]":
        if sample_from is None:
            sample_from = xory
            
        xory[xory.isna()] = g.randomGen.choice(
            a=sample_from,
            size=len(xory))
        return xory

    x_withnans: "Union[pd.Series[int],pd.Series[str]]" = replaceMissingValuesWithNan(
        xory=x, replace=[-1, 0, "missing"])
    y_withnans: "Union[pd.Series[int],pd.Series[str]]" = replaceMissingValuesWithNan(
        y, [-1, 0, 1, 'missing'])

    sample_from_x: "Optional[Union[pd.Series[int], pd.Series[str]]]" = kwargs.get(
        'sample_from_x', None)
    sample_from_y: "Optional[Union[pd.Series[int], pd.Series[str]]]" = kwargs.get(
        'sample_from_y', None)

    x_randomised: "Union[pd.Series[int], pd.Series[str]]" = replaceNaNWithRandom(
        x_withnans, sample_from=sample_from_x)
    y_randomised: "Union[pd.Series[int], pd.Series[str]]" = replaceNaNWithRandom(
        y_withnans, sample_from=sample_from_y)

    return x_randomised, y_randomised
    

def filter_by_parent(x: "pd.Series[int]", y: "pd.Series[int]") -> "tuple[pd.Series[int],pd.Series[int]]":
    # As y may be smaller than x, by masking x with y we risk going from:
    # x = [ 1,1,1,1 ]
    # y = [ NaN, 1, 1, -1 ] (where NaN or -1 indicates a module not found)
    # TO
    # x_filtered = [1,1]
    # y_filtered = [1,1]
    # Statistically, it would appear the labels align perfectly. But this is not the case before filtering.
    # Instead, we will enlarge the y window (padded with -1) to match the x window.
    y_maskedby_y: 'pd.Series[int]'
    x_maskedby_y: 'pd.Series[int]'
    x_maskedby_y, y_maskedby_y = mask(x, y)

    x_final_modules: 'pd.Series[int]' = x_maskedby_y
    y_final_modules: 'pd.Series[Union[int,float]]' = pd.Series(
        np.full(y_maskedby_y.size, np.nan, dtype=np.float64), index=y_maskedby_y.index)

    for y_module_name in y_maskedby_y.unique():
        # Get current X module (by taking mode)
        x_module_name: int = x_maskedby_y[y_maskedby_y == y_module_name].mode()[
            0]
        x_module: "pd.Series[int]" = x_maskedby_y[x_maskedby_y == x_module_name]

        # Reset current Y module to include X
        if (y_final_modules[x_module.index].isna()).all():
            # If the current Y module is empty, fill it with the Y module within X
            y_final_modules[x_module.index] = y_maskedby_y[x_module.index]
        else:
            g.logger.warning(
                "Overwriting functional modules is prohibited. Logic needed.")

    x_out: "pd.Series[int]" = x_final_modules
    y_out: "pd.Series[int]" = y_final_modules.fillna(-1).astype(int)
    return x_out, y_out
