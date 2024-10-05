from pathlib import Path
import modules.globals as g
import config
from modules.hcp_data_manager.downloader import getFile
from ..file_directory.file_directory import createDirectories
from modules.subprocess_caller.call import *
import includes.anatomicalLabels as anatomicalLabels
from shutil import copy2


def runDsiStudio(subjectId: str) -> bool:
  return \
    generateSrcFile(subjectId) and \
    reconstructImage(subjectId) and \
    trackFibres(subjectId) and \
    registerDsiStudioTemplateToSubject(subjectId)

def generateSrcFile(subjectId: str) -> bool:
  if(config.DSI_STUDIO_USE_RECONST):
    sourceFile = getFile(localPath=config.SUBJECT_DIR / 'T1w' / config.DIFFUSION_FOLDER / 'data.nii.gz' )
    bval = getFile(localPath=config.SUBJECT_DIR / 'T1w' / config.DIFFUSION_FOLDER / 'bvals' )
    bvec = getFile(localPath=config.SUBJECT_DIR / 'T1w' / config.DIFFUSION_FOLDER / 'bvecs' )

    # The destination file need not exist locally already, but its folders must.
    destinationFolder = config.SUBJECT_DIR / 'T1w' / config.DIFFUSION_FOLDER
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
  destinationFolder = config.SUBJECT_DIR / 'T1w' / config.DIFFUSION_FOLDER
  createDirectories(directoryPaths=[destinationFolder], createParents=True, throwErrorIfExists=False)
  
  if(config.DSI_STUDIO_USE_RECONST):
    sourceFile = Path(config.SUBJECT_DIR / 'T1w' / config.DIFFUSION_FOLDER / 'data.src.gz' ).resolve(strict=True)
    threadCount = config.CPU_THREADS # Default: CPU number.
    method = config.DSI_STUDIO_RECONSTRUCTION_METHOD
    maskFile = getFile(localPath=config.SUBJECT_DIR / 'T1w' / config.DIFFUSION_FOLDER / 'nodif_brain_mask.nii.gz' )
    
    if(config.NORMALISE_TO_MNI152):
      destinationFile: str = str(destinationFolder / ('automated_'+'data.src.gz.gqi.1.25.fib.gz'))
      
      # TODO: Convert the filename to parameter.
      # refFile = getFile(localPath=config.SUBJECT_DIR / "MNINonLinear" / "T1w_restore_brain.nii.gz" )
      # refFile = getFile(localPath=config.SUBJECT_DIR / "T1w" / "T1w_acpc_dc_restore_brain.nii.gz" )
      refFile = getFile(localPath=config.SUBJECT_DIR / "T1w" / "T1w_acpc_dc_restore_brain.nii.gz" )
      copiedRefFile = config.SUBJECT_DIR / "T1w" / ("automated_"+"T1w_acpc_dc_restore_brain.nii.gz")
      
      refFile = copy2(refFile, copiedRefFile)
    else:
      refFile = "NOT-SET" #TODO
      # TODO: Does this need to change if not mni?
      destinationFile: str = str(destinationFolder / 'data.src.gz.gqi.1.25.fib.gz')
    
    
    # processedFile: str = str(destinationFolder / 'data_proc.nii.gz')
    g.logger.info("Running DSI Studio: reconstructing image (.fib.gz).")
    return call(cmdLabel="DSIStudio",
                cmd=[
                        config.DSI_STUDIO,
                        '--action=rec',
                        f'--source={sourceFile}',
                        f'--align_acpc=0',
                        f'--align_to={refFile}',
                        f'--motion_correction=1',
                        f'--template=0',
                        # f'--save_nii={processedFile}',
                        f'--method={method}',
                        f'--mask={maskFile}',
                        f'--thread_count={threadCount}',
                        f'--output={destinationFile}',
                        f'--param0=1.25',
                        f'--record_odf=1',
                        f'--dti_no_high_b=1',
                        f'--check_btable=1',
                        f'--other_output=all',
                        ])
  else:
    # Ensure Bedpost files exist.
    subjectDir = config.SUBJECT_DIR / "T1w"
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
  if(config.NORMALISE_TO_MNI152):
    sourceFile = Path(config.SUBJECT_DIR / 'T1w' / config.DIFFUSION_FOLDER / (('automated_'+'data.src.gz.gqi.1.25.fib.gz') if config.DSI_STUDIO_USE_RECONST else 'automated.fib') ).resolve(strict=True)

    # The destination file need not exist locally already, but its folders must.
    destinationFolder = config.SUBJECT_DIR / 'T1w' / config.DIFFUSION_FOLDER
  
    createDirectories(directoryPaths=[destinationFolder, destinationFolder/ 'dsistudio'], createParents=True, throwErrorIfExists=False)
    

    refFile = getFile(localPath=config.SUBJECT_DIR / "T1w" / "aparc+aseg.nii.gz" )
    copiedRefFile = config.SUBJECT_DIR / "T1w" / ("automated_"+"aparc+aseg.nii.gz")
    copy2(refFile, copiedRefFile)
    refFile = copiedRefFile

    # Needed when using bedpostX reconstructed images. As --other_slices
    t1wFile = getFile(localPath=config.SUBJECT_DIR / "T1w" / "T1w_acpc_dc_restore_brain.nii.gz" )
    copiedT1wFile = config.SUBJECT_DIR / "T1w" / ("automated_reg_"+"T1w_acpc_dc_restore_brain.nii.gz")
    copy2(t1wFile, copiedT1wFile)
    t1wFile = copiedT1wFile
    
  else:
    t1wFile="NOT-SET-TODO" #TODO
    sourceFile = Path(config.SUBJECT_DIR / 'T1w' / config.DIFFUSION_FOLDER / ('data.src.gz.gqi.1.25.fib.gz' if config.DSI_STUDIO_USE_RECONST else 'automated.fib') ).resolve(strict=True)

    # The destination file need not exist locally already, but its folders must.
    destinationFolder = config.SUBJECT_DIR / 'T1w' / config.DIFFUSION_FOLDER
    createDirectories(directoryPaths=[destinationFolder, destinationFolder/ 'dsistudio'], createParents=True, throwErrorIfExists=False)
    
    refFile = getFile(localPath=config.SUBJECT_DIR / "T1w" / "T1w_restore_brain.nii.gz" )

  if (config.DSI_STUDIO_USE_ROI):
    createRoiFiles(subjectId)
    
  iterationSuccess: "list[bool]" = []
  for currentIteration in range(0, config.DSI_STUDIO_ITERATION_COUNT, 1):
    destinationFile: str = str(destinationFolder / ('1m'+str(currentIteration)+'.trk') )
    # destinationFile_template: str = str(destinationFolder / ('template_'+'1m'+str(currentIteration)+'.trk') )

    
    cmd = [config.DSI_STUDIO,
                        '--action=trk',
                        f'--source={sourceFile}',
                        f'--random_seed={str(currentIteration*100)}', #Set seed for reproducability
                        f'--thread_count={config.CPU_THREADS}',
                        # f'--output={destinationFolder / "dsistudio"}',
                        f'--fiber_count={config.DSI_STUDIO_FIBRE_COUNT}',
                        f'--seed_count={config.DSI_STUDIO_SEED_COUNT}',
                        f'--method={config.DSI_STUDIO_TRACKING_METHOD}',
                        f'--fa_threshold={config.DSI_STUDIO_FA_THRESH}',
                        f'--step_size={config.DSI_STUDIO_STEP_SIZE}',
                        f'--turning_angle={config.DSI_STUDIO_TURNING_ANGLE}',
                        f'--smoothing={config.DSI_STUDIO_SMOOTHING}',
                        f'--min_length={config.DSI_STUDIO_MIN_LENGTH}',
                        f'--max_length={config.DSI_STUDIO_MAX_LENGTH}',
                        # f'--ref={refFileMni152}',
                        # f'--template_track={destinationFile_template}',
                        f'--check_ending={config.DSI_STUDIO_CHECK_ENDING}',
                        f'--ref={refFile}',
                        ]

    if(config.DSI_STUDIO_USE_RECONST == False):
      cmd = cmd + [
        f'--other_slices={Path(t1wFile).resolve(True)}'
      ]

    # Limit tracks to only those that pass through the precentral gyri.
    lhTractFile: str = destinationFile.replace("/1m","/"+"L_"+"1m")
    rhTractFile: str = destinationFile.replace("/1m","/"+"R_"+"1m")
    if (config.DSI_STUDIO_USE_ROI):
      if(config.NORMALISE_TO_MNI152):
        lhRoiFilePath_dti: Path = Path(str(config.SUBJECT_DIR / "T1w" / config.IMAGES["T1w"]["STANDARD_RES"]["MASKS"]["LEFT"]).replace(".nii.gz",".dti_space.nii.gz")).resolve(strict=True)
        rhRoiFilePath_dti: Path = Path(str(config.SUBJECT_DIR / "T1w" / config.IMAGES["T1w"]["STANDARD_RES"]["MASKS"]["RIGHT"]).replace(".nii.gz",".dti_space.nii.gz")).resolve(strict=True)

        #Run command on left hemisphere.
        lhCmd = cmd.copy()
        lhCmd = lhCmd + [
          f'--tip_iteration=16',
          f'--output={lhTractFile}',
          # f'--lim={roiFile.resolve(strict=True)},dilation',
          f'--seed={lhRoiFilePath_dti}',
          # f'--end2={roiFile.resolve(strict=True)},dilation',
          f'--nend={lhRoiFilePath_dti},negate'
        ]
        iterationSuccess.append(call(cmdLabel="DSIStudio",
              cmd=lhCmd))

        #Run command on right hemisphere.
        rhCmd = cmd.copy()
        rhCmd = rhCmd + [
          f'--tip_iteration=16',
          f'--output={rhTractFile}',
          # f'--lim={roiFile.resolve(strict=True)},dilation',
          f'--seed={rhRoiFilePath_dti.resolve(strict=True)}',
          # f'--end2={roiFile.resolve(strict=True)},dilation',
          f'--nend={rhRoiFilePath_dti.resolve(strict=True)},negate'
        ]
        iterationSuccess.append(call(cmdLabel="DSIStudio",
              cmd=rhCmd))

        del cmd
        
        iterationSuccess.append(mergeTracts(sourceFile, lhTractFile, rhTractFile, destinationFile))
    else:
      cmd = cmd + [
        f'--output={destinationFile}',
      ]
      iterationSuccess.append(call(cmdLabel="DSIStudio",
              cmd=cmd))
      
  g.logger.info("Running DSI Studio: tracking fibres.")
  return all(iterationSuccess)

def registerDsiStudioTemplateToSubject(subjectId: str) -> bool:
  # TODO: Is mov correctly set in non-MNI152 settings?
  targ = getFile(config.SCRIPTS_DIR / 'matlab' / 'toolboxes' / 'DsiStudio' / 'atlas' / 'ICBM152_adult' /'ICBM152_adult.T1W.nii.gz', localOnly=True)
  mov = getFile(config.SUBJECT_DIR / 'MNINonLinear' / 'T1w_restore_brain.nii.gz')
  reg = str(config.SUBJECT_DIR / config.NATIVEORMNI152FOLDER / 'register_t1w_to_mninonlinear.dat')
  return call(cmdLabel="createRegisterDatFile",
              cmd=[
                      "tkregister2",
                      '--mov',
                      mov,
                      '--targ',
                      targ,
                      '--reg',
                      reg,
                      '--regheader',
                      '--noedit',
                      ])

def createRoiFiles(subjectId: str) -> bool:
  brainMaskOfDiffusion: Path = config.SUBJECT_DIR / "T1w" / "Diffusion" / config.IMAGES["DIFFUSION"]["STANDARD_RES"]["NODIF_BRAIN_MASK"]["PATH"]
  lhRoiFilePath: Path = config.SUBJECT_DIR / "T1w" / config.IMAGES["T1w"]["STANDARD_RES"]["MASKS"]["LEFT"]
  rhRoiFilePath: Path = config.SUBJECT_DIR / "T1w" / config.IMAGES["T1w"]["STANDARD_RES"]["MASKS"]["RIGHT"]
  inversedLhRoiFilePath: Path = config.SUBJECT_DIR / "T1w" / config.IMAGES["T1w"]["STANDARD_RES"]["MASKS"]["LEFT_INVERSED"]
  inversedRhRoiFilePath: Path = config.SUBJECT_DIR / "T1w" / config.IMAGES["T1w"]["STANDARD_RES"]["MASKS"]["RIGHT_INVERSED"]
  labelledFilePath: Path = config.SUBJECT_DIR / "T1w" / config.IMAGES["T1w"]["STANDARD_RES"]["MASKS"]["ALL_LABELS"]

  _ = [getFile(localPath=fileToExist) for fileToExist in [brainMaskOfDiffusion]]

  lhRoiFilePath_dti: str = str(config.SUBJECT_DIR / "T1w" / config.IMAGES["T1w"]["STANDARD_RES"]["MASKS"]["LEFT"]).replace(".nii.gz",".dti_space.nii.gz")
  rhRoiFilePath_dti: str = str(config.SUBJECT_DIR / "T1w" / config.IMAGES["T1w"]["STANDARD_RES"]["MASKS"]["RIGHT"]).replace(".nii.gz",".dti_space.nii.gz")
  
  lhRoiFileSuccess = all([
    call(cmdLabel="Freesurfer",
              cmd=[
                "mri_binarize",
                "--i",
                labelledFilePath.resolve(),
                "--o",
                lhRoiFilePath.resolve(),
                "--match",
                "1024",
                "--surf",
                str(lhRoiFilePath.resolve()).replace(".nii.gz",".surf.gii"),
                ]),
    call(cmdLabel="Freesurfer",
              cmd=[
                "mri_vol2vol",
                "--mov",
                lhRoiFilePath.resolve(),
                "--targ",
                brainMaskOfDiffusion.resolve(),
                "--o",
                lhRoiFilePath_dti,
                "--regheader",
                "--nearest",
                ]),
                          ])
  rhRoiFileSuccess = all([
    call(cmdLabel="Freesurfer",
              cmd=[
                "mri_binarize",
                "--i",
                labelledFilePath.resolve(),
                "--o",
                rhRoiFilePath.resolve(),
                "--match",
                "2024",
                "--surf",
                str(rhRoiFilePath.resolve()).replace(".nii.gz",".surf.gii"),
                ]),
    call(cmdLabel="Freesurfer",
              cmd=[
                "mri_vol2vol",
                "--mov",
                rhRoiFilePath.resolve(),
                "--targ",
                brainMaskOfDiffusion.resolve(),
                "--o",
                rhRoiFilePath_dti,
                "--regheader",
                "--nearest",
                ])
    ])
  
  lhInversedRoiFileSuccess = call(cmdLabel="Freesurfer",
              cmd=[
                "mri_binarize",
                "--i",
                Path(lhRoiFilePath_dti).resolve(strict=True),
                "--o",
                inversedLhRoiFilePath.resolve(),
                "--match",
                "1",
                "--inv",
                ])
  rhInversedRoiFileSuccess = call(cmdLabel="Freesurfer",
              cmd=[
                "mri_binarize",
                "--i",
                Path(rhRoiFilePath_dti).resolve(strict=True),
                "--o",
                inversedRhRoiFilePath.resolve(),
                "--match",
                "1",
                "--inv",
                ])
  return lhRoiFileSuccess and rhRoiFileSuccess and lhInversedRoiFileSuccess and rhInversedRoiFileSuccess

def mergeTracts(sourceFile: Path, lhTractFile: str, rhTractFile: str, destinationFile: str) -> bool:
  # dsi_studio --action=ana --source=avg.mean.fib.gz --tract=Tracts1.tt.gz,Tract2.tt.gz --output=Tracts1.txt
  cmd = [config.DSI_STUDIO,
                        '--action=ana',
                        f'--source={sourceFile}',
                        f'--tract={lhTractFile},{rhTractFile}',
                        f'--output={destinationFile}',
                        ]
  return call(cmdLabel="DSIStudio",
              cmd=cmd)
