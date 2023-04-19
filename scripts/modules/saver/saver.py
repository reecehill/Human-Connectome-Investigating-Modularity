from pathlib import Path
import shutil
from time import strftime
from typing import Optional
import subprocess
from modules.saver.streamToLogger import StreamToLogger

import modules.globals as g
import config

class SaverClass:
    def __init__(self, user: str, host: str, pathToKey: str) -> None:
        self.connection: "Optional[object]" = None
        self.user: str = user
        self.host: str = host
        self.userHost = f"{self.user}@{self.host}" 
        self.uploadsDir: Path = config.UPLOADS_DIR
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
            self.uploadsDir,
            "/",
            #self.userHost,
        ]
        self.initiateSSHConnection()

    def compress(self, filePathsToCompress: "list[Optional[str]]" = []) -> Optional[str]:
        archivePath = None
        for filePathToCompress in filePathsToCompress:
            if (filePathToCompress):
                path = Path(filePathToCompress)

                if(path.is_file()):
                    g.logger.info(f"Copying file '{str(path)}' to {str(self.uploadsDir)}'") # type: ignore
                    shutil.copy2(src=str(path), dst=str(self.uploadsDir), follow_symlinks=True)
                elif(path.is_dir()):
                    g.logger.info(f"Copying directory '{str(path)}' to {str(self.uploadsDir)}'") # type: ignore
                    shutil.copytree(src=filePathToCompress, dst=self.uploadsDir) 
                else:
                    g.logger.error('Specified path is neither file nor directory: ' + str(path)) # type: ignore

        archivePath = shutil.make_archive(
            base_name=f'{strftime("%d%m%Y-%H%M%S")}',
            format="zip",
            root_dir=self.uploadsDir.resolve(strict=True),
            base_dir=self.uploadsDir.resolve(strict=True),
            logger=g.logger, # type: ignore
            )
        
        return archivePath

    def closeSSH(self) -> None:
        self.connection.stdin.write(b'exit\n') # type: ignore
        self.connection.stdin.flush() # type: ignore

    def initiateSSHConnection(self, terminateUponConnection: bool = True) -> Optional[bool]:
        try:
            self.connection = subprocess.Popen(self.sshCmd,stdin=subprocess.PIPE,
                                               stdout=StreamToLogger(g.logger, 20), # type: ignore
                                               stderr=StreamToLogger(g.logger, 50)) # type: ignore
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
            fileToUploadPath.resolve() or self.uploadsDir.__str__(),
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
            #self.rsync(local=self.uploadsDir.__str__(), dst="/")
        except Exception:
            raise