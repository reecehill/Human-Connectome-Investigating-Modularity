# type: ignore

# !!!!!!!!!!!!!!!!!!!!!!!
# THIS FILE DOES NOT CALCULATE SPATIAL STATS YET. DO NOT USE.
# !!!!!!!!!!!!!!!!!!!!!!!


# Re-importing necessary libraries and preparing data again
import numpy as np
import pandas as pd
from sklearn.metrics import (
    mutual_info_score,
    normalized_mutual_info_score,
    adjusted_mutual_info_score,
)
from sklearn.metrics import (
    v_measure_score,
    homogeneity_score,
    adjusted_rand_score,
    fowlkes_mallows_score,
)
from sklearn.metrics import make_scorer
from sklearn.metrics import silhouette_score
import random
import string
import modules.globals as g

# Function to generate a random word


def random_word(length=6):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


y: pd.DataFrame = pd.read_csv(
    "/home/reece/HCIM/core/Human-Connectome-Investigating-Modularity/data/subjects/100307/right_functional_modules.csv",
    sep=",",
    header=None,
    keep_default_na=False,
).T
x: pd.DataFrame = pd.read_csv(
    "/home/reece/HCIM/core/Human-Connectome-Investigating-Modularity/data/subjects/100307/right_structural_modules.csv",
    sep=",",
    header=None,
    keep_default_na=False,
).T

# Cleaning data to exclude NaN values
useMask = True
if useMask:
    mask = ~x.isna() & ~y.isna()

    x_clean = np.array(x)[mask]
    y_clean = np.array(y)[mask]
else:
    x_clean = np.array(x)
    y_clean = np.array(y)
    # Allowing NaN values for the tests
    pass


# Step 1: Get unique labels in x and y
unique_labels_x = set(x_clean)  # Assuming x is an array or list
unique_labels_y = set(y_clean)  # Assuming y is an array or list

# Step 2: Create a dictionary to map each label to a random word
label_to_word_map_x: "dict[str, str]" = {
    label: random_word() for label in unique_labels_x
}
label_to_word_map_y: "dict[str, str]" = {
    label: random_word() for label in unique_labels_y
}

# Step 3: Apply the mapping to x and y
x_as_words: "list[str]" = [label_to_word_map_x[label] for label in x_clean]
y_as_words: "list[str]" = [label_to_word_map_y[label] for label in y_clean]

x_clean: "list[str]" = x_as_words
y_clean: "list[str]" = y_as_words

# For absolute confidence that Python is not converting strings to integers, convert labels to random words.


# Load the data again from temp.py
# file_path = '/home/reece/coding/temp-L-100307-lf.py'

# Read the python file content to extract the variables
# with open(file_path, 'r') as f:
# file_content = f.read()

# exec(file_content)

# Convert X and y to pandas series to handle any inconsistencies
# x_series = pd.Series(x)
# y_series = pd.Series(y)

# # Ensure both X and y are numeric
# x_numeric = pd.to_numeric(x_series, errors='coerce', downcast='float')
# y_numeric = pd.to_numeric(y_series, errors='coerce', downcast='float')


# Define range information for each test
test_ranges = {
    "Mutual Information Score": "Unbounded (non-negative)",
    "Normalized Mutual Information": "[0, 1]",
    "Adjusted Mutual Information": "[-1, 1]",
    "V-measure Cluster Labeling": "[0, 1]",
    "Homogeneity Score": "[0, 1]",
    "Adjusted Random Score": "[-1, 1]",
    "Fowlkes-Mallows Index": "[0, 1]",
    "Purity Score": "[0, 1]",
}

# Prepare results storage
results_x_truth_with_range = []
results_y_truth_with_range = []

# Define list of test functions and their names
test_functions_with_range = [
    ("Mutual Information Score", mutual_info_score),
    ("Normalized Mutual Information", normalized_mutual_info_score),
    ("Adjusted Mutual Information", adjusted_mutual_info_score),
    ("V-measure Cluster Labeling", v_measure_score),
    ("Homogeneity Score", homogeneity_score),
    ("Adjusted Random Score", adjusted_rand_score),
    ("Fowlkes-Mallows Index", fowlkes_mallows_score),
]

