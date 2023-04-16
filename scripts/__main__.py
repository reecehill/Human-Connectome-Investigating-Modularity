# This file is the starter file. It's steps include:

# 1) Configuring variables.
# 2) Confirming the environment.
# 3) Directing the pipeline.
# 4) Handling shell output.


# ------------------------------------------------------------
# [START] main()
# ------------------------------------------------------------
def main() -> None:
    try:
        from modules.logger.logger import LoggerClass

        # ------------------------------------------------------------
        # [START] Check environment.
        # ------------------------------------------------------------
        try:
            pass
        except Exception as e:
            print(e)
            exit()
        # ------------------------------------------------------------
            # [END] Check environment.
        # ------------------------------------------------------------

        # ------------------------------------------------------------
        # [START] Initializing.
        # Initialize each step in the pipeline. This includes:
        # 1) Clearing writeable folders.
        # 2) Ensuring new filepaths and files are made where necessary.
        # 3) Check that included modules are available on the system.
        # ------------------------------------------------------------
        try:
            logger = LoggerClass()
        except Exception as e:
            print(e)
            exit()

        # ------------------------------------------------------------
        # [END] Initializing.
        # ------------------------------------------------------------

        # ------------------------------------------------------------
        # [START] Running pipeline.
        # Run each step in the pipeline. See each class "run" function for what occurs.
        # ------------------------------------------------------------

        try:
            # ********
            # LOAD THE LOGGER
            # ********
            logger = logger.run()
            logger.info("Logger ran successfully.")

            # After this point, the logger is loaded so we can use this for improved logging.
            # From here, logs are shown both in-console and file.

        except Exception as e:
            print(e)
            exit()
        # ------------------------------------------------------------
        # [END] Running pipeline.
        # ------------------------------------------------------------
    except Exception as e:
        print(e)
        exit()
# ------------------------------------------------------------
# [END] main()
# ------------------------------------------------------------

if __name__ == "__main__":
    main()
