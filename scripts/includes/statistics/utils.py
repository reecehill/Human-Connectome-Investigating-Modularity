import pandas as pd
import random
import string
from typing import Any, Optional, Union, cast
import numpy as np
import numpy.typing as npt
from pathlib import Path
from scipy.stats import mode
from sklearn.metrics.cluster import contingency_matrix
from scipy.optimize import linear_sum_assignment  # type: ignore
import Levenshtein
import modules.globals as g

# Function to generate a random word


def random_word(length=10):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


def createLabelToRandomWordLookup(
    x: "Optional[pd.Series[int]]" = None, y: "Optional[pd.Series[int]]" = None
) -> dict[int, str]:
    if x is None and y is None:
        raise ValueError("At least one of x or y must be provided.")
    if x is None:
        x = pd.Series([], dtype=int)
    if y is None:
        y = pd.Series([], dtype=int)

    unique_labels_xory: set[int] = set(x.to_list() + y.to_list())

    # Step 2: Create a dictionary to map each label to a random word
    label_to_word_map_xory: "dict[int, str]" = {
        label: random_word() for label in unique_labels_xory
    }

    # Step 3: For missing modules, make their labels "missing". (So we can easily identify them)
    if -1 in unique_labels_xory:
        label_to_word_map_xory[-1] = f"missing"

    return label_to_word_map_xory


def convertNumericalModuleToWords(
    xory: "pd.Series[int]", label_to_word_map_xory: "dict[int,str]"
) -> "pd.Series[str]":
    # Step 4: Apply the mapping to x and y
    xory_as_words: "pd.Series[str]" = pd.Series(
        [label_to_word_map_xory[label] for label in xory], index=xory.index
    )
    return xory_as_words


def convertNumericalModulesToWords(
    x: "pd.Series[int]", y: "pd.Series[int]", dataIsMapped: bool = False
) -> "tuple[pd.Series[str], pd.Series[str]]":
    if dataIsMapped:
        # Take from same dictionary of labels
        label_to_word_map_xory: dict[int, str] = createLabelToRandomWordLookup(x=x, y=y)
        y_labels: dict[int, str] = label_to_word_map_xory
        x_labels: dict[int, str] = label_to_word_map_xory
    else:
        # Take from different dictionaries of labels
        label_to_word_map_x: dict[int, str] = createLabelToRandomWordLookup(x=x)
        label_to_word_map_y: dict[int, str] = createLabelToRandomWordLookup(y=y)
        x_labels: dict[int, str] = label_to_word_map_x
        y_labels: dict[int, str] = label_to_word_map_y

    x_as_words: "pd.Series[str]" = convertNumericalModuleToWords(
        xory=x, label_to_word_map_xory=x_labels
    )
    y_as_words: "pd.Series[str]" = convertNumericalModuleToWords(
        xory=y, label_to_word_map_xory=y_labels
    )

    return x_as_words, y_as_words


def enlarge_mask_with_mode_priority(mask: "pd.Series[int]", n: int, mode_method: str):
    if n == 1:
        # No padding needed
        return mask
    padded_mask: "pd.Series[int]" = mask.copy(deep=True).sample(frac=1)  # random
    possibleIndexes: "pd.Index[Any]" = padded_mask.index
    valueCounts: "pd.Series[int]" = padded_mask.value_counts().drop(
        [-1], errors="ignore"
    )
    for idx in possibleIndexes:
        # Define window for smoothing
        start_window = max(0, idx - n)
        end_window = min(possibleIndexes.max(), idx + n + 1)

        # Find the mode of the values in the window
        window = mask[start_window:end_window]
        mode_value: float
        if mode_method == "window":
            if window.size != 0.0:
                mode_value = mode(window, axis=None, nan_policy="omit", keepdims=True)[
                    0
                ]
            else:
                mode_value = -1.0
        elif mode_method == "roi":
            # Within the mask, just select module that is the largest (mode)
            currentModules = window.values
            # Not all modules in window are unset, so continue to keep this one unset.
            if pd.Series(currentModules == -1).all():
                mode_value = -1
            else:
                modulesBySize: "pd.Series[int]" = valueCounts[
                    currentModules[currentModules != -1]
                ]
                largestModule: float = float(modulesBySize.idxmax())
                mode_value = largestModule
        else:
            raise ValueError(
                f'Invalid mode_method: {mode_method}. Expected "window" or "roi".'
            )

        # Overwrite the current index with the mode
        padded_mask[idx] = mode_value

    return padded_mask


def append_result_to_csv(df: pd.DataFrame, filename: Path):
    # Check if the file exists
    if not filename.is_file():
        # If the file doesn't exist, write the header and data
        df.to_csv(filename, mode="w", header=True, index=False)
    else:
        # If the file exists, append the data without writing the header
        df.to_csv(filename, mode="a", header=False, index=False)


def calcModuleSizes(
    x_module: "Union[pd.Series[str], pd.Series[int]]",
    y_module: "Union[pd.Series[str], pd.Series[int]]",
    xy_surface_area: "npt.NDArray[np.float64]",
) -> "tuple[np.float64, np.float64, np.float64]":
    x_indices = x_module.index
    y_indices = y_module.index

    x_module_sa: np.float64 = xy_surface_area[x_indices].sum()

    y_module_sa: np.float64 = xy_surface_area[y_indices].sum()

    ydivx_modula_sa: np.float64 = y_module_sa / x_module_sa

    return x_module_sa, y_module_sa, ydivx_modula_sa


def mapAllModulesToSameSet(
    x: "Union[pd.Series[int],pd.Series[str]]",
    y: "Union[pd.Series[int],pd.Series[str]]",
    mappedNames: "Optional[dict[str,str]]" = None,
) -> "tuple[dict[str,str],Union[pd.Series[int],pd.Series[str]], Union[pd.Series[int],pd.Series[str]]]":
    row_ind: list[int]
    col_ind: list[int]
    x_mapped: Union[pd.Series[int], pd.Series[str]] = x.copy()
    y_mapped: Union[pd.Series[int], pd.Series[str]] = y.copy()
    if mappedNames is None:
        # Mapping has not been performed before.
        mappingProvided = False

        # Use linear sum assignment to find the optimal mapping between the two sets

        # Get a matrix of occurrence of each module name
        cont_matrix: npt.NDArray = cast(
            npt.NDArray,
            contingency_matrix(
                labels_true=x.to_numpy(), labels_pred=y.to_numpy(), sparse=False
            ),
        )

        unique_x = pd.Series(x.unique())  # Unique labels in x
        unique_y = pd.Series(y.unique())  # Unique labels in y

        norm_lev_matrix = pd.DataFrame(index=unique_x, columns=unique_y)
        g.logger.info(
            "Computing normalised levenshtein distance for all possible module pairs"
        )
        # Populate the Levenshtein distance matrix
        for i, x_label in enumerate(unique_x):
            for j, y_label in enumerate(unique_y):
                norm_lev_matrix.iloc[i, j] = calculateNormalisedLevenshteinDistance(
                    x.where(x == x_label), y.where(y == y_label)
                )

        # Step 3: Combine the contingency matrix and Levenshtein distance matrix
        # Normalize both matrices and combine them into a cost matrix
        max_contingency = cont_matrix.max() if cont_matrix.max() != 0 else 1
        # Normalize contingency to 0-1 range
        norm_cont_matrix = cont_matrix / max_contingency

        # Use Hungarian algorithm to find the optimal mapping between the two sets
        row_ind, col_ind = linear_sum_assignment(
            (0.5 * (1 - norm_cont_matrix)) + (0.5 * norm_lev_matrix)
        )  # type:ignore
        # Create a mapping of the modules

        mapping = zip(row_ind, col_ind)

        xLabels: "npt.NDArray" = x.unique()
        yLabels: "npt.NDArray" = y.unique()
        mappedNames = {f"{yLabels[col]}": f"{xLabels[row]}" for row, col in mapping}

    else:
        pass
    # We must apply a previously acquired map to the data
    for yModuleName, xModuleName in mappedNames.items():
        if yModuleName == "-1":
            # continue
            xModuleName = f"missing"
        y_mapped[y_mapped == yModuleName] = xModuleName
    return mappedNames, x_mapped, y_mapped


def calculateLevenshteinDistance(
    x: "Union[pd.Series[str],pd.Series[int]]", y: "Union[pd.Series[str],pd.Series[int]]"
) -> int:
    # This is a token based approach to calculate the distance between modules.
    distance = Levenshtein.distance(x.to_list(), y.to_list())
    return distance


def calculateNormalisedLevenshteinDistance(
    x: "Union[pd.Series[str],pd.Series[int]]", y: "Union[pd.Series[str],pd.Series[int]]"
) -> float:
    # This is a token based approach to calculate the distance between modules.
    distance: float = Levenshtein.distance(x.to_list(), y.to_list()) / max(
        x.size, y.size
    )
    return distance
