# Re-importing necessary libraries and preparing data again
from typing import Literal, Union
import numpy as np
from numpy._typing import NDArray
import pandas as pd
import random
import string
from scipy.stats import mode
from includes.statistics import test_ranges, test_functions_with_range, generate_interpretation, convertResultsToDataFrames
from pathlib import Path

def runTests(subjectId: str, pathToXCsv: Path, pathToYCsv: Path, pathToOutputtedXlsx: Path) -> None:
    # Function to generate a random word
    def random_word(length=10):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

    x_raw: pd.DataFrame = pd.read_csv(pathToXCsv.absolute().__str__(), sep=',', header=None, keep_default_na=True).T
    y_raw: pd.DataFrame = pd.read_csv(pathToYCsv.absolute().__str__(), sep=',', header=None, keep_default_na=True).T
    x: pd.Series = x_raw[0]
    y: pd.Series = y_raw[0]

    # Padding/smoothing function
    def enlarge_mask_with_mode_priority(mask: pd.Series, n, mode_method: str):
        padded_mask = mask.copy(deep=True)
        possibleIndexes = padded_mask.index
        valueCounts = padded_mask.value_counts().drop([-1], errors='ignore')
        for idx in possibleIndexes:
            # Define window for smoothing
            start_window = max(0, idx - n)
            end_window = min(possibleIndexes.max(), idx + n + 1)
            
            # Find the mode of the values in the window
            window = mask[start_window : end_window]
            mode_value: float
            if mode_method == 'window':
                if(window.size != 0.0 ):
                    mode_value = mode(window, axis=None, nan_policy='omit',keepdims=True)[0]
                else:
                    mode_value = -1.0
            elif mode_method == 'roi':
                # Within the mask, just select module that is the largest (mode)
                currentModules = window.values
                # Not all modules in window are unset, so continue to keep this one unset.
                if(pd.Series(currentModules == -1).all()):
                    mode_value = -1
                else:
                    modulesBySize = valueCounts[currentModules[currentModules != -1]]
                    largestModule = modulesBySize.idxmax()
                    mode_value = largestModule
            else:
                raise ValueError(f'Invalid mode_method: {mode_method}. Expected "window" or "roi".')

            
            # Overwrite the current index with the mode
            padded_mask[idx] = mode_value
        
        return padded_mask

    # Cleaning data to exclude NaN values
    def switch(nan_handler: str, x: pd.Series, y: pd.Series) -> tuple[pd.Series,pd.Series]:
        idsOfNonNan: pd.Series = (x > 0) & (y > 0) # All modules begin counting from 1 onwards.
        x_out: pd.Series
        y_out: pd.Series
        print(f'n of structural modules: {len(x.unique())}')
        print(f'n of functional modules: {len(y.unique())}')
        if(nan_handler == 'mask'):
            x_out = x[idsOfNonNan]
            y_out = y[idsOfNonNan]
        elif(nan_handler == 'ffill'):
            y_out = y.ffill().bfill()
            x_out = x.ffill().bfill()
        elif(nan_handler == 'smoothed'):
            y_smoothed = y.fillna(value=int(-1), axis=0, inplace=False)
            y_smoothed = enlarge_mask_with_mode_priority(y_smoothed, n=2, mode_method='roi')
            y_smoothed = enlarge_mask_with_mode_priority(y_smoothed, n=1, mode_method='window')
            y_filtered = y_smoothed[idsOfNonNan]
            y_out = y_filtered
            x_smoothed = x.fillna(value=int(-1), axis=0, inplace=False)
            x_smoothed = enlarge_mask_with_mode_priority(x_smoothed, n=1, mode_method='window')
            x_smoothed = enlarge_mask_with_mode_priority(x_smoothed, n=1, mode_method='roi')
            x_filtered = x_smoothed[idsOfNonNan]
            x_out = x_filtered
        else:
            raise ValueError(f'Invalid nan_handler: {nan_handler}. Expected "mask", "ffill" or "smoothed".')
        print(f'n of structural modules (post-{nan_handler}): {len(x_out.unique())}')
        print(f'n of functional modules (post-{nan_handler}): {len(y_out.unique())}')
        return x_out, y_out

    def convertNumericalModuleToWords(xory: "Union[pd.Series[float],np.ndarray]") -> "pd.Series[str]":
        # Step 1: Get unique labels in x and y
        unique_labels_xory = set(xory)  # Assuming x or y is an array or list

        # Step 2: Create a dictionary to map each label to a random word
        label_to_word_map_xory: dict[float, str] = {label: random_word() for label in unique_labels_xory}

        # Step 3: Apply the mapping to x and y
        xory_as_words: pd.Series[str] = pd.Series([label_to_word_map_xory[label] for label in xory])
        return xory_as_words

    def convertNumericalModulesToWords(x, y) -> "tuple[pd.Series[str], pd.Series[str]]":
        x_as_words: pd.Series[str] = convertNumericalModuleToWords(x)
        y_as_words: pd.Series[str] = convertNumericalModuleToWords(y)
        # Step 1: Get unique labels in x and y
        unique_labels_x = set(x)  # Assuming x is an array or list
        unique_labels_y = set(y)  # Assuming y is an array or list

        # Step 2: Create a dictionary to map each label to a random word
        label_to_word_map_x: dict[str, str] = {label: random_word() for label in unique_labels_x}
        label_to_word_map_y: dict[str, str] = {label: random_word() for label in unique_labels_y}

        # Step 3: Apply the mapping to x and y
        x_as_words: pd.Series[str] = pd.Series([label_to_word_map_x[label] for label in x])
        y_as_words: pd.Series[str] = pd.Series([label_to_word_map_y[label] for label in y])

        return x_as_words, y_as_words

    # Mask, or smooth module names.
    x_clean, y_clean = switch(nan_handler="mask", x=x, y=y)

    # For absolute confidence that Python is not converting strings to integers, convert labels to random words.
    x_final, y_final = convertNumericalModulesToWords(x_clean, y_clean)


    # Prepare results storage
    results_x_truth_with_range = []
    results_y_truth_with_range = []

    # Run tests for X as truth
    for test_name, test_func in test_functions_with_range:
        try:
            score_x_defined = test_func(x_final, y_final)
            score_x_imported_random_y = test_func(
                x_final, 
                convertNumericalModuleToWords(np.random.choice(
                        a=y_final.unique(),
                        size=len(y_final)
                        ))
                )
            score_x_random_y_imported = test_func(
                convertNumericalModuleToWords(np.random.choice(
                    a=x_final.unique(),
                    size=len(x_final)
                    )),
                y_final
                )
            
            results_x_truth_with_range.append([
                test_name, 
                score_x_defined, 
                score_x_imported_random_y, 
                score_x_random_y_imported, 
                generate_interpretation(test_name, score_x_defined),
                test_ranges[test_name]
            ])
        except Exception as e:
            print(f"Error running {test_name} with x as truth: {e}")

    # Run tests for Y as truth
    for test_name, test_func in test_functions_with_range:
        try:
            score_y_defined = test_func(y_final, x_final)
            score_y_imported_random_x = test_func(
                y_final,
                convertNumericalModuleToWords(np.random.choice(
                    x_final.unique(),
                    size=len(x_final)
                    ))
            )
            score_y_random_x_imported = test_func(
                convertNumericalModuleToWords(np.random.choice(
                    y_final.unique(),
                    size=len(y_final)
                    )),
                x_final)
            
            results_y_truth_with_range.append([
                test_name, 
                score_y_defined, 
                score_y_imported_random_x, 
                score_y_random_x_imported, 
                generate_interpretation(test_name, score_y_defined),
                test_ranges[test_name]
            ])
        except Exception as e:
            print(f"Error running {test_name} with y as truth: {e}")

        # Convert results to DataFrames

    # For tests not requiring truth, take x.
    df_x_truth_with_range, df_y_truth_with_range, df_no_truth_with_range = convertResultsToDataFrames(results_x_truth_with_range, results_y_truth_with_range)

    
    # Write results to Excel
    with pd.ExcelWriter(path=pathToOutputtedXlsx, engine='xlsxwriter') as writer:
        df_x_truth_with_range.to_excel(writer, sheet_name='X as Truth', index=False)
        df_y_truth_with_range.to_excel(writer, sheet_name='Y as Truth', index=False)
        df_no_truth_with_range.to_excel(writer, sheet_name='No Truth Required', index=False)

    # Write results also to numpy file
    np.savez_compressed(
        file=str(pathToOutputtedXlsx.resolve()).replace('.xlsx','.npz'),
        df_x_truth_with_range=df_x_truth_with_range,
        df_y_truth_with_range=df_y_truth_with_range,
        df_no_truth_with_range=df_no_truth_with_range,
        )