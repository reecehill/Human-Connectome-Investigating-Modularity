# Re-importing necessary libraries and preparing data again
from typing import Union, cast
import numpy as np
from includes.statistics.nan_handlers import white_noise
from includes.statistics.testFunctions import pad_indexes
import modules.globals as g
import pandas as pd
import config
from includes.statistics import test_ranges, test_functions_with_range, generateInterpretation, convertModuleWideResultsToDataFrames
from includes.statistics.clean_data import clean_data
from includes.statistics.testVariables import Float, ResultRowModuleWide
from includes.statistics.utils import calculateLevenshteinDistance, convertNumericalModuleToWords, calcModuleSizes, convertNumericalModulesToWords
from includes.stepper.functions import allStepsAreSuccessful
from includes.statistics.save_results import save_results
from sklearn.metrics.cluster import contingency_matrix
from scipy.optimize import linear_sum_assignment  # type: ignore


def perModuleStat(datasetDescriptor: str, x_final: "pd.Series[str]", y_final: "pd.Series[str]", x: "Union[pd.Series[str],pd.Series[int]]", y: "Union[pd.Series[str],pd.Series[int]]", xy_surface_areas: "pd.DataFrame") -> None:
    # --- MODULE-SPECIFIC TESTS [START] ---
    y_module_names: "pd.Series[str]" = y_final.drop_duplicates()

    for (_, y_module_name) in enumerate(y_module_names):
        # Looping through each Y module.
        if (y_module_name == 'missing'):
            # Do not process missing fMRI modules and proceed to next module.
            continue

        # Prepare results storage
        results_x_truth_by_module: "list[ResultRowModuleWide]" = []
        results_y_truth_by_module: "list[ResultRowModuleWide]" = []

        # ------
        # Get current Y module
        # NB: This works because indexes persist as we constrain the vector.
        # ------
        orig_y_module: "pd.Series[str]" = y_final.where(y_final == y_module_name)

        # ------
        # Get optimal X module
        # NB: Functional modules may overlay multiple structural modules.
        # We need to find the structural module that best represents the functional module, in
        # order to derive optimal structure-function pairs.
        # ------
        if ("mapped" in datasetDescriptor):
            # The x and y modules are mapped to the same set. So, we can take x just by knowing y.
            x_module_name: str = y_module_name
        else:
            # The x and y modules are not mapped to the same set. So, we need to find the optimal x module.
            # Get the x module that is most common to the y module.
            x_module_name: str = x_final[orig_y_module.dropna().index].mode()[
                0]

        # With the optimal x-y pair found within our filtered x and y, we now get pre-filtered x (to expose missing y values that were removed by masking).
        x_module: "pd.Series[str]" = x_final.where(x_final == x_module_name)
        x_module_orig: "Union[pd.Series[str], pd.Series[int]]" = x[x_module.dropna().index]
        x_module_orig_unique = x_module_orig.unique()
        if (x_module_orig_unique.size == 1):
            x_module_name_orig: int = x_module_orig.values[0]
        else:
            g.logger.error(
                "X module is not unique. Explicit logic for this edge case is required. X modules found: ["+', '.join(str(moduleName) for moduleName in x_module_orig_unique)+"]")
            raise ValueError("X module is not unique, or is possibly empty. Statistics for this subject skipped.")
        
        x_final_module: "Union[pd.Series[str], pd.Series[int]]" = x.where(x == x_module_name_orig)

        y_final_module_within_x: "Union[pd.Series[str], pd.Series[int]]" = y.where(
            y.index.isin(x_final_module[x_final_module.notna()].index))


        # Calculate module surface areas, including relative x-y SA (y divided by x)
        x_module_sa, y_module_sa, ydivx_modula_sa = calcModuleSizes(
            x_final_module.dropna(), orig_y_module.dropna(), xy_surface_areas.to_numpy().flatten())

        # -----
        # Pad the x modules to include surrounding modules
        # NB: This widens the window to include adjacent modules and thus increase the number of module boundaries.
        # This may result in more detailed module boundaries, but it may also increase the complexity of the analysis.
        # We leave this as an option for the user to decide.
        # -----
        if (1 == 0):
            x_paddedIndexes: "list[int]" = pad_indexes(
            x_final_module.dropna().index, x.index, n=1)

            x_final_module, y_final_module_within_x = x.where(x.index.isin(pd.Index(x_paddedIndexes))), y.where(y.index.isin(pd.Index(x_paddedIndexes)))


        # -----
        # Handle the missing y data.
        # NB: Now we've potentially selected more y modules, we may have included some NaN values. These must be handled.
        handlerForNaNYValues: str = 'do_nothing'

        if (handlerForNaNYValues == "randomise"):
            # Replace missing y modules with random values, but without affecting the distribution of y.
            _, _y_final_module_within_x_with_missing =  white_noise(
                x=x_final_module.dropna(),
                y=y_final_module_within_x[y_final_module_within_x.index.isin(x_final_module.dropna().index)],
                sample_from_y=y.dropna()
            )
            y_final_module_within_x_with_missing = cast(
                "Union[pd.Series[str],pd.Series[int]]", _y_final_module_within_x_with_missing)
            y_final_module_within_x[y_final_module_within_x_with_missing.index] = y_final_module_within_x_with_missing
            pass
        elif "do_nothing":
            pass
        else:
            raise ValueError(
                f"Invalid handler for NaN Y values: {handlerForNaNYValues}")

        if(isinstance(x_final_module, pd.Series)):
            if(x_final_module.dtype == 'object'):
                x_final_module.fillna("missing", inplace=True)
                y_final_module_within_x.fillna("missing", inplace=True)
            elif (pd.api.types.is_integer_dtype(x_final_module)):
                x_final_module.fillna(-1, inplace=True)
                y_final_module_within_x.fillna(-1, inplace=True)
            else:
                raise ValueError(
                    f"Invalid data typee for x_final_module: {x_final_module.dtype}")
        else:
            raise ValueError(
                f"Invalid data type for x_final_module: {type(x_final_module)}")
            
        # ------
        # Run tests for X as truth
        for test_name, test_func in test_functions_with_range:
            try:
                score_x_defined: Float = test_func(
                    x_final_module, y_final_module_within_x)

                score_x_imported_random_y: Float = test_func(
                    x_final_module,
                    pd.Series(
                        g.randomGen.choice(
                            a=y.unique(),
                            size=y_final_module_within_x.size,
                        ),
                    ).astype(y_final_module_within_x.dtype)
                )

                score_x_random_y_imported: Float = test_func(
                    
                    pd.Series(
                        g.randomGen.choice(
                            a=x.unique(),
                            size=y_final_module_within_x.size,
                        ),
                    ).astype(x_final_module.dtype),
                    y_final_module_within_x
                )

                results_x_truth_by_module.append((
                    config.TIMESTAMP_OF_SCRIPT,
                    config.CURRENT_SUBJECT,
                    allStepsAreSuccessful(),
                    config.CURRENT_HEMISPHERE,
                    config.CURRENT_TASK,
                    f'{datasetDescriptor}',
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
                    pd.Series(
                        g.randomGen.choice(
                            a=x.unique(),
                            size=y_final_module_within_x.size,
                        ),
                    ).astype(x_final_module.dtype)
                )
                score_y_random_x_imported = test_func(
                    pd.Series(
                        g.randomGen.choice(
                            a=y.unique(),
                            size=x_final_module.size,
                        ),
                    ).astype(y_final_module_within_x.dtype),
                    x_final_module)

                results_y_truth_by_module.append((
                    config.TIMESTAMP_OF_SCRIPT,
                    config.CURRENT_SUBJECT,
                    allStepsAreSuccessful(),
                    config.CURRENT_HEMISPHERE,
                    config.CURRENT_TASK,
                    f'{datasetDescriptor}',
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
                    f'{datasetDescriptor}',
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
