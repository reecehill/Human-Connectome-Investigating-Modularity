# This file is the starter file. It's steps include:

# 1) Configuring variables.
# 2) Confirming the environment.
# 3) Directing the pipeline.
# 4) Handling shell output.


# ------------------------------------------------------------
# [START] main()
# ------------------------------------------------------------

def main(user: str, host: str, pathToKey: str) -> None:
    try:
        from modules.logger.logger import LoggerClass
        from modules.saver.saver import SaverClass
        # ------------------------------------------------------------
        # [START] Check environment.
        # ------------------------------------------------------------

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
            saver = SaverClass(user, host, pathToKey)
        except Exception as e:
            raise e

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
            
            try:
              logger.info("Ready to begin accepting steps")
              
              # INSERT STEPS.

              # Test Save
              saver.upload(filesToSave=[logger.root.handlers[0].baseFilename]) # type: ignore
              logger.info("Script end")
            except Exception as e:
              logger.info(e)
              exit()

        except Exception as e:
            raise e
        # ------------------------------------------------------------
        # [END] Running pipeline.
        # ------------------------------------------------------------
    except Exception as e:
        print(e)
        exit()
# ------------------------------------------------------------
# [END] main()
# ------------------------------------------------------------

# ------------------------------------------------------------
# [START] save()
# ------------------------------------------------------------

def save() -> None:
    pass

# ------------------------------------------------------------
# [end] save()
# ------------------------------------------------------------

if __name__ == "__main__":
    try:
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument("user", type=str)
        parser.add_argument("host", type=str)
        parser.add_argument("pathToKey", type=str)
        args = parser.parse_args()
    except Exception as e:
        raise e
    main(args.user, args.host, args.pathToKey)
