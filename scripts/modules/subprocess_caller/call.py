from io import TextIOWrapper
from pathlib import Path
import re
import subprocess
from typing import IO, Any, Optional, Union
import modules.globals as g

def call(cmd: "list[Union[str,Path]]", cmdLabel: str = "?", cwd: "Optional[str]" = None, saveToFile: Optional[str] = None) -> bool: # type: ignore
  try:
    g.logger.info("CMD: " + ' '.join(str(x) for x in cmd))
  
    process: subprocess.Popen[Any] = subprocess.Popen(cmd,
              stdout=subprocess.PIPE,
              stderr=subprocess.STDOUT,
              #text=True,
              cwd=cwd
              )


    assert process.stdout is not None

    # clear the data in the info file
    if(saveToFile):
      emptyFile = open(saveToFile,'w')
      emptyFile.close()
    
    with TextIOWrapper(buffer=process.stdout):
      for line in iter(process.stdout.readline, b''): # b'\n'-separated lines
          line = line.decode().strip()
          if(saveToFile):
            with open(saveToFile, "a") as myfile:
              myfile.write(line)
              myfile.write("\n")
            myfile.close()
          if(re.search('[a-zA-Z]', line)):
            g.logger.info(msg=f"{cmdLabel}: "+line)
          else:
            g.logger.debug(msg="Output omitted (does not contain alpha characters)")

    if(process.returncode != 0): 
      if(process.returncode is None):
        g.logger.warning(f"{cmdLabel}: Command did not return a code. We will assume it was successful, but check logs.")
        return True
      else:
        g.logger.error(f"{cmdLabel}: Command failed with exit code {process.returncode}")
        g.logger.error(f"{process.stdout}")
        g.logger.error(f"{process.stderr}")
        return False
    else:
      return True
  except:
    g.logger.error(f"An error occurred while running command: {cmd}")
    return False