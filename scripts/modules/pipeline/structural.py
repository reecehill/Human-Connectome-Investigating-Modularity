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