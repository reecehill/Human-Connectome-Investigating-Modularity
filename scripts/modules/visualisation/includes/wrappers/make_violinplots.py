from pathlib import Path
from typing import List, Literal
from modules.visualisation.includes.wrappers.violinplots.generate import (
    generate_violinplot_grouped_by,
)
from pandas import DataFrame


def make_violinplots(
    pathTo: dict[str, Path],
    allSubjects: DataFrame,
    allModules: DataFrame,
    allHemispheres: List[Literal["left", "right"]],
    allStats: List[str],
    allTasks: List[Literal["lf", "rf", "rh", "lh", "t"]],
    subjectSample: List[str],
):
    generate_violinplot_grouped_by(
        subjects=[],
        hemispheres=[],
        tasks=[],
        dataset=None,
        group_by=["Statistical Test"],
        statistic=[
            "Levenshtein Distance - Y as Truth",
            "Levenshtein Distance - X as Truth",
        ],
        modules_df=allSubjects,
        title_append="Across all subjects",
        output_path=pathTo["figures"] / "violinplot_figure_levenshtein.svg",
    )

    generate_violinplot_grouped_by(
        subjects=[],
        hemispheres=allHemispheres,
        tasks=[],
        group_by=["Statistical Test"],
        dataset=None,
        statistic=[
            "Mutual Information Score - X as Truth",
            "Mutual Information Score - Y as Truth",
        ],
        modules_df=allSubjects,
        title_append="Across all subjects",
        output_path=pathTo["figures"] / "violinplot_figure_mutual_information.svg",
    )

    generate_violinplot_grouped_by(
        subjects=[],
        hemispheres=allHemispheres,
        tasks=[],
        dataset=None,
        group_by=["Statistical Test"],
        statistic=[
            # "Levenshtein Distance - X as Truth",
            # "Normalised Levenshtein Distance - X as Truth",
            # "Mutual Information Score - X as Truth",
            "Normalized Mutual Information - X as Truth",
            "Adjusted Mutual Information - X as Truth",
            "V-measure Cluster Labeling - X as Truth",
            "Homogeneity Score - X as Truth",
            "Adjusted Random Score - X as Truth",
            "Fowlkes-Mallows Index - X as Truth",
            # "Levenshtein Distance - Y as Truth",
            # "Normalised Levenshtein Distance - Y as Truth",
            # "Mutual Information Score - Y as Truth",
            "Normalized Mutual Information - Y as Truth",
            "Adjusted Mutual Information - Y as Truth",
            "V-measure Cluster Labeling - Y as Truth",
            "Homogeneity Score - Y as Truth",
            "Adjusted Random Score - Y as Truth",
            "Fowlkes-Mallows Index - Y as Truth",
        ],
        modules_df=allSubjects,
        title_append="Across all subjects",
        output_path=pathTo["figures"] / "violinplot_figure_normalised_all.svg",
    )

    generate_violinplot_grouped_by(
        subjects=[],
        hemispheres=allHemispheres,
        tasks=[],
        dataset=None,
        group_by=["Statistical Test", "Hemisphere"],
        statistic=[
            # "Levenshtein Distance - X as Truth",
            # "Normalised Levenshtein Distance - X as Truth",
            # "Mutual Information Score - X as Truth",
            "Normalized Mutual Information - X as Truth",
            "Adjusted Mutual Information - X as Truth",
            "V-measure Cluster Labeling - X as Truth",
            "Homogeneity Score - X as Truth",
            "Adjusted Random Score - X as Truth",
            "Fowlkes-Mallows Index - X as Truth",
            # "Levenshtein Distance - Y as Truth",
            # "Normalised Levenshtein Distance - Y as Truth",
            # "Mutual Information Score - Y as Truth",
            "Normalized Mutual Information - Y as Truth",
            "Adjusted Mutual Information - Y as Truth",
            "V-measure Cluster Labeling - Y as Truth",
            "Homogeneity Score - Y as Truth",
            "Adjusted Random Score - Y as Truth",
            "Fowlkes-Mallows Index - Y as Truth",
        ],
        modules_df=allSubjects,
        title_append="Across all subjects",
        output_path=pathTo["figures"]
        / "violinplot_figure_normalised_by_hemisphere.svg",
    )

    generate_violinplot_grouped_by(
        subjects=subjectSample,
        hemispheres=allHemispheres,
        tasks=[],
        statistic=[
            "Normalized Mutual Information - X as Truth",
            "Normalized Mutual Information - Y as Truth",
        ],
        dataset=["cleaned_words_mapped"],
        modules_df=allModules,
        title_append="All modules, including non-optimal",
        group_by=["Hemisphere", "Subject ID", "Statistical Test"],
        output_path=pathTo["figures"]
        / "violinplot_figure_mutual_information_by_subject.svg",
    )

    generate_violinplot_grouped_by(
        subjects=subjectSample,
        hemispheres=allHemispheres,
        tasks=[],
        statistic=[
            "Normalized Mutual Information - X as Truth",
        ],
        dataset=["cleaned_words_mapped"],
        modules_df=allModules,
        title_append="All modules, including non-optimal",
        group_by=["Task", "Hemisphere", "Statistical Test"],
        output_path=pathTo["figures"]
        / "violinplot_figure_mutual_information_by_task.svg",
    )

    generate_violinplot_grouped_by(
        subjects=subjectSample,
        hemispheres=allHemispheres,
        tasks=[],
        statistic=[
            "Normalized Mutual Information - X as Truth",
        ],
        dataset=["cleaned_words"],
        modules_df=allModules,
        title_append="All modules, including non-optimal",
        group_by=["Task", "Hemisphere", "Statistical Test"],
        output_path=pathTo["figures"]
        / "violinplot_figure_mutual_information_by_task_nonmapped.svg",
    )
