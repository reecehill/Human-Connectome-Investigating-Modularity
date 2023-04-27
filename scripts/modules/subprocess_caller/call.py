from pathlib import Path
import subprocess
from typing import Any, Optional, Union
import modules.globals as g

def call(cmd: "list[Union[str,Path]]", cmdLabel: str = "?", cwd: "Optional[str]" = None) -> bool:
  process: subprocess.Popen[Any] = subprocess.Popen(cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            cwd=cwd
            )
  
  assert process.stdout is not None
  with process.stdout:
    for line in process.stdout.read().splitlines(): # b'\n'-separated lines
        g.logger.info(msg=f"{cmdLabel}: "+line)
    
  return process.returncode == 0