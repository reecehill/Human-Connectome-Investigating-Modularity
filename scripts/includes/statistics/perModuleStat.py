# Re-importing necessary libraries and preparing data again
from typing import Any, Dict, List, Literal, Union, cast
import numpy as np
from includes.statistics.nan_handlers import white_noise
from includes.statistics.testFunctions import pad_indexes
from includes.visualisation.plot_timeline import plot_timeline
import modules.globals as g
import pandas as pd
import config
from includes.statistics.clean_data import clean_data
from includes.statistics import (
    test_ranges,
    test_functions_with_range,
    generateInterpretation,
    convertModuleWideResultsToDataFrames,
)
from includes.statistics.testVariables import Float, ResultRowModuleWide, XYZDict
from includes.statistics.utils import calculateEuclidianDistance, calcModuleSizes
from includes.stepper.functions import allStepsAreSuccessful
from includes.statistics.save_results import save_results


def getModuleXNameFromModuleYName(
    x_final: "pd.Series[str]",
    orig_y_module: "pd.Series[str]",
    y_module_name: str,
    useModeMethod: bool = True,
) -> str:
    # ------
    # Get optimal X module
    # NB: Functional modules may overlay multiple structural modules.
    # We need to find the structural module that best represents the functional module, in
    # order to derive optimal structure-function pairs.
    # ------
    if useModeMethod:
        # The x and y modules are not mapped to the same set. So, we need to find the optimal x module.
        # Get the x module that is most common to the y module.
        x_module_name: str = x_final[orig_y_module.dropna().index].mode()[0]
    else:
        # The x and y modules are mapped to the same set. So, we can take x just by knowing y.
        x_module_name: str = y_module_name

    return x_module_name


def transformMappedMatrixScores(
    y: "pd.Series[Any]",
    mappedMatrixScores: "Dict[str, Dict[str, float]]",
) -> "Dict[str, Dict[str, float]]":
    # Matrix scores are stored in a dictionary using keys equal to the name of Y modules at the time. Following mapping, these may have changed. Hence, we remap the matrix to conform to the new Y names. We loop, in reverse order, through changes to the dataset until we arrive at mapAllModulesToSameSet (which should only be applied to the set once!)

    y_applied_handlers: list[Dict[str, Any]] = y.attrs.get("applied_handlers", [])

    # Check specifically for 'mapAllModulesToSameSet' duplication
    handlers_used = np.array([handler["name"] for handler in y_applied_handlers])
    if np.count_nonzero(handlers_used == "mapAllModulesToSameSet") != 1:
        raise ValueError("Must apply 'mapAllModulesToSameSet' once to a dataset.")

    # Find the index of 'mapAllModulesToSameSet', so we can apply transformations from this point.
    mapper_is_applied_from = np.argmax(handlers_used == "mapAllModulesToSameSet")

    for y_applied_handler in y_applied_handlers[mapper_is_applied_from + 1 :]:
        if y_applied_handler["name"] == "convertNumericalModulesToWords":
            # Map the matrix scores to the new Y module names.
            mapping = y_applied_handler["metadata"]["label_to_word_map_xory"].items()
            pass

    return mappedMatrixScores


