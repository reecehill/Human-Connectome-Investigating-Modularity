# This file is the starter file. It's steps include:

# 1) Configuring variables.
# 2) Confirming the environment.
# 3) Directing the pipeline.
# 4) Handling shell output.
from modules.logger.logger import LoggerClass

# ----------
# [START] Initializing.
# Initialize each step in the pipeline. This includes:
# 1) Clearing writeable folders.
# 2) Ensuring new filepaths and files are made where necessary.
# ----------
logger = LoggerClass()

# --------
# [END] Initializing.
# --------

# ----------
# [START] Running pipeline.
# Run each step in the pipeline. See each class "run" function for what occurs.
# ----------

# Get logger instance
logger = logger.run()
logger.info("Logger is instantiated.")
logger.info("Beginning script now.")



# --------
# [END] Running pipeline.
# --------