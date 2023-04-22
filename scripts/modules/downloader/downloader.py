from typing import Any
import modules.globals as g
import datalad.api as dl

def buildDataDirectory() -> "list[Any]":
  g.logger.info("Building dataset")
  #return dl.install(source="https://github.com/OpenNeuroDatasets/ds002685", path=config.DATA_DIR, return_type="list")

def downloadFile(filePath: str) -> "list[Any]":
  g.logger.info("Downloading "+filePath)
  file = dl.get(filePath, return_type="list", get_data=True, recursive=True)  
  ok= dl.unlock(path=filePath)
  return file

def clean():
  dl.clean()