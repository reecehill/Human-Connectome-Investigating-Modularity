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
    maskFile = getFile(localPath=config.DATA_DIR / 'subjects' / subjectId / 'T1w' / config.DIFFUSION_FOLDER / 'nodif_brain_mask.nii.gz' )
    
    if(config.NORMALISE_TO_MNI152):
      destinationFile: str = str(destinationFolder / ('automated_'+'data.src.gz.gqi.1.25.fib.gz'))
      
      # TODO: Convert the filename to parameter.
      # refFile = getFile(localPath=config.DATA_DIR / 'subjects' / subjectId / "MNINonLinear" / "T1w_restore_brain.nii.gz" )
      # refFile = getFile(localPath=config.DATA_DIR / 'subjects' / subjectId / "T1w" / "T1w_acpc_dc_restore_brain.nii.gz" )
      refFile = getFile(localPath=config.DATA_DIR / 'subjects' / subjectId / "T1w" / "T1w_acpc_dc_restore_brain.nii.gz" )
      copiedRefFile = config.DATA_DIR / 'subjects' / subjectId / "T1w" / ("automated_"+"T1w_acpc_dc_restore_brain.nii.gz")
      
      refFile = copy2(refFile, copiedRefFile)
    else:
      # TODO: Does this need to change if not mni?
      destinationFile: str = str(destinationFolder / 'data.src.gz.gqi.1.25.fib.gz')
    
    
    processedFile: str = str(destinationFolder / 'data_proc.nii.gz')
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
  if(config.NORMALISE_TO_MNI152):
    sourceFile = Path(config.DATA_DIR / 'subjects' / subjectId / 'T1w' / config.DIFFUSION_FOLDER / (('automated_'+'data.src.gz.gqi.1.25.fib.gz') if config.DSI_STUDIO_USE_RECONST else 'automated.fib') ).resolve(strict=True)

    # The destination file need not exist locally already, but its folders must.
    destinationFolder = config.DATA_DIR / 'subjects' / subjectId / 'T1w' / config.DIFFUSION_FOLDER
  
    createDirectories(directoryPaths=[destinationFolder, destinationFolder/ 'dsistudio'], createParents=True, throwErrorIfExists=False)
    

    refFile = getFile(localPath=config.DATA_DIR / 'subjects' / subjectId / "T1w" / "aparc+aseg.nii.gz" )
    copiedRefFile = config.DATA_DIR / 'subjects' / subjectId / "T1w" / ("automated_"+"aparc+aseg.nii.gz")
    copy2(refFile, copiedRefFile)
    refFile = copiedRefFile

    # Needed when using bedpostX reconstructed images. As --other_slices
    t1wFile = getFile(localPath=config.DATA_DIR / 'subjects' / subjectId / "T1w" / "T1w_acpc_dc_restore_brain.nii.gz" )
    copiedT1wFile = config.DATA_DIR / 'subjects' / subjectId / "T1w" / ("automated_reg_"+"T1w_acpc_dc_restore_brain.nii.gz")
    copy2(t1wFile, copiedT1wFile)
    t1wFile = copiedT1wFile
    
  else:
    sourceFile = Path(config.DATA_DIR / 'subjects' / subjectId / 'T1w' / config.DIFFUSION_FOLDER / ('data.src.gz.gqi.1.25.fib.gz' if config.DSI_STUDIO_USE_RECONST else 'automated.fib') ).resolve(strict=True)

    # The destination file need not exist locally already, but its folders must.
    destinationFolder = config.DATA_DIR / 'subjects' / subjectId / 'T1w' / config.DIFFUSION_FOLDER
    createDirectories(directoryPaths=[destinationFolder, destinationFolder/ 'dsistudio'], createParents=True, throwErrorIfExists=False)
    
    refFile = getFile(localPath=config.DATA_DIR / 'subjects' / subjectId / "T1w" / "T1w_restore_brain.nii.gz" )

  if (config.DSI_STUDIO_USE_ROI):
    createRoiFiles(subjectId)
    
  iterationSuccess: list[bool] = []
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
        lhRoiFilePath = config.DATA_DIR / 'subjects' / subjectId / "T1w" / config.IMAGES["T1w"]["STANDARD_RES"]["MASKS"]["LEFT"]
        rhRoiFilePath = config.DATA_DIR / 'subjects' / subjectId / "T1w" / config.IMAGES["T1w"]["STANDARD_RES"]["MASKS"]["RIGHT"]

        #Run command on left hemisphere.
        lhCmd = cmd.copy()
        lhCmd = lhCmd + [
           f'--tip_iteration=16',
           f'--output={lhTractFile}',
          # f'--lim={roiFile.resolve(strict=True)},dilation',
          f'--seed={lhRoiFilePath.resolve(strict=True)}',
          # f'--end2={roiFile.resolve(strict=True)},dilation',
          f'--nend={lhRoiFilePath.resolve(strict=True)},negate'
        ]
        iterationSuccess.append(call(cmdLabel="DSIStudio",
              cmd=lhCmd))

        #Run command on right hemisphere.
        rhCmd = cmd.copy()
        rhCmd = rhCmd + [
           f'--tip_iteration=16',
           f'--output={rhTractFile}',
          # f'--lim={roiFile.resolve(strict=True)},dilation',
          f'--seed={rhRoiFilePath.resolve(strict=True)}',
          # f'--end2={roiFile.resolve(strict=True)},dilation',
          f'--nend={rhRoiFilePath.resolve(strict=True)},negate'
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

def createRoiFiles(subjectId: str) -> bool:
  lhRoiFilePath = config.DATA_DIR / 'subjects' / subjectId / "T1w" / config.IMAGES["T1w"]["STANDARD_RES"]["MASKS"]["LEFT"]
  rhRoiFilePath = config.DATA_DIR / 'subjects' / subjectId / "T1w" / config.IMAGES["T1w"]["STANDARD_RES"]["MASKS"]["RIGHT"]
  inversedLhRoiFilePath = config.DATA_DIR / 'subjects' / subjectId / "T1w" / config.IMAGES["T1w"]["STANDARD_RES"]["MASKS"]["LEFT_INVERSED"]
  inversedRhRoiFilePath = config.DATA_DIR / 'subjects' / subjectId / "T1w" / config.IMAGES["T1w"]["STANDARD_RES"]["MASKS"]["RIGHT_INVERSED"]
  labelledFilePath = config.DATA_DIR / 'subjects' / subjectId / "T1w" / config.IMAGES["T1w"]["STANDARD_RES"]["MASKS"]["ALL_LABELS"]
  
  lhRoiFileSuccess = call(cmdLabel="Freesurfer",
              cmd=[
                "mri_binarize",
                "--i",
                labelledFilePath.resolve(),
                "--o",
                lhRoiFilePath.resolve(),
                "--match",
                "1024"
                ])
  rhRoiFileSuccess = call(cmdLabel="Freesurfer",
              cmd=[
                "mri_binarize",
                "--i",
                labelledFilePath.resolve(),
                "--o",
                rhRoiFilePath.resolve(),
                "--match",
                "2024",
                ])
  
  lhInversedRoiFileSuccess = call(cmdLabel="Freesurfer",
              cmd=[
                "mri_binarize",
                "--i",
                labelledFilePath.resolve(),
                "--o",
                inversedLhRoiFilePath.resolve(),
                "--match",
                "1024",
                "--inv",
                ])
  rhInversedRoiFileSuccess = call(cmdLabel="Freesurfer",
              cmd=[
                "mri_binarize",
                "--i",
                labelledFilePath.resolve(),
                "--o",
                inversedRhRoiFilePath.resolve(),
                "--match",
                "2024",
                "--inv",
                ])
  return lhRoiFileSuccess and rhRoiFileSuccess and lhInversedRoiFileSuccess and rhInversedRoiFileSuccess

def registerDsiStudioTemplateToSubject(subjectId: str) -> bool:
  # TODO: Is mov correctly set in non-MNI152 settings?
  targ = getFile(config.SCRIPTS_DIR / 'matlab' / 'toolboxes' / 'DsiStudio' / 'atlas' / 'ICBM152_adult' /'ICBM152_adult.T1W.nii.gz', localOnly=True)
  mov = getFile(config.DATA_DIR / 'subjects' / subjectId / config.NATIVEORMNI152FOLDER / 'automated_T1w_restore_brain.nii.gz')
  reg = str(config.DATA_DIR / 'subjects' / subjectId / config.NATIVEORMNI152FOLDER / 'register.dat')
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
def registerSubjectT1ToMNIT1(subjectId: str) -> bool:
  # TODO: Is mov correctly set in non-MNI152 settings?
  mov = getFile(config.DATA_DIR / 'subjects' / subjectId / "T1w" / 'T1w_acpc_dc_restore_brain.nii.gz')
  targ = getFile(config.DATA_DIR / 'subjects' / subjectId / "MNINonLinear" / 'T1w_restore_brain.nii.gz')
  reg = str(config.DATA_DIR / 'subjects' / subjectId / "MNINonLinear" / 'acpc2standard_byT1.dat')
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

def runDsiStudio(subjectId: str) -> bool:
  return \
    generateSrcFile(subjectId) and \
    reconstructImage(subjectId) and \
    trackFibres(subjectId)



def getDsiStudioTemplateIntoStandardSpace(subjectId: str) -> bool:
  # TODO.
  # One option is:
  # /home/reece/dsi-studio/dsi_studio --action=reg --from=/home/reece/dsi-studio/atlas/ICBM152_adult/ICBM152_adult.T1W.nii.gz --to=/home/reece/HCIM/core/Human-Connectome-Investigating-Modularity/data/subjects/100307/MNINonLinear/T1w.nii.gz  --output_warp=/home/reece/HCIM/core/Human-Connectome-Investigating-Modularity/data/subjects/100307/MNINonLinear/dsistudioTemplate2standard.nii.gz --output=/home/reece/HCIM/core/Human-Connectome-Investigating-Modularity/data/subjects/100307/MNINonLinear/ignoreme.nii.gz

  # Then:
  # /home/reece/dsi-studio/dsi_studio --action=reg --apply_warp=/home/reece/HCIM/core/Human-Connectome-Investigating-Modularity/data/subjects/100307/T1w/Diffusion/template_1m0.nii.gz --warp=/home/reece/HCIM/core/Human-Connectome-Investigating-Modularity/data/subjects/100307/MNINonLinear/dsistudioTemplate2standard.nii.gz.map.gz --output=/home/reece/HCIM/core/Human-Connectome-Investigating-Modularity/data/subjects/100307/MNINonLinear/templateTrackWarped.nii.gz

  # Alternatively, get fMRI into diffusion space
  # wb_command -surface-apply-warpfield /home/reece/HCIM/core/Human-Connectome-Investigating-Modularity/data/subjects/100307/MNINonLinear/fsaverage_LR32k/100307.L.pial.32k_fs_LR.surf.gii  /home/reece/HCIM/core/Human-Connectome-Investigating-Modularity/data/subjects/100307/MNINonLinear/xfms/acpc_dc2standard.nii.gz  /home/reece/HCIM/core/Human-Connectome-Investigating-Modularity/data/subjects/100307/MNINonLinear/output.surf.gii -fnirt /home/reece/HCIM/core/Human-Connectome-Investigating-Modularity/data/subjects/100307/MNINonLinear/xfms/standard2acpc_dc.nii.gz
  return True

def matlabProcessDiffusion(subjectId: str) -> bool:
  
  g.logger.info("Running MATLAB: converting tracked fibres into endpoints and adjacency matrices.")
  subjectFolder = config.DATA_DIR / 'subjects' / subjectId

  # Downsampled surface files (e.g., 32k)
  subjectDownsampledFolder = subjectFolder / config.IMAGES["FMRI"]["LOW_RES"]["SURFACE"]["FOLDER"]
  subjectLowResSurfacePath_left = subjectFolder / config.IMAGES["FMRI"]["LOW_RES"]["SURFACE"]["FOLDER"] / config.IMAGES["FMRI"]["LOW_RES"]["SURFACE"]["L_HEMISPHERE_PATH"].replace("$subjectId$",subjectId)
  subjectLowResSurfacePath_right = subjectFolder / config.IMAGES["FMRI"]["LOW_RES"]["SURFACE"]["FOLDER"] / config.IMAGES["FMRI"]["LOW_RES"]["SURFACE"]["R_HEMISPHERE_PATH"].replace("$subjectId$",subjectId)

  # Original/high-resolution surface files (e.g., native or 164k).
  subjectHiResSurfaceFolder = subjectFolder / config.IMAGES["FMRI"]["HIGH_RES"]["SURFACE"]["FOLDER"] 
  subjectHiResSurface_left = subjectHiResSurfaceFolder / config.IMAGES["FMRI"]["HIGH_RES"]["SURFACE"]["L_HEMISPHERE_PATH"].replace("$subjectId$",subjectId)
  subjectHiResSurface_right = subjectHiResSurfaceFolder / config.IMAGES["FMRI"]["HIGH_RES"]["SURFACE"]["R_HEMISPHERE_PATH"].replace("$subjectId$",subjectId)

  
  # Ensure necessary files exist from previous steps.
  anatomicalLabelsToExist: list[str] = anatomicalLabels.anatomicalLabelsToExist
  remoteFilesToExist: "list[Path]" = [
                  (subjectFolder / config.NATIVEORMNI152FOLDER / 'aparc+aseg.nii.gz'),
                  (subjectFolder / 'T1w' / subjectId / 'mri' / 'transforms' / 'talairach.xfm'),
                  subjectHiResSurface_left,
                  subjectHiResSurface_right,
                  ]
  
  localFilesToExist: "list[Path]" = [\
    (subjectFolder / 'T1w' / config.DIFFUSION_FOLDER / ('1m'+str(currentIteration)+'.trk')) for currentIteration in range(0, config.DSI_STUDIO_ITERATION_COUNT, 1)] + [\
      (subjectFolder / config.NATIVEORMNI152FOLDER / subjectId / 'label' / 'label_type2' / label) for label in anatomicalLabelsToExist]

  # Ensure, if required, the downsampled meshes already exist.
  if(config.USE_PRESET_DOWNSAMPLED_MESH):
    remoteFilesToExist.append(subjectLowResSurfacePath_left)
    remoteFilesToExist.append(subjectLowResSurfacePath_right)
  else:
    # We will create our own downsampled surfaces, so ensure the folder exists. 
    createDirectories(directoryPaths=[subjectDownsampledFolder], createParents=True, throwErrorIfExists=False)
  
  _ = [getFile(localPath=fileToExist) for fileToExist in remoteFilesToExist]
  _ = [getFile(localPath=fileToExist, localOnly=True) for fileToExist in localFilesToExist]

  subjectDownsampledFolder.resolve(strict=True)
  return call(cmdLabel="MATLAB",
              cmd=[
                      config.MATLAB,
                      f'-batch "batch_process \'{config.matLabDriveAndPathToSubjects}\' \'{subjectId}\' {config.PIAL_SURFACE_TYPE} \'{config.DOWNSAMPLE_SURFACE}\' \'{config.DOWNSAMPLE_RATE}\' \'{config.DSI_STUDIO_ITERATION_COUNT}\' \'{config.USE_PRESET_DOWNSAMPLED_MESH}\' \'{subjectLowResSurfacePath_left.resolve(strict=False)}\' \'{subjectLowResSurfacePath_right.resolve(strict=False)}\'"',
                      ],
              cwd=config.matlabScriptsFolder)