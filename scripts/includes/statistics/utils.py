import pandas as pd
import random
import string
from typing import Any, Dict, Optional, Tuple, TypedDict, Union, cast
import numpy as np
import numpy.typing as npt
from pathlib import Path
from scipy.stats import mode
from sklearn.metrics.cluster import contingency_matrix
from scipy.optimize import linear_sum_assignment  # type: ignore
import Levenshtein
import modules.globals as g


# Function to generate a random word
class XYZDict(TypedDict):
    x: float
    y: float
    z: float


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
) -> "tuple[pd.Series[str], pd.Series[str], dict[int, str]]":
    if dataIsMapped:
        # Take from same dictionary of labels
        label_to_word_map_xory: dict[int, str] = createLabelToRandomWordLookup(x=x, y=y)
        y_labels: dict[int, str] = label_to_word_map_xory
        x_labels: dict[int, str] = label_to_word_map_xory
    else:
        # Take from different dictionaries of labels
        label_to_word_map_x: dict[int, str] = createLabelToRandomWordLookup(x=x)
        label_to_word_map_y: dict[int, str] = createLabelToRandomWordLookup(y=y)
        label_to_word_map_xory: dict[int, str] = (
            label_to_word_map_y  # We need to return what functional modules were mapped to.
        )
        x_labels: dict[int, str] = label_to_word_map_x
        y_labels: dict[int, str] = label_to_word_map_y

    x_as_words: "pd.Series[str]" = convertNumericalModuleToWords(
        xory=x, label_to_word_map_xory=x_labels
    )
    y_as_words: "pd.Series[str]" = convertNumericalModuleToWords(
        xory=y, label_to_word_map_xory=y_labels
    )

    return x_as_words, y_as_words, label_to_word_map_xory


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
    centroid_coords: "pd.DataFrame",
    mappedNames: "Optional[dict[str,str]]" = None,
    mappedMatrixScores: Optional[Dict[str, Dict[str, float]]] = None,
) -> "tuple[dict[str,str],Union[pd.Series[int],pd.Series[str]], Union[pd.Series[int],pd.Series[str]], Dict[str, Dict[str, float]]]":
    row_ind: list[int]
    col_ind: list[int]
    x_mapped: Union[pd.Series[int], pd.Series[str]] = x.copy()
    y_mapped: Union[pd.Series[int], pd.Series[str]] = y.copy()
    if mappedNames is None or mappedMatrixScores is None:
        # Mapping has not been performed before.
        mappingProvided = False

        # CONTINGENCY MATRIX
        # Get a matrix of occurrence of each module name
        cont_matrix: npt.NDArray = cast(
            npt.NDArray,
            contingency_matrix(
                labels_true=x.to_numpy(), labels_pred=y.to_numpy(), sparse=False
            ),
        )
        # Normalize both matrices and combine them into a cost matrix
        max_contingency = cont_matrix.max() if cont_matrix.max() != 0 else 1
        # Normalize contingency to 0-1 range
        norm_cont_matrix = (1 - (cont_matrix / max_contingency)) / 3

        # LEVENSHTEIN MATRIX
        unique_x = pd.Series(x.unique())  # Unique labels in x
        unique_y = pd.Series(y.unique())  # Unique labels in y
        norm_lev_matrix: npt.NDArray[np.float64] = np.zeros(
            (len(unique_x), len(unique_y))
        )  # Initialize the matrix with zeros

        g.logger.info(
            "Computing normalised levenshtein distance for all possible module pairs"
        )
        # Populate the Levenshtein distance matrix
        for i, x_label in enumerate(unique_x):
            for j, y_label in enumerate(unique_y):
                norm_lev_matrix[i, j] = np.float64(
                    calculateNormalisedLevenshteinDistance(
                        x=pd.Series(np.where(x == x_label, 1, 0)).astype(int),
                        y=pd.Series(np.where(y == y_label, 1, 0)).astype(int),
                    )
                )
        # max_lev_distance = norm_lev_matrix.max().max()
        # norm_lev_matrix = (norm_lev_matrix / max_lev_distance) / 3
        norm_lev_matrix = norm_lev_matrix / 3

        # CENTROID DISTANCE MATRIX
        centroid_distance_matrix = np.zeros(
            (len(unique_x), len(unique_y))
        )  # Initialize the matrix with zeros
        g.logger.info(
            "Computing centroid Euclidean distance for all possible module pairs"
        )
        # Populate the centroid Euclidean distance matrix
        for i, x_label in enumerate(unique_x):
            for j, y_label in enumerate(unique_y):
                centroid_distance_matrix[i, j], _, _ = calculateEuclidianDistance(
                    centroid_coords=centroid_coords,
                    x=x.where(x == x_label),
                    y=y.where(y == y_label),
                )
        # Normalise the Euclidian distance matrix
        max_centroid_distance = centroid_distance_matrix.max().max()
        norm_centroid_distance_matrix: npt.NDArray[np.float64] = (
            centroid_distance_matrix / max_centroid_distance
        ) / 3

        # Combine the contingency matrix, Levenshtein distance matrix, and centroid Euclidean distance matrix
        # Use Hungarian algorithm to find the optimal mapping between the two sets
        row_ind, col_ind = linear_sum_assignment(
            # NOTE: Matrices are divided by three previously so cost sum should be 1.
            (1 * (norm_cont_matrix))
            + (1 * norm_lev_matrix)
            + (1 * norm_centroid_distance_matrix)
        )
        # Create a mapping of the modules
        mapping = zip(row_ind, col_ind)

        xLabels: "npt.NDArray" = x.unique()
        yLabels: "npt.NDArray" = y.unique()
        mappedNames = dict()
        mappedMatrixScores = dict()
        norm_total_cost_matrix = (
            norm_cont_matrix + norm_lev_matrix + norm_centroid_distance_matrix
        )
        for row, col in mapping:
            mappedNames[f"{yLabels[col]}"] = f"{xLabels[row]}"
            mappedMatrixScores[f"{yLabels[col]}"] = {
                "norm_cont": float(norm_cont_matrix[row, col]),
                "norm_lev": float(norm_lev_matrix[row, col]),
                "norm_centroid_distance": float(
                    norm_centroid_distance_matrix[row, col]
                ),
                "norm_total_cost": float(norm_total_cost_matrix[row, col]),
            }
        pass
    else:
        pass
    # We must apply a previously acquired map to the data
    for yModuleName, xModuleName in mappedNames.items():
        if yModuleName == "-1":
            # continue
            xModuleName = f"missing"
        y_mapped[y_mapped == yModuleName] = xModuleName
    return mappedNames, x_mapped, y_mapped, mappedMatrixScores


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


