# Re-importing necessary libraries and preparing data again
from typing import Dict, Union

from includes.statistics.reindexFaces import reindexFacesToEnsureAdjacency
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
                "centroid_coords": centroid_coords,
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
                "centroid_coords": centroid_coords,
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
        x_orig, y_orig = clean_data(
            nan_handlers=["save"], x=x_orig.copy(), y=y_orig.copy()
        )

        # We apply Reverse Cuthill McKee to the adjacency matrix to reduce the bandwidth of the matrix.
        # Put simply, we reindex the faces so that connected faces are adjacacent (or more likely to be).
        x_orig, y_orig, centroid_coords = reindexFacesToEnsureAdjacency(
            x_orig, y_orig, centroid_coords
        )
        # new_index_order = x_orig.attrs["applied_handlers"][-1]["metadata"]["mapping"]

        x_orig, y_orig = clean_data(
            nan_handlers=["save"], x=x_orig.copy(), y=y_orig.copy()
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
        orig_mapping, _x_mapped, _y_mapped, mappedMatrixScores = mapAllModulesToSameSet(
            x=x_orig, y=y_orig, centroid_coords=centroid_coords
        )
        x_mapped, y_mapped = clean_data(nan_handlers=["save"], x=_x_mapped, y=_y_mapped)
        del _x_mapped, _y_mapped

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

        x_cleaned, y_cleaned = clean_data(
            nan_handlers=[
                "mask_removeMissing",
                "filter_by_parent",
            ],
            x=x_orig.copy(),
            y=y_orig.copy(),
        )

        # -----
        # Convert pd.Series[int] => pd.Series[str]
        # NB: To demonstrate that statistical tests must work on categorical named data (and definitely not numerical), map module names (e.g., "2") to random words (e.g., "hsjjrnsyhf").
        # ------
        # Convert original mapped data to words. (For comparison only.)
        _x_orig_words, _y_orig_words, label_to_word_map_y = (
            convertNumericalModulesToWords(
                x_orig, x_orig, mapName=f"orig_{config.CURRENT_TASK}"
            )
        )
        x_orig_words, y_orig_words = clean_data(
            nan_handlers=["save"], x=_x_orig_words, y=_y_orig_words
        )
        del _x_orig_words, _y_orig_words

        mappedMatrixScores_orig_words = {
            label_to_word_map_y.get(int(old_key), old_key): value
            for old_key, value in mappedMatrixScores.items()
        }

        _x_cleaned_words, _y_cleaned_words, label_to_word_map_y = (
            convertNumericalModulesToWords(
                x_cleaned, y_cleaned, mapName=f"cleaned_{config.CURRENT_TASK}"
            )
        )
        x_cleaned_words, y_cleaned_words = clean_data(
            nan_handlers=["save"], x=_x_cleaned_words, y=_y_cleaned_words
        )
        del _x_cleaned_words, _y_cleaned_words

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
        x_mapped_cleaned, y_mapped_cleaned = clean_data(
            nan_handlers=[
                "mask_removeMissing",
                "filter_by_parent",
            ],
            x=x_mapped,
            y=y_mapped,
            orig_x=x_mapped,  # Used to pass original x to filter_by_parent
            xRetrievalMethod="getAll",
            centroid_coords=centroid_coords,
        )

        # ------
        # Convert pd.Series[int] => pd.Series[str]
        # NB: To demonstrate that statistical tests must work on categorical named data (and definitely not numerical), map module names (e.g., "2") to random words (e.g., "hsjjrnsyhf").
        # ------
        _x_mapped_words, _y_mapped_words, label_to_word_map_y = (
            convertNumericalModulesToWords(
                x=x_mapped,
                y=y_mapped,
                dataIsMapped=True,
                mapName=f"mapped_{config.CURRENT_TASK}",
            )
        )
        x_mapped_words, y_mapped_words = clean_data(
            nan_handlers=["save"], x=_x_mapped_words, y=_y_mapped_words
        )
        del _x_mapped_words, _y_mapped_words

        mappedMatrixScores_mapped_words = {
            label_to_word_map_y.get(
                int(old_key), f"KeyNotFoundInIntToStringMap-{old_key}"
            ): value
            for old_key, value in mappedMatrixScores.items()
        }

        _x_cleaned_mapped_words, _y_cleaned_mapped_words, label_to_word_map_y = (
            convertNumericalModulesToWords(
                x_mapped_cleaned,
                y_mapped_cleaned,
                dataIsMapped=True,
                mapName=f"cleaned_mapped_{config.CURRENT_TASK}",
            )
        )
        x_mapped_cleaned_words, y_mapped_cleaned_words = clean_data(
            nan_handlers=["save"], x=_x_cleaned_mapped_words, y=_y_cleaned_mapped_words
        )
        del _x_cleaned_mapped_words, _y_cleaned_mapped_words

        mappedMatrixScores_cleaned_mapped_words = {
            label_to_word_map_y.get(int(old_key), old_key): value
            for old_key, value in mappedMatrixScores.items()
        }

        for xory_as_words in [x_mapped_cleaned_words, y_mapped_cleaned_words]:
            xory_as_words.attrs.update(
                {
                    "dataset_descriptors": xory_as_words.attrs["dataset_descriptors"],
                    "applied_handlers": xory_as_words.attrs["applied_handlers"],
                }
            )

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
            ("mapped", x_mapped, y_mapped),
            ("orig_words", x_orig_words, y_orig_words),
            ("mapped_words", x_mapped_words, y_mapped_words),
            ("cleaned", x_cleaned, y_cleaned),
            ("cleaned_words", x_cleaned_words, y_cleaned_words),
            ("mapped_cleaned", x_mapped_cleaned, y_mapped_cleaned),
            ("mapped_cleaned_words", x_mapped_cleaned_words, y_mapped_cleaned_words),
        ]:
            x: "pd.Series[Union[int,str]]"
            y: "pd.Series[Union[int,str]]"
            pass

        perSubjectStat("cleaned_words", x_cleaned_words.copy(), y_cleaned_words.copy())
        perSubjectStat(
            "cleaned_words_mapped",
            x_mapped_cleaned_words.copy(),
            y_mapped_cleaned_words.copy(),
        )

        # perModuleStat(
        #     datasetDescriptor="cleaned_words",
        #     x_final=x_mapped_cleaned_words,
        #     y_final=y_mapped_cleaned_words,
        #     x=x_orig_words,
        #     y=y_orig_words,
        #     xy_surface_areas=xy_surface_area,
        #     centroid_coords=centroid_coords,
        #     mappedMatrixScores=mappedMatrixScores_cleaned_words,
        # )
        perModuleStat(
            x_final=x_mapped_words.copy(),
            y_final=y_mapped_words.copy(),
            x=x_mapped_words.copy(),
            y=y_mapped_words.copy(),
            xy_surface_areas=xy_surface_area,
            centroid_coords=centroid_coords,
            mappedMatrixScores=mappedMatrixScores_mapped_words,
        )
        perModuleStat(
            x_final=x_mapped_cleaned_words.copy(),
            y_final=y_mapped_cleaned_words.copy(),
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
