from io import TextIOWrapper
from pathlib import Path
import subprocess
from typing import Any, Optional, Union
import modules.globals as g

def call(cmd: "list[Union[str,Path]]", cmdLabel: str = "?", cwd: "Optional[str]" = None) -> bool:
  process: subprocess.Popen[Any] = subprocess.Popen(cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            #text=True,
            cwd=cwd
            )
  
  assert process.stdout is not None
  with TextIOWrapper(process.stdout):
    for line in iter(process.stdout.readline, b''): # b'\n'-separated lines
        g.logger.info(msg=f"{cmdLabel}: "+line.decode().rstrip())
    
  return process.returncode == 0