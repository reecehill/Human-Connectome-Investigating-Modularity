import pandas as pd
import random
import string
from typing import Any, Union
import numpy as np
import numpy.typing as npt
from pathlib import Path
from scipy.stats import mode

# Function to generate a random word


def random_word(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def convertNumericalModuleToWords(xory: "pd.Series[int]") -> "pd.Series[str]":
    # Step 1: Get unique labels in x and y
    # Assuming x or y is an array or list
    unique_labels_xory = set(xory)

    # Step 2: Create a dictionary to map each label to a random word
    label_to_word_map_xory: "dict[float, str]" = {
        label: random_word() for label in unique_labels_xory
    }

    # Step 3: For missing modules, make their labels "missing". (So we can easily identify them)
    if (-1 in unique_labels_xory):
        label_to_word_map_xory[-1] = f'missing'

    # Step 4: Apply the mapping to x and y
    xory_as_words: "pd.Series[str]" = pd.Series(
        [label_to_word_map_xory[label] for label in xory], index=xory.index)
    return xory_as_words


def convertNumericalModulesToWords(x: "pd.Series[int]", y: "pd.Series[int]") -> "tuple[pd.Series[str], pd.Series[str]]":
    x_as_words: "pd.Series[str]" = convertNumericalModuleToWords(x)
    y_as_words: "pd.Series[str]" = convertNumericalModuleToWords(y)

    return x_as_words, y_as_words


def enlarge_mask_with_mode_priority(mask: "pd.Series[int]", n: int, mode_method: str):
    if n == 1:
        # No padding needed
        return mask
    padded_mask: "pd.Series[int]" = mask.copy(
        deep=True).sample(frac=1)  # random
    possibleIndexes: "pd.Index[Any]" = padded_mask.index
    valueCounts: "pd.Series[int]" = padded_mask.value_counts().drop(
        [-1], errors='ignore')
    for idx in possibleIndexes:
        # Define window for smoothing
        start_window = max(0, idx - n)
        end_window = min(possibleIndexes.max(), idx + n + 1)

        # Find the mode of the values in the window
        window = mask[start_window: end_window]
        mode_value: float
        if mode_method == 'window':
            if (window.size != 0.0):
                mode_value = mode(window, axis=None,
                                  nan_policy='omit', keepdims=True)[0]
            else:
                mode_value = -1.0
        elif mode_method == 'roi':
            # Within the mask, just select module that is the largest (mode)
            currentModules = window.values
            # Not all modules in window are unset, so continue to keep this one unset.
            if (pd.Series(currentModules == -1).all()):
                mode_value = -1
            else:
                modulesBySize: "pd.Series[int]" = valueCounts[currentModules[currentModules != -1]]
                largestModule: float = float(modulesBySize.idxmax())
                mode_value = largestModule
        else:
            raise ValueError(
                f'Invalid mode_method: {mode_method}. Expected "window" or "roi".')

        # Overwrite the current index with the mode
        padded_mask[idx] = mode_value

    return padded_mask


def append_result_to_csv(df: pd.DataFrame, filename: Path):
    # Check if the file exists
    if not filename.is_file():
        # If the file doesn't exist, write the header and data
        df.to_csv(filename, mode='w', header=True, index=False)
    else:
        # If the file exists, append the data without writing the header
        df.to_csv(filename, mode='a', header=False, index=False)


def calcModuleSizes(x_module: "pd.Series[str]", y_module: "pd.Series[str]", xy_surface_area: "npt.NDArray[np.float64]") -> "tuple[np.float64, np.float64, np.float64]":
    x_indices = x_module.index
    y_indices = y_module.index

    x_module_sa: np.float64 = xy_surface_area[
        x_indices].sum()

    y_module_sa: np.float64 = xy_surface_area[
        y_indices].sum()

    ydivx_modula_sa: np.float64 = y_module_sa / x_module_sa

    return x_module_sa, y_module_sa, ydivx_modula_sa
