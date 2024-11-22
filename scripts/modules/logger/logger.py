from logging.handlers import QueueListener
from pathlib import Path
from typing import Any, Tuple, Union
import boto3

try:
    from shutil import copy
    import logging.config
    from logging import Logger, LoggerAdapter
    import config
    from includes.logging_schema import logging_schema
    from ..file_directory.file_directory import createDirectories
    from multiprocessing import Manager
    from queue import Queue as Queue
    from logging import LogRecord, Logger
    from logging.handlers import QueueListener, QueueHandler


except Exception as e:
    print(e)
    exit()

extra_logging_info: "dict[str, str]" = {"ADDITIONAL": ""}


class LoggerClass:
    def __init__(self) -> None:

        self.logger: "LoggerAdapter[Logger]"
        self.log_queue: "Queue[Any]"
        self.folderPathsNeeded: "list[Path]" = [config.LOGS_DIR]
        # self.filePathsNeeded: "list[Optional[str]]"" = []
        # deleteDirectories(directoryPaths=[self.folderPathsNeeded[0].parent])
        createDirectories(
            directoryPaths=self.folderPathsNeeded,
            createParents=True,
            throwErrorIfExists=False,
        )

    def run(self) -> "Tuple[LoggerAdapter[Logger], Queue[Any]]":

        def configureBoto3Logs(log_queue: "Queue[Union[LogRecord,None]]") -> None:
            boto3_logger = logging.getLogger("boto3")
            boto3_logger.addHandler(QueueHandler(log_queue))
            boto3_adapter: "LoggerAdapter[Logger]" = logging.LoggerAdapter(
            boto3_logger, extra=extra_logging_info
            )
            boto3_logger = logging.getLogger("boto3")

            boto3_logger = logging.getLogger("botocore")
            boto3.set_stream_logger()
            # boto3_logger.addHandler(QueueHandler(log_queue))
        logging.config.dictConfig(logging_schema)

        self.log_queue = Manager().Queue()

        # Set up a handler for both standard output stream and to output file.
        # targets = logging.StreamHandler(sys.stdout), logging.FileHandler(config.logFilePath)

        # Configure logging package to output only the message without the log level.
        # logging.basicConfig(format='%(message)s', level=logging.INFO, handlers=targets)
        # logging.config.dictConfig(logging_schema)

        logger_nocontext: Logger = logging.getLogger("queued")

        # multiprocessing_logging.install_mp_handler(logger=logger_nocontext)

        queue_handler = QueueHandler(self.log_queue)
        logger_nocontext.addHandler(queue_handler)
        logger_nocontext.setLevel(logging.INFO)

        logger_nocontext_adapter: "LoggerAdapter[Logger]" = logging.LoggerAdapter(
            logger_nocontext, extra=extra_logging_info
        )
        self.logger = logger_nocontext_adapter
        self.logger.info("Logger is instantiated.")
        self.logger.error("Logger is instantiated.")
        self.logger.info("Logs are saved to: " + config.LOGS_DIR.__str__())
        copy(config.SCRIPTS_DIR / "config.py", config.LOGS_DIR / "config.py")
        self.logger.info(
            "A copy of parameters are saved to: " + config.LOGS_DIR.__str__()
        )
        return self.logger, self.log_queue


def config_root_logger(log_queue: "Queue[Union[LogRecord,None]]") -> QueueListener:
    # Set up the root logger to process the queue
    root_logger: Logger = logging.getLogger("root_logger")

    logger_adapter: "LoggerAdapter[Logger]" = logging.LoggerAdapter(
        root_logger, extra=extra_logging_info
    )

    queue_listener: "QueueListener" = QueueListener(log_queue, *logger_adapter.logger.handlers)

    return queue_listener

def stop_root_logger(listener: QueueListener):
    # Stop the listener when done
    listener.enqueue_sentinel()
    listener.stop()