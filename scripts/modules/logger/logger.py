from pathlib import Path
from typing import Any
import typing
try:
  import logging.config
  from logging import Logger 
  import config
  from parameters.logging_schema import logging_schema
  from ..file_directory.file_directory import deleteDirectories, createDirectories
except Exception as e:
  print(e)
  exit()

class LoggerClass:
  def __init__(self) -> None:
      self.folderPathsNeeded: "list[Path]" = [config.LOGS_DIR]
      #self.filePathsNeeded: list[Optional[str]] = []
      deleteDirectories(directoryPaths=self.folderPathsNeeded)
      createDirectories(directoryPaths=self.folderPathsNeeded, createParents=True, throwErrorIfExists=False)
    
  def run(self) -> typing.Union[Logger, Any]:
    # Set up a handler for both standard output stream and to output file.
    #targets = logging.StreamHandler(sys.stdout), logging.FileHandler(config.logFilePath)

    # Configure logging package to output only the message without the log level.
    #logging.basicConfig(format='%(message)s', level=logging.INFO, handlers=targets)
    logging.config.dictConfig(logging_schema)
    self.logger: Logger  = logging.getLogger(__name__)

    self.logger.info("Logger is instantiated.")
    self.logger.info("Logs are saved to: " + self.logger.root.handlers[0].baseFilename) # type: ignore
    
    return self.logger