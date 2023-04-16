from logging import Logger
from typing import Optional
import config
from parameters.logging_schema import logging_schema
import logging.config
from ..file_directory.file_directory import deleteDirectories, createDirectories

class LoggerClass:
  def __init__(self) -> None:
      self.folderPathsNeeded: list[Optional[str]] = [config.logDirectoryPath]
      self.filePathsNeeded: list[Optional[str]] = ["added1"]
      deleteDirectories(directoryPaths=self.folderPathsNeeded)
      createDirectories(directoryPaths=self.folderPathsNeeded, createParents=True, throwErrorIfExists=False)
    
  def run(self) -> Logger:
    # Set up a handler for both standard output stream and to output file.
    #targets = logging.StreamHandler(sys.stdout), logging.FileHandler(config.logFilePath)

    # Configure logging package to output only the message without the log level.
    #logging.basicConfig(format='%(message)s', level=logging.INFO, handlers=targets)
    
    logging.config.dictConfig(logging_schema) # type: ignore
    self.logger  = logging.getLogger(__name__)
    return self.logger