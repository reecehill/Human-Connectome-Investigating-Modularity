from pathlib import Path
import modules.globals as g
import config
from modules.hcp_data_manager.downloader import getFile
from ..file_directory.file_directory import createDirectories
from modules.subprocess_caller.call import *
import includes.anatomicalLabels as anatomicalLabels
from shutil import copy2

def generateSrcFile(subjectId: str) -> bool:
  if(config.DSI_STUDIO_USE_RECONST):
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
  else:
    return True; # If we use BedpostX data, we do not need to generate a .src file. 
    
def reconstructImage(subjectId: str) -> bool:
  # The destination file need not exist locally already, but its folders must.
  destinationFolder = config.DATA_DIR / 'subjects' / subjectId / 'T1w' / config.DIFFUSION_FOLDER
  createDirectories(directoryPaths=[destinationFolder], createParents=True, throwErrorIfExists=False)
  
  if(config.DSI_STUDIO_USE_RECONST):
    sourceFile = Path(config.DATA_DIR / 'subjects' / subjectId / 'T1w' / config.DIFFUSION_FOLDER / 'data.src.gz' ).resolve(strict=True)
    threadCount = config.CPU_THREADS # Default: CPU number.
    method = config.DSI_STUDIO_RECONSTRUCTION_METHOD
    
    # destinationFile: str = str(destinationFolder / 'data.src.gz.gqi.1.25.fib.gz')
    destinationFile: str = str(destinationFolder / 'data.src.gz.icbm152_adult.qsdr.1.25.R68.fib.gz')
    # TODO: Convert the filename to parameter.
    refFile = getFile(localPath=config.DATA_DIR / 'subjects' / subjectId / 'MNINonLinear' / config.DSI_STUDIO_REF_IMG )
    refFileMni152 = copy2(refFile, config.DATA_DIR / 'subjects' / subjectId / 'MNINonLinear' / ''.join(('automated_mni152.', config.DSI_STUDIO_REF_IMG)))
    
    processedFile: str = str(destinationFolder / 'data_proc.nii.gz')
    g.logger.info("Running DSI Studio: reconstructing image (.fib.gz).")
    return call(cmdLabel="DSIStudio",
                cmd=[
                        config.DSI_STUDIO,
                        '--action=rec',
                        f'--source={sourceFile}',
                        # f'--align_acpc=1',
                        # f'--align_to={refFile}',
                        f'--motion_correction=0',
                        f'--template=0',
                        # f'--save_nii={processedFile}',
                        f'--method={method}',
                        f'--thread_count={threadCount}',
                        f'--output={destinationFile}',
                        f'--param0=1.25',
                        f'--check_btable=1',
                        f'--other_output=all',
                        ])
  else:
    # Ensure Bedpost files exist.
    subjectDir = config.SUBJECTS_DIR / subjectId / "T1w"
    filesToExist = [
                    (subjectDir / 'Diffusion.bedpostX' / 'mean_f1samples.nii.gz'),
                    (subjectDir / 'Diffusion.bedpostX' / 'mean_f2samples.nii.gz'),
                    (subjectDir / 'Diffusion.bedpostX' / 'mean_f3samples.nii.gz'),
                    (subjectDir / 'Diffusion.bedpostX' / 'mean_ph1samples.nii.gz'),
                    (subjectDir / 'Diffusion.bedpostX' / 'mean_ph2samples.nii.gz'),
                    (subjectDir / 'Diffusion.bedpostX' / 'mean_ph3samples.nii.gz'),
                    (subjectDir / 'Diffusion.bedpostX' / 'mean_th1samples.nii.gz'),
                    (subjectDir / 'Diffusion.bedpostX' / 'mean_th2samples.nii.gz'),
                    (subjectDir / 'Diffusion.bedpostX' / 'mean_th3samples.nii.gz'),
                    ]
    _ = [getFile(localPath=fileToExist) for fileToExist in filesToExist]
      
    return call(cmdLabel="MATLAB",
              cmd=[
                      config.MATLAB,
                      f'-batch "bedpostXtoDsiStudio {config.matLabDriveAndPathToSubjects} {subjectId}"',
                      ],
              cwd=config.matlabScriptsFolder)

