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
from subprocess import Popen, PIPE
from traceback import format_exc
from typing import Any
import modules.globals as g
from modules.saver.streamToLogger import StreamToLogger
from config import BASE_DIR
def main(user: str, host: str, pathToKey: str, startAFresh: bool = False) -> None:
    import config
    config.START_A_FRESH = startAFresh
    try:
        from modules.logger.logger import LoggerClass
        from modules.saver.saver import SaverClass
        from modules.file_directory.file_directory import deleteDirectories, createDirectories
        import modules.pipeline.pipeline as pipeline

        # ------------------------------------------------------------
        # [START] Load and run the global logger.
        # ------------------------------------------------------------
        try:
            g.logger = LoggerClass()
            g.logger = g.logger.run()

            # -- [START] LOGGER AVAILABLE 

            # ------------------------------------------------------------
            # [START] Check environment.
            # ------------------------------------------------------------
            if(True == False):
                try:
                    # Check pyprocess works.
                    cmd1 = f"cd {(config.SCRIPTS_DIR / 'src' / 'pypreprocess' / 'examples' / 'easy_start').resolve(strict=True).__str__()}"
                    cmd1 = 'python -c "import nipype; print(nipype.__version__)"'
                    cmd2 = 'python -c "import nipype; nipype.test()"'
                    cmd3 = "python nipype_preproc_spm_auditory.py"
                    check: Popen[Any] = Popen("{}; {}; {}".format(cmd1, cmd2, cmd3),
                                            shell=True,
                                            stdin=PIPE, # type: ignore
                                            stdout=StreamToLogger(g.logger, 20), # type: ignore
                                            stderr=StreamToLogger(g.logger, 50), # type: ignore
                                            close_fds=True)
                    
                    if(check is not 0):
                        g.logger.info("There was a problem finding the SPM12 installation.")
                        Popen([". continuous_integration/install_spm12.sh"])
                except Exception as e:
                    raise
            # Ensure pyprocess has its SPM12 pre-compiled version of the programme installed.
            # Popen([". continuous_integration/install_spm12.sh"])
            
            # ------------------------------------------------------------
                # [END] Check environment.
            # ------------------------------------------------------------
        
            try:
                # ------------------------------------------------------------
                # Clear writeable folders from previous runs. (Optional)
                # ------------------------------------------------------------
                if (startAFresh):
                    g.logger.info("Deleting uploads ?and data folder? from previous runs.")
                    deleteDirectories([config.UPLOADS_DIR.parent,
                                       config.DATA_DIR
                                       ], ignoreErrors=True)

                    g.logger.info("Creating uploads ?and data? folder.")
                    createDirectories(directoryPaths=[config.UPLOADS_DIR,
                                                      config.DATA_DIR
                                                      ], createParents=True)
            except Exception as e:
                raise
            
           
            try:
                # ------------------------------------------------------------
                # [START] Load the global saver and upload current configuration.
                # ------------------------------------------------------------
                try:
                    g.logger.info("Instantiating saver class...")
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
                    g.logger.info("Ready to begin accepting steps")
                    pipeline.runPipeline()
                    g.logger.info("Pipeline scripts finished.")
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
            print(format_exc())
            exit()
        # ------------------------------------------------------------
            # [END] Initialize and run the logger.
        # ------------------------------------------------------------
    except Exception as e:
        print("Failed to import necessary modules.")
        print(format_exc())
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
            from argparse import ArgumentParser
            parser = ArgumentParser()
            parser.add_argument("-U", "--user", type=str, default="CLI_ARGUMENT_ERROR")
            parser.add_argument("-H", "--host", type=str, default="CLI_ARGUMENT_ERROR")
            parser.add_argument("-K", "--pathToKey", type=str, default="CLI_ARGUMENT_ERROR")
            parser.add_argument("-S", "--startAFresh", type=bool, default=False)
            parser.add_argument("-A", "--awsConfigFile", type=bool, default="CLI_ARGUMENT_ERROR")
            args = parser.parse_args()
            user = args.user
            host = args.host
            pathToKey = args.pathToKey
            startAFresh = args.startAFresh
        else:
            from os import getenv
            from dotenv import load_dotenv
            k = load_dotenv(str(BASE_DIR / '.env'))
            user = getenv('DEFAULT_USER') or "ENV_ERROR"
            host = getenv('DEFAULT_HOST') or "ENV_ERROR"
            pathToKey = getenv('DEFAULT_PATH_TO_KEY') or "ENV_ERROR"
            startAFresh = getenv('DEFAULT_START_A_FRESH') == 'True' or False

        print("Launching main using: ")
        print("User: "+user)
        print("Host: "+host)
        print("pathToKey: "+pathToKey)
        print("startAFresh: " + str(startAFresh))
        main(user, host, pathToKey, startAFresh)
    except Exception as e:
        print(e)
        raise
    
