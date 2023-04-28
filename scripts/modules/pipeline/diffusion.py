from pathlib import Path
import modules.globals as g
import config
from modules.hcp_data_manager.downloader import getFile
from ..file_directory.file_directory import createDirectories
from modules.subprocess_caller.call import *

def generateSrcFile(subjectId: str) -> bool:
  sourceFile = getFile(localPath=config.DATA_DIR / 'subjects' / subjectId / 'T1w' / config.DIFFUSION_FOLDER / 'data.nii.gz' )
  bval = getFile(localPath=config.DATA_DIR / 'subjects' / subjectId / 'T1w' / config.DIFFUSION_FOLDER / 'bvals' )
  bvec = getFile(localPath=config.DATA_DIR / 'subjects' / subjectId / 'T1w' / config.DIFFUSION_FOLDER / 'bvecs' )

  # The destination file need not exist locally already, but its folders must.
  destinationFolder = config.DATA_DIR / 'subjects' / subjectId / 'T1w' / config.DIFFUSION_FOLDER
  createDirectories(directoryPaths=[destinationFolder], createParents=True, throwErrorIfExists=False)
  
  destinationFile: str = str(destinationFolder / 'data.src.gz')
  g.logger.info("Running DSI Studio: generate Src file.")

  return call(cmdLabel="DSI Studio",
              cmd=[
                      config.DSI_STUDIO.__str__(),
                      '--action=src',
                      f'--source={sourceFile}',
                      f'--bval={bval}',
                      f'--bvec={bvec}',
                      f'--output={destinationFile}',
                      ])

def reconstructImage(subjectId: str) -> bool:
  sourceFile = Path(config.DATA_DIR / 'subjects' / subjectId / 'T1w' / config.DIFFUSION_FOLDER / 'data.src.gz' ).resolve(strict=True)
  threadCount = config.CPU_THREADS # Default: CPU number.
  method = config.DSI_STUDIO_RECONSTRUCTION_METHOD
  
  # The destination file need not exist locally already, but its folders must.
  destinationFolder = config.DATA_DIR / 'subjects' / subjectId / 'T1w' / config.DIFFUSION_FOLDER
  createDirectories(directoryPaths=[destinationFolder], createParents=True, throwErrorIfExists=False)
  
  destinationFile: str = str(destinationFolder / 'data.src.gz.gqi.1.25.fib.gz')
  g.logger.info("Running DSI Studio: reconstructing image (.fib.gz).")
  return call(cmdLabel="DSIStudio",
              cmd=[
                      config.DSI_STUDIO,
                      '--action=rec',
                      f'--source={sourceFile}',
                      f'--method={method}',
                      f'--thread_count={threadCount}',
                      f'--output={destinationFile}',
                      f'--param0=1.25',
                      f'--check_btable=1',
                      ])

def trackFibres(subjectId: str) -> bool:
  sourceFile = Path(config.DATA_DIR / 'subjects' / subjectId / 'T1w' / config.DIFFUSION_FOLDER / 'data.src.gz.gqi.1.25.fib.gz' ).resolve(strict=True)
  threadCount = config.CPU_THREADS # Default: CPU number.
  method = config.DSI_STUDIO_TRACKING_METHOD
  nFibres = config.DSI_STUDIO_FIBRE_COUNT
  nSeeds = config.DSI_STUDIO_SEED_COUNT
  
  # The destination file need not exist locally already, but its folders must.
  destinationFolder = config.DATA_DIR / 'subjects' / subjectId / 'T1w' / config.DIFFUSION_FOLDER
  createDirectories(directoryPaths=[destinationFolder], createParents=True, throwErrorIfExists=False)
  destinationFile: str = str(destinationFolder / '1m0.trk')

  refFile = getFile(localPath=config.DATA_DIR / 'subjects' / subjectId / 'T1w' / 'aparc+aseg.nii.gz' )
  
  g.logger.info("Running DSI Studio: tracking fibres.")
  return call(cmdLabel="DSIStudio",
              cmd=[config.DSI_STUDIO,
                      '--action=trk',
                      f'--source={sourceFile}',
                      f'--method={method}',
                      f'--thread_count={threadCount}',
                      f'--output={destinationFile}',
                      f'--fiber_count={nFibres}',
                      f'--seed_count={nSeeds}',
                      f'--fa_threshold={config.DSI_STUDIO_FA_THRESH}',
                      f'--step_size={config.DSI_STUDIO_STEP_SIZE}',
                      f'--turning_angle={config.DSI_STUDIO_TURNING_ANGLE}',
                      f'--smoothing={config.DSI_STUDIO_SMOOTHING}',
                      f'--min_length={config.DSI_STUDIO_MIN_LENGTH}',
                      f'--max_length={config.DSI_STUDIO_MAX_LENGTH}',
                      #f'--ref={refFile}',
                      ])



def runDsiStudio(subjectId: str) -> bool:
  return \
    generateSrcFile(subjectId) and \
    reconstructImage(subjectId) and \
    trackFibres(subjectId)


def matlabProcessDiffusion(subjectId: str) -> bool:
  g.logger.info("Running MATLAB: converting tracked fibres into endpoints and adjacency matrices.")
  driveAndPathToSubjects = (config.DATA_DIR / 'subjects').resolve(strict=True).__str__()+"/"
  matlabFolder = (config.SCRIPTS_DIR / "matlab" ).resolve(strict=True).__str__()

  # Ensure neccessary files exist from previous steps.
  anatomicalLabelsToExist: list[str] = ['lh.bankssts.label','lh.caudalanteriorcingulate.label','lh.caudalmiddlefrontal.label','lh.cuneus.label','lh.entorhinal.label','lh.frontalpole.label','lh.fusiform.label','lh.inferiorparietal.label','lh.inferiortemporal.label','lh.insula.label','lh.isthmuscingulate.label','lh.lateraloccipital.label','lh.lateralorbitofrontal.label','lh.lingual.label','lh.medialorbitofrontal.label','lh.middletemporal.label','lh.paracentral.label','lh.parahippocampal.label','lh.parsopercularis.label','lh.parsorbitalis.label','lh.parstriangularis.label','lh.pericalcarine.label','lh.postcentral.label','lh.posteriorcingulate.label','lh.precentral.label','lh.precuneus.label','lh.rostralanteriorcingulate.label','lh.rostralmiddlefrontal.label','lh.superiorfrontal.label','lh.superiorparietal.label','lh.superiortemporal.label','lh.supramarginal.label','lh.temporalpole.label','lh.transversetemporal.label','rh.bankssts.label','rh.caudalanteriorcingulate.label','rh.caudalmiddlefrontal.label','rh.cuneus.label','rh.entorhinal.label','rh.frontalpole.label','rh.fusiform.label','rh.inferiorparietal.label','rh.inferiortemporal.label','rh.insula.label','rh.isthmuscingulate.label','rh.lateraloccipital.label','rh.lateralorbitofrontal.label','rh.lingual.label','rh.medialorbitofrontal.label','rh.middletemporal.label','rh.paracentral.label','rh.parahippocampal.label','rh.parsopercularis.label','rh.parsorbitalis.label','rh.parstriangularis.label','rh.pericalcarine.label','rh.postcentral.label','rh.posteriorcingulate.label','rh.precentral.label','rh.precuneus.label','rh.rostralanteriorcingulate.label','rh.rostralmiddlefrontal.label','rh.superiorfrontal.label','rh.superiorparietal.label','rh.superiortemporal.label','rh.supramarginal.label','rh.temporalpole.label','rh.transversetemporal.label']
  remoteFilesToExist: "list[Path]" = [
                  (config.DATA_DIR / 'subjects' / subjectId / 'T1w' / 'aparc+aseg.nii.gz'),
                  (config.DATA_DIR / 'subjects' / subjectId / 'T1w' / subjectId / 'mri' / 'transforms' / 'talairach.xfm'),
                  (config.DATA_DIR / 'subjects' / subjectId / 'T1w' / subjectId / 'surf' / 'lh.pial'),
                  (config.DATA_DIR / 'subjects' / subjectId / 'T1w' / subjectId / 'surf' / 'rh.pial'),
                  ]
  localFilesToExist: "list[Path]" = [
     (config.DATA_DIR / 'subjects' / subjectId / 'T1w' / config.DIFFUSION_FOLDER / '1m0.trk'),
     
    ] + [(config.DATA_DIR / 'subjects' / subjectId / 'T1w' / subjectId / 'label' / 'label_type2' / label) for label in anatomicalLabelsToExist]
  
  _ = [getFile(localPath=fileToExist) for fileToExist in remoteFilesToExist]
  _ = [getFile(localPath=fileToExist, localOnly=True) for fileToExist in localFilesToExist]
  
  return call(cmdLabel="MATLAB",
              cmd=[
                      config.MATLAB,
                      f'-batch "batch_process {driveAndPathToSubjects} {subjectId} {config.PIAL_SURFACE_TYPE} {config.DOWNSAMPLE_SURFACE} {config.DOWNSAMPLE_RATE}"',
                      ],
              cwd=matlabFolder)