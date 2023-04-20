from pathlib import Path
import shutil
from typing import Any, Optional
import subprocess
from modules.saver.streamToLogger import StreamToLogger

import modules.globals as g
import config

class SaverClass:
    def __init__(self, user: str, host: str, pathToKey: str) -> None:
        self.connection: subprocess.Popen[Any]
        self.user: str = user
        self.host: str = host
        self.userHost = f"{self.user}@{self.host}" 
        try:
            self.pathToKey: str = Path(
                pathToKey).resolve(strict=True).__str__()
        except FileNotFoundError:
            raise
        self.sshCmd = [
                "ssh",
                "-T",
                self.userHost,
                "-i",
                self.pathToKey]
        self.rsyncCmd = [
            "rsync",
            "-avz",
            "-e",
            "ssh",
            "-i",
            self.pathToKey,
            "-r",
            config.UPLOADS_DIR,
            "/",
            #self.userHost,
        ]
        self.initiateSSHConnection()

    def compress(self, filePathsToCompress: "list[Path]" = []) -> str:
        archivePath = None
        for filePathToCompress in filePathsToCompress:
            if (filePathToCompress):
                if(filePathToCompress.is_file()):
                    g.logger.info(f"Copying file '{str(filePathToCompress)}' to {str(config.UPLOADS_DIR)}'")
                    shutil.copy2(src=str(filePathToCompress), dst=str(config.UPLOADS_DIR), follow_symlinks=True)
                elif(filePathToCompress.is_dir()):
                    g.logger.info(f"Copying directory '{str(filePathToCompress)}' to {str(config.UPLOADS_DIR)}'")
                    shutil.copytree(src=filePathToCompress, dst=config.UPLOADS_DIR, dirs_exist_ok=True) 
                else:
                    g.logger.error('Specified path is neither file nor directory: ' + str(filePathToCompress))

        archivePath = shutil.make_archive(
            base_name=f'{config.TIMESTAMP_OF_SCRIPT}',
            format="zip",
            root_dir=config.UPLOADS_DIR.resolve(strict=True),
            base_dir=config.UPLOADS_DIR.resolve(strict=True),
            logger=g.logger,
            )
        
        return archivePath

    def closeSSH(self) -> None:
        assert self.connection.stdin is not None
        self.connection.stdin.write(b'exit\n')
        self.connection.stdin.flush()

    def initiateSSHConnection(self, terminateUponConnection: bool = True) -> Optional[bool]:
        try:
            self.connection = subprocess.Popen(self.sshCmd,stdin=subprocess.PIPE,
                                               stdout=StreamToLogger(g.logger, 20), # type: ignore
                                               stderr=StreamToLogger(g.logger, 50))  # type: ignore
            if (terminateUponConnection):
                self.closeSSH()
        except Exception:
            raise
        finally:
            self.connection.communicate()

    def initiateSCPConnection(self) -> None:
        try:
            self.connection = subprocess.Popen(self.rsyncCmd,
                                               stdin=subprocess.PIPE,
                                               stdout=StreamToLogger(g.logger, 20), # type: ignore
                                               stderr=StreamToLogger(g.logger, 50)) # type: ignore
        except Exception:
            raise

    def rsync(self, fileToUploadPath : Path) -> None:
        try:
            self.rsyncCmd = [
            "scp",
            "-i",
            self.pathToKey,
            "-C",
            "-r",
            "-v",
            fileToUploadPath.resolve() or config.UPLOADS_DIR.__str__(),
            f'{self.userHost}:$HOME/PROJECT_TRANSFERS/',
        ]
            #cmd = " ".join(map(str,self.rsyncCmd)) + "\n"
            #self.initiateSSHConnection(terminateUponConnection=False)
            self.initiateSCPConnection()
            self.connection.communicate()
        except Exception:
            raise
        
        
    def upload(self, filesToSave: "list[Optional[str]]" = [], directoriesToSave: "list[Optional[str]]" = []) -> None:
        try:
            self.initiateSSHConnection(terminateUponConnection=False)
            #self.rsync(local=config.UPLOADS_DIR.__str__(), dst="/")
        except Exception:
            raise