from typing import Union
import pandas as pd
from includes.statistics import Float
from includes.statistics.testVariables import ResultRowSubjectWide, ResultRowModuleWide


def generateInterpretation(test_name: str, score: "Float") -> str:
    # Define a function to generate interpretations
    if test_name in [
        "Normalized Mutual Information",
        "Adjusted Mutual Information",
        "Mutual Information Score",
    ]:
        if score == 0.0:
            return "No mutual information between variables."
        elif score == 1.0:
            return "Perfect correlation between variables."
        else:
            return f"Partial mutual information: {score}."
    elif test_name in [
        "V-measure Cluster Labeling",
        "Homogeneity Score",
        "Fowlkes-Mallows Index",
        "Purity Score",
    ]:
        if score == 0.0:
            return "No agreement between clustering and truth."
        elif score == 1.0:
            return "Perfect agreement between clustering and truth."
        else:
            return f"Moderate agreement: {score}."
    elif test_name == "Adjusted Random Score":
        if score < 0.0:
            return "Less agreement than expected by chance."
        elif score == 0.0:
            return "No agreement."
        elif score > 0.0:
            return "Positive agreement."
    return "Score interpretation not available."


def convertSubjectWideResultsToDataFrames(
    results_x_truth_with_range: list[ResultRowSubjectWide],
    results_y_truth_with_range: list[ResultRowSubjectWide],
) -> "tuple[pd.DataFrame, pd.DataFrame]":

    columns: "list[str]" = [
        "Timestamp of config",
        "Subject ID",
        "Subject-pipeline Success",
        "Hemisphere",
        "Task",
        "Dataset",
        "Statistical Test",
        "Score: (x real, y real)",
        "Score: (x real, y random)",
        "Score: (x random, y real)",
        "Interpretation",
        "Range",
    ]
    # Convert results to DataFrames
    dfXTruthWithRange = pd.DataFrame(results_x_truth_with_range, columns=columns)
    dfYTruthWithRange = pd.DataFrame(results_y_truth_with_range, columns=columns)

    return dfXTruthWithRange, dfYTruthWithRange


def convertModuleWideResultsToDataFrames(
    results_x_truth_by_module: list[ResultRowModuleWide],
    results_y_truth_by_module: list[ResultRowModuleWide],
) -> "tuple[pd.DataFrame, pd.DataFrame]":

    columns: "list[str]" = [
        "Timestamp of config",
        "Subject ID",
        "Subject-pipeline Success",
        "Hemisphere",
        "Task",
        "Dataset",
        "X Module Name",
        "Y Module Name",
        "X Surface Area (mm)",
        "X Surface Area (faces)",
        "Y Surface Area (mm)",
        "Y Surface Area (faces)",
        "Y/X Surface Area (mm)",
        "X Module Centroid Coords",
        "Y Module Centroid Coords",
        "X-Y Centroid Euclidean Distance",
        "Normalised Centroid Distance Cost",
        "Normalised Contingency Cost",
        "Total Pairing Cost",
        "Statistical Test",
        "Score: (x real, y real)",
        "Score: (x real, y random)",
        "Score: (x random, y real)",
        "Interpretation",
        "Range",
    ]
    # Convert results to DataFrames
    dfXTruthByModule = pd.DataFrame(results_x_truth_by_module, columns=columns)
    dfYTruthByModule = pd.DataFrame(results_y_truth_by_module, columns=columns)

    return dfXTruthByModule, dfYTruthByModule


# Define the padding function


def pad_indexes(
    currentIndexes: "Union[pd.MultiIndex,pd.Index[int]]",
    validIndexes: "Union[pd.MultiIndex,pd.Index[int]]",
    n: int,
) -> "list[int]":
    # will pad an array of indexes in both directions n number of times.
    # Example usage
    # X_indexes = [3, 4, 5, 56, 58, 70]
    # n = 2
    # X_indexes_new = pad_indexes(X_indexes, n)
    # Output -> [1, 2, 3, 4, 5, 6, 7, 54, 55, 56, 57, 58, 59, 60, 68, 69, 70, 71, 72]

    # Used to get expand modules a little beyond their boundaries.

    padded_indexes = set()
    for index in currentIndexes:
        # Add indexes within range n in both directions
        for i in range(max(0, index - n), index + n + 1):
            if i in validIndexes:
                padded_indexes.add(i)
    return sorted(padded_indexes)
