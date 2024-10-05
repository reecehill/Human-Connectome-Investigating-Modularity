from typing import Optional, Tuple
import config
import pandas as pd
import modules.globals as g

def getPipelineSuccessStatus() -> dict[str, Tuple[Optional[bool], str]]:
  # Check if the file exists
  existing_success_dict: dict[str, Tuple[Optional[bool], str]]
  if not config.PIPELINE_SUCCESS_FILE.is_file():
    existing_success_dict = {
      stepFn.__name__: (None, "") for stepFn in g.allSteps.keys()}
  else:
    existing_success: pd.DataFrame = pd.read_csv(config.PIPELINE_SUCCESS_FILE)
    # Convert existing DataFrame to a dictionary for easier updating
    existing_success_dict = dict(
      zip(
        existing_success['Step'],
        zip(existing_success['Success'], existing_success['Last Modified']),
        )
      )

  return existing_success_dict

def updateStepSuccessStatus():
  existing_success_dict: dict[str, Tuple[Optional[bool], str]] = getPipelineSuccessStatus()
  # Update the existing dictionary with the new data
  
  existing_success_dict.update({ 
                                config.CURRENT_STEP: (config.SUBJECT_STEP_SUCCESS==True, config.TIMESTAMP_OF_SCRIPT)})

  # Convert the updated dictionary back into a DataFrame
  df_updated: pd.DataFrame = pd.DataFrame(
    [
        (step, success, last_modified)
        for step, (success, last_modified) in existing_success_dict.items()
    ],
    columns=['Step', 'Success', 'Last Modified']
    )

  # Save the updated DataFrame back to the CSV file, overwriting the old file
  df_updated.to_csv(config.PIPELINE_SUCCESS_FILE, index=False)

def allStepsAreSuccessful() -> bool:
  if not config.PIPELINE_SUCCESS_FILE.is_file():
    g.logger.info("No steps have actually been ran. Using data found on disk.")

  allStatuses: dict[str, Tuple[Optional[bool], str]] = getPipelineSuccessStatus()
  return all(status is True for status, _ in allStatuses.values())

def prevStepWasSuccessful() -> bool:
  existing_success_dict: dict[str, Tuple[Optional[bool], str]] = getPipelineSuccessStatus()
  allStepsList = [stepFn.__name__ for stepFn in g.allSteps.keys()]
  currentStepIndex = allStepsList.index(config.CURRENT_STEP)
  if currentStepIndex == 0:
    return True
  prevStepName = allStepsList[currentStepIndex - 1]
  prevStepStatus = existing_success_dict[prevStepName][0]
  return prevStepStatus is True