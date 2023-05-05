from logging import Logger
import os
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
       self.fdRead, self.fdWrite = os.pipe()
       self.pipeReader = os.fdopen(self.fdRead)

    def __getattr__(self, attr: Any) -> Any:
        return getattr(self.terminal, attr)
     
    def write(self, buf: str) -> None:
       for line in buf.rstrip().splitlines():
          self.logger.info(line.rstrip())

    def run(self) -> None:
        """Run the thread, logging everything."""
        for line in iter(self.pipeReader.readline, ''):
            self.logger.info(line.strip('\n'))

        self.pipeReader.close()
        
    # def flush(self) -> None:
    #     pass
    def flush(self):
        if self.linebuf != '':
            self.logger.log(self.log_level, self.linebuf.rstrip())
        self.linebuf = ''