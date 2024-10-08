from pathlib import Path

try:
  from shutil import copy
  import logging.config
  from logging import Logger, LoggerAdapter 
  import config
  from includes.logging_schema import logging_schema
  from ..file_directory.file_directory import createDirectories
  import multiprocessing_logging

except Exception as e:
  print(e)
  exit()

extra_logging_info: dict[str, str] = {'ADDITIONAL': ''}

class LoggerClass:
  def __init__(self) -> None:
      self.logger: Logger
      self.folderPathsNeeded: "list[Path]" = [config.LOGS_DIR]
      #self.filePathsNeeded: "list[Optional[str]]"" = []
      # deleteDirectories(directoryPaths=[self.folderPathsNeeded[0].parent])
      createDirectories(directoryPaths=self.folderPathsNeeded, createParents=True, throwErrorIfExists=False)
    
  def run(self) -> Logger:
    # Set up a handler for both standard output stream and to output file.
    #targets = logging.StreamHandler(sys.stdout), logging.FileHandler(config.logFilePath)

    # Configure logging package to output only the message without the log level.
    #logging.basicConfig(format='%(message)s', level=logging.INFO, handlers=targets)
    logging.config.dictConfig(logging_schema)
    logger = logging.getLogger(__name__)
    multiprocessing_logging.install_mp_handler(logger)
    logger = LoggerAdapter(logger, extra_logging_info)
    self.logger = logger # type: ignore
    self.logger.info("Logger is instantiated.")
    self.logger.error("Logger is instantiated.")
    self.logger.info("Logs are saved to: " + config.LOGS_DIR.__str__())
    copy(config.SCRIPTS_DIR / "config.py", config.LOGS_DIR / "config.py")
    self.logger.info("A copy of parameters are saved to: " + config.LOGS_DIR.__str__())
    return self.logger