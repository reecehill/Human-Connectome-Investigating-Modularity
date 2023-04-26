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
import subprocess
import traceback
from typing import Any
import modules.globals as g
from .modules.saver.streamToLogger import StreamToLogger

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
            try:
                # Check pyprocess works.
                cmd1 = f"cd {(config.SCRIPTS_DIR / 'src' / 'pypreprocess' / 'examples' / 'easy_start').resolve(strict=True).__str__()}"
                cmd1 = 'python -c "import nipype; print(nipype.__version__)"'
                cmd2 = 'python -c "import nipype; nipype.test()"'
                cmd3 = "python nipype_preproc_spm_auditory.py"
                check: subprocess.Popen[Any] = subprocess.Popen("{}; {}; {}".format(cmd1, cmd2, cmd3),
                                         shell=True,
                                         stdin=subprocess.PIPE, # type: ignore
                                         stdout=StreamToLogger(g.logger, 20), # type: ignore
                                         stderr=StreamToLogger(g.logger, 50), # type: ignore
                                         close_fds=True)
                
                if(check is not 0):
                    g.logger.info("There was a problem finding the SPM12 installation.")
                    subprocess.Popen([". continuous_integration/install_spm12.sh"])
            except Exception as e:
                raise
            # Ensure pyprocess has its SPM12 pre-compiled version of the programme installed.
            # subprocess.popen([". continuous_integration/install_spm12.sh"])
            
            # ------------------------------------------------------------
                # [END] Check environment.
            # ------------------------------------------------------------
        
            try:
                # ------------------------------------------------------------
                # Clear writeable folders from previous runs. (Optional)
                # ------------------------------------------------------------
                if (startAFresh):
                    deleteDirectories([config.UPLOADS_DIR.parent, config.DATA_DIR], ignoreErrors=False)
                    createDirectories(directoryPaths=[config.UPLOADS_DIR, config.DATA_DIR], createParents=True)
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
                    # (1) RETRIEVE BRAIN SCAN TREE DIRECTORY.
                    pipeline.getData()

                    # (2) PREPROCESSING DATA
                    pipeline.preprocessData()
                    
                    
                    #for i in ['sub-01', 'sub-02', 'sub-04', 'sub-05', 'sub-06', 'sub-07', 'sub-08', 'sub-09', 'sub-11', 'sub-12', 'sub-13', 'sub-14', 'sub-15']:
                    for i in ['sub-01']:
                        file = (config.DATA_DIR / 'ds002685' / i / 'ses-00' / 'anat' / f"{i}_ses-00_" "acq-tse_T2w" ".nii.gz").__str__()
                        downloader.downloadFile(file)
                        
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
            parser.add_argument("-A", "--awsConfigFile", type=bool, default="CLI_ARGUMENT_ERROR")
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
    
