from io import TextIOWrapper
from pathlib import Path
import re
import subprocess
from typing import Any, Optional, Union
import modules.globals as g

def call(cmd: "list[Union[str,Path]]", cmdLabel: str = "?", cwd: "Optional[str]" = None) -> bool:
  g.logger.info("CMD: " + ' '.join(str(x) for x in cmd))
  process: subprocess.Popen[Any] = subprocess.Popen(cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            #text=True,
            cwd=cwd
            )
  
  assert process.stdout is not None
  with TextIOWrapper(process.stdout):
    for line in iter(process.stdout.readline, b''): # b'\n'-separated lines
        line = line.decode().strip()
        if(re.search('[a-zA-Z]', line)):
          g.logger.info(msg=f"{cmdLabel}: "+line)
        else:
          g.logger.debug(msg="Output omitted (does not contain alpha characters)")
    
  return process.returncode == None