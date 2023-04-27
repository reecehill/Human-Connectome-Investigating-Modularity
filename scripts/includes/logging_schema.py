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
        # Formatter Name
        "standard": {
            # class is always "logging.Formatter"
            "class": "logging.Formatter",
            # Optional: logging output format
            "format": " '%(asctime)s [%(filename)s:%(module)s:%(funcName)s:%(lineno)d] %(levelname)-8s %(message)s'",
            # Optional: asctime format
            "datefmt": "%d %b %y %H:%M:%S"
        }
    },
    # Handlers use the formatter names declared above
    "handlers": {
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
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "standard",
            "level": "INFO",
            "filename": LOGS_DIR / "log.txt",
            "mode": "w",
            "encoding": "utf-8",
            "maxBytes": 500000,
            "backupCount": 4
        }
    },
    # Loggers use the handler names declared above
    "loggers": {
        "__main__": {  # if __name__ == "__main__"
            # Use a list even if one handler is used
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": True
        },
        "boto3": {
            "level": "INFO",
            "handlers": ["console", "file"],
            "propagate": True,
        },
        "botocore": {
            "level": "INFO",
            "handlers": ["console", "file"],
            "propagate": True,
        },
        "nose": {
            "level": "INFO",
            "handlers": ["console", "file"],
            "propagate": True,
        }
    },
    # Just a standalone kwarg for the root logger
    "root": {
        "level": "DEBUG",
        "handlers": ["file", "console"]
    }
}


# ----------
# [END] Logging schema.
# ----------
