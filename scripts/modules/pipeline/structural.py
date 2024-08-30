import os
import modules.globals as g
import config
from modules.file_directory.file_directory import createDirectories
from modules.hcp_data_manager.downloader import getFile
from modules.subprocess_caller.call import *

def generateLabels(subjectId: str) -> bool:
  g.logger.info("Running Freesurfer: generating label files by annotating the pial surfaces.")
  g.logger.info(f"SUBJECTS_DIR: {os.environ['SUBJECTS_DIR']}")
  subjectDir = config.SUBJECTS_DIR / subjectId / "T1w"
  outputDir = subjectDir / subjectId / 'label' / 'label_type2'
  createDirectories(directoryPaths=[outputDir], createParents=True, throwErrorIfExists=False)
  outputPath = (outputDir).resolve(strict=True).__str__()

  # Ensure pial and annot files exist.
  filesToExist = [
                  (subjectDir / subjectId / 'surf' / 'lh.pial'),
                  (subjectDir / subjectId / 'surf' / 'rh.pial'),
                  (subjectDir / subjectId / 'label' / 'lh.aparc.annot'),
                  (subjectDir / subjectId / 'label' / 'rh.aparc.annot'),
                  ]
  _ = [getFile(localPath=fileToExist) for fileToExist in filesToExist]
  
  lhLabelsSuccess = call(cmdLabel="Freesurfer",
              cmd=[
                "mri_annotation2label",
                "--subject",
                subjectId,
                "--hemi",
                "lh",
                "--surf",
                "pial",
                "--sd",
                subjectDir,
                "--outdir",
                outputPath
                ])
  
  rhLabelsSuccess = call(cmdLabel="Freesurfer",
              cmd=[
                "mri_annotation2label",
                "--subject",
                subjectId,
                "--hemi",
                "rh",
                "--surf",
                "pial",
                "--sd",
                subjectDir,
                "--outdir",
                outputPath
                ])
  
  return (lhLabelsSuccess and rhLabelsSuccess)

def generateMni152Labels(subjectId: str) -> bool:
  g.logger.info("Running Freesurfer: generating label files in Native/MNI152 space by annotating the pial surfaces.")
  g.logger.info(f"SUBJECTS_DIR: {os.environ['SUBJECTS_DIR']}")
  subjectDir = config.SUBJECTS_DIR / subjectId / config.NATIVEORMNI152FOLDER
  labelDir: config.Path = subjectDir / subjectId / 'label' / 'label_type2'
  surfDir = subjectDir / subjectId / 'surf'
  createDirectories(directoryPaths=[labelDir, surfDir], createParents=True, throwErrorIfExists=False)
  outputPath = (labelDir).resolve(strict=True).__str__()

  # Ensure pial and annot files (both (gifti format) exist.
  filesToExist = [
                  # TODO: Do not hard code this file name?
                  (subjectDir  / 'fsaverage_LR32k' / f'{subjectId}.R.pial.32k_fs_LR.surf.gii'), # Right surface
                  (subjectDir  / 'fsaverage_LR32k' / f'{subjectId}.L.pial.32k_fs_LR.surf.gii'), # Left surface
                  (subjectDir  / 'fsaverage_LR32k' / f'{subjectId}.R.aparc.32k_fs_LR.label.gii'), # Right annotation
                  (subjectDir  / 'fsaverage_LR32k' / f'{subjectId}.L.aparc.32k_fs_LR.label.gii'), # Left annotation
                  ]
                  # (subjectDir  / f'{subjectId}.R.pial_MSMAll.164k_fs_LR.surf.gii'), # Right surface
                  # (subjectDir  / f'{subjectId}.L.pial_MSMAll.164k_fs_LR.surf.gii'), # Left surface
                  # (subjectDir  / f'{subjectId}.R.aparc.164k_fs_LR.label.gii'), # Right annotation
                  # (subjectDir  / f'{subjectId}.L.aparc.164k_fs_LR.label.gii'), # Left annotation
                  # ]
  surfaceAndAnnotFiles = [getFile(localPath=fileToExist) for fileToExist in filesToExist]

  rhGiftiSurfaceToFreesurferSuccess = call(cmdLabel="Freesurfer",
              cmd=[
                "mris_convert",
                surfaceAndAnnotFiles[0],
                surfDir / 'rh.pial'
                ])
  lhGiftiSurfaceToFreesurferSuccess = call(cmdLabel="Freesurfer",
              cmd=[
                "mris_convert",
                surfaceAndAnnotFiles[1],
                surfDir / 'lh.pial'
                ])

  rhGiftiLabelToFreesurferSuccess = call(cmdLabel="Freesurfer",
              cmd=[
                "mris_convert",
                "--annot",
                surfaceAndAnnotFiles[2],
                surfaceAndAnnotFiles[0],
                surfDir / 'rh.aparc.annot'
                ])

  lhGiftiLabelToFreesurferSuccess = call(cmdLabel="Freesurfer",
              cmd=[
                "mris_convert",
                "--annot",
                surfaceAndAnnotFiles[3],
                surfaceAndAnnotFiles[1],
                surfDir / 'lh.aparc.annot'
                ])
  
  rhLabelsSuccess = call(cmdLabel="Freesurfer",
              cmd=[
                "mri_annotation2label",
                "--subject",
                subjectId,
                "--hemi",
                "rh",
                "--surf",
                "pial",
                "--annotation",
                surfDir / 'rh.aparc.annot',
                # "--label",
                # "24",
                "--sd",
                subjectDir,
                "--outdir",
                outputPath
                ])
  
  lhLabelsSuccess = call(cmdLabel="Freesurfer",
              cmd=[
                "mri_annotation2label",
                "--subject",
                subjectId,
                "--hemi",
                "lh",
                "--surf",
                "pial",
                "--annotation",
                surfDir / 'lh.aparc.annot',
                # "--label",
                # "24",
                "--sd",
                subjectDir,
                "--outdir",
                outputPath
                ])

  g.logger.info("Tidying anatomical label file names.")
  lhLabelPath = labelDir / 'lh.???.label'
  if(lhLabelPath.exists()):
    lhLabelPath.rename(labelDir / 'lh.L_unknown.label')
    g.logger.info("lh.???.label -> lh.L_unknown.label")
  else:
    g.logger.info("lh.???.label does not exist...")

  rhLabelPath = labelDir / 'rh.???.label'
  if(rhLabelPath.exists()):
    rhLabelPath.rename(labelDir / 'rh.R_unknown.label')
    g.logger.info("rh.???.label -> rh.R_unknown.label")
  else:
    g.logger.info("rh.???.label does not exist...")
  
  return (
    rhGiftiSurfaceToFreesurferSuccess and
    lhGiftiSurfaceToFreesurferSuccess and
    rhGiftiLabelToFreesurferSuccess and
    lhGiftiLabelToFreesurferSuccess and
    rhLabelsSuccess and
    lhLabelsSuccess)