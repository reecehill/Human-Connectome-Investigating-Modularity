import subprocess
from typing import Any
from modules.saver.streamToLogger import StreamToLogger
import globals as g
import config
from modules.hcp_data_manager.downloader import getFile
from ..file_directory.file_directory import createDirectories

def generateSrcFile(subjectId: str) -> int:
  sourceFile = getFile(localPath=config.DATA_DIR / subjectId / 'T1w' / config.DIFFUSION_FOLDER / 'data.nii.gz' )
  bval = getFile(localPath=config.DATA_DIR / subjectId / 'T1w' / config.DIFFUSION_FOLDER / 'bvals' )
  bvec = getFile(localPath=config.DATA_DIR / subjectId / 'T1w' / config.DIFFUSION_FOLDER / 'bvecs' )

  # The destination file need not exist locally already, but its folders must.
  destinationFolder = config.UPLOADS_DIR / subjectId / 'T1w' / config.DIFFUSION_FOLDER
  createDirectories([destinationFolder])
  
  destinationFile: str = str(destinationFolder / 'data.src.gz')
  process: subprocess.Popen[Any] = subprocess.Popen([config.DSI_STUDIO,
                    '--action=src',
                    f'--source={sourceFile}',
                    f'--bval={bval}',
                    f'--bvec={bvec}',
                    f'--output={destinationFile}',
                    ],
                   stdin=subprocess.PIPE,
                   stdout=StreamToLogger(g.logger, 20), # type: ignore
                   stderr=StreamToLogger(g.logger, 50)) # type: ignore
  process.communicate()
  return process.returncode

def reconstructImage(subjectId: str):
  pass

def trackFibres(subjectId: str):
  pass



def runDsiStudio(subjectId: str) -> None:
  generateSrcFile(subjectId)

def matlabProcessDiffusion(subjectId: str) -> None:
  pass