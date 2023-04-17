from logging import Logger
import sys
from typing import Any

class StreamToLogger(object):
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """
    def __init__(self, logger: Logger, level: int=20) -> None:
       self.logger: Logger = logger
       self.terminal = sys.stdout
       self.level: int = level
       self.linebuf: str = ''

    def __getattr__(self, attr: Any) -> Any:
        return getattr(self.terminal, attr)
     
    def write(self, buf: str) -> None:
       for line in buf.rstrip().splitlines():
          self.logger.info(line.rstrip())

    def flush(self) -> None:
        pass