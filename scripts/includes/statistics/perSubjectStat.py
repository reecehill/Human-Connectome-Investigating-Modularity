# Re-importing necessary libraries and preparing data again
import numpy as np
import modules.globals as g
import pandas as pd
import config
from includes.statistics import (
    test_ranges,
    test_functions_with_range,
    generateInterpretation,
    convertSubjectWideResultsToDataFrames,
)
from includes.statistics.testVariables import Float, ResultRowSubjectWide
from includes.stepper.functions import allStepsAreSuccessful
from includes.statistics.save_results import append_results


def perSubjectStat(
    datasetDescriptor: str, x_final: "pd.Series[str]", y_final: "pd.Series[str]"
) -> None:
    # Prepare results storage
    results_x_truth_with_range: "list[ResultRowSubjectWide]" = []
    results_y_truth_with_range: "list[ResultRowSubjectWide]" = []
    random_x = pd.Series()
    random_y = pd.Series()

    # --- SUBJECT-WIDE TESTS [START] ---
    # Run tests for X as truth
    for test_name, test_func in test_functions_with_range:
        try:
            score_x_defined: Float = test_func(x_final, y_final)

            y_probabilities: pd.Series[float] = y_final.value_counts(normalize=True)
            random_y = pd.Series(
                g.randomGen.choice(
                    y_probabilities.index,
                    size=y_final.size,
                    p=y_probabilities.to_numpy(),
                ),
                index=y_final.index,
            ).astype(y_final.dtype)
            random_y.attrs = y_final.attrs

            score_x_imported_random_y: Float = test_func(
                x_final,
                random_y,
            )

            x_probabilities: pd.Series[float] = x_final.value_counts(normalize=True)
            random_x = pd.Series(
                g.randomGen.choice(
                    x_probabilities.index,
                    size=x_final.size,
                    p=x_probabilities.to_numpy(),
                ),
                index=x_final.index,
            ).astype(x_final.dtype)
            random_x.attrs = x_final.attrs
            score_x_random_y_imported: Float = test_func(
                random_x,
                y_final,
            )

            results_x_truth_with_range.append(
                (
                    config.TIMESTAMP_OF_SCRIPT,
                    config.CURRENT_SUBJECT,
                    allStepsAreSuccessful(),
                    config.CURRENT_HEMISPHERE,
                    config.CURRENT_TASK,
                    f"{datasetDescriptor}",
                    f"{test_name} - X as Truth",
                    score_x_defined,
                    score_x_imported_random_y,
                    score_x_random_y_imported,
                    generateInterpretation(test_name, score_x_defined),
                    test_ranges[test_name],
                )
            )

        except Exception as e:
            g.logger.error(f"Error running {test_name} with x as truth: {e}")

            # Run tests for Y as truth
    for test_name, test_func in test_functions_with_range:
        try:
            score_y_defined = test_func(y_final, x_final)

            x_probabilities: pd.Series[float] = x_final.value_counts(normalize=True)
            random_x = pd.Series(
                g.randomGen.choice(
                    x_probabilities.index,
                    size=x_final.size,
                    p=x_probabilities.to_numpy(),
                ),
                index=x_final.index,
            ).astype(x_final.dtype)
            random_x.attrs = x_final.attrs

            score_y_imported_random_x = test_func(
                y_final,
                random_x,
            )

            y_probabilities: pd.Series[float] = y_final.value_counts(normalize=True)
            random_y = pd.Series(
                g.randomGen.choice(
                    y_probabilities.index,
                    size=y_final.size,
                    p=y_probabilities.to_numpy(),
                ),
                index=y_final.index,
            ).astype(y_final.dtype)
            random_y.attrs = y_final.attrs

            score_y_random_x_imported = test_func(
                random_y,
                x_final,
            )

            results_y_truth_with_range.append(
                (
                    config.TIMESTAMP_OF_SCRIPT,
                    config.CURRENT_SUBJECT,
                    allStepsAreSuccessful(),
                    config.CURRENT_HEMISPHERE,
                    config.CURRENT_TASK,
                    f"{datasetDescriptor}",
                    f"{test_name} - Y as Truth",
                    score_y_defined,
                    score_y_imported_random_x,
                    score_y_random_x_imported,
                    generateInterpretation(test_name, score_y_defined),
                    test_ranges[test_name],
                )
            )
        except Exception as e:
            g.logger.error(f"Error running {test_name} with y as truth: {e}")
            results_y_truth_with_range.append(
                (
                    config.TIMESTAMP_OF_SCRIPT,
                    config.CURRENT_SUBJECT,
                    allStepsAreSuccessful(),
                    config.CURRENT_HEMISPHERE,
                    config.CURRENT_TASK,
                    f"{datasetDescriptor}",
                    f"{test_name} - failed",
                    np.nan,
                    np.nan,
                    np.nan,
                    generateInterpretation(test_name, np.nan),
                    test_ranges[test_name],
                )
            )

        # Convert results to DataFrames

    # For demo purposes, make a timeline plot of random.
    # plot_timeline(
    #     x_final, random_y, title=f"Real X, Random Y - perSubject[{datasetDescriptor}]"
    # )
    # plot_timeline(
    #     random_x, y_final, title=f"Random X, Real Y - perSubject[{datasetDescriptor}]"
    # )

    # For tests not requiring truth, take x.
    dfXTruthWithRange, dfYTruthWithRange = convertSubjectWideResultsToDataFrames(
        results_x_truth_with_range, results_y_truth_with_range
    )

    append_results(dfXTruthWithRange, dfYTruthWithRange, config.STAT_FILE_BY_SUBJECT)
    del results_y_truth_with_range, results_x_truth_with_range
    # --- SUBJECT-WIDE TESTS [END] ---
