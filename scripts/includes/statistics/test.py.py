from typing import List, TypedDict
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr

use_modules_data = True
use_mapped_dataset_only = True
use_best_performing_pairs_only = True
use_iqr_of_y_x_ratio_to_clean = True
# Paths to uploaded files
alignment_scores_path = (
    "/home/reece/HCIM/core/Human-Connectome-Investigating-Modularity/data_processed/allModules_170.csv"
    if use_modules_data
    else "/home/reece/HCIM/core/Human-Connectome-Investigating-Modularity/data_processed/allSubjects_170.csv"
)
behavioural_metrics_path = "/home/reece/HCIM/core/Human-Connectome-Investigating-Modularity/data_processed/allSubjects_170_behavioural_metrics.csv"

alignment_scores = pd.read_csv(alignment_scores_path)
tests_to_drop = [
    # "Levenshtein Distance - X as Truth",
    "Levenshtein Distance - Y as Truth",
    # "Mutual Information Score - X as Truth",
    "Mutual Information Score - Y as Truth",
]
alignment_scores = alignment_scores[
    ~alignment_scores["Statistical Test"].str.contains(
        "|".join(tests_to_drop), regex=True, case=False
    )
]

behavioural_metrics = pd.read_csv(behavioural_metrics_path)

# Ensure linking columns are consistent in type
alignment_scores["Subject ID"] = alignment_scores["Subject ID"].astype(str)
behavioural_metrics["Subject"] = behavioural_metrics["Subject"].astype(str)

pivoted_indexes = [
    "Timestamp of config",
    "Subject ID",
    "Subject-pipeline Success",
    "Hemisphere",
    "Task",
    "Dataset",
]
if use_modules_data:
    alignment_scores["abs(Y/X Surface Area (mm) - 1.0)"] = abs(
        alignment_scores["Y/X Surface Area (mm)"] - 1.0
    )
    pivoted_indexes.extend(
        [
            "X Module Name",
            "Y Module Name",
            "Y Surface Area (mm)",
            "X Surface Area (mm)",
            "Y/X Surface Area (mm)",
            "abs(Y/X Surface Area (mm) - 1.0)",
        ]
    )


pivoted_df: pd.DataFrame = alignment_scores.pivot_table(
    index=pivoted_indexes,
    columns="Statistical Test",
    values="Score: (x real, y real)",
)

df_replaced = alignment_scores.drop(
    columns=[
        "Statistical Test",
        "Score: (x real, y real)",
        "Score: (x real, y random)",
        "Score: (x random, y real)",
    ]
)
df_replaced = pd.merge(
    df_replaced,
    pivoted_df,
    on=pivoted_indexes,
    how="inner",
)

merged_data = pd.merge(
    left=behavioural_metrics,
    right=df_replaced,
    left_on="Subject",
    right_on="Subject ID",
)

# Delete rows where column=A
if use_mapped_dataset_only:
    merged_data = merged_data.drop(
        merged_data[merged_data["Dataset"] == "cleaned_words"].index
    )


# merged_data = merged_data.drop(
#     merged_data[merged_data["Y/X Surface Area (mm)"] > 1].index
# )

if use_modules_data:
    merged_data.to_csv(
        "/home/reece/HCIM/core/Human-Connectome-Investigating-Modularity/data_processed/allSubjects_with_behavioural_metrics_merged_not_inc_best_performing.csv"
    )
    min_rows = (
        merged_data.groupby(
            ["Subject ID", "Task", "Hemisphere", "Dataset", "Y Module Name"]
        )["Y/X Surface Area (mm)"]
        .mean()
        .reset_index()
    )
    merged_data = merged_data.merge(
        min_rows,
        on=["Subject ID", "Task", "Hemisphere", "Dataset", "Y Module Name"],
        suffixes=("", "_mean"),
    )
    if use_iqr_of_y_x_ratio_to_clean:
        Q1 = merged_data["abs(Y/X Surface Area (mm) - 1.0)"].quantile(0.25)
        Q3 = merged_data["abs(Y/X Surface Area (mm) - 1.0)"].quantile(0.75)
        # Q1 = merged_data["Y/X Surface Area (mm)"].quantile(0.25)
        # Q3 = merged_data["Y/X Surface Area (mm)"].quantile(0.75)
        IQR = Q3 - Q1

        # Define outlier thresholds
        # lower_bound = Q1 - 1.5 * IQR
        lower_bound = 0
        upper_bound = Q3 + 1.5 * IQR

        merged_data = merged_data[
            (merged_data["abs(Y/X Surface Area (mm) - 1.0)"] >= lower_bound)
            & (merged_data["abs(Y/X Surface Area (mm) - 1.0)"] <= upper_bound)
        ]
    if use_best_performing_pairs_only:
        target_value = 1.0
        merged_data["abs_diff"] = abs(
            (merged_data["Y/X Surface Area (mm)"] - target_value)
        ) + abs((merged_data["Normalised Levenshtein Distance - X as Truth"] - 0.0))

        merged_data = merged_data.loc[
            merged_data.groupby(["Subject ID", "Task", "Hemisphere", "Dataset"])[
                "abs_diff"
            ].idxmin()
        ]

merged_data.to_csv(
    "/home/reece/HCIM/core/Human-Connectome-Investigating-Modularity/data_processed/allSubjects_with_behavioural_metrics_merged.csv"
)

# Select only numeric columns for correlation analysis
numeric_data = merged_data.select_dtypes(include=["float", "int", "float64", "int64"])

# Compute the correlation matrix
correlation_matrix = numeric_data.corr()
np.fill_diagonal(correlation_matrix.values, np.nan)
# Set a threshold
threshold = 0.1

columns_to_keep = correlation_matrix.columns[
    (correlation_matrix.abs() > threshold).any()
]

