from logging import Logger
from typing import Callable, Dict
from modules.saver.saver import SaverClass


logger: Logger
saver: SaverClass
allSteps: Dict[Callable[[str], bool], bool] = {}