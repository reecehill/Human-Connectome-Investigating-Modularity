from pathlib import Path
from typing import List, Literal, Optional, Union

import pandas as pd

from modules.visualisation.includes.filter_data.functions import (
    filter_modules,
    filter_subjects,
)
from modules.visualisation.includes.generate_figures.corrplots import (
    generate_dynamic_corrplot,
)

if __name__ == "__main__":
    raise Exception("This file is meant to be imported.")
else:

    def generate_corrplot(
        modules_df: pd.DataFrame,
        subjects: List[str],
        hemispheres: List[Literal["left", "right"]],
        tasks: List[Literal["lf", "rf", "rh", "lh", "t"]],
        statistic: List[str],
        dataset: Optional[List[Literal["cleaned_words", "cleaned_words_mapped"]]] = [],
        title_append: str = "",
        group_by: List[str] = ["Subject ID", "Statistical Test"],
        output_path: Union[str, Path] = "subject_scores_corrplot.png",
    ) -> None:
        if dataset is not None:
            filtered_df, applied_filters = filter_modules(
                modules_df, subjects, hemispheres, tasks, statistic, dataset
            )
        else:
            filtered_df, applied_filters = filter_subjects(
                modules_df, subjects, hemispheres, tasks, statistic
            )

        generate_dynamic_corrplot(
            filtered_df=filtered_df,
            group_by=group_by,
            statistic=statistic,
            applied_filters=applied_filters,
            title_append=title_append,
            output_path=output_path,
        )
