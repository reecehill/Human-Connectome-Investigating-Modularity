from pathlib import Path
from pandas import DataFrame
from typing import Optional, Union


def read_csv(file_path: Union[str, Path], delimiter: Optional[str] = ",") -> DataFrame:
    """
    Reads a CSV file into a pandas DataFrame.

    Parameters:
    - file_path (str): Path to the CSV file.
    - delimiter (Optional[str]): Delimiter used in the CSV file. Defaults to ','.

    Returns:
    - pd.DataFrame: The DataFrame containing the data from the CSV file.
    """
    try:
        from pandas import read_csv

        df: DataFrame = read_csv(file_path, delimiter=delimiter)
        print(f"Successfully loaded data from {file_path}. Shape: {df.shape}")
        return df
    except Exception as e:
        print(f"Error reading the CSV file: {e}")
        raise
