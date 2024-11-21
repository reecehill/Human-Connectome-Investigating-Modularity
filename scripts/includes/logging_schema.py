# ----------
# [START] Logging schema, taken from:
# https://stackoverflow.com/questions/7507825/where-is-a-complete-example-of-logging-config-dictconfig
# ----------
from config import LOGS_DIR

logging_schema = {
    # Always 1. Schema versioning may be added in a future release of logging
    "version": 1,
    # "Name of formatter" : {Formatter Config Dict}
    "formatters": {
        "simple": {
            "format": "'%(asctime)s [%(filename)s:%(module)s:%(funcName)s:%(lineno)d] %(levelname)-8s %(message)s'"
        },
        # Formatter Name
        "standard": {
            # class is always "logging.Formatter"
            "class": "logging.Formatter",
            # Optional: logging output format
            "format": "'%(asctime)s [%(filename)s:%(module)s:%(funcName)s:%(lineno)d] %(ADDITIONAL)s %(levelname)-8s %(message)s'",
            # Optional: asctime format
            "datefmt": "%d %b %y %H:%M:%S"
        }
    },
    # Handlers use the formatter names declared above
    "handlers": {
        # Name of handler
        "console_simple": {
            # The class of logger. A mixture of logging.config.dictConfig() and
            # logger class-specific keyword arguments (kwargs) are passed in here.
            "class": "logging.StreamHandler",
            # This is the formatter name declared above
            "formatter": "simple",
            "level": "DEBUG",
            # The default is stderr
            "stream": "ext://sys.stdout"
        },
        # Name of handler
        "console": {
            # The class of logger. A mixture of logging.config.dictConfig() and
            # logger class-specific keyword arguments (kwargs) are passed in here.
            "class": "logging.StreamHandler",
            # This is the formatter name declared above
            "formatter": "standard",
            "level": "DEBUG",
            # The default is stderr
            "stream": "ext://sys.stdout"
        },
        # Same as the StreamHandler example above, but with different
        # handler-specific kwargs.
        "file_simple": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "simple",
            "level": "INFO",
            "filename": LOGS_DIR / "log-simple.txt",
            "mode": "a",
            "encoding": "utf-8",
            "maxBytes": 500000,
            "backupCount": 500
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "standard",
            "level": "INFO",
            "filename": LOGS_DIR / "log.txt",
            "mode": "a",
            "encoding": "utf-8",
            "maxBytes": 500000,
            "backupCount": 500
        }
    },
    # Loggers use the handler names declared above
    "loggers": {
        "modules.logger.logger": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": True
        },
        "__main__": {  # if __name__ == "__main__"
            # Use a list even if one handler is used
            "handlers": ["console_simple", "file_simple"],
            "level": "INFO",
            "propagate": True
        },
        "boto3": {
            "level": "INFO",
            "handlers": ["console_simple", "file_simple"],
            "propagate": True,
        },
        "botocore": {
            "level": "INFO",
            "handlers": ["console_simple", "file_simple"],
            "propagate": True,
        },
        "nose": {
            "level": "INFO",
            "handlers": ["console_simple", "file_simple"],
            "propagate": True,
        }
    },
    # Just a standalone kwarg for the root logger
    "root": {
        "level": "INFO",
        "handlers": ["file_simple", "console_simple"]
    }
}


# ----------
# [END] Logging schema.
# ----------