stat_columns = [
    "Normalized Mutual Information - X as Truth",
    # "Mutual Information Score - X as Truth",
    "Normalised Levenshtein Distance - X as Truth",
    # "Levenshtein Distance - X as Truth",
]
stat_column = stat_columns[0]  # The single statistical column to compare against
analysis_columns = {
    # # "Dexterity Analysis": "Dexterity_AgeAdj",
    # # "Strength Analysis": "Strength_AgeAdj",
    # # "Endurance Analysis": "Endurance_AgeAdj",
    # # "Gait Analysis": "GaitSpeed_Comp",
    # # "Random Analysis: Friendship": "Friendship_Unadj",
    # "MMSE_Score": "MMSE_Score",
    # "PSQI_Score": "PSQI_Score",
    # "PSQI_Comp1": "PSQI_Comp1",
    # "PSQI_Comp2": "PSQI_Comp2",
    # "PSQI_Comp3": "PSQI_Comp3",
    # "PSQI_Comp4": "PSQI_Comp4",
    # "PSQI_Comp5": "PSQI_Comp5",
    # "PSQI_Comp6": "PSQI_Comp6",
    # "PSQI_Comp7": "PSQI_Comp7",
    # # "PSQI_BedTime": "PSQI_BedTime",
    # "PSQI_Min2Aslee": "PSQI_Min2Asleep",
    # "PSQI_AmtSleep": "PSQI_AmtSleep",
    # "PSQI_Latency30Min": "PSQI_Latency30Min",
    # "PSQI_WakeUp": "PSQI_WakeUp",
    # "PSQI_Bathroom": "PSQI_Bathroom",
    # "PSQI_Breathe": "PSQI_Breathe",
    # "PSQI_Snore": "PSQI_Snore",
    # "PSQI_TooCold": "PSQI_TooCold",
    # "PSQI_TooHot": "PSQI_TooHot",
    # "PSQI_BadDream": "PSQI_BadDream",
    # "PSQI_Pain": "PSQI_Pain",
    # "PSQI_Other": "PSQI_Other",
    # "PSQI_Quality": "PSQI_Quality",
    # "PSQI_SleepMeds": "PSQI_SleepMeds",
    # "PSQI_DayStayAwake": "PSQI_DayStayAwake",
    # "PSQI_DayEnthusiasm": "PSQI_DayEnthusiasm",
    # "PSQI_BedPtnrRmat": "PSQI_BedPtnrRmate",
    # "PicSeq_Unadj": "PicSeq_AgeAdj",
    # "CardSort_Unadj": "CardSort_Unadj",
    # "CardSort_AgeAdj": "CardSort_AgeAdj",
    # "Flanker_Unadj": "Flanker_Unadj",
    # "Flanker_AgeAdj": "Flanker_AgeAdj",
    # "PMAT24_A_CR": "PMAT24_A_CR",
    # "PMAT24_A_SI": "PMAT24_A_SI",
    # "PMAT24_A_RTCR": "PMAT24_A_RTCR",
    # "ReadEng_Unadj": "ReadEng_Unadj",
    # "ReadEng_AgeAdj": "ReadEng_AgeAdj",
    # "PicVocab_Unadj": "PicVocab_Unadj",
    # "PicVocab_AgeAdj": "PicVocab_AgeAdj",
    # "ProcSpeed_Unadj": "ProcSpeed_Unadj",
    # "ProcSpeed_AgeAdj": "ProcSpeed_AgeAdj",
    # "DDisc_SV_1mo_200": "DDisc_SV_1mo_200",
    # "DDisc_SV_6mo_200": "DDisc_SV_6mo_200",
    # "DDisc_SV_1yr_200": "DDisc_SV_1yr_200",
    # "DDisc_SV_3yr_200": "DDisc_SV_3yr_200",
    # "DDisc_SV_5yr_200": "DDisc_SV_5yr_200",
    # "DDisc_SV_10yr_200": "DDisc_SV_10yr_200",
    # "DDisc_SV_1mo_40K": "DDisc_SV_1mo_40K",
    # "DDisc_SV_6mo_40K": "DDisc_SV_6mo_40K",
    # "DDisc_SV_1yr_40K": "DDisc_SV_1yr_40K",
    # "DDisc_SV_3yr_40K": "DDisc_SV_3yr_40K",
    # "DDisc_SV_5yr_40K": "DDisc_SV_5yr_40K",
    # "DDisc_SV_10yr_40K": "DDisc_SV_10yr_40K",
    # "DDisc_AUC_200": "DDisc_AUC_200",
    # "DDisc_AUC_40K": "DDisc_AUC_40K",
    # "VSPLOT_TC": "VSPLOT_TC",
    # "VSPLOT_CRTE": "VSPLOT_CRTE",
    # "VSPLOT_OFF": "VSPLOT_OFF",
    # "SCPT_TP": "SCPT_TP",
    # "SCPT_TN": "SCPT_TN",
    # "SCPT_FP": "SCPT_FP",
    # "SCPT_FN": "SCPT_FN",
    # "SCPT_TPRT": "SCPT_TPRT",
    # "SCPT_SEN": "SCPT_SEN",
    # "SCPT_SPEC": "SCPT_SPEC",
    # "SCPT_LRNR": "SCPT_LRNR",
    # "IWRD_TOT": "IWRD_TOT",
    # "IWRD_RTC": "IWRD_RTC",
    # "ListSort_Unadj": "ListSort_Unadj",
    # "ListSort_AgeAdj": "ListSort_AgeAdj",
    # "CogFluidComp_Unadj": "CogFluidComp_Unadj",
    # "CogFluidComp_AgeAdj": "CogFluidComp_AgeAdj",
    # "CogEarlyComp_Unadj": "CogEarlyComp_Unadj",
    # "CogEarlyComp_AgeAdj": "CogEarlyComp_AgeAdj",
    # "CogTotalComp_Unadj": "CogTotalComp_Unadj",
    # "CogTotalComp_AgeAdj": "CogTotalComp_AgeAdj",
    # "CogCrystalComp_Unadj": "CogCrystalComp_Unadj",
    # "CogCrystalComp_AgeAdj": "CogCrystalComp_AgeAdj",
    # "ER40_CR": "ER40_CR",
    # "ER40_CRT": "ER40_CRT",
    # "ER40ANG": "ER40ANG",
    # "ER40FEAR": "ER40FEAR",
    # "ER40HAP": "ER40HAP",
    # "ER40NOE": "ER40NOE",
    # "ER40SAD": "ER40SAD",
    # "AngAffect_Unadj": "AngAffect_Unadj",
    # "AngHostil_Unadj": "AngHostil_Unadj",
    # "AngAggr_Unadj": "AngAggr_Unadj",
    # "FearAffect_Unadj": "FearAffect_Unadj",
    # "FearSomat_Unadj": "FearSomat_Unadj",
    # "Sadness_Unadj": "Sadness_Unadj",
    # "LifeSatisf_Unadj": "LifeSatisf_Unadj",
    # "MeanPurp_Unadj": "MeanPurp_Unadj",
    # "PosAffect_Unadj": "PosAffect_Unadj",
    # "Friendship_Unadj": "Friendship_Unadj",
    # "Loneliness_Unadj": "Loneliness_Unadj",
    # "PercHostil_Unadj": "PercHostil_Unadj",
    # "PercReject_Unadj": "PercReject_Unadj",
    # "EmotSupp_Unadj": "EmotSupp_Unadj",
    # "InstruSupp_Unadj": "InstruSupp_Unadj",
    # "PercStress_Unadj": "PercStress_Unadj",
    # "SelfEff_Unadj": "SelfEff_Unadj",
    "Endurance_Unadj": "Endurance_Unadj",
    "Endurance_AgeAdj": "Endurance_AgeAdj",
    "GaitSpeed_Comp": "GaitSpeed_Comp",
    "Dexterity_Unadj": "Dexterity_Unadj",
    "Dexterity_AgeAdj": "Dexterity_AgeAdj",
    "Strength_Unadj": "Strength_Unadj",
    "Strength_AgeAdj": "Strength_AgeAdj",
    # "NEOFAC_A": "NEOFAC_A",
    # "NEOFAC_O": "NEOFAC_O",
    # "NEOFAC_C": "NEOFAC_C",
    # "NEOFAC_N": "NEOFAC_N",
    # "NEOFAC_E": "NEOFAC_E",
    # "Noise_Comp": "Noise_Comp",
    # "Odor_Unadj": "Odor_Unadj",
    # "Odor_AgeAdj": "Odor_AgeAdj",
    # "PainIntens_RawScore": "PainIntens_RawScore",
    # "PainInterf_Tscore": "PainInterf_Tscore",
    # "Taste_Unadj": "Taste_Unadj",
    # "Taste_AgeAdj": "Taste_AgeAdj",
    # "Mars_Log_Score": "Mars_Log_Score",
    # "Mars_Errs": "Mars_Errs",
    # "Mars_Final": "Mars_Final",
}

