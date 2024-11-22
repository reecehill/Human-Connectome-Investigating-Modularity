from pathlib import Path
from typing import Any
import boto3
import os
import config
import modules.globals as g
from modules.file_directory.file_directory import createDirectories
import sys


def getRemotePathOf(localPath: Path) -> str:
    # Remove local path prefix.
    localPathWithoutDataDir = str(localPath).replace(
        str(config.DATA_DIR / 'subjects'), "")
    if not localPathWithoutDataDir.startswith("/"):
        localPathWithoutDataDir = "/"+localPathWithoutDataDir
    remotePath = f'HCP_1200{localPathWithoutDataDir}'
    return remotePath


def getFile(localPath: Path, forceDownload: bool = False, localOnly: bool = False) -> str:
    """
    Downloads a file from remote storage if it doesnt exist on the system, and returns a string to its path on local storage.
    localPath: path to the file on local storage that should exist
    forceDownload: download the file, overwriting the version stored locally.
    localOnly: skip downloading the file (useful when the file is generated locally only). This just ensures it exists.
    """

    if (localPath.exists() and forceDownload == False):
        return str(localPath)
    elif (localOnly == False):
        g.logger.info(
            f"File ({localPath}) not found in local storage, prompting download.")
        os.environ["AWS_CONFIG_FILE"] = (
            config.BASE_DIR / "awsconfig").resolve(strict=True).__str__()
        createDirectories(directoryPaths=[
                          localPath.parent], createParents=True, throwErrorIfExists=False)

        s3 = boto3.client("s3")
        meta_data = s3.head_object(
            Bucket='hcp-openaccess', Key=getRemotePathOf(localPath))
        total_length = int(meta_data.get('ContentLength', 0))
        downloaded: float = 0

        def progress(chunk: float) -> None:
            nonlocal downloaded
            downloaded += chunk
            done = int(50 * downloaded / total_length)
            sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)))
            sys.stdout.flush()

        g.logger.info(f"Downloading: {localPath}...")
        remotePath = getRemotePathOf(localPath)
        s3.download_file('hcp-openaccess', remotePath,
                         str(localPath), Callback=progress)
        g.logger.info(f"Downloaded: {localPath}).")
        g.downloadedFiles.append(localPath)

    try:
        return localPath.resolve(strict=True).__str__()
    except Exception as e:
        raise FileNotFoundError(f"File not found: {localPath}")
