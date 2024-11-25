from pathlib import Path
from typing import List, Literal
from modules.visualisation.includes.wrappers.corrplots.generate import generate_corrplot
from modules.visualisation.includes.wrappers.scatterplots.generate import (
    generate_scatterplot_grouped_by,
)
from pandas import DataFrame


def make_corrplots(
    pathTo: dict[str, Path],
    allSubjects: DataFrame,
    allModules: DataFrame,
    allHemispheres: List[Literal["left", "right"]],
    allStats: List[str],
    allTasks: List[Literal["lf", "rf", "rh", "lh", "t"]],
    subjectSample: List[str],
):
    generate_corrplot(
        subjects=[],
        hemispheres=[],
        tasks=[],
        dataset=None,
        group_by=["Statistical Test"],
        statistic=[],
        modules_df=allSubjects,
        title_append="Across all subjects",
        output_path=pathTo["figures"] / "corrplot_figure_all_subjects.svg",
    )

    generate_corrplot(
        subjects=[],
        hemispheres=[],
        tasks=[],
        dataset=["cleaned_words_mapped"],
        group_by=["Statistical Test"],
        statistic=[],
        modules_df=allModules,
        title_append="All modules, including non-optimal",
        output_path=pathTo["figures"] / "corrplot_figure_mapped.svg",
    )

    generate_corrplot(
        subjects=[],
        hemispheres=[],
        tasks=[],
        dataset=["cleaned_words"],
        group_by=["Statistical Test"],
        statistic=[],
        modules_df=allModules,
        title_append="All modules, including non-optimal",
        output_path=pathTo["figures"] / "corrplot_figure_unmapped.svg",
    )
