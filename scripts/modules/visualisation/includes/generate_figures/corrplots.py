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


def generate_dynamic_corrplot(
    filtered_df: pd.DataFrame,
    statistic: List[str],
    applied_filters: Dict[str, Any],
    group_by: List[str],  # Dynamic list of grouping columns
    title_append: str = "",
    output_path: Union[str, Path] = "corrplot_figure.png",
):
    if filtered_df.empty:
        print("Filtered data is empty. Cannot generate boxplot.")
        return

    index_columns = [
        "Subject ID",
        "Hemisphere",
        "Task",
        "Dataset",
    ]
    if("X Module Name" in filtered_df.columns):
      index_columns.append("X Module Name")
    if("Y Module Name" in filtered_df.columns):
      index_columns.append("Y Module Name")

      
    # Select numeric columns from allModules
    test_columns = filtered_df.pivot(
        index=index_columns,  # Keep the same index
        columns="Statistical Test",  # Create a column for each test
        values="Score: (x real, y real)",  # Use the score as values
    )

    # Flatten column names (if necessary)
    test_columns.columns = [str(col) for col in test_columns.columns]
    test_columns = test_columns.reset_index()

    modified_df = filtered_df.merge(test_columns, on=index_columns, how="left")
    columns_to_drop = [
        col for col in modified_df.columns if any(substring in col for substring in ["Y as Truth", "Subject ID", "Score: "])
    ]
    modified_df = modified_df.drop(columns=columns_to_drop)
    # Compute the correlation matrix
    numerical_data = modified_df.select_dtypes(include=["number"])

    # Drop columns that are completely empty (all NaN values)
    numerical_data = numerical_data.dropna(axis=1, how="all")
    correlation_matrix = numerical_data.corr()
    threshold = 0
    mask = (correlation_matrix < threshold) & (correlation_matrix > -threshold)

    # Plot the correlation heatmap
    plt.figure(figsize=(12, 12))
    heatmap = sns.heatmap(
        correlation_matrix,
        annot=True,
        annot_kws={"size": 6},
        fmt=".2f",
        cmap="coolwarm",
        cbar=True,
        square=True,
        xticklabels=correlation_matrix.columns.to_list(),
        yticklabels=correlation_matrix.columns.to_list(),
        linecolor="w",
        linewidths=0.1,
        mask=mask,
    )
    title = f"Correlation Heatmap of Numerical Variables"
    plt.title(f"{title} \n{title_append}", fontsize=16)
    plt.suptitle(genSubtitleFromFilters(applied_filters), fontsize=10, y=1)
    plt.xlabel("Numerical variable", fontsize=14)
    plt.ylabel("Numerical variable", fontsize=14)
    plt.xticks(rotation=90, fontsize=10)
    plt.tight_layout()
    # Save the figure
    plt.savefig(output_path)
    save_fig_as_pickle(Path(output_path).with_suffix(".pkl"), plt.gcf())
    plt.close()
    print(f"Correlation figure saved as '{output_path}'.")
