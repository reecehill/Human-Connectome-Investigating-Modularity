# This file is the starter file. It's steps include:

# 1) Configuring variables.
# 2) Confirming the environment.
# 3) Directing the pipeline.
# 4) Handling shell output.

# NOTE: We make logger and saver global (by prefixing g. and importing modules.globals)

# ------------------------------------------------------------
# [START] main()
# ------------------------------------------------------------
from pathlib import Path
import traceback
import modules.globals as g

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
        # [START] Load and run the global logger.
        # ------------------------------------------------------------
        try:
            g.logger = LoggerClass()
            g.logger = g.logger.run()
            # From here, logs are shown both in-console and files


            # ------------------------------------------------------------
            # [START] Initializing.
            # Initialize each step in the pipeline. This includes:
            # 1) Clearing writeable folders.
            # 2) Ensuring new filepaths and files are made where necessary.
            # 3) Check that included modules are available on the system.
            # ------------------------------------------------------------
            try:
                g.saver = SaverClass(user, host, pathToKey)
            except Exception:
                raise
            # ------------------------------------------------------------
            # [END] Initializing.
            # ------------------------------------------------------------

            # ------------------------------------------------------------
            # [START] Running pipeline.
            # Run each step in the pipeline. See each class "run" function for what occurs.
            # ------------------------------------------------------------
            g.logger.info("Ready to begin accepting steps") # type: ignore

            # Test Save
            archive: Path = g.saver.compress(filePathsToCompress=[g.logger.root.handlers[0].baseFilename]) # type: ignore
            archive: Path = Path(archive).resolve(strict=True)
            g.saver.rsync(archive)
            

            g.logger.info("Script end") # type: ignore
            # ------------------------------------------------------------
            # [END] Running pipeline.
            # ------------------------------------------------------------
            
        except Exception as e:
            if hasattr(g.logger, 'exception'):
                g.logger.exception(e, stack_info=True) # type: ignore
            else:
                print(traceback.format_exc())
                exit()
        # ------------------------------------------------------------
            # [END] Initialize and run the logger.
        # ------------------------------------------------------------
    except Exception as e:
        print(traceback.format_exc())
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
        import sys
        if len( sys.argv ) > 1:
            import argparse
            parser = argparse.ArgumentParser()
            parser.add_argument("-U", "--user", type=str, default="CLI_ARGUMENT_ERROR")
            parser.add_argument("-H", "--host", type=str, default="CLI_ARGUMENT_ERROR")
            parser.add_argument("-K", "--pathToKey", type=str, default="CLI_ARGUMENT_ERROR")
            args = parser.parse_args()
            user = args.user
            host = args.host
            pathToKey = args.pathToKey
        else:
            import os
            from dotenv import load_dotenv
            k = load_dotenv(os.getcwd()+"/../.env")
            user = os.getenv('DEFAULT_USER') or "ENV_ERROR"
            host = os.getenv('DEFAULT_HOST') or "ENV_ERROR"
            pathToKey = os.getenv('DEFAULT_PATH_TO_KEY') or "ENV_ERROR"

        print("Launching main using: ")
        print("User: "+user)
        print("Host: "+host)
        print("pathToKey: "+pathToKey)
        main(user, host, pathToKey)
    except Exception as e:
        raise
    