def trackFibres(subjectId: str) -> bool:
  sourceFile = Path(config.DATA_DIR / 'subjects' / subjectId / 'T1w' / config.DIFFUSION_FOLDER / ('data.src.gz.icbm152_adult.qsdr.1.25.R68.fib.gz' if config.DSI_STUDIO_USE_RECONST else 'automated.fib') ).resolve(strict=True)
  threadCount = config.CPU_THREADS # Default: CPU number.
  method = config.DSI_STUDIO_TRACKING_METHOD
  nFibres = config.DSI_STUDIO_FIBRE_COUNT
  nSeeds = config.DSI_STUDIO_SEED_COUNT
  
  # The destination file need not exist locally already, but its folders must.
  destinationFolder = config.DATA_DIR / 'subjects' / subjectId / 'T1w' / config.DIFFUSION_FOLDER
  createDirectories(directoryPaths=[destinationFolder, destinationFolder/ 'dsistudio'], createParents=True, throwErrorIfExists=False)
  destinationFile: str = str(destinationFolder / '1m0.tt.nii.gz')
  templateFile: str = str(destinationFolder / '1m0_mni152.tt.nii.gz')
  #templateFile: str = str(destinationFolder / '1m0_mni152.mat')

  # If it is in the T1w space, then it is aparc+aseg space.
  # refFile = getFile(localPath=config.DATA_DIR / 'subjects' / subjectId / 'T1w' / 'aparc+aseg.nii.gz' )
  refFile = getFile(localPath=config.DATA_DIR / 'subjects' / subjectId / 'MNINonLinear' / config.DSI_STUDIO_REF_IMG )
  # refFile = getFile(localPath=config.DATA_DIR / 'subjects' / subjectId / 'MNINonLinear' / 'T1w_moddedheader.native.nii.gz', localOnly=True)
  refFileMni152 = copy2(refFile, config.DATA_DIR / 'subjects' / subjectId / 'MNINonLinear' / ''.join(('automated_mni152.', config.DSI_STUDIO_REF_IMG)))
  refFileMni152Registered = copy2(refFile, config.DATA_DIR / 'subjects' / subjectId / 'MNINonLinear' / ''.join(('automated_mni152.reg_', config.DSI_STUDIO_REF_IMG)))
  
 

  cmd = [config.DSI_STUDIO,
                      '--action=trk',
                      f'--source={sourceFile}',
                      f'--random_seed=1', #Set seed for reproducability
                      f'--thread_count={threadCount}',
                      # f'--output={destinationFolder / "dsistudio"}',
                      f'--output={destinationFile}',
                      f'--fiber_count={nFibres}',
                      f'--seed_count={nSeeds}',
                      # f'--method={method}',
                      f'--fa_threshold={config.DSI_STUDIO_FA_THRESH}',
                      f'--step_size={config.DSI_STUDIO_STEP_SIZE}',
                      f'--turning_angle={config.DSI_STUDIO_TURNING_ANGLE}',
                      # f'--smoothing={config.DSI_STUDIO_SMOOTHING}',
                      f'--min_length={config.DSI_STUDIO_MIN_LENGTH}',
                      f'--max_length={config.DSI_STUDIO_MAX_LENGTH}',
                      f'--template_track={templateFile}',
                      # f'--ref={refFileMni152}'
                      f'--ref={refFile}'
                      ]
  # Limit tracks to only those that pass through the precentral gyri.
  if (config.DSI_STUDIO_USE_ROI):
    roiFile = getFile(localPath=config.DATA_DIR / 'subjects' / subjectId / 'MNINonLinear' / config.DSI_STUDIO_ANNOTATED_IMG )
    roiFileMni152 = copy2(roiFile, config.DATA_DIR / 'subjects' / subjectId / 'MNINonLinear' / 'automated_mni152.aparcaseg.nii.gz')

    roiCmd = f'--roi={roiFileMni152}:ctx-lh-precentral,dilation,dilation+{roiFileMni152}:ctx-rh-precentral,dilation,dilation'
    cmd.append(roiCmd)
  
  g.logger.info("Running DSI Studio: tracking fibres.")
  return call(cmdLabel="DSIStudio",
              cmd=cmd)

def runDsiStudio(subjectId: str) -> bool:
  return generateSrcFile(subjectId) and reconstructImage(subjectId) and trackFibres(subjectId)
  # return reconstructImage(subjectId) and trackFibres(subjectId)
  # return trackFibres(subjectId)


def matlabProcessDiffusion(subjectId: str) -> bool:
  g.logger.info("Running MATLAB: converting tracked fibres into endpoints and adjacency matrices.")

  # Ensure neccessary files exist from previous steps.
  anatomicalLabelsToExist: list[str] = anatomicalLabels.anatomicalLabelsToExist
  remoteFilesToExist: "list[Path]" = [
                  (config.DATA_DIR / 'subjects' / subjectId / 'MNINonLinear' / 'aparc+aseg.nii.gz'),
                  (config.DATA_DIR / 'subjects' / subjectId / 'T1w' / subjectId / 'mri' / 'transforms' / 'talairach.xfm'),
                  # (config.DATA_DIR / 'subjects' / subjectId / 'T1w' / subjectId / 'surf' / 'lh.pial'),
                  # (config.DATA_DIR / 'subjects' / subjectId / 'T1w' / subjectId / 'surf' / 'rh.pial'),
                  ]
  localFilesToExist: "list[Path]" = [
     (config.DATA_DIR / 'subjects' / subjectId / 'T1w' / config.DIFFUSION_FOLDER / '1m0.trk'),
     
    ] + [(config.DATA_DIR / 'subjects' / subjectId / 'MNINonLinear' / subjectId / 'label' / 'label_type2' / label) for label in anatomicalLabelsToExist]
  
  _ = [getFile(localPath=fileToExist) for fileToExist in remoteFilesToExist]
  _ = [getFile(localPath=fileToExist, localOnly=True) for fileToExist in localFilesToExist]
  
  return call(cmdLabel="MATLAB",
              cmd=[
                      config.MATLAB,
                      f'-batch "batch_process {config.matLabDriveAndPathToSubjects} {subjectId} {config.PIAL_SURFACE_TYPE} {config.DOWNSAMPLE_SURFACE} {config.DOWNSAMPLE_RATE}"',
                      ],
              cwd=config.matlabScriptsFolder)