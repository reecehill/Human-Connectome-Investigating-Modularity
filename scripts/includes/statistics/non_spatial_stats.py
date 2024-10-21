# Re-importing necessary libraries and preparing data again
from enum import unique
import numpy as np
import numpy.typing as npt
import modules.globals as g
import pandas as pd
import config
from includes.statistics.perSubjectStat import perModuleStat, perSubjectStat
from pathlib import Path
from includes.statistics.utils import convertNumericalModulesToWords
from includes.statistics.clean_data import clean_data


def runTests(subjectId: str, pathToXCsv: Path, pathToYCsv: Path) -> bool:
    result = False
    try:

        x_raw: pd.DataFrame = pd.read_csv(pathToXCsv.absolute(
        ).__str__(), sep=',', header=None, keep_default_na=True).T
        y_raw: pd.DataFrame = pd.read_csv(pathToYCsv.absolute(
        ).__str__(), sep=',', header=None, keep_default_na=True).T

        xy_surface_area: pd.DataFrame = pd.read_csv((pathToXCsv.parent.parent / 'face_surface_areas' / f'{config.CURRENT_HEMISPHERE}_sa_by_face.csv').absolute(
        ).__str__(), sep=',', header=None, keep_default_na=True).T

        x: "pd.Series[int]" = x_raw[0]
        y: "pd.Series[int]" = y_raw[0]

        # Mask, or smoothed module names.
        x_clean, y_clean = clean_data(nan_handler="filter_by_parent", x=x, y=y)

        # For absolute confidence that Python is not converting strings to integers, convert labels to random words.
        x_final, y_final = convertNumericalModulesToWords(x_clean, y_clean)
        # x_final, y_final = (x_clean, y_clean)

        perSubjectStat(x_final, y_final)
        perModuleStat(x_final, y_final, x, y, xy_surface_area)
        
        result: bool = True
    except Exception as e:
        result = False
        if (f'{e}' == 'index 4274 is out of bounds for axis 0 with size 4274'):
            pass
        g.logger.error(f"Error whilst running stats - {e}")
        raise e
    finally:
        return result
