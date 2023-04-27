from pathlib import Path
import subprocess
from typing import Any
from modules.saver.streamToLogger import StreamToLogger
import modules.globals as g
import config
from modules.hcp_data_manager.downloader import getFile
from ..file_directory.file_directory import createDirectories
import multiprocessing

def generateSrcFile(subjectId: str) -> bool:
  sourceFile = getFile(localPath=config.DATA_DIR / 'subjects' / subjectId / 'T1w' / config.DIFFUSION_FOLDER / 'data.nii.gz' )
  bval = getFile(localPath=config.DATA_DIR / 'subjects' / subjectId / 'T1w' / config.DIFFUSION_FOLDER / 'bvals' )
  bvec = getFile(localPath=config.DATA_DIR / 'subjects' / subjectId / 'T1w' / config.DIFFUSION_FOLDER / 'bvecs' )

  # The destination file need not exist locally already, but its folders must.
  destinationFolder = config.UPLOADS_DIR / 'subjects' / subjectId / 'T1w' / config.DIFFUSION_FOLDER
  createDirectories(directoryPaths=[destinationFolder], createParents=True, throwErrorIfExists=False)
  
  destinationFile: str = str(destinationFolder / 'data.src.gz')
  g.logger.info("Running DSI Studio: generate Src file.")
  process: subprocess.Popen[Any] = subprocess.Popen([config.DSI_STUDIO,
                      '--action=src',
                      f'--source={sourceFile}',
                      f'--bval={bval}',
                      f'--bvec={bvec}',
                      f'--output={destinationFile}',
                      ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
                    )

  out, _ = process.communicate()
  if out:
    g.logger.info(out.decode())

  return process.returncode == 0

def reconstructImage(subjectId: str) -> bool:
  sourceFile = Path(config.UPLOADS_DIR / 'subjects' / subjectId / 'T1w' / config.DIFFUSION_FOLDER / 'data.src.gz' ).resolve(strict=True)
  threadCount = config.CPU_THREADS # Default: CPU number.
  method = config.DSI_STUDIO_RECONSTRUCTION_METHOD
  
  # The destination file need not exist locally already, but its folders must.
  destinationFolder = config.UPLOADS_DIR / 'subjects' / subjectId / 'T1w' / config.DIFFUSION_FOLDER
  createDirectories(directoryPaths=[destinationFolder], createParents=True, throwErrorIfExists=False)
  
  destinationFile: str = str(destinationFolder / 'data.src.gz.gqi.1.25.fib.gz')
  g.logger.info("Running DSI Studio: reconstructing image (.fib.gz).")
  process: subprocess.Popen[Any] = subprocess.Popen([config.DSI_STUDIO,
                      '--action=rec',
                      f'--source={sourceFile}',
                      f'--method={method}',
                      f'--thread_count={threadCount}',
                      f'--output={destinationFile}',
                      f'--param0=1.25',
                      f'--check_btable=1',
                      ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
                    )

  out, _ = process.communicate()
  if out:
    g.logger.info(out.decode())
  return process.returncode == 0

def trackFibres(subjectId: str) -> bool:
  sourceFile = Path(config.UPLOADS_DIR / 'subjects' / subjectId / 'T1w' / config.DIFFUSION_FOLDER / 'data.src.gz.gqi.1.25.fib.gz' ).resolve(strict=True)
  threadCount = config.CPU_THREADS # Default: CPU number.
  method = config.DSI_STUDIO_TRACKING_METHOD
  nFibres = config.DSI_STUDIO_FIBRE_COUNT
  nSeeds = config.DSI_STUDIO_SEED_COUNT
  
  # The destination file need not exist locally already, but its folders must.
  destinationFolder = config.UPLOADS_DIR / 'subjects' / subjectId / 'T1w' / config.DIFFUSION_FOLDER
  createDirectories(directoryPaths=[destinationFolder], createParents=True, throwErrorIfExists=False)
  destinationFile: str = str(destinationFolder / '1m0.trk')

  refFile = getFile(localPath=config.DATA_DIR / 'subjects' / subjectId / 'T1w' / 'aparc+aseg.nii.gz' )
  
  g.logger.info("Running DSI Studio: tracking fibres.")
  process: subprocess.Popen[Any] = subprocess.Popen([config.DSI_STUDIO,
                      '--action=trk',
                      f'--source={sourceFile}',
                      f'--method={method}',
                      f'--thread_count={threadCount}',
                      f'--output={destinationFile}',
                      f'--fibre_count={nFibres}',
                      f'--seed_count={nSeeds}',
                      f'--initial_dir={config.DSI_STUDIO_INITIAL_DIREC}',
                      f'--fa_threshold={config.DSI_STUDIO_FA_THRESH}',
                      f'--step_size={config.DSI_STUDIO_STEP_SIZE}',
                      f'--turning_angle={config.DSI_STUDIO_TURNING_ANGLE}',
                      f'--smoothing={config.DSI_STUDIO_SMOOTHING}',
                      f'--min_length={config.DSI_STUDIO_MIN_LENGTH}',
                      f'--max_length={config.DSI_STUDIO_MAX_LENGTH}',
                      f'--ref={refFile}',
                      ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
                    )

  out, _ = process.communicate()
  if out:
    g.logger.info(out.decode())
  return process.returncode == 0



def runDsiStudio(subjectId: str) -> bool:
  return generateSrcFile(subjectId) and reconstructImage(subjectId) and trackFibres(subjectId)

def matlabProcessDiffusion(subjectId: str) -> None:
  pass