def perModuleStat(
    datasetDescriptor: str,
    x_final: "Union[pd.Series[str],pd.Series[int]]",
    y_final: "Union[pd.Series[str],pd.Series[int]]",
    x: "Union[pd.Series[str],pd.Series[int]]",
    y: "Union[pd.Series[str],pd.Series[int]]",
    xy_surface_areas: "pd.DataFrame",
    centroid_coords: "pd.DataFrame",
    mappedMatrixScores: "Dict[str, Dict[str, float]]",
) -> None:
    
    _x_cleaned_mapped_modules, _y_cleaned_mapped_modules = clean_data(
            nan_handlers=[
                # "mask_removeMissing",
                "get_main_fn_module_by_topology",
                "filter_by_parent",
            ],
            x=x_final,
            y=y_final,
            orig_x=x,  # Used to pass original x to filter_by_parent
            xRetrievalMethod="getMode",
            centroid_coords=centroid_coords,
        )
    x_cleaned_mapped_modules: "pd.Series[int]" = cast(
            "pd.Series[int]", _x_cleaned_mapped_modules
        )
    y_cleaned_mapped_modules: "pd.Series[int]" = cast(
            "pd.Series[int]", _y_cleaned_mapped_modules
        )
    del _x_cleaned_mapped_modules, _y_cleaned_mapped_modules

    x_final = x_cleaned_mapped_modules.astype(str)
    y_final = y_cleaned_mapped_modules.astype(str)

    # --- MODULE-SPECIFIC TESTS [START] ---
    y_module_names: "pd.Series[str]" = y_final.drop_duplicates().astype(str)
    # transformMappedMatrixScores(y=y_final, mappedMatrixScores=mappedMatrixScores)
    random_x = pd.Series()
    random_y = pd.Series()

    for _, y_module_name in enumerate(y_module_names):
        # Looping through each Y module.
        if any(substring in y_module_name for substring in ["missing", "-1", "nan"]):
            # Do not process missing fMRI modules and proceed to next module.
            continue

        # Prepare results storage
        results_x_truth_by_module: "list[ResultRowModuleWide]" = []
        results_y_truth_by_module: "list[ResultRowModuleWide]" = []

        # ------
        # Get current Y module
        # NB: This works because indexes persist despite constraining the vector.
        # ------
        orig_y_module: "pd.Series[str]" = y_final.where(
            y_final == y_module_name
        ).dropna()

        if "mapped" not in datasetDescriptor:
            x_module_name = getModuleXNameFromModuleYName(
                x_final=x_final,
                orig_y_module=orig_y_module,
                y_module_name=y_module_name,
                useModeMethod=True,
            )
            pass
        else:
            x_module_name = (
                y_module_name  # For mapped data, we use Y module name as X module name.
            )

        orig_x_module: "pd.Series[str]" = x_final.where(x_final == x_module_name)

        # With the optimal x-y pair found within our filtered x and y, we now get pre-filtered x (to expose missing y values that were removed by masking).
        x_final_module, y_final_module_within_x = clean_data(
            nan_handlers=[
                "filter_by_parent",
            ],
            x=x_final,  # type: ignore
            y=orig_y_module,  # type: ignore
            orig_x=x,
            xRetrievalMethod="getMode",
            title="final_module_hard_masked",
            hardMask=True,
        )
        x_final_module.dropna(inplace=True)
        y_final_module_within_x.dropna(inplace=True)

        # Ensure type consistency as clean_data returns pd.Series[int]
        if pd.api.types.infer_dtype(y_final) == "string":
            y_final_module_within_x = y_final_module_within_x.replace(-1, "missing-B")

        if pd.api.types.infer_dtype(x_final) == "string":
            x_final_module = x_final_module.replace(-1, "missing-B")

        # Calculate module surface areas, including relative x-y SA (y divided by x)
        x_module_sa, y_module_sa, ydivx_module_sa = calcModuleSizes(
            x_final_module,
            orig_y_module,
            xy_surface_areas.to_numpy().flatten(),
        )

        # -----
        # Pad the x modules to include surrounding modules
        # NB: This widens the window to include adjacent modules and thus increase the number of module boundaries.
        # This may result in more detailed module boundaries, but it may also increase the complexity of the analysis.
        # We leave this as an option for the user to decide.
        # -----
        if 1 == 0:
            x_paddedIndexes: "list[int]" = pad_indexes(
                x_final_module.dropna().index, x.index, n=1
            )

            x_final_module, y_final_module_within_x = x.where(
                x.index.isin(pd.Index(x_paddedIndexes))
            ), y.where(y.index.isin(pd.Index(x_paddedIndexes)))

        # -----
        # Handle the missing y data.
        # NB: Now we've potentially selected more y modules, we may have included some NaN values. These must be handled.
        handlerForNaNYValues: str = "do_nothing"

        if handlerForNaNYValues == "randomise":
            # Replace missing y modules with random values, but without affecting the distribution of y.
            _, _y_final_module_within_x_with_missing = white_noise(
                x=x_final_module.dropna(),
                y=y_final_module_within_x[
                    y_final_module_within_x.index.isin(x_final_module.dropna().index)
                ],
                sample_from_y=y.dropna(),
            )
            y_final_module_within_x_with_missing = cast(
                "Union[pd.Series[str],pd.Series[int]]",
                _y_final_module_within_x_with_missing,
            )
            y_final_module_within_x[y_final_module_within_x_with_missing.index] = (
                y_final_module_within_x_with_missing
            )
            pass
        elif "do_nothing":
            pass
        else:
            raise ValueError(
                f"Invalid handler for NaN Y values: {handlerForNaNYValues}"
            )

            # Get module centroid

        x_final_module_centroid: XYZDict
        y_final_module_within_x_centroid: XYZDict
        centroid_distance, x_final_module_centroid, y_final_module_within_x_centroid = (
            calculateEuclidianDistance(
                centroid_coords=centroid_coords,
                x=x_final_module,
                y=orig_y_module,
            )
        )

        if isinstance(x_final_module, pd.Series):
            if x_final_module.dtype == "object":
                x_final_module.fillna("missing-B", inplace=True)
                y_final_module_within_x.fillna("missing-B", inplace=True)
            elif pd.api.types.is_integer_dtype(x_final_module):
                x_final_module.fillna(-1, inplace=True)
                y_final_module_within_x.fillna(-1, inplace=True)
            else:
                raise ValueError(
                    f"Invalid data type for x_final_module: {x_final_module.dtype}"
                )
        else:
            raise ValueError(
                f"Invalid data type for x_final_module: {type(x_final_module)}"
            )

        # ------
        # Run tests for X as truth
        for test_name, test_func in test_functions_with_range:
            try:
                score_x_defined: Float = test_func(
                    x_final_module, y_final_module_within_x
                )

                y_probabilities: pd.Series[float] = y_final.value_counts(normalize=True)
                random_y = pd.Series(
                    g.randomGen.choice(
                        y_probabilities.index,
                        size=y_final_module_within_x.size,
                        p=y_probabilities.to_numpy(),
                    ),
                    index=y_final_module_within_x.index,
                ).astype(y_final_module_within_x.dtype)
                random_y.attrs = y_final_module_within_x.attrs

                score_x_imported_random_y: Float = test_func(
                    x_final_module,
                    random_y,
                )

                x_probabilities: pd.Series[float] = x_final.value_counts(normalize=True)
                random_x = pd.Series(
                    g.randomGen.choice(
                        x_probabilities.index,
                        size=x_final_module.size,
                        p=x_probabilities.to_numpy(),
                    ),
                    index=x_final_module.index,
                ).astype(x_final_module.dtype)
                random_x.attrs = x_final_module.attrs

                score_x_random_y_imported: Float = test_func(
                    random_x,
                    y_final_module_within_x,
                )

                results_x_truth_by_module.append(
                    (
                        config.TIMESTAMP_OF_SCRIPT,
                        config.CURRENT_SUBJECT,
                        allStepsAreSuccessful(),
                        config.CURRENT_HEMISPHERE,
                        config.CURRENT_TASK,
                        f"{datasetDescriptor}",
                        x_module_name,
                        y_module_name,
                        x_module_sa,
                        x_final_module.size,
                        y_module_sa,
                        orig_y_module.size,
                        ydivx_module_sa,
                        x_final_module_centroid,
                        y_final_module_within_x_centroid,
                        centroid_distance,
                        mappedMatrixScores[y_module_name]["norm_centroid_distance"],
                        mappedMatrixScores[y_module_name]["norm_cont"],
                        mappedMatrixScores[y_module_name]["norm_total_cost"],
                        f"{test_name} - X as Truth",
                        score_x_defined,
                        score_x_imported_random_y,
                        score_x_random_y_imported,
                        generateInterpretation(test_name, score_x_defined),
                        test_ranges[test_name],
                    )
                )
            except Exception as e:
                g.logger.warning(f"Warning running {test_name} with x as truth: {e}")

                # Run tests for Y as truth

            # Run tests for Y as truth

        # For demo purposes, make a timeline plot of random.
        plot_timeline(x_final_module, random_y, title="Real X, Random Y - perModule")
        plot_timeline(
            random_x, y_final_module_within_x, title="Random X, Real Y - perModule"
        )

        # Run tests for Y as truth
        for test_name, test_func in test_functions_with_range:
            try:
                score_y_defined = test_func(y_final_module_within_x, x_final_module)

                x_probabilities: pd.Series[float] = x_final.value_counts(normalize=True)
                random_x = pd.Series(
                    g.randomGen.choice(
                        x_probabilities.index,
                        size=x_final_module.size,
                        p=x_probabilities.to_numpy(),
                    ),
                    index=x_final_module.index,
                ).astype(x_final_module.dtype)
                random_x.attrs = x_final_module.attrs

                score_y_imported_random_x = test_func(y_final_module_within_x, random_x)

                y_probabilities: pd.Series[float] = y_final.value_counts(normalize=True)
                random_y = pd.Series(
                    g.randomGen.choice(
                        y_probabilities.index,
                        size=y_final_module_within_x.size,
                        p=y_probabilities.to_numpy(),
                    ),
                    index=y_final_module_within_x.index,
                ).astype(y_final_module_within_x.dtype)
                random_y.attrs = y_final_module_within_x.attrs

                score_y_random_x_imported = test_func(
                    random_y,
                    x_final_module,
                )

                results_y_truth_by_module.append(
                    (
                        config.TIMESTAMP_OF_SCRIPT,
                        config.CURRENT_SUBJECT,
                        allStepsAreSuccessful(),
                        config.CURRENT_HEMISPHERE,
                        config.CURRENT_TASK,
                        f"{datasetDescriptor}",
                        x_module_name,
                        y_module_name,
                        x_module_sa,
                        x_final_module.size,
                        y_module_sa,
                        orig_y_module.size,
                        ydivx_module_sa,
                        x_final_module_centroid,
                        y_final_module_within_x_centroid,
                        centroid_distance,
                        mappedMatrixScores[y_module_name]["norm_centroid_distance"],
                        mappedMatrixScores[y_module_name]["norm_cont"],
                        mappedMatrixScores[y_module_name]["norm_total_cost"],
                        f"{test_name} - Y as Truth",
                        score_y_defined,
                        score_y_imported_random_x,
                        score_y_random_x_imported,
                        generateInterpretation(test_name, score_y_defined),
                        test_ranges[test_name],
                    )
                )
            except Exception as e:
                g.logger.warning(f"Warning running {test_name} with y as truth: {e}")
                results_y_truth_by_module.append(
                    (
                        config.TIMESTAMP_OF_SCRIPT,
                        config.CURRENT_SUBJECT,
                        allStepsAreSuccessful(),
                        config.CURRENT_HEMISPHERE,
                        config.CURRENT_TASK,
                        f"{datasetDescriptor}",
                        x_module_name,
                        y_module_name,
                        x_module_sa,
                        x_final_module.size,
                        y_module_sa,
                        orig_y_module.size,
                        ydivx_module_sa,
                        {"x": 0, "y": 0, "z": 0},
                        {"x": 0, "y": 0, "z": 0},
                        np.nan,
                        np.nan,
                        np.nan,
                        np.nan,
                        f"{test_name} - failed",
                        np.nan,
                        np.nan,
                        np.nan,
                        generateInterpretation(test_name, np.nan),
                        test_ranges[test_name],
                    )
                )

        dfXTruthByModule, dfYTruthByModule = convertModuleWideResultsToDataFrames(
            results_x_truth_by_module, results_y_truth_by_module
        )

        save_results(dfXTruthByModule, dfYTruthByModule, config.STAT_FILE_BY_MODULE)
