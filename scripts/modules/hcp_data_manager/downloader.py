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
  localPathWithoutDataDir = str(localPath).replace(str(config.DATA_DIR / 'subjects'), "")
  if not localPathWithoutDataDir.startswith("/"): localPathWithoutDataDir = "/"+localPathWithoutDataDir
  remotePath = f'HCP_1200{localPathWithoutDataDir}'
  return remotePath

def getFile(localPath: Path, forceDownload: bool = False) -> str:
  """
  Downloads a file from remote storage if it doesnt exist on the system, and returns a string to its path on local storage.
  """
    
  if(localPath.exists() and forceDownload == False):
    return localPath.__str__()
  else:
    g.logger.info("File not found in local storage, prompting download.")
    os.environ["AWS_CONFIG_FILE"] = (config.BASE_DIR / "awsconfig").resolve(strict=True).__str__()
    createDirectories(directoryPaths=[localPath.parent], createParents=True, throwErrorIfExists=False)

    s3: Any = boto3.client("s3") # type: ignore
    meta_data = s3.head_object(Bucket='hcp-openaccess', Key=getRemotePathOf(localPath))
    total_length = int(meta_data.get('ContentLength', 0))
    downloaded: float = 0
    
    def progress(chunk: float) -> None:
      nonlocal downloaded
      downloaded += chunk
      done = int(50 * downloaded / total_length)
      sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )
      sys.stdout.flush()

    g.logger.info(f"Downloading: {localPath}...")
    s3.download_file('hcp-openaccess', getRemotePathOf(localPath), localPath, Callback=progress)
    g.logger.info(f"Downloaded: {localPath}).")
    
    try:
      return localPath.resolve(strict=True).__str__()
    except Exception:
      raise
