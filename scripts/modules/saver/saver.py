from pathlib import Path
import shutil
from typing import Optional
import os
import subprocess
from modules.saver.streamToLogger import StreamToLogger

import modules.globals as g


class SaverClass:
    def __init__(self, user: str, host: str, pathToKey: str) -> None:
        self.connection: Optional[object] = None
        self.user: str = user
        self.host: str = host
        self.userHost = f"{self.user}@{self.host}" 
        self.uploadedFolder = Path(__file__).parent.parent.parent.resolve(strict=True) / "uploaded"
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
            self.uploadedFolder,
            "/",
            #self.userHost,
        ]
        self.testSSHConnection()

    def compress(self, filePathsToCompress: list[Optional[str]] = []) -> Optional[Path]:
        path = None
        for filePathToCompress in filePathsToCompress:
            if (filePathToCompress):
                path = Path(filePathToCompress)
                shutil.make_archive(
                    base_name=path.__str__(),
                    format="zip",
                    root_dir=path.parent.resolve(strict=True),
                    base_dir=self.uploadedFolder.resolve(strict=True),
                    logger=g.logger,
                    )
        return path

    def closeSSH(self) -> None:
        self.connection.stdin.write(b'exit\n')
        self.connection.stdin.flush()

    def testSSHConnection(self, terminateUponConnection: bool = True) -> Optional[bool]:
        try:
            self.connection = subprocess.Popen(self.sshCmd,stdin=subprocess.PIPE, stdout=StreamToLogger(g.logger, 20), stderr=StreamToLogger(g.logger, 50))
            if (terminateUponConnection):
                self.closeSSH()
        except Exception as e:
            raise

    def rsync(self) -> None:
        pass
        
        
    def upload(self, filesToSave: list[Optional[str]] = [], directoriesToSave: list[Optional[str]] = []) -> None:
        try:
            self.testSSHConnection(terminateUponConnection=False)
            self.rsync(localDirectory, remoteDirectory)
        except Exception:
            raise

        try:
            ssh.communicate(os.linesep.join([self.pathToKey]))
        except Exception:
            raise

        # subprocess.check_call(['scp', 'server:file', 'file'])
