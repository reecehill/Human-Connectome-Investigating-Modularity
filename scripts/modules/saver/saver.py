from typing import Any, Optional
import os

try:
  import subprocess
except Exception as e:
  raise e

class SaverClass:
  def __init__(self, user: str, host: str, pathToKey: str) -> None:
    self.user = user
    self.host = host
    self.pathToKey = pathToKey

  def upload(self, filesToSave: list[Optional[str]] = [], directoriesToSave: list[Optional[str]] = []) -> None:
    try:
      ssh: Any = subprocess.Popen(f"ssh {self.user}@{self.host} -i {self.pathToKey}", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception:
      raise

    try:
      ssh.communicate(os.linesep.join([self.pathToKey]))
    except Exception:
      raise

    ##subprocess.check_call(['scp', 'server:file', 'file'])