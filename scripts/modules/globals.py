from logging import Logger, LoggerAdapter
from pathlib import Path
from typing import Callable, Dict
from modules.saver.saver import SaverClass


logger: LoggerAdapter[Logger]
saver: SaverClass
allSteps: Dict[Callable[[str], bool], bool] = {}
downloadedFiles: list[Path] = []