def getCentroid(
    centroid_coords: pd.DataFrame,
    x: "Union[pd.Series[str],pd.Series[int]]",
    y: "Union[pd.Series[str],pd.Series[int]]",
):

    x_module_indices: npt.NDArray[np.int64] = np.where(~x.isna())[0]
    x_module_coords: npt.NDArray[np.float64] = centroid_coords.T.values[
        x_module_indices
    ]
    x_module_centroid_coords_np: Tuple[np.float64, np.float64, np.float64] = tuple(
        x_module_coords.mean(axis=0)
    )
    x_module_centroid_coords: XYZDict = {
        "x": float(x_module_centroid_coords_np[0]),
        "y": float(x_module_centroid_coords_np[1]),
        "z": float(x_module_centroid_coords_np[2]),
    }

    y_module_indices: npt.NDArray[np.int64] = np.where(~y.isna())[0]
    y_module_coords: npt.NDArray[np.float64] = centroid_coords.T.values[
        y_module_indices
    ]
    y_module_centroid_coords_np: Tuple[np.float64, np.float64, np.float64] = tuple(
        y_module_coords.mean(axis=0)
    )
    y_module_centroid_coords: XYZDict = {
        "x": float(y_module_centroid_coords_np[0]),
        "y": float(y_module_centroid_coords_np[1]),
        "z": float(y_module_centroid_coords_np[2]),
    }

    return x_module_centroid_coords, y_module_centroid_coords


def calculateEuclidianDistance(
    centroid_coords: "pd.DataFrame",
    x: "Union[pd.Series[str],pd.Series[int]]",
    y: "Union[pd.Series[str],pd.Series[int]]",
) -> Tuple[float, XYZDict, XYZDict]:
    x_module_centroid_coords, y_module_centroid_coords = getCentroid(
        centroid_coords, x, y
    )
    x_coords = np.array(list(x_module_centroid_coords.values()))
    y_coords = np.array(list(y_module_centroid_coords.values()))
    distance: np.float64 = np.linalg.norm(x=np.subtract(x_coords, y_coords))

    return (float(distance), x_module_centroid_coords, y_module_centroid_coords)


def calculate_dice_coefficient(
    labels_true: "Union[pd.Series[str], pd.Series[int]]",
    labels_pred: "Union[pd.Series[str], pd.Series[int]]",
) -> float:
    """
    Calculate the Dice Coefficient between two sets of labels.

    Args:
        labels_true (Union[pd.Series[str], pd.Series[int]]): The ground truth labels.
        labels_pred (Union[pd.Series[str], pd.Series[int]]): The predicted labels.

    Returns:
        float: The Dice Coefficient (0 to 1).
    """
    # Ensure inputs are pandas Series
    if not isinstance(labels_true, pd.Series) or not isinstance(labels_pred, pd.Series):
        raise TypeError("Both labels_true and labels_pred must be pandas Series.")

    # Ensure both Series have the same length
    if len(labels_true) != len(labels_pred):
        raise ValueError("labels_true and labels_pred must have the same length.")

    # Create binary masks for labels_true and labels_pred
    unique_labels = set(labels_true.dropna().unique()) | set(
        labels_pred.dropna().unique()
    )
    dice_scores = []

    # Compute the Dice Coefficient for each unique label
    for label in unique_labels:
        true_mask = (labels_true == label).astype(int)
        pred_mask = (labels_pred == label).astype(int)

        intersection = np.sum(true_mask & pred_mask)
        size_true = np.sum(true_mask)
        size_pred = np.sum(pred_mask)

        # Avoid division by zero
        if size_true + size_pred == 0:
            dice_scores.append(1.0)  # Perfect agreement for empty labels
        else:
            dice_scores.append(2 * intersection / (size_true + size_pred))

    # Return the average Dice Coefficient across all labels
    return float(np.mean(dice_scores))
