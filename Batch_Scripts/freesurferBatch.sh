#!/bin/bash
export FS_LICENSE=$1
export FREESURFER_HOME=/usr/local/freesurfer
source $FREESURFER_HOME/SetUpFreeSurfer.sh
export pathToParticipants=$2
export subjectId=$3
export dataToUse=$4
export SUBJECTS_DIR="$pathToParticipants/$subjectId/data";
cd $pathToParticipants

function runFreesurferReconAll {
  ### recon-all to processing data
  mri_convert "$SUBJECTS_DIR/anat/T1w.nii.gz" "$SUBJECTS_DIR/anat/T1w.nii"
  recon-all -i "$SUBJECTS_DIR/anat/T1w.nii" -s "bert" -all
}
### get aparc+aseg.nii
function getAparcAsecNii {
  # $1 = $SUBJECTS_DIR
  echo  "Called getAparcAsecNii";
  mri_convert "$SUBJECTS_DIR/bert/mri/aparc+aseg.mgz" "$SUBJECTS_DIR/bert/mri/aparc+aseg.nii"
  if [ ! -f $SUBJECTS_DIR/bert/mri/aparc+aseg.nii ]; then
    echo "There was an error. Freesurfer did not convert aparc+aseg.mgz -> .nii.";
    exit 0;
  fi
}

function getROILabels {
  # "Since normalization can introduce unwanted interpolations into the data, we can run our ROI analyses in native space using the parcellations from FreeSurfer" (https://andysbrainbook.readthedocs.io/en/latest/ML/ML_AppendixA_AFNI_Code.html?highlight=mri_annotation2label#creating-rois-from-freesurfer)

  ### get 68 ROI labels based on pial file
  echo  "Called getROILabels"
  echo  "$SUBJECTS_DIR";
  # The pial file is provided by FreeSurfer.
  mri_annotation2label --subject "bert" --hemi lh --surf pial --outdir $SUBJECTS_DIR/bert/label/label_type2
  mri_annotation2label --subject "bert" --hemi rh --surf pial --outdir $SUBJECTS_DIR/bert/label/label_type2

### get 68 ROI labels based on pial.surf.gii file
# The HCP dataset provides both pial.surf.gii AND alongside pial.  
#mri_annotation2label --subject "bert" --hemi lh --surf pial.surf.gii --outdir $SUBJECTS_DIR/bert/label/label_type1
#mri_annotation2label --subject "bert" --hemi rh --surf pial.surf.gii --outdir $SUBJECTS_DIR/bert/label/label_type1
}

if [ "$dataToUse" = 'U' ]; then 
  runFreesurferReconAll;
  getAparcAsecNii;
  getROILabels;
elif [ "$dataToUse" = 'P' ]; then 
  getAparcAsecNii;
  getROILabels;
else
  echo  "You must enter either U or P.";
  exit;
fi;