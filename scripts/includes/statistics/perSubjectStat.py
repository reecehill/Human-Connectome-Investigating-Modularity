# Re-importing necessary libraries and preparing data again
from enum import unique
import numpy as np
import numpy.typing as npt
from sklearn.metrics import silhouette_score
from includes.statistics.testFunctions import pad_indexes
import modules.globals as g
import pandas as pd
import config
from includes.statistics import test_ranges, test_functions_with_range, generateInterpretation, convertSubjectWideResultsToDataFrames, convertModuleWideResultsToDataFrames
from pathlib import Path
from includes.statistics.testVariables import Float, ResultRowSubjectWide, ResultRowModuleWide
from includes.statistics.utils import convertNumericalModuleToWords, convertNumericalModulesToWords, calcModuleSizes
from includes.stepper.functions import allStepsAreSuccessful
from includes.statistics.clean_data import clean_data
from includes.statistics.save_results import save_results


def perModuleStat(x_final: "pd.Series[str]", y_final: "pd.Series[str]", x: "pd.Series[int]", y: "pd.Series[int]", xy_surface_area: "pd.DataFrame") -> None:
    # --- MODULE-SPECIFIC TESTS [START] ---
    # Prepare results storage

    y_module_names: pd.Series[str] = y_final.drop_duplicates()
    for (_, y_module_name) in enumerate(y_module_names):
        results_x_truth_by_module: list[ResultRowModuleWide] = []
        results_y_truth_by_module: list[ResultRowModuleWide] = []
        # Looping through each Y module.
        if (y_module_name == 'missing'):
            # Do not process missing fMRI modules and proceed to next module.
            continue
        
        # Get current Y module
        y_module: pd.Series[str] = y_final[(y_final == y_module_name)]

        # Get current X module (by taking mode) in both cleaned and uncleaned data
        x_module_name: str = x_final[y_module.index].mode()[0]
        x_module: "pd.Series[str]" = x_final[(x_final == x_module_name)]
        x_module_orig: "pd.Series[int]" = x[x_module.index]

        if (len(x_module_orig.unique()) == 1):
            x_module_name_orig: int = x_module_orig.values[0]
        else:
            raise ValueError("X module is not unique.")

        x_final_module_all: pd.Series[str] = convertNumericalModuleToWords(
            x[x == x_module_name_orig])

        # ------
        # Calculate module surface areas
        # ------
        x_module_sa, y_module_sa, ydivx_modula_sa = calcModuleSizes(
            x_final_module_all, y_module, xy_surface_area.to_numpy().flatten())

        if("padXModules" == "padXModules" and 1 == 1):
            x_final_module_all_paddedIndexes: list[int] = pad_indexes(x_final_module_all.index, x.index, n=5)
            x_final_module_all_padded: pd.Series[str] = convertNumericalModuleToWords(
                x[pd.Index(x_final_module_all_paddedIndexes)])
            x_final_module_all = x_final_module_all_padded

        if ("randomiseMissingYModules" == "randomiseMissingYModules" and 1 == 1):
        # Get the y modules underlying all of x_1. Note that this may yield missing/non-labelled y modules. 
        # Replace missing y modules with random values
            y_final_module_within_x_with_missing: pd.Series[int] = y[x_final_module_all.index].replace([0,1,"1"], np.nan)
            y_final_module_within_x_with_missing[y_final_module_within_x_with_missing.isna()] = np.random.normal(loc=0, scale=1, size=y_final_module_within_x_with_missing.isna().sum())
        else:
            y_final_module_within_x_with_missing: pd.Series[int] = y[x_final_module_all.index].replace([0,1,"1",np.nan], -1)

        # Convert to words.
        y_final_module_within_x: pd.Series[str] = convertNumericalModuleToWords(y_final_module_within_x_with_missing)

        
        x_final_module = x_final_module_all[y_final_module_within_x.index]
        
        # ------
        # Make x and y symmetric
        x_final_module_symm = pd.concat(
            [x_final_module, pd.Series(np.flip(x_final_module))])
        y_final_module_symm = pd.concat(
            [y_final_module_within_x, pd.Series(np.flip(y_final_module_within_x))])

        if ("makeModulesSymmetrical" == "makeModulesSymmetrical" and 1 == 1):
            x_final_module = x_final_module_symm
            y_final_module_within_x = y_final_module_symm

        # ------
        # Run tests for X as truth
        for test_name, test_func in test_functions_with_range:
            try:
                score_x_defined: Float = test_func(
                    x_final_module, y_final_module_within_x)

                score_x_imported_random_y: Float = test_func(
                    x_final_module,
                    convertNumericalModuleToWords(
                        pd.Series(
                            g.randomGen.integers(
                                low=len(y_final_module_within_x.unique()),
                                high=None,
                                size=len(y_final_module_within_x)
                            )
                        )
                    ),
                )

                score_x_random_y_imported: Float = test_func(
                    convertNumericalModuleToWords(
                        pd.Series(
                            g.randomGen.integers(
                                low=len(x_final_module.unique()),
                                high=None,
                                size=len(x_final_module)
                            )
                        )
                    ),
                    y_final_module_within_x
                )

                results_x_truth_by_module.append((
                    config.TIMESTAMP_OF_SCRIPT,
                    config.CURRENT_SUBJECT,
                    allStepsAreSuccessful(),
                    config.CURRENT_HEMISPHERE,
                    config.CURRENT_TASK,
                    x_module_name,
                    y_module_name,
                    x_module_sa,
                    y_module_sa,
                    ydivx_modula_sa,
                    f'{test_name} - X as Truth',
                    score_x_defined,
                    score_x_imported_random_y,
                    score_x_random_y_imported,
                    generateInterpretation(test_name, score_x_defined),
                    test_ranges[test_name]
                ))
            except Exception as e:
                g.logger.error(
                    f"Error running {test_name} with x as truth: {e}")

                # Run tests for Y as truth

            # Run tests for Y as truth
        # Run tests for Y as truth
        for test_name, test_func in test_functions_with_range:
            try:             
                score_y_defined = test_func(
                    y_final_module_within_x, x_final_module)
                score_y_imported_random_x = test_func(
                    y_final_module_within_x,
                    convertNumericalModuleToWords(
                        pd.Series(
                            g.randomGen.integers(
                                low=len(x_final_module.unique()),
                                high=None,
                                size=len(x_final_module)
                            )
                        )
                    ),
                )
                score_y_random_x_imported = test_func(
                    convertNumericalModuleToWords(
                        pd.Series(
                            g.randomGen.integers(
                                low=len(y_final_module_within_x.unique()),
                                high=None,
                                size=len(y_final_module_within_x)
                            )
                        )
                    ),
                    x_final_module)

                results_y_truth_by_module.append((
                    config.TIMESTAMP_OF_SCRIPT,
                    config.CURRENT_SUBJECT,
                    allStepsAreSuccessful(),
                    config.CURRENT_HEMISPHERE,
                    config.CURRENT_TASK,
                    x_module_name,
                    y_module_name,
                    x_module_sa,
                    y_module_sa,
                    ydivx_modula_sa,
                    f'{test_name} - Y as Truth',
                    score_y_defined,
                    score_y_imported_random_x,
                    score_y_random_x_imported,
                    generateInterpretation(test_name, score_y_defined),
                    test_ranges[test_name],
                ))
            except Exception as e:
                g.logger.error(
                    f"Error running {test_name} with y as truth: {e}")
                results_y_truth_by_module.append((
                    config.TIMESTAMP_OF_SCRIPT,
                    config.CURRENT_SUBJECT,
                    allStepsAreSuccessful(),
                    config.CURRENT_HEMISPHERE,
                    config.CURRENT_TASK,
                    x_module_name,
                    y_module_name,
                    x_module_sa,
                    y_module_sa,
                    ydivx_modula_sa,
                    f'{test_name} - failed',
                    np.nan,
                    np.nan,
                    np.nan,
                    generateInterpretation(test_name, np.nan),
                    test_ranges[test_name],
                ))

        dfXTruthByModule, dfYTruthByModule = convertModuleWideResultsToDataFrames(
            results_x_truth_by_module, results_y_truth_by_module)

        save_results(dfXTruthByModule, dfYTruthByModule,
                     config.STAT_FILE_BY_MODULE)


def perSubjectStat(x_final: "pd.Series[str]", y_final: "pd.Series[str]") -> None:
    # Prepare results storage
    results_x_truth_with_range: list[ResultRowSubjectWide] = []
    results_y_truth_with_range: list[ResultRowSubjectWide] = []

    # --- SUBJECT-WIDE TESTS [START] ---
    # Run tests for X as truth
    for test_name, test_func in test_functions_with_range:
        try:
            score_x_defined: Float = test_func(x_final, y_final)
            score_x_imported_random_y: Float = test_func(
                x_final,
                convertNumericalModuleToWords(
                    pd.Series(
                        g.randomGen.integers(
                            low=len(y_final.unique()),
                            high=None,
                            size=len(y_final)
                        )
                    )
                )
            )
            score_x_random_y_imported: Float = test_func(
                convertNumericalModuleToWords(
                    pd.Series(
                        g.randomGen.integers(
                            low=len(x_final.unique()),
                            high=None,
                            size=len(x_final)
                        )
                    )
                ),
                y_final
            )

            results_x_truth_with_range.append((
                config.TIMESTAMP_OF_SCRIPT,
                config.CURRENT_SUBJECT,
                allStepsAreSuccessful(),
                config.CURRENT_HEMISPHERE,
                config.CURRENT_TASK,
                f'{test_name} - X as Truth',
                score_x_defined,
                score_x_imported_random_y,
                score_x_random_y_imported,
                generateInterpretation(test_name, score_x_defined),
                test_ranges[test_name]
            ))

        except Exception as e:
            g.logger.error(
                f"Error running {test_name} with x as truth: {e}")

            # Run tests for Y as truth
    for test_name, test_func in test_functions_with_range:
        try:
            score_y_defined = test_func(y_final, x_final)
            score_y_imported_random_x = test_func(
                y_final,
                convertNumericalModuleToWords(
                    pd.Series(
                        g.randomGen.integers(
                            low=len(x_final.unique()),
                            high=None,
                            size=len(x_final)
                        )
                    )
                ),
            )
            score_y_random_x_imported = test_func(
                convertNumericalModuleToWords(
                    pd.Series(
                        g.randomGen.integers(
                            low=len(y_final.unique()),
                            high=None,
                            size=len(y_final)
                        )
                    )
                ),
                x_final)

            results_y_truth_with_range.append((
                config.TIMESTAMP_OF_SCRIPT,
                config.CURRENT_SUBJECT,
                allStepsAreSuccessful(),
                config.CURRENT_HEMISPHERE,
                config.CURRENT_TASK,
                f'{test_name} - Y as Truth',
                score_y_defined,
                score_y_imported_random_x,
                score_y_random_x_imported,
                generateInterpretation(test_name, score_y_defined),
                test_ranges[test_name],
            ))
        except Exception as e:
            g.logger.error(
                f"Error running {test_name} with y as truth: {e}")
            results_y_truth_with_range.append((
                config.TIMESTAMP_OF_SCRIPT,
                config.CURRENT_SUBJECT,
                allStepsAreSuccessful(),
                config.CURRENT_HEMISPHERE,
                config.CURRENT_TASK,
                f'{test_name} - failed',
                np.nan,
                np.nan,
                np.nan,
                generateInterpretation(test_name, np.nan),
                test_ranges[test_name],
            ))

        # Convert results to DataFrames

    # For tests not requiring truth, take x.
    dfXTruthWithRange, dfYTruthWithRange = convertSubjectWideResultsToDataFrames(
        results_x_truth_with_range, results_y_truth_with_range)

    save_results(dfXTruthWithRange, dfYTruthWithRange,
                 config.STAT_FILE_BY_SUBJECT)
    del results_y_truth_with_range, results_x_truth_with_range
    # --- SUBJECT-WIDE TESTS [END] ---
