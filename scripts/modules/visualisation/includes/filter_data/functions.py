import pandas as pd
from typing import Any, Dict, List, Literal, Optional, Tuple


def check_filters_are_valid(filters: Dict[str, Any], df: pd.DataFrame) -> None:
    for col, _ in filters.items():
        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found in the DataFrame.")


# Function to filter subject data based on provided parameters
def filter_subjects(
    df: pd.DataFrame,
    subjects: List[str],
    hemispheres: List[Literal["left", "right"]],
    tasks: List[Literal["lf", "rf", "rh", "lh", "t"]],
    statistic: List[str],
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Filters the modules DataFrame based on the provided parameters.
    If 'subjects' is empty, it includes all subjects.

    Parameters:
    - df (pd.DataFrame): The DataFrame to filter.
    - subjects (List[str]): List of subject IDs to include. If empty, include all.
    - hemispheres (List[Literal["left", "right"]]): Hemispheres to filter by.
    - tasks (List[Literal["lf", "rf", "rh", "lh", "t"]]): Tasks to filter by.
    - statistic (List[str]): Statistical tests to filter by.

    Returns:
    - pd.DataFrame: The filtered DataFrame.
    """
    applied_filters: Dict[str, Any] = {}

    conditions = pd.Series(True, index=df.index)  # Start with all rows included

    if subjects:
        conditions &= df["Subject ID"].astype(str).isin(subjects)
        applied_filters["Subject ID"] = (
            subjects if subjects else f"All ({df['Subject ID'].nunique()})"
        )
    if hemispheres:
        conditions &= df["Hemisphere"].isin(hemispheres)
        applied_filters["Hemisphere"] = (
            hemispheres if hemispheres else f"All ({df['Hemisphere'].nunique()})"
        )
    if tasks:
        conditions &= df["Task"].isin(tasks)
        applied_filters["Task"] = tasks if tasks else f"All ({df['Task'].nunique()})"
    if statistic:
        conditions &= df["Statistical Test"].isin(statistic)
        applied_filters["Statistical Test"] = (
            statistic if statistic else f"All ({df['Statistical Test'].nunique()})"
        )

    check_filters_are_valid(applied_filters, df)
    return df[conditions], applied_filters


def filter_modules(
    df: pd.DataFrame,
    subjects: List[str],
    hemispheres: List[Literal["left", "right"]],
    tasks: List[Literal["lf", "rf", "rh", "lh", "t"]],
    statistic: List[str],
    dataset: List[Literal["cleaned_words", "cleaned_words_mapped"]],
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Filters the modules DataFrame based on provided parameters.

    Parameters:
    - df (pd.DataFrame): The DataFrame to filter.
    - subjects (List[str]): List of subject IDs to include. If empty, include all.
    - hemispheres (List[Literal["left", "right"]]): Hemispheres to filter by.
    - tasks (List[Literal["lf", "rf", "rh", "lh", "t"]]): Tasks to filter by.
    - statistic (List[str]): Statistical tests to filter by.
    - dataset (List[Literal["cleaned_words", "cleaned_words_mapped"]]): Datasets to filter by.

    Returns:
    - pd.DataFrame: The filtered DataFrame.
    """
    applied_filters: Dict[str, Any] = {}
    conditions = pd.Series(True, index=df.index)  # Start with all rows included

    if subjects:
        conditions &= df["Subject ID"].astype(str).isin(subjects)
        applied_filters["Subject ID"] = (
            subjects if subjects else f"All ({df['Subject ID'].nunique()})"
        )
    if hemispheres:
        conditions &= df["Hemisphere"].isin(hemispheres)
        applied_filters["Hemisphere"] = (
            hemispheres if hemispheres else f"All ({df['Hemisphere'].nunique()})"
        )
    if tasks:
        conditions &= df["Task"].isin(tasks)
        applied_filters["Task"] = tasks if tasks else f"All ({df['Task'].nunique()})"
    if statistic:
        conditions &= df["Statistical Test"].isin(statistic)
        applied_filters["Statistical Test"] = (
            statistic if statistic else f"All ({df['Statistical Test'].nunique()})"
        )
    if dataset:
        conditions &= df["Dataset"].isin(dataset)
        applied_filters["Dataset"] = (
            dataset if dataset else f"All ({df['Dataset'].nunique()})"
        )

    check_filters_are_valid(applied_filters, df)

    return df[conditions], applied_filters
