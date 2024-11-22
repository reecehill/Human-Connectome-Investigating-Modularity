from logging import LogRecord, Logger, LoggerAdapter
from logging.handlers import QueueListener
from multiprocessing import Queue
from pathlib import Path
from typing import Callable, Dict, Union
from modules.saver.saver import SaverClass
from numpy.random import default_rng

logger: "LoggerAdapter[Logger]"
log_queue: "Queue[Union[LogRecord,None]]"
queue_listener: "QueueListener"
saver: SaverClass
allSteps: "Dict[Callable[[str], bool], bool]" = {}
downloadedFiles: "list[Path]" = []
randomGen = default_rng()
