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
import config

def main(user: str, host: str, pathToKey: str, startAFresh: bool = False) -> None:
    config.START_A_FRESH = startAFresh
    try:
        from modules.logger.logger import LoggerClass
        from modules.saver.saver import SaverClass
        from modules.file_directory.file_directory import deleteDirectories, createDirectories

        # ------------------------------------------------------------
        # [START] Check environment.
        # ------------------------------------------------------------
            # EMPTY
        # ------------------------------------------------------------
            # [END] Check environment.
        # ------------------------------------------------------------

        # ------------------------------------------------------------
        # [START] Load and run the global logger.
        # ------------------------------------------------------------
        try:
            g.logger = LoggerClass()
            g.logger = g.logger.run()

            # -- [START] LOGGER AVAILABLE 

            try:
                # ------------------------------------------------------------
                # Clear writeable folders from previous runs. (Optional)
                # ------------------------------------------------------------
                if (startAFresh):
                    deleteDirectories([config.UPLOADS_DIR.parent], ignoreErrors=True)
                    createDirectories(directoryPaths=[config.UPLOADS_DIR], createParents=True)
            except Exception as e:
                raise
            
           
            try:
                # ------------------------------------------------------------
                # [START] Load the global saver and upload current configuration.
                # ------------------------------------------------------------
                try:
                    g.saver = SaverClass(user, host, pathToKey)
                    compressedFiles: str = g.saver.compress(filePathsToCompress=[config.SCRIPTS_DIR / 'config.py', config.INCLUDES_DIR]) 
                    archivePath: Path = Path(compressedFiles).resolve(strict=True)
                    g.saver.saveToServer(archivePath) 
                except Exception:
                    raise

                # ------------------------------------------------------------
                # [START] Running pipeline.
                # Run each step in the pipeline. See each class "run" function for what occurs.
                # ------------------------------------------------------------
                try:
                    # getData()
                    # confirmData()
                    g.logger.info("Ready to begin accepting steps")

                    # Test Save #1
                    archive: str = g.saver.compress(filePathsToCompress=[config.LOGS_DIR]) 
                    archivePath: Path = Path(archive).resolve(strict=True)
                    g.saver.saveToServer(archivePath) 

                    # Test Save #2
                    archive: str = g.saver.compress(filePathsToCompress=[config.LOGS_DIR]) 
                    archivePath: Path = Path(archive).resolve(strict=True)
                    g.saver.saveToServer(archivePath) 
                    

                    g.logger.info("Script end")
                except:
                    raise
                # ------------------------------------------------------------
                # [END] Running pipeline.
                # ------------------------------------------------------------
            except Exception as e:
                g.logger.error("An error occurred", exc_info=e)
                exit()
            # -- [END] LOGGER AVAILABLE
            
        except Exception as e:
            print("There was an error instantiating the logger.")
            print(traceback.format_exc())
            exit()
        # ------------------------------------------------------------
            # [END] Initialize and run the logger.
        # ------------------------------------------------------------
    except Exception as e:
        print("Failed to import necessary modules.")
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
            parser.add_argument("-S", "--startAFresh", type=bool, default=False)
            args = parser.parse_args()
            user = args.user
            host = args.host
            pathToKey = args.pathToKey
            startAFresh = args.startAFresh
        else:
            import os
            from dotenv import load_dotenv
            k = load_dotenv(os.getcwd()+"/../.env")
            user = os.getenv('DEFAULT_USER') or "ENV_ERROR"
            host = os.getenv('DEFAULT_HOST') or "ENV_ERROR"
            pathToKey = os.getenv('DEFAULT_PATH_TO_KEY') or "ENV_ERROR"
            startAFresh = os.getenv('DEFAULT_START_A_FRESH') == 'True' or False

        print("Launching main using: ")
        print("User: "+user)
        print("Host: "+host)
        print("pathToKey: "+pathToKey)
        print("startAFresh: " + str(startAFresh))
        main(user, host, pathToKey, startAFresh)
    except Exception as e:
        print(e)
        raise
    
