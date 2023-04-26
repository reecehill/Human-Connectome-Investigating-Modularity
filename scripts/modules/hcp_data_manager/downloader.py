from pathlib import Path
from typing import Any
import boto3
import os
import config
import modules.globals as g
from modules.file_directory.file_directory import createDirectories
def getRemotePathOf(localPath: Path) -> str:
  # Remove local path prefix.
  localPathWithoutDataDir = str(localPath).replace(str(config.DATA_DIR), "")
  remotePath = f'HCP_1200/{localPathWithoutDataDir}'
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
    s3: Any = boto3.client("s3")
    s3.download_file('hcp-openaccess', getRemotePathOf(localPath), localPath)

    try:
      return localPath.resolve(strict=True).__str__()
    except Exception:
      raise
