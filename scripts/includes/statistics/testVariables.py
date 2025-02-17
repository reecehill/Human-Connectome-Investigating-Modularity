from typing import Any, Callable, Optional, Union, cast
from sklearn.calibration import LabelEncoder
from sklearn.metrics import (
    mutual_info_score,
    normalized_mutual_info_score,
    adjusted_mutual_info_score,
    v_measure_score,
    homogeneity_score,
    adjusted_rand_score,
    fowlkes_mallows_score,
    cohen_kappa_score,
    hamming_loss,
    accuracy_score,
    jaccard_score,
    completeness_score,
)
from scipy.stats.contingency import association, chi2_contingency
import numpy as np
import pandas as pd

from includes.statistics.utils import (
    XYZDict,
    calculateLevenshteinDistance,
    calculateNormalisedLevenshteinDistance,
    calculate_dice_coefficient,
    calculate_percent_identity,
)


def encode_nonmapped_labels_to_labels(
    label_true: "pd.Series[Any]", label_pred: "pd.Series[Any]"
) -> "tuple[pd.Series[float], pd.Series[float]]":
    if not "mapped" in label_true.attrs["dataset_descriptors"]["dataset_name"]:
        """
        Encodes label_true and label_pred separately to avoid false category associations.
        """
        le1 = LabelEncoder()
        le2 = LabelEncoder()

        _label_true_encoded = le1.fit_transform(label_true)
        _label_pred_encoded = le2.fit_transform(label_pred)

    else:
        """
        Encodes label_true and label_pred together as they have been mapped.
        """
        le = LabelEncoder()
        allLabels = pd.concat([pd.Series(label_true), pd.Series(label_pred)]).unique()
        le.fit(allLabels)

        _label_true_encoded = le.transform(label_true)
        _label_pred_encoded = le.fit(label_pred)

    label_true_encoded = pd.Series(
        np.array(_label_true_encoded), index=label_true.index
    )
    label_pred_encoded = pd.Series(
        np.array(_label_pred_encoded), index=label_pred.index
    )
    return label_true_encoded, label_pred_encoded


# Wrapper function to ensure a float is returned
def calculate_jaccard_score(
    label_true: "Union[pd.Series[str], pd.Series[int]]",
    label_pred: "Union[pd.Series[str], pd.Series[int]]",
) -> "np.float64":
    return cast(np.float64, jaccard_score(label_true, label_pred, average="weighted"))


def calculate_cramer_score(
    label_true: "Union[pd.Series[str], pd.Series[int]]",
    label_pred: "Union[pd.Series[str], pd.Series[int]]",
) -> "np.float64":
    if not "mapped" in label_true.attrs["dataset_descriptors"]["dataset_name"]:
        # If not mapped, encode labels to be the same.
        label_true_encoded, label_pred_encoded = encode_nonmapped_labels_to_labels(
            label_true, label_pred
        )
    else:
        label_true_encoded = label_true
        label_pred_encoded = label_pred

    contingency_table = pd.crosstab(
        np.array(label_true_encoded), np.array(label_pred_encoded)
    )
    return association(contingency_table, method="cramer", correction=False)


def calculate_tschuprow_score(
    label_true: "Union[pd.Series[str], pd.Series[int]]",
    label_pred: "Union[pd.Series[str], pd.Series[int]]",
) -> "np.float64":
    label_true_encoded, label_pred_encoded = encode_nonmapped_labels_to_labels(
        label_true, label_pred
    )

    contingency_table = pd.crosstab(
        np.array(label_true_encoded), np.array(label_pred_encoded)
    )
    return association(contingency_table, method="tschuprow", correction=False)


def calculate_chi2(
    label_true: "Union[pd.Series[str], pd.Series[int]]",
    label_pred: "Union[pd.Series[str], pd.Series[int]]",
) -> "str":
    label_true_encoded, label_pred_encoded = encode_nonmapped_labels_to_labels(
        label_true, label_pred
    )

    contingency_table = pd.crosstab(label_true_encoded, label_pred_encoded)

    # Compute Chi-Square test
    chi2_stat, p, dof, expected_freq = chi2_contingency(contingency_table)

    return f"dependent:{'True' if p<0.01 else 'False'}|p:{p}|chi2:{chi2_stat}|dof:{dof}"


Float = Union[float, np.float16, np.float32, np.float64]
ResultRowSubjectWide = tuple[
    str,
    str,
    Optional[bool],
    str,
    str,
    str,
    str,
    Union[str, Float],
    Union[str, Float],
    Union[str, Float],
    str,
    str,
]
ResultRowModuleWide = tuple[
    str,
    str,
    Optional[bool],
    str,
    str,
    str,
    str,
    str,
    Float,
    Float,
    Float,
    Float,
    Float,
    XYZDict,
    XYZDict,
    Float,
    Float,
    Float,
    Float,
    str,
    Union[str, Float],
    Union[str, Float],
    Union[str, Float],
    str,
    str,
]

# Define range information for each test
test_ranges: "dict[str, str]" = {
    "Levenshtein Distance": "Unbounded (non-negative)",
    "Normalised Levenshtein Distance": "[0, 1]",
    "Mutual Information Score": "Unbounded (non-negative)",
    "Normalized Mutual Information": "[0, 1]",
    "Adjusted Mutual Information": "[-1, 1]",
    "V-measure Cluster Score": "[0, 1]",
    "Homogeneity Score": "[0, 1]",
    "Adjusted Random Score": "[-1, 1]",
    "Fowlkes-Mallows Index": "[0, 1]",
    "Purity Score": "[0, 1]",
    "Dice Coefficient": "[0, 1]",
    "Percent Identity": "[0, 1]",
    "Jaccard Index": "[0, 1]",
    "Cohen Kappa Score": "[-1, 1]",
    "Hamming Loss": "[0,1]",
    "Accuracy Score": "[0,1]",
    "Completeness Score": "[0,1]",
    "Association Score (Cramer's V)": "[0,1]",
    "Association Score (Tschuprow's T)": "[0,1]",
    "Chi Score": "[0,1]",
}


# Define list of test functions and their names
test_functions_with_range: "list[tuple[str, Callable[[Union[pd.Series[str], pd.Series[int]],Union[pd.Series[str], pd.Series[int]]], Union[str,Float]]]]" = [
    ("Levenshtein Distance", calculateLevenshteinDistance),
    ("Normalised Levenshtein Distance", calculateNormalisedLevenshteinDistance),
    ("Mutual Information Score", mutual_info_score),
    ("Normalized Mutual Information", normalized_mutual_info_score),
    ("Adjusted Mutual Information", adjusted_mutual_info_score),
    ("V-measure Cluster Score", v_measure_score),
    ("Homogeneity Score", homogeneity_score),
    ("Adjusted Random Score", adjusted_rand_score),
    ("Fowlkes-Mallows Index", fowlkes_mallows_score),
    ("Dice Coefficient", calculate_dice_coefficient),
    ("Percent Identity", calculate_percent_identity),
    ("Jaccard Index", calculate_jaccard_score),
    ("Cohen Kappa Score", cohen_kappa_score),
    ("Hamming Loss", hamming_loss),
    ("Accuracy Score", accuracy_score),
    ("Completeness Score", completeness_score),
    ("Association Score (Cramer's V)", calculate_cramer_score),
    ("Association Score (Tschuprow's T)", calculate_tschuprow_score),
    ("Chi Score", calculate_chi2),
]
