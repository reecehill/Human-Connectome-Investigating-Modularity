# Re-importing necessary libraries and preparing data again
from typing import cast
import modules.globals as g
import pandas as pd
import numpy as np
from includes.statistics.perModuleStat import perModuleStat
from includes.statistics.perSubjectStat import perSubjectStat
from pathlib import Path
from includes.statistics.utils import convertNumericalModulesToWords, mapAllModulesToSameSet
from includes.statistics.clean_data import clean_data


def runTests(subjectId: str, pathToXCsv: Path, pathToYCsv: Path, pathToXYSurfaceAreas: Path) -> bool:
    result = False
    try:
        x_raw: pd.DataFrame = pd.read_csv(pathToXCsv.absolute(
        ).__str__(), sep=',', header=None, keep_default_na=True).T
        y_raw: pd.DataFrame = pd.read_csv(pathToYCsv.absolute(
        ).__str__(), sep=',', header=None, keep_default_na=True).T
        xy_surface_area: pd.DataFrame = pd.read_csv((pathToXYSurfaceAreas).absolute(
        ).__str__(), sep=',', header=None, keep_default_na=True).T

        # We begin by standardising what "missing" data looks like (set it to -1).
        x_orig: "pd.Series[int]" = x_raw[0].replace(
            to_replace=[np.nan, -1, 0], value=-1, inplace=False, )
        y_orig: "pd.Series[int]" = y_raw[0].replace(
            to_replace=[np.nan, -1, 0, 1], value=-1, inplace=False)

        # ------
        # Map x and y to same set
        # NB: This uses Hungarian algorith to map modules to the same set of words.
        # ?This may introduce some artefacts into the data (i.e., inappropriate mapping)
        # We map once using the complete dataset, then apply this mapping to subsets.
        # ------

        # Map the cleaned words to the same set.
        orig_mapping: "dict[str,str]"
        orig_mapping, _x_orig_mapped, _y_orig_mapped = mapAllModulesToSameSet(
            x=x_orig,
            y=y_orig)
        x_orig_mapped: "pd.Series[int]" = cast(
            "pd.Series[int]", _x_orig_mapped)
        y_orig_mapped: "pd.Series[int]" = cast(
            "pd.Series[int]", _y_orig_mapped)

        # ------
        # Mask, or smooth module names.
        # ------
        # Clean original data.
        _x_cleaned, _y_cleaned = clean_data(
            nan_handler="filter_by_parent", x=x_orig, y=y_orig)
        x_cleaned: "pd.Series[int]" = cast("pd.Series[int]", _x_cleaned)
        y_cleaned: "pd.Series[int]" = cast("pd.Series[int]", _y_cleaned)

        # Clean mapped data.
        _x_cleaned_mapped, _y_cleaned_mapped = clean_data(
            nan_handler="filter_by_parent", x=x_orig_mapped, y=y_orig_mapped)
        x_cleaned_mapped: "pd.Series[int]" = cast(
            "pd.Series[int]", _x_cleaned_mapped)
        y_cleaned_mapped: "pd.Series[int]" = cast(
            "pd.Series[int]", _y_cleaned_mapped)

        # ------
        # Convert pd.Series[int] => pd.Series[str]
        # NB: To demonstrate that statistical tests must work on categorical named data (and definitely not numerical), map module names (e.g., "2") to random words (e.g., "hsjjrnsyhf").
        # ------

        x_orig_words, y_orig_words = convertNumericalModulesToWords(
            x_orig, y_orig)

        x_mapped_words, y_mapped_words = convertNumericalModulesToWords(
            x=x_orig_mapped, y=y_orig_mapped, dataIsMapped=True)

        x_cleaned_words, y_cleaned_words = convertNumericalModulesToWords(
            x_cleaned, y_cleaned)

        x_cleaned_mapped_words, y_cleaned_mapped_words = convertNumericalModulesToWords(
            x_cleaned_mapped, y_cleaned_mapped, dataIsMapped=True)

        # ------
        # Make x and y symmetric
        # NB: To demonstrate that statistical tests are unaffected by data symmetry.
        # ------
        if (1 == 0):
            x_clean_words: "pd.Series[str]" = pd.concat(
                [x_cleaned_words, pd.Series(np.flip(x_cleaned_words))])
            y_clean_words: "pd.Series[str]" = pd.concat(
                [y_cleaned_words, pd.Series(np.flip(y_cleaned_words))])

        # TODO: For some reason -> the stats show no improvement in performance for modules against randomised data. This is impossible.
        perSubjectStat("cleaned_words", x_cleaned_words, y_cleaned_words)
        perSubjectStat("cleaned_words_mapped",
                       x_cleaned_mapped_words, y_cleaned_mapped_words)
        
        perModuleStat("cleaned_words", x_cleaned_words, y_cleaned_words, x_orig_words, y_orig_words, xy_surface_area)
        perModuleStat(datasetDescriptor="cleaned_words_mapped", x_final=x_cleaned_mapped_words,
                      y_final=y_cleaned_mapped_words, xy_surface_areas=xy_surface_area, x=x_mapped_words, y=y_mapped_words)

        result: bool = True
    except Exception as e:
        result = False
        g.logger.error(f"Error whilst running stats - {e}")
        raise e
    finally:
        return result
