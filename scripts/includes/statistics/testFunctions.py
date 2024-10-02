from typing import Union
import pandas as pd
from includes.statistics import Float
def generate_interpretation(test_name: str, score: "Union[float,Float]") -> str:
    # Define a function to generate interpretations
    if test_name in ["Normalized Mutual Information", "Adjusted Mutual Information", "Mutual Information Score"]:
        if score == 0.0:
            return "No mutual information between variables."
        elif score == 1.0:
            return "Perfect correlation between variables."
        else:
            return f"Partial mutual information: {score}."
    elif test_name in ["V-measure Cluster Labeling", "Homogeneity Score", "Fowlkes-Mallows Index", "Purity Score"]:
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

def convertResultsToDataFrames(results_x_truth_with_range, results_y_truth_with_range) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    # Convert results to DataFrames
    df_x_truth_with_range = pd.DataFrame(results_x_truth_with_range, columns=[
        "Statistical Test", "Score: (x real, y real)", "Score: (x real, y random)", 
        "Score: (x random, y real)", "Interpretation", "Range"])

    df_y_truth_with_range = pd.DataFrame(results_y_truth_with_range, columns=[
        "Statistical Test", "Score: (x real, y real)", "Score: (x real, y random)", 
        "Score: (x random, y real)", "Interpretation", "Range"])

    # It does not matter which truth we yield from, as functions should be symmetrical.
    df_no_truth_with_range = df_x_truth_with_range[df_x_truth_with_range["Statistical Test"].isin([
        "Normalized Mutual Information", "Adjusted Mutual Information", "Mutual Information Score"])]

    return df_x_truth_with_range, df_y_truth_with_range, df_no_truth_with_range