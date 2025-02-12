from logging import Logger, LoggerAdapter
from logging.handlers import QueueHandler
from types import ModuleType
from typing import Any, Dict

# Annotate the global variable at the module level

extra_logging_info: "dict[str, str]" = {"ADDITIONAL": ""}


def initialize_pool(c1: Dict[str, Any], g1: Dict[str, Any]) -> None:
    global g
    import modules.globals as g
    from config import LOG_LEVEL
    from sys import modules

    if g.__name__ in modules:
        del modules[g.__name__]  # Remove any cached version

    import logging

    queued_logger: Logger = logging.getLogger("queued")
    queued_logger.addHandler(QueueHandler(queue=g1["log_queue"]))
    queued_logger.setLevel(LOG_LEVEL)
    logger_adapter: "LoggerAdapter[Logger]" = logging.LoggerAdapter(
        queued_logger, extra=extra_logging_info
    )
    g1["logger"] = logger_adapter

    # new_g = ModuleType(g.__name__)  # Create a new module
    for k, v in g1.items():  # Populate the module with attributes
        setattr(g, k, v)

    modules[g.__name__] = g  # Insert into modules
    # g = modules["modules.globals"]
    # globals()["g"] = modules["modules.globals"]
    # print(vars(g).values())

    # Initialize and inject 'config'
    print("Initialising config")

    global config
    config = modules["config"]

    if config.__name__ in modules:
        del modules[config.__name__]  # Remove any cached version
    # config = ModuleType(config.__name__)  # Create a new module
    for k, v in c1.items():  # Populate the module with attributes
        setattr(config, k, v)
    modules[config.__name__] = config  # Insert into modules.

    # g.queue_listener.start()
    g.logger.info("Process pool logger initialised.")
    pass
