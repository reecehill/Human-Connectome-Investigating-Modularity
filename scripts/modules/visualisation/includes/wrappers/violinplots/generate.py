from pathlib import Path
from typing import List, Literal, Optional, Union

import pandas as pd

from modules.visualisation.includes.filter_data.functions import (
    filter_modules,
    filter_subjects,
)
from modules.visualisation.includes.generate_figures.violinplots import (
    generate_dynamic_violinplot,
)

if __name__ == "__main__":
    raise Exception("This file is meant to be imported.")
else:

    def generate_violinplot_grouped_by(
        modules_df: pd.DataFrame,
        subjects: List[str],
        hemispheres: List[Literal["left", "right"]],
        tasks: List[Literal["lf", "rf", "rh", "lh", "t"]],
        statistic: List[str],
        dataset: Optional[List[Literal["cleaned_words", "cleaned_words_mapped"]]] = [],
        title_append: str = "",
        group_by: List[str] = ["Subject ID", "Statistical Test"],
        output_path: Union[str, Path] = "subject_scores_boxplot.png",
    ) -> None:
        """
        Reads modules, filters data, and generates a violinplot of statistical test scores grouped by subject ID.

        Parameters:
        - modules_file_path (str): Path to the modules CSV file.
        - subjects (List[str]): List of subject IDs to include. If empty, include all.
        - hemispheres (List[Literal["left", "right"]]): Hemispheres to filter by.
        - tasks (List[Literal["lf", "rf", "rh", "lh", "t"]]): Tasks to filter by.
        - statistic (List[str]): Statistical tests to filter by.
        - dataset (List[Literal["cleaned_words", "cleaned_words_mapped"]]): Datasets to filter by.
        - output_path (Union[str, Path]): File path to save the plot.
        """
        if dataset is not None:
            filtered_df, applied_filters = filter_modules(
                modules_df, subjects, hemispheres, tasks, statistic, dataset
            )
        else:
            filtered_df, applied_filters = filter_subjects(
                modules_df, subjects, hemispheres, tasks, statistic
            )

        generate_dynamic_violinplot(
            filtered_df=filtered_df,
            group_by=group_by,
            statistic=statistic,
            applied_filters=applied_filters,
            title_append=title_append,
            output_path=output_path,
        )