# Define a function to generate interpretations


def generateInterpretation(test_name, score):
    if test_name in [
        "Normalized Mutual Information",
        "Adjusted Mutual Information",
        "Mutual Information Score",
    ]:
        if score == 0:
            return "No mutual information between variables."
        elif score == 1:
            return "Perfect correlation between variables."
        else:
            return f"Partial mutual information: {score}."
    elif test_name in [
        "V-measure Cluster Labeling",
        "Homogeneity Score",
        "Fowlkes-Mallows Index",
        "Purity Score",
    ]:
        if score == 0:
            return "No agreement between clustering and truth."
        elif score == 1:
            return "Perfect agreement between clustering and truth."
        else:
            return f"Moderate agreement: {score}."
    elif test_name == "Adjusted Random Score":
        if score < 0:
            return "Less agreement than expected by chance."
        elif score == 0:
            return "No agreement."
        elif score > 0:
            return "Positive agreement."
    return "Score interpretation not available."


# Run tests for X as truth
for test_name, test_func in test_functions_with_range:
    try:
        score_x_defined = test_func(x_clean, y_clean)
        score_x_imported_random_y = test_func(
            x_clean, np.random.choice(np.unique(y_clean), size=len(y_clean))
        )
        score_x_random_y_imported = test_func(
            np.random.choice(np.unique(x_clean), size=len(x_clean)), y_clean
        )

        results_x_truth_with_range.append(
            [
                test_name,
                score_x_defined,
                score_x_imported_random_y,
                score_x_random_y_imported,
                generateInterpretation(test_name, score_x_defined),
                test_ranges[test_name],
            ]
        )
    except Exception as e:
        g.logger.error(f"Error running {test_name} with x as truth: {e}")

# Run tests for Y as truth
for test_name, test_func in test_functions_with_range:
    try:
        score_y_defined = test_func(y_clean, x_clean)
        score_y_imported_random_x = test_func(
            y_clean, np.random.choice(np.unique(x_clean), size=len(x_clean))
        )
        score_y_random_x_imported = test_func(
            np.random.choice(np.unique(y_clean), size=len(y_clean)), x_clean
        )

        results_y_truth_with_range.append(
            [
                test_name,
                score_y_defined,
                score_y_imported_random_x,
                score_y_random_x_imported,
                generateInterpretation(test_name, score_y_defined),
                test_ranges[test_name],
            ]
        )
    except Exception as e:
        g.logger.error(f"Error running {test_name} with y as truth: {e}")

# Convert results to DataFrames
dfXTruthWithRange = pd.DataFrame(
    results_x_truth_with_range,
    columns=[
        "Statistical Test",
        "Score: (x real, y real)",
        "Score: (x real, y random)",
        "Score: (x random, y real)",
        "Interpretation",
        "Range",
    ],
)

dfYTruthWithRange = pd.DataFrame(
    results_y_truth_with_range,
    columns=[
        "Statistical Test",
        "Score: (x real, y real)",
        "Score: (x real, y random)",
        "Score: (x random, y real)",
        "Interpretation",
        "Range",
    ],
)

# For third sheet, no truth required for some tests (NMI, AMI, MI)
df_no_truth_with_range = dfXTruthWithRange[
    dfXTruthWithRange["Statistical Test"].isin(
        [
            "Normalized Mutual Information",
            "Adjusted Mutual Information",
            "Mutual Information Score",
        ]
    )
]

# Write results to Excel
excel_path_with_range = "/home/reece/HCIM/core/Human-Connectome-Investigating-Modularity/data/subjects/100307/statistical_test_results_with_ranges_excluding_nan_L.xlsx"
with pd.ExcelWriter(excel_path_with_range, engine="xlsxwriter") as writer:
    dfXTruthWithRange.to_excel(writer, sheet_name="X as Truth", index=False)
    dfYTruthWithRange.to_excel(writer, sheet_name="Y as Truth", index=False)
    df_no_truth_with_range.to_excel(writer, sheet_name="No Truth Required", index=False)


# Provide link to download the Excel file
excel_path_with_range
