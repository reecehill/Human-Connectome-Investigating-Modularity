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
    def get_latest_label_to_word_map(
        x: "pd.Series[Any]", y: "pd.Series[Any]"
    ) -> "set[int]":
        attrs = x.attrs.get("applied_handlers", y.attrs.get("applied_handlers", []))
        for item in reversed(attrs):  # Check from the latest to earliest
            if "metadata" in item and "label_to_word_map_xory" in item["metadata"]:
                return item["metadata"]["label_to_word_map_xory"]
        return set(x.to_list() + y.to_list())

    if x is None and y is None:
        raise ValueError("At least one of x or y must be provided.")
    if x is None:
        x = pd.Series([], dtype=int)
    if y is None:
        y = pd.Series([], dtype=int)

    unique_labels_xory: set[int] = get_latest_label_to_word_map(x, y)

    def label_to_string(label: int) -> str:
        """
        Converts a label into a predictable string by encoding its digits.

        Each digit (1-9) is mapped to A-I, and 0 is mapped to Z.
        For multi-digit numbers, the characters are concatenated in order.
        """
        encoding = {
            -1: "Z",
            0: "A",
            1: "B",
            2: "C",
            3: "D",
            4: "E",
            5: "F",
            6: "G",
            7: "H",
            8: "I",
            9: "J",
        }
        if label == -1:
            # Handle negative numbers by prefixing "NEG-" to the encoded digits
            digits = [int(d) for d in str(abs(label))]
            return "missing-" + "".join(encoding[d] for d in digits)
        else:
            digits = [int(d) for d in str(label)]
            return "".join(encoding[d] for d in digits)

    # Step 2: Create a dictionary to map each label to a predictable string
    try:
        label_to_word_map_xory: "dict[int, str]" = {
            label: label_to_string(label) for label in unique_labels_xory
        }
    except Exception as e:
        print(f"Error while creating label_to_word_map_xory: {e}")
        return {}  # Return an empty dictionary in case of error.

    return label_to_word_map_xory


def convertNumericalModuleToWords(
    xory: "pd.Series[int]", label_to_word_map_xory: "dict[int,str]"
) -> "pd.Series[str]":
    # Step 4: Apply the mapping to x and y
    xory_as_words: "pd.Series[str]" = pd.Series(
        [label_to_word_map_xory[label] for label in xory], index=xory.index
    )
    xory_as_words.attrs = xory.attrs
    return xory_as_words


def convertNumericalModulesToWords(
    x: "pd.Series[int]",
    y: "pd.Series[int]",
    dataIsMapped: bool = False,
    mapName: str = "blankMapName",
) -> "tuple[pd.Series[str], pd.Series[str], dict[int, str]]":

    import config

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

    # Write the DataFrame to a CSV file without a header
    df = pd.DataFrame(list(label_to_word_map_xory.items()), columns=["int", "str"])
    map_csv = config.SUBJECT_DIR / "exported_modules" / f"map_{mapName}.csv"
    df.to_csv(str(map_csv), index=False, header=False)

    x_as_words.attrs.update(
        {
            "dataset_descriptors": {
                **x_as_words.attrs.get("dataset_descriptors", {}),
                "data_type": "words",
            },
            "applied_handlers": x_as_words.attrs["applied_handlers"]
            + [
                {
                    "name": "convertNumericalModulesToWords",
                    "metadata": {"label_to_word_map_xory": label_to_word_map_xory},
                }
            ],
        }
    )

    y_as_words.attrs.update(
        {
            "dataset_descriptors": {
                **y_as_words.attrs.get("dataset_descriptors", {}),
                "data_type": "words",
            },
            "applied_handlers": y_as_words.attrs["applied_handlers"]
            + [
                {
                    "name": "convertNumericalModulesToWords",
                    "metadata": {"label_to_word_map_xory": label_to_word_map_xory},
                }
            ],
        }
    )
    return x_as_words, y_as_words, label_to_word_map_xory


