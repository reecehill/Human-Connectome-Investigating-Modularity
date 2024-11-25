from pathlib import Path
from typing import List, Literal
from modules.visualisation.includes.wrappers.scatterplots.generate import (
    generate_scatterplot_grouped_by,
)
from pandas import DataFrame


def make_scatterplots(
    pathTo: dict[str, Path],
    allSubjects: DataFrame,
    allModules: DataFrame,
    allHemispheres: List[Literal["left", "right"]],
    allStats: List[str],
    allTasks: List[Literal["lf", "rf", "rh", "lh", "t"]],
    subjectSample: List[str],
):
    generate_scatterplot_grouped_by(
        subjects=[],
        hemispheres=[],
        tasks=[],
        dataset=["cleaned_words_mapped"],
        group_by=["Statistical Test"],
        statistic=[
            "Normalized Mutual Information - X as Truth",
        ],
        x_vars=["X Surface Area (mm)", "Y Surface Area (mm)"],
        y_var="Score: (x real, y real)",
        modules_df=allModules,
        title_append="All modules, including non-optimal",
        output_path=pathTo["figures"] / "scatterplot_figure_levenshtein.svg",
    )

    generate_scatterplot_grouped_by(
        subjects=[],
        hemispheres=[],
        tasks=[],
        dataset=["cleaned_words_mapped"],
        group_by=["Dataset"],
        statistic=[
            "Levenshtein Distance - Y as Truth",  # The stat here doesnt matter. As its not used.
        ],
        x_vars=["X Surface Area (mm)"],
        y_var="Y Surface Area (mm)",
        modules_df=allModules,
        title_append="All modules, including non-optimal",
        output_path=pathTo["figures"] / "scatterplot_figure_x_to_y_mm.svg",
    )

    generate_scatterplot_grouped_by(
        subjects=[],
        hemispheres=[],
        tasks=[],
        dataset=["cleaned_words"],
        group_by=["Dataset"],
        statistic=[
            "Levenshtein Distance - Y as Truth",  # The stat here doesnt matter. As its not used.
        ],
        x_vars=["X Surface Area (mm)"],
        y_var="Y Surface Area (mm)",
        modules_df=allModules,
        title_append="All modules, including non-optimal",
        output_path=pathTo["figures"] / "scatterplot_figure_x_to_y_mm.svg",
    )
