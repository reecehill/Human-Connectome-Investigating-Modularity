from typing import Any, Optional
import os

try:
  import subprocess
except Exception as e:
  raise e

class SaverClass:
  def __init__(self, user: str, host: str, password: str) -> None:
    self.user = user
    self.host = host
    self.password = password

  def upload(self, filesToSave: list[Optional[str]] = [], directoriesToSave: list[Optional[str]] = []) -> None:
    try:
      ssh: Any = subprocess.Popen(f"ssh {self.user}@{self.host}")
    except Exception as e:
      raise

    try:
      ssh.communicate(os.linesep.join([self.password]))
    except Exception as e:
      raise

    ##subprocess.check_call(['scp', 'server:file', 'file'])