if use_modules_data:
    analysis_columns.update(
        {
            "X Surface Area (mm)": "X Surface Area (mm)",
            "Y Surface Area (mm)": "Y Surface Area (mm)",
            "Y/X Surface Area (mm)": "Y/X Surface Area (mm)",
            "abs(Y/X Surface Area (mm) - 1.0)": "abs(Y/X Surface Area (mm) - 1.0)",
            "Y/X Surface Area (mm)_mean": "Y/X Surface Area (mm)_mean",
        }
    )


# columns_to_keep = columns_to_keep.union(pd.Index(analysis_columns.values()))
columns_to_keep = pd.Index(analysis_columns.values()).union(pd.Index(stat_columns))

# Filter the correlation matrix to retain only the desired columns and rows
filtered_corr: pd.DataFrame = correlation_matrix.loc[columns_to_keep, columns_to_keep]

# Optionally reset the diagonal to 1
np.fill_diagonal(filtered_corr.values, 1)
filtered_corr.to_csv(
    "/home/reece/HCIM/core/Human-Connectome-Investigating-Modularity/data_processed/correlation_matrix.csv"
)

filtered_corr = filtered_corr[filtered_corr.abs() > threshold]
makeCorrelationMatrix = 1
if makeCorrelationMatrix == 1:
    chunk_size = 400
    chunks = [
        filtered_corr.iloc[i : i + chunk_size, i : i + chunk_size]
        for i in range(0, filtered_corr.shape[0], chunk_size)
    ]

    for i, chunk in enumerate(chunks):
        plt.figure(figsize=(8, 6))
        sns.heatmap(
            chunk,
            annot=True,
            fmt=".2f",
            cmap="coolwarm",
            linewidths=0.5,
            annot_kws={"size": 6},
            square=True,
        )
        plt.title(f"Correlation Matrix Chunk {i+1}")
        if use_modules_data:
            plt.suptitle(
                f"Average Y/X Value: {merged_data['Y/X Surface Area (mm)'].mean()} \n Average Normalised Levenshtein Distance: {merged_data['Normalised Levenshtein Distance - X as Truth'].mean()}"
            )
        plt.tight_layout()
    print("Done")
    plt.show()
    print("ok")
# # Display the top of the correlation matrix
# print(filtered_corr.head())
# plt.figure(figsize=(12, 12))
# sns.heatmap(
#     filtered_corr,
#     annot=True,  # Show correlation values
#     annot_kws={"size": 6},  # Size of font for annotations
#     fmt=".2f",  # Format for numbers
#     cmap="coolwarm",  # Color map
#     cbar=False,  # Show color bar
#     linewidths=0.5,  # Line width between cells
#     square=True,
# )  # Make cells square
# plt.title("Correlation Matrix Heatmap", fontsize=6)
# plt.xticks(rotation=45, ha="right")  # Rotate x-axis labels
# plt.yticks(rotation=0)  # Keep y-axis labels horizontal
# plt.tight_layout()
# plt.show()

# Extract relevant columns for analysis


class ResultsDict(TypedDict):
    Title: str
    Correlation: float
    Effect_size: float
    P_value: float
    Number_of_observations: int


# Prepare a list to hold results
results: List[ResultsDict] = []

# Iterate through the analysis columns
for title, analysis_col in analysis_columns.items():
    # Filter the data
    filtered_data = merged_data[[analysis_col, stat_column]].dropna()

    # Calculate the correlation and p-value
    correlation, p_value = pearsonr(
        filtered_data[analysis_col], filtered_data[stat_column]
    )

    # Append the result to the list
    results.append(
        {
            "Title": title,
            "Correlation": float(correlation),
            "Effect_size": float(correlation**2),
            "P_value": float(p_value),
            "Number_of_observations": len(filtered_data),
        }
    )

sorted_results: List[ResultsDict] = sorted(
    results, key=lambda x: abs(x["Correlation"]), reverse=True
)
df = pd.DataFrame(sorted_results)
csv_file_path = "/home/reece/HCIM/core/Human-Connectome-Investigating-Modularity/data_processed/correlation_and_p_values.csv"
df.to_csv(csv_file_path, index=False)

# Display results
for result in sorted_results:
    print(result)


print("Now selecting highest performing module pairs")
min_rows = (
    merged_data.groupby(
        ["Subject ID", "Task", "Hemisphere", "Dataset", "Y Module Name"]
    )["Y/X Surface Area (mm)"]
    .mean()
    .reset_index()
)
merged_data = merged_data.merge(
    min_rows,
    on=["Subject ID", "Task", "Hemisphere", "Dataset", "Y Module Name"],
    suffixes=("", "_mean"),
)

min_rows.to_csv(
    "/home/reece/HCIM/core/Human-Connectome-Investigating-Modularity/data_processed/min_normalised_levenshtein_distance.csv"
)
print("Done")