def enlarge_mask_with_mode_priority(
    mask: "pd.Series[int]", n: int, mode_method: str
) -> "pd.Series[int]":
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
    x_str: "pd.Series[str]" = x.astype(str)
    y_str: pd.Series[str] = y.astype(str)

    if mappedNames is None or mappedMatrixScores is None:
        # CONTINGENCY MATRIX
        # Get a matrix of occurrence of each module name
        y_unique = np.unique(y_str.to_numpy()).astype(str)
        x_unique = np.unique(x_str.to_numpy()).astype(str)

        cont_matrix: pd.DataFrame = pd.DataFrame(
            cast(
                npt.NDArray,
                contingency_matrix(
                    labels_true=x_str.to_numpy(),
                    labels_pred=y_str.to_numpy(),
                    sparse=False,
                ),
            ),
            index=x_unique,
            columns=y_unique,
        )

        # We avoid mapping Y=-1 as this could prevent an optimal mapping of a good module
        cont_matrix.drop(
            np.array([-1]).astype(str).tolist(), inplace=True, errors="ignore", axis=0
        )
        cont_matrix.drop(
            np.array([-1]).astype(str).tolist(), inplace=True, errors="ignore", axis=1
        )

        x_labels = cont_matrix.index.tolist()
        y_labels = cont_matrix.columns.tolist()

        # Normalize both matrices and combine them into a cost matrix
        max_contingency = (
            np.max(cont_matrix.values) if np.max(cont_matrix.values) != 0 else 1
        )

        # Normalize contingency to 0-1 range
        # norm_cont_matrix = (1 - (cont_matrix / max_contingency)) / 2
        norm_cont_matrix = 1 - (cont_matrix / max_contingency)

        # CENTROID DISTANCE MATRIX
        centroid_distance_matrix = pd.DataFrame(
            np.zeros(cont_matrix.shape, dtype=np.float64),
            index=x_labels,
            columns=y_labels,
        )  # Initialize the matrix with zeros
        g.logger.info(
            "Computing centroid Euclidean distance for all possible module pairs"
        )

        # Populate the centroid Euclidean distance matrix
        # Cache labels to avoid redundant calls

        # Precompute masks for x and y
        x_conditions = {label: (x_str == label) for label in x_labels}
        y_conditions = {label: (y_str == label) for label in y_labels}

        for x_label in x_labels:
            for y_label in y_labels:
                x_filtered = x_str.where(x_conditions[x_label])
                y_filtered = y_str.where(y_conditions[y_label])

                # Calculate the Euclidean distance
                centroid_distance_matrix.at[x_label, y_label], _, _ = (
                    calculateEuclidianDistance(
                        centroid_coords=centroid_coords,
                        x=x_filtered,
                        y=y_filtered,
                    )
                )

        # Normalise the Euclidian distance matrix
        max_centroid_distance = centroid_distance_matrix.max().max()
        norm_centroid_distance_matrix: pd.DataFrame = (
            centroid_distance_matrix / max_centroid_distance
        )

        # Combine the contingency matrix, Levenshtein distance matrix, and centroid Euclidean distance matrix
        # Use Hungarian algorithm to find the optimal mapping between the two sets
        row_ind, col_ind = linear_sum_assignment(
            # NOTE: Matrices are divided by three previously so cost sum should be 1.
            (1 * (norm_cont_matrix / 1))
            # + (1 * norm_centroid_distance_matrix /2)
        )
        # Create a mapping of the modules
        mapping = zip(cont_matrix.index[row_ind], cont_matrix.columns[col_ind])
        mappedNames = dict()
        mappedMatrixScores = dict()
        # norm_total_cost_matrix = norm_cont_matrix + norm_centroid_distance_matrix
        norm_total_cost_matrix = norm_cont_matrix
        for xLabel, yLabel in mapping:
            pass
            if f"{yLabel}" == "-1":
                # Do not map missing values
                xLabel = "-1"
            mappedNames[f"{yLabel}"] = f"{xLabel}"
            # Note we map according to X value (as if post-mapping)
            mappedMatrixScores[f"{xLabel}"] = {
                "norm_cont": float(norm_cont_matrix.at[xLabel, yLabel]),
                "norm_centroid_distance": float(
                    norm_centroid_distance_matrix.at[xLabel, yLabel]
                ),
                "norm_total_cost": float(norm_total_cost_matrix.at[xLabel, yLabel]),
            }
            pass
        pass
    else:
        pass
    # We must apply a previously acquired map to the data
    y_mapped = y_mapped.astype(str).map(mappedNames).fillna(y_mapped.astype(str))

    if y_mapped.attrs["dataset_descriptors"]["data_type"] == "int":
        # Ensure "1"(str) is cast back to 1(int).
        y_mapped = y_mapped.astype(int)

    x_mapped.attrs.update(
        {
            "dataset_descriptors": {
                **x_mapped.attrs.get("dataset_descriptors", {}),
                "dataset_name": "mapped",
            },
            "applied_handlers": x_mapped.attrs["applied_handlers"]
            + [
                {
                    "name": "mapAllModulesToSameSet",
                    "metadata": {
                        "pre_handler_length": x_mapped.size,
                        "mappedNames": mappedNames,
                        "mappedMatrixScores": mappedMatrixScores,
                    },
                }
            ],
        }
    )
    y_mapped.attrs.update(
        {
            "dataset_descriptors": {
                **y_mapped.attrs.get("dataset_descriptors", {}),
                "dataset_name": "mapped",
            },
            "applied_handlers": y_mapped.attrs["applied_handlers"]
            + [
                {
                    "name": "mapAllModulesToSameSet",
                    "metadata": {
                        "pre_handler_length": y_mapped.size,
                        "mappedNames": mappedNames,
                        "mappedMatrixScores": mappedMatrixScores,
                    },
                }
            ],
        }
    )
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


def calculate_percent_identity(
    labels_truth: "Union[pd.Series[str], pd.Series[int]]",
    labels_pred: "Union[pd.Series[int], pd.Series[str]]",
) -> "np.float64":
    """
    Calculate the percent identity between true labels and predicted labels.

    Parameters:
    labels_truth (pd.Series[str] or pd.Series[int]): The ground truth labels.
    labels_pred (pd.Series[str] or pd.Series[int]): The predicted labels.

    Returns:
    np.float64: The percent identity as a float64 value.
    """
    # Ensure both Series have the same shape
    if labels_truth.shape != labels_pred.shape:
        raise ValueError("labels_truth and labels_pred must have the same shape.")

    # Calculate the number of matches
    matches = (labels_truth == labels_pred).sum()

    # Calculate the percent identity
    percent_identity_value = (matches / len(labels_truth))

    return np.float64(percent_identity_value)
