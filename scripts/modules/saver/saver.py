# pyright: reportMissingTypeStubs=true

from pathlib import Path

# import shutil
# import scripts.modules.file_directory.shutil_ported as shutil
# from ..file_directory import shutil_ported as shutil
import shutil
from typing import Any, Optional
import subprocess
from modules.saver.streamToLogger import StreamToLogger
from .. import globals as g
import config
from typing import cast


class SaverClass:
    def __init__(self, user: str, host: str, pathToKey: str) -> None:
        self.connection: subprocess.Popen[Any]
        self.user: str = user
        self.host: str = host
        self.uploadRunCount = 0
        self.uploadName = ""
        self.userHost = f"{self.user}@{self.host}"
        try:
            self.pathToKey: str = (
                Path(config.BASE_DIR / pathToKey).resolve(strict=True).__str__()
            )
        except FileNotFoundError:
            raise
        self.sshCmd = [
            "ssh",
            "-T",
            self.userHost,
            "-i",
            self.pathToKey,
            "mkdir -p $HOME/PROJECT_TRANSFERS/" + config.TIMESTAMP_OF_SCRIPT,
        ]
        self.initiateSSHConnection()

    def compress(self, filePathsToCompress: "list[Path]" = []) -> str:
        g.logger.info("Compressing files for saving.")
        self.uploadRunCount = self.uploadRunCount + 1
        g.logger.info(f"Upload run count: {self.uploadRunCount}")
        filesToIgnore: "list[str]" = [
            "Participants",
            "tmp",
            ".git",
            ".vscode",
            "__pycache__",
            "modules",
            "matlab",
            "data",
            "uploads",
            "src",
            "typings",
            "project.egg-info",
        ]
        archivePath = None
        rawPath = str(config.UPLOADS_DIR / "raw" / str(self.uploadRunCount))

        def ignoreAllFiles(dir: str, files: "list[str]") -> "list[str]":
            for f in files:
                filePath = Path(dir) / f
                if (
                    filePath.is_file()
                    or (not filePath.exists())
                    or (filePath.is_dir() and f == config.TIMESTAMP_OF_SCRIPT)
                ):
                    filesToIgnore.append(f)
            return filesToIgnore

        def ignoreDefaultFiles(dir: str, files: "list[str]") -> "list[str]":
            return [f for f in files if f in filesToIgnore]

        # Copy project directory tree
        shutil.copytree(src=str(config.BASE_DIR), dirs_exist_ok=False, dst=rawPath, symlinks=False, ignore=ignoreAllFiles)  # type: ignore

        for filePathToCompress in filePathsToCompress:
            if filePathToCompress:
                destPathFromRoot = str(filePathToCompress.resolve()).replace(
                    str(config.BASE_DIR.resolve()), ""
                )
                destPath = str(Path(str(rawPath) + destPathFromRoot).resolve())
                if filePathToCompress.is_file():
                    g.logger.info(
                        f"Copying file '{str(filePathToCompress)}' to {destPath}'"
                    )
                    shutil.copy2(src=str(filePathToCompress), dst=destPath, follow_symlinks=True)  # type: ignore
                elif filePathToCompress.is_dir():
                    g.logger.info(
                        f"Copying directory '{str(filePathToCompress)}' to {destPath}'"
                    )
                    shutil.copytree(src=filePathToCompress, dst=destPath, dirs_exist_ok=True, ignore=ignoreDefaultFiles)  # type: ignore
                    # shutil.copytree(src=filePathToCompress, dst=destPath, ignore=ignoreDefaultFiles)
                else:
                    g.logger.error(
                        "Specified path is neither file nor directory: "
                        + str(filePathToCompress)
                    )

        archivePath = cast(
            str,
            shutil.make_archive(  # type: ignore
                base_name=f"{(config.UPLOADS_DIR / 'compressed' / str(self.uploadRunCount)).resolve(strict=False)}",
                format="zip",
                root_dir=str(rawPath),
                base_dir="./",
                logger=g.logger,
            ),
        )

        return archivePath

    def closeSSH(self) -> None:
        assert self.connection.stdin is not None
        self.connection.stdin.write(b"exit\n")
        self.connection.stdin.flush()

    def initiateSSHConnection(
        self, terminateUponConnection: bool = True
    ) -> "Optional[bool]":
        try:
            self.connection = subprocess.Popen(
                self.sshCmd,
                stdin=subprocess.PIPE,
                stdout=StreamToLogger(g.logger, 20),  # type: ignore
                stderr=StreamToLogger(g.logger, 50),
            )  # type: ignore
            if terminateUponConnection:
                self.closeSSH()
        except Exception:
            raise
        finally:
            self.connection.communicate()

    def initiateSCPConnection(self) -> None:
        try:
            self.connection = subprocess.Popen(
                self.rsyncCmd,
                stdin=subprocess.PIPE,
                stdout=StreamToLogger(g.logger, 20),  # type: ignore
                stderr=StreamToLogger(g.logger, 50),
            )  # type: ignore
        except Exception:
            raise

    def saveToServer(self, fileToUploadPath: Path) -> None:
        if bool(config.logUsingSSH) == True:
            try:
                self.rsyncCmd = [
                    "scp",
                    "-i",
                    self.pathToKey,
                    "-C",
                    "-r",
                    # "-v",
                    fileToUploadPath.resolve() or config.UPLOADS_DIR.__str__(),
                    f"{self.userHost}:$HOME/PROJECT_TRANSFERS/{config.TIMESTAMP_OF_SCRIPT}",
                ]
                self.initiateSCPConnection()
                self.connection.communicate()
            except Exception:
                raise
