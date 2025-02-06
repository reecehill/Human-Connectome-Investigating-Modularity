# Re-importing necessary libraries and preparing data again
from typing import Dict, Union, cast

from includes.visualisation.plot_timeline import plot_timeline
import modules.globals as g
import pandas as pd
import numpy as np
from includes.statistics.perModuleStat import perModuleStat
from includes.statistics.perSubjectStat import perSubjectStat
from pathlib import Path
from includes.statistics.utils import (
    convertNumericalModulesToWords,
    mapAllModulesToSameSet,
)
from includes.statistics.clean_data import clean_data


def runTests(
    subjectId: str,
    pathToXCsv: Path,
    pathToYCsv: Path,
    pathToXYSurfaceAreas: Path,
    pathToCentroidCoords: Path,
) -> bool:
    import config

    result = False
    try:
        x_raw: pd.DataFrame = pd.read_csv(
            pathToXCsv.absolute().__str__(), sep=",", header=None, keep_default_na=True
        ).T
        y_raw: pd.DataFrame = pd.read_csv(
            pathToYCsv.absolute().__str__(), sep=",", header=None, keep_default_na=True
        ).T
        xy_surface_area: pd.DataFrame = pd.read_csv(
            (pathToXYSurfaceAreas).absolute().__str__(),
            sep=",",
            header=None,
            keep_default_na=True,
        ).T
        centroid_coords: pd.DataFrame = pd.read_csv(
            (pathToCentroidCoords).absolute().__str__(),
            sep=",",
            header=None,
            keep_default_na=True,
        ).T


        # We begin by standardising what "missing" data looks like (set it to -1).
        x_orig = x_raw[0].replace([np.nan, -1, 0], -1)
        x_orig.attrs.update(
            {
                "applied_handlers": x_orig.attrs.get("applied_handlers", [])
                + [
                    {
                        "name": "read_csv",
                        "metadata": {"pre_handler_length": x_orig.size},
                    }
                ],
                "dataset_descriptors": {
                    "dataset_name": "orig",
                    "data_type": "int",
                    "subject_id": config.CURRENT_SUBJECT,
                    "task": config.CURRENT_TASK,
                    "hemisphere": config.CURRENT_HEMISPHERE,
                },
            }
        )

        y_orig = y_raw[0].replace([np.nan, -1, 0, 1], -1)
        y_orig.attrs.update(
            {
                "dataset_descriptors": {
                    "dataset_name": "orig",
                    "subject_id": config.CURRENT_SUBJECT,
                    "data_type": "int",
                    "task": config.CURRENT_TASK,
                    "hemisphere": config.CURRENT_HEMISPHERE,
                },
                "applied_handlers": y_orig.attrs.get("applied_handlers", [])
                + [
                    {
                        "name": "read_csv",
                        "metadata": {"pre_handler_length": y_orig.size},
                    }
                ],
            }
        )

        # ------
        # Map x and y to same set
        # NB: This uses Hungarian algorithm to map modules to the same set of words.
        # ?This may introduce some artefacts into the data (i.e., inappropriate mapping)
        # We map once using the complete dataset, then apply this mapping to subsets.
        # ------
        # Map the cleaned words to the same set.
        orig_mapping: "dict[str,str]"
        mappedMatrixScores: "Dict[str, Dict[str, float]]"
        orig_mapping, _x_orig_mapped, _y_orig_mapped, mappedMatrixScores = (
            mapAllModulesToSameSet(x=x_orig, y=y_orig, centroid_coords=centroid_coords)
        )

        x_orig_mapped: "pd.Series[int]" = cast("pd.Series[int]", _x_orig_mapped)
        y_orig_mapped: "pd.Series[int]" = cast("pd.Series[int]", _y_orig_mapped)
        del _x_orig_mapped, _y_orig_mapped

        # ------
        # There are now two datasets: mapped and unmapped.
        # The statistics that can be calculated on each are different owing to their different labelling.
        # ------

        # ----------------------------------------------------------------
        # Handle unmapped dataset.
        # 1. Smooth structural and functional modules.
        # 2. Convert pd.Series[int] -> pd.Series[str]
        # ----------------------------------------------------------------

        # ------
        # Mask, or smooth module names.
        # ------
        # Clean original data.

        _x_cleaned, _y_cleaned = clean_data(
            nan_handlers=[
                "mask_removeMissing",
                # "get_main_fn_module_by_topology",
                "filter_by_parent",
            ],
            x=x_orig,
            y=y_orig,
            orig_x=x_orig_mapped,  # Used to pass original x to filter_by_parent
            # xRetrievalMethod="getMode",
            # centroid_coords=centroid_coords,
        )
        x_cleaned: "pd.Series[int]" = cast("pd.Series[int]", _x_cleaned)
        y_cleaned: "pd.Series[int]" = cast("pd.Series[int]", _y_cleaned)
        del _x_cleaned, _y_cleaned

        # -----
        # Convert pd.Series[int] => pd.Series[str]
        # NB: To demonstrate that statistical tests must work on categorical named data (and definitely not numerical), map module names (e.g., "2") to random words (e.g., "hsjjrnsyhf").
        # ------
        # Convert original mapped data to words. (For comparison only.)
        x_orig_words, y_orig_words, label_to_word_map_y = (
            convertNumericalModulesToWords(
                x_orig_mapped, x_orig_mapped, mapName=f"orig_{config.CURRENT_TASK}"
            )
        )
        mappedMatrixScores_orig_words = {
            label_to_word_map_y.get(int(old_key), old_key): value
            for old_key, value in mappedMatrixScores.items()
        }

        x_cleaned_words, y_cleaned_words, label_to_word_map_y = (
            convertNumericalModulesToWords(
                x_cleaned, y_cleaned, mapName=f"cleaned_{config.CURRENT_TASK}"
            )
        )
        mappedMatrixScores_cleaned_words = {
            label_to_word_map_y.get(int(old_key), old_key): value
            for old_key, value in mappedMatrixScores.items()
        }

        # ----------------------------------------------------------------
        # Handle mapped dataset.
        # 1. Smooth structural and functional modules.
        # 2. Convert pd.Series[int] -> pd.Series[str]
        # ----------------------------------------------------------------
        # ------
        # Mask, or smooth module names.
        # ------
        # Clean original data.
        # Clean mapped data.
        _x_cleaned_mapped, _y_cleaned_mapped = clean_data(
            nan_handlers=[
                "mask_removeMissing",
                "get_main_fn_module_by_topology",
                "filter_by_parent",
            ],
            x=x_orig_mapped,
            y=y_orig_mapped,
            orig_x=x_orig_mapped,  # Used to pass original x to filter_by_parent
            xRetrievalMethod="getMode",
            centroid_coords=centroid_coords,
        )
        x_cleaned_mapped: "pd.Series[int]" = cast("pd.Series[int]", _x_cleaned_mapped)
        y_cleaned_mapped: "pd.Series[int]" = cast("pd.Series[int]", _y_cleaned_mapped)
        del _x_cleaned_mapped, _y_cleaned_mapped

        # ------
        # Convert pd.Series[int] => pd.Series[str]
        # NB: To demonstrate that statistical tests must work on categorical named data (and definitely not numerical), map module names (e.g., "2") to random words (e.g., "hsjjrnsyhf").
        # ------
        x_mapped_words, y_mapped_words, label_to_word_map_y = (
            convertNumericalModulesToWords(
                x=x_orig_mapped,
                y=y_orig_mapped,
                dataIsMapped=True,
                mapName=f"mapped_{config.CURRENT_TASK}",
            )
        )
        mappedMatrixScores_mapped_words = {
            label_to_word_map_y.get(
                int(old_key), f"KeyNotFoundInIntToStringMap-{old_key}"
            ): value
            for old_key, value in mappedMatrixScores.items()
        }

        x_cleaned_mapped_words, y_cleaned_mapped_words, label_to_word_map_y = (
            convertNumericalModulesToWords(
                x_cleaned_mapped,
                y_cleaned_mapped,
                dataIsMapped=True,
                mapName=f"cleaned_mapped_{config.CURRENT_TASK}",
            )
        )
        mappedMatrixScores_cleaned_mapped_words = {
            label_to_word_map_y.get(int(old_key), old_key): value
            for old_key, value in mappedMatrixScores.items()
        }

        # ------
        # Make x and y symmetric
        # NB: To demonstrate that statistical tests are unaffected by data symmetry.
        # ------
        if 1 == 0:
            x_clean_words: "pd.Series[str]" = pd.concat(
                [x_cleaned_words, pd.Series(np.flip(x_cleaned_words))]
            )
            y_clean_words: "pd.Series[str]" = pd.concat(
                [y_cleaned_words, pd.Series(np.flip(y_cleaned_words))]
            )

        # For visualisation purposes, save the new x and y.
        for descriptor, x, y in [
            ("orig", x_orig, y_orig),
            ("orig_mapped", x_orig_mapped, y_orig_mapped),
            ("orig_words", x_orig_words, y_orig_words),
            ("mapped_words", x_mapped_words, y_mapped_words),
            ("cleaned", x_cleaned, y_cleaned),
            ("cleaned_words", x_cleaned_words, y_cleaned_words),
            ("cleaned_mapped", x_cleaned_mapped, y_cleaned_mapped),
            ("cleaned_mapped_words", x_cleaned_mapped_words, y_cleaned_mapped_words),
        ]:
            x: "pd.Series[Union[int,str]]"
            y: "pd.Series[Union[int,str]]"
            plot_timeline(x=x, y=y)
            x.to_csv(
                config.SUBJECT_STAT_DIR
                / f"{config.CURRENT_HEMISPHERE}_hemisphere"
                / "datasets"
                / f"{descriptor}_{pathToXCsv.name}",
                index=True,
                header=False,
            )
            y.to_csv(
                config.SUBJECT_STAT_DIR
                / f"{config.CURRENT_HEMISPHERE}_hemisphere"
                / "datasets"
                / f"{descriptor}_{pathToYCsv.name}",
                index=True,
                header=False,
            )

        perSubjectStat("cleaned_words", x_cleaned_words, y_cleaned_words)
        perSubjectStat(
            "cleaned_words_mapped", x_cleaned_mapped_words, y_cleaned_mapped_words
        )

        # perModuleStat(
        #     datasetDescriptor="cleaned_words",
        #     x_final=x_cleaned_words,
        #     y_final=y_cleaned_words,
        #     x=x_orig_words,
        #     y=y_orig_words,
        #     xy_surface_areas=xy_surface_area,
        #     centroid_coords=centroid_coords,
        #     mappedMatrixScores=mappedMatrixScores_cleaned_words,
        # )
        perModuleStat(
            datasetDescriptor="mapped_words",
            x_final=x_mapped_words.copy(),
            y_final=y_mapped_words.copy(),
            x=x_mapped_words.copy(),
            y=y_mapped_words.copy(),
            xy_surface_areas=xy_surface_area,
            centroid_coords=centroid_coords,
            mappedMatrixScores=mappedMatrixScores_mapped_words,
        )
        perModuleStat(
            datasetDescriptor="cleaned_words_mapped",
            x_final=x_cleaned_mapped_words.copy(),
            y_final=y_cleaned_mapped_words.copy(),
            x=x_mapped_words.copy(),
            y=y_mapped_words.copy(),
            xy_surface_areas=xy_surface_area,
            centroid_coords=centroid_coords,
            mappedMatrixScores=mappedMatrixScores_cleaned_mapped_words,
        )

        result: bool = True
    except Exception as e:
        result = False
        g.logger.error(f"Error whilst running stats - {e}")
        raise e
    finally:
        return result
