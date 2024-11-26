from pathlib import Path
from typing import Any, Dict, List, Union
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors as mcolors

from modules.visualisation.includes.filter_data.functions import filter_modules
from modules.visualisation.includes.generate_figures.includes.functions import (
    genSubtitleFromFilters,
)
from modules.visualisation.includes.io import save_fig_as_pickle


def generate_dynamic_violinplot(
    filtered_df: pd.DataFrame,
    statistic: List[str],
    applied_filters: Dict[str, Any],
    group_by: List[str],  # Dynamic list of grouping columns
    title_append: str = "",
    output_path: Union[str, Path] = "violinplot_figure.png",
):
    """
    Generates a violinplot grouped by a dynamic list of columns.

    Parameters:
    - filtered_df (pd.DataFrame): Filtered DataFrame.
    - statistic (List[str]): Statistical tests included in the DataFrame.
    - applied_filters (Dict[str, Any]): Filters applied to the DataFrame.
    - group_by (List[str]): List of columns to group by dynamically.
    - title_append (str): Additional text for the plot title.
    - output_path (Union[str, Path]): File path to save the plot.
    """
    if filtered_df.empty:
        print("Filtered data is empty. Cannot generate violinplot.")
        return

    # Validate group_by columns
    for col in group_by:
        if col not in filtered_df.columns:
            raise ValueError(f"Column '{col}' not found in the DataFrame.")

    # Create a dynamic x_label based on grouping columns
    x_label = " - ".join(group_by)

    filtered_df = filtered_df.sort_values(by=group_by).copy()
    filtered_df[x_label] = filtered_df[group_by].astype(str).agg(" - ".join, axis=1)

    # Melt the DataFrame
    y_label = "Score"
    melted_df = filtered_df.melt(
        id_vars=[x_label],
        value_vars=[
            "Score: (x real, y real)",
            # "Score: (x real, y random)",
            "Score: (x random, y real)",
        ],
        var_name="Score Type",
        value_name=y_label,
    )
    melted_df[x_label] = pd.Categorical(
        melted_df[x_label], categories=filtered_df[x_label].unique(), ordered=True
    )

    # Create the violinplot
    plt.figure(figsize=(12, 12))
    ax = sns.violinplot(
        data=melted_df, x=x_label, y=y_label, hue="Score Type", split=True
    )

    if len(group_by) > 1:
        # Add zebra coloring for groups
        unique_colours = filtered_df[group_by[0]].unique()
        color_list = list(mcolors.TABLEAU_COLORS.values())
        zebra_colors = {
            subject: color_list[i % len(color_list)]  # Cycle through the list of colors
            for i, subject in enumerate(unique_colours)
        }
        # Apply zebra coloring
        for i, subject in enumerate(unique_colours):
            # Filter positions for this subject
            positions = [
                pos
                for pos, label in enumerate(melted_df[x_label].unique())
                if str(subject) in label
            ]
            base_color = zebra_colors[subject]
            for j, pos in enumerate(positions):
                shade = (
                    0.2 if j % 2 == 0 else 0.4
                )  # Alternate between lighter and darker shades
                len2 = len(group_by)
                ax.axvspan(
                    pos - 0.5,
                    pos + 0.5,
                    color=mcolors.to_rgba(base_color, alpha=shade),
                    zorder=0,
                )
    else:
        # Add zebra pattern (greyscale) to violinplot

        unique_tests = melted_df[group_by[0]].unique()
        for i, test in enumerate(unique_tests):
            if i % 2 == 0:  # Apply zebra pattern on alternate columns
                ax.axvspan(i - 0.5, i + 0.5, color="gray", alpha=0.1)

    # Customize the plot
    title = f"Violinplot of Scores Grouped by {', '.join(group_by)}"
    plt.title(f"{title} \n{title_append}", fontsize=16)
    plt.suptitle(genSubtitleFromFilters(applied_filters), fontsize=10, y=1)
    plt.xlabel(x_label, fontsize=14)
    plt.ylabel(y_label, fontsize=14)
    plt.xticks(rotation=90, fontsize=10)
    plt.legend(
        title="Score Type", fontsize=12, loc="upper right", bbox_to_anchor=(1.05, 1)
    )
    plt.tight_layout()

    # Save the figure
    plt.savefig(output_path)
    save_fig_as_pickle(Path(output_path).with_suffix(".pkl"), plt.gcf())
    plt.close()
    print(f"Violinplot figure saved as '{output_path}'.")
