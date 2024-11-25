from pathlib import Path
from typing import List, Literal, Optional, Union, Dict, Any
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from modules.visualisation.includes.filter_data.functions import (
    filter_modules,
    filter_subjects,
)
from modules.visualisation.includes.generate_figures.includes.functions import genSubtitleFromFilters
from modules.visualisation.includes.io.save_pickled_object import save_fig_as_pickle

if __name__ == "__main__":
    raise Exception("This file is meant to be imported.")
else:

    def generate_scatterplot_grouped_by(
        modules_df: pd.DataFrame,
        subjects: List[str],
        hemispheres: List[Literal["left", "right"]],
        tasks: List[Literal["lf", "rf", "rh", "lh", "t"]],
        statistic: List[str],
        group_by: List[str],
        x_vars: List[str],
        y_var: str,
        title_append: str = "",
        output_path: Union[str, Path] = "surface_area_nmi_plot_grouped.png",
        dataset: Optional[List[Literal["cleaned_words", "cleaned_words_mapped"]]] = [],
    ):
        """
        Generates scatter plots of surface area vs normalized mutual information (NMI) with trendlines,
        grouped dynamically by the specified columns.

        Parameters:
        - filtered_df (pd.DataFrame): Filtered DataFrame containing the data.
        - applied_filters (Dict[str, Any]): Filters applied to the DataFrame.
        - x_vars (List[str]): List of surface area variables to include (e.g., ["X Surface Area (mm)", "Y Surface Area (mm)"]).
        - y_var (str): Dependent variable (e.g., "Normalized Mutual Information Score").
        - group_by (List[str]): List of columns to group by dynamically.
        - title_append (str): Additional text for the plot title.
        - output_path (Union[str, Path]): Base file path to save the plot(s).
        """
        if dataset is not None:
            filtered_df, applied_filters = filter_modules(
                modules_df, subjects, hemispheres, tasks, statistic, dataset
            )
        else:
            filtered_df, applied_filters = filter_subjects(
                modules_df, subjects, hemispheres, tasks, statistic
            )

        if filtered_df.empty:
            print("Filtered data is empty. Cannot generate plot.")
            return

        # Validate group_by columns
        for col in group_by:
            if col not in filtered_df.columns:
                raise ValueError(f"Column '{col}' not found in the DataFrame.")

        # Group the data and iterate through groups
        grouped = filtered_df.groupby(group_by)
        for group_keys, group_data in grouped:
            group_label = (
                " - ".join(map(str, group_keys))
                if isinstance(group_keys, tuple)
                else str(group_keys)
            )
            group_output_path = Path(output_path).with_name(
                f"{Path(output_path).stem}_{group_label}.svg"
            )

            # Initialize the plot for the current group
            plt.figure(figsize=(10, 8))
            colors = sns.color_palette(
                "Set1", len(x_vars)
            )  # Use distinct colors for the x variables

            for i, x_var in enumerate(x_vars):
                if x_var not in group_data.columns or y_var not in group_data.columns:
                    raise ValueError(
                        f"Columns '{x_var}' or '{y_var}' not found in the group data."
                    )

                # Scatter plot for each x_var
                sns.scatterplot(
                    data=group_data,
                    x=x_var,
                    y=y_var,
                    label=f"{x_var}",
                    color=colors[i],
                    alpha=0.7,
                )

                # Fit a linear trendline
                sns.regplot(
                    data=group_data,
                    x=x_var,
                    y=y_var,
                    scatter=False,
                    label=f"Linear ({x_var})",
                    color=colors[i],
                    line_kws={"linestyle": "--"},
                )

            # Customize the plot
            title = f"Effect of {', '.join(x_vars)} on {y_var}\nGroup: {group_label}"
            plt.title(f"{title} \n{title_append}", fontsize=16)
            plt.suptitle(genSubtitleFromFilters(applied_filters), fontsize=10, y=1)
            plt.xlabel("Surface Area (mm)", fontsize=14)
            plt.ylabel(ylabel=y_var, fontsize=14)
            plt.legend(title="Legend", fontsize=12)
            plt.grid(True, linestyle="--", alpha=0.6)
            plt.tight_layout()

            # Save the figure for this group
            plt.savefig(group_output_path)
            save_fig_as_pickle(Path(group_output_path).with_suffix(".pkl"), plt.gcf())
            plt.close()
            print(f"Boxplot figure saved as '{group_output_path}'.")
