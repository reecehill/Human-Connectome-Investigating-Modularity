from typing import Dict, Optional, Tuple, Union
import pandas as pd
import config
import modules.globals as g


def getPipelineSuccessStatus() -> "Dict[str, Tuple[Optional[bool], str]]":
    """
    The function `getPipelineSuccessStatus` reads a CSV file containing pipeline success statuses and
    returns a dictionary mapping step names to tuples of success status and last modified timestamp.
    :return: A dictionary is being returned where the keys are the names of pipeline steps and the
    values are tuples containing the success status (a boolean or None) and the last modified timestamp
    as a string.
    """
    # Check if the file exists
    existing_success_dict: "dict[str, Tuple[Optional[bool], str]]"
    if not config.PIPELINE_SUCCESS_FILE.is_file():
        existing_success_dict = {
            stepFn.__name__: (None, "") for stepFn in g.allSteps.keys()
        }
    else:
        existing_success: pd.DataFrame = pd.read_csv(config.PIPELINE_SUCCESS_FILE)
        # Convert existing DataFrame to a dictionary for easier updating
        existing_success_dict = dict(
            zip(
                existing_success["Step"],
                zip(existing_success["Success"], existing_success["Last Modified"]),
            )
        )

    return existing_success_dict


def updateStepSuccessStatus():
    existing_success_dict: "dict[str,Tuple[Optional[bool], str]]" = (
        getPipelineSuccessStatus()
    )
    # Update the existing dictionary with the new data

    existing_success_dict.update(
        {
            config.CURRENT_STEP: (
                config.SUBJECT_STEP_SUCCESS == True,
                config.TIMESTAMP_OF_SCRIPT,
            )
        }
    )

    # Convert the updated dictionary back into a DataFrame
    df_updated: pd.DataFrame = pd.DataFrame(
        [
            (step, success, last_modified)
            for step, (success, last_modified) in existing_success_dict.items()
        ],
        columns=["Step", "Success", "Last Modified"],
    )
    # Save the updated DataFrame back to the CSV file, overwriting the old file
    df_updated.to_csv(config.PIPELINE_SUCCESS_FILE, index=False)


def allStepsAreSuccessful() -> bool:
    if not config.PIPELINE_SUCCESS_FILE.is_file():
        g.logger.info("No steps have actually been ran. Using data found on disk.")

    allStatuses: "dict[str, Tuple[Optional[bool], str]]" = getPipelineSuccessStatus()
    return all(status is True for status, _ in allStatuses.values())


def prevStepWasSuccessful() -> bool:
    existing_success_dict: "dict[str, Tuple[Optional[bool], str]]" = (
        getPipelineSuccessStatus()
    )
    allStepsList = [stepFn.__name__ for stepFn in g.allSteps.keys()]
    currentStepIndex = allStepsList.index(config.CURRENT_STEP)
    if currentStepIndex == 0:
        return True
    prevStepName = allStepsList[currentStepIndex - 1]
    prevStepStatus = existing_success_dict[prevStepName][0]
    return prevStepStatus is True


def getPipelineSuccessStatusForSubjects(
    subjects: list[str] = config.ALL_SUBJECTS,
) -> "Dict[str, Dict[str, Tuple[Optional[bool], str]]]":
    """
    This function will collect the pipeline success status for all subjects
    and return it as a dictionary of dictionaries.

    """
    all_subjects_success_dict: "Dict[str,Dict[str, Tuple[Optional[bool], str]]]" = {}
    subject_success_dict: "Dict[str, Tuple[Optional[bool], str]]" = {}

    # Loop over all subjects to get their pipeline success status
    for subjectId in subjects:
        # Check if the subject's file exists
        file_path = config.SUBJECTS_DIR / subjectId / "pipeline_success.csv"

        if not file_path.exists():
            g.logger.info(
                "The pipeline success file for subject {subjectId} does not yet exist. Subject assumed to have not been run."
            )
            subject_success_dict = {
                stepFn.__name__: (None, "") for stepFn in g.allSteps.keys()
            }
        else:
            # Read the CSV for the subject and convert it into a dictionary
            existing_success: pd.DataFrame = pd.read_csv(file_path)
            subject_success_dict = dict(
                zip(
                    existing_success["Step"],
                    zip(existing_success["Success"], existing_success["Last Modified"]),
                )
            )

        # Store the subject's success dictionary in the master dictionary
        all_subjects_success_dict[subjectId] = subject_success_dict
    return all_subjects_success_dict


def updateBatchStatus(batchSubjects: list[str]) -> bool:
    all_subjects_success_dict: "Dict[str, Dict[str, Tuple[Optional[bool], str]]]" = (
        getPipelineSuccessStatusForSubjects(subjects=batchSubjects)
    )

    # Step 1: Flatten the dictionary for each subject into a format Pandas can handle more easily
    flattened_data: "Dict[str, Dict[str, Optional[Union[bool, str]]]]" = {}
    for subject_id, steps_dict in all_subjects_success_dict.items():
        flattened_data[subject_id] = {}
        for step, (status, last_modified) in steps_dict.items():
            flattened_data[subject_id][f"{step}_status"] = status
            flattened_data[subject_id][f"{step}_last_modified"] = last_modified

    # Step 2: Convert to a Pandas DataFrame
    df: pd.DataFrame = pd.DataFrame.from_dict(
        flattened_data, orient="index"
    ).reset_index()

    # Step 3: Rename 'index' column to 'subjectId'
    df.rename(columns={"index": "subjectId"}, inplace=True)

    # Step 4: Add a column that checks if all steps ()'_status' columns) are True
    status_columns: "list[str]" = [
        f"{col.__name__}_status" for col in g.allSteps.keys()
    ]
    df["allSteps_success"] = (
        df[status_columns].fillna(value=False).all(axis="columns", skipna=False)
    )
    df["allSteps_last_modified"] = config.TIMESTAMP_OF_SCRIPT

    allSubjectsAllStepsSuccess: bool = df["allSteps_success"].all()
    # Step 5: Export the DataFrame to a CSV file
    df.to_csv(config.BATCH_SUCCESS_FILE, index=False)

    return allSubjectsAllStepsSuccess
