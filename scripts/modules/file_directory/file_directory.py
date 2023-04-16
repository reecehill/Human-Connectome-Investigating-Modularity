#
# Ensures that the directory tree is intact, and that folders are created where appropriate.
#


from pathlib import Path
from shutil import rmtree
from typing import Optional, Union

# ----------
# [START]
# ----------

def deleteDirectories(directoryPaths: list[Optional[str]] = []):
  for directoryPath in directoryPaths:
    if(directoryPath):
        if(Path(directoryPath).exists()):
          try:
            rmtree(path=directoryPath, ignore_errors=False)
          except Exception as e: print(e)
            

def createDirectories(
  directoryPaths: list[Optional[str]] = [],
  createParents: bool = False,
  throwErrorIfExists: bool = True) -> Union[FileNotFoundError, FileExistsError, None]:
    """
    createDirectory verifies if a (sub-)directory exists, and creates it (with/without parents) if not. 

    Args:
        directoryPath (list[str]): A list of paths to folders to be created.
        createParents (bool): If createParents is false (the default), a missing parent raises FileNotFoundError. If createParents is true, any missing parents of this path are created as needed; they are created with the default permissions without taking mode into account. 
        throwErrorIfExists (bool): If throwErrorIfExists is true (the default), FileExistsError is raised if the target directory already exists.

    Returns:

        None: Does not return anything.
    """
    for directoryPath in directoryPaths:
        if(directoryPath):
          if(not Path(directoryPath).exists()):
            try:
              Path(directoryPath).mkdir(parents=createParents,exist_ok=throwErrorIfExists)
            except Exception as e: print(e)

# ----------
# [END]
# ----------
