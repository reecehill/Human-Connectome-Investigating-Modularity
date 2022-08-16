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
  mri_convert "$SUBJECTS_DIR/anat/T1w.nii.gz" "$SUBJECTS_DIR/anat/T1w.nii";
  recon-all -i "$SUBJECTS_DIR/anat/T1w.nii" -s "bert" -T2 "$SUBJECTS_DIR/anat/spc_T2w.nii" -T2pial -all;
  mri_convert "$SUBJECTS_DIR/bert/mri/T1.mgz" "$SUBJECTS_DIR/bert/mri/T1.nii";
}
### get aparc+aseg.nii
function getAparcAsecNii {
  # $1 = $SUBJECTS_DIR
  echo  "Called getAparcAsecNii";
  mri_convert "$SUBJECTS_DIR/bert/mri/aparc+aseg.mgz" "$SUBJECTS_DIR/bert/mri/aparc+aseg.nii"
  if [ ! -f $SUBJECTS_DIR/bert/mri/aparc+aseg.nii ]; then
    echo "There was an error. Freesurfer did not convert aparc+aseg.mgz -> aparc+aseg.nii.";
    exit 0;
  fi
   mri_binarize --i "$SUBJECTS_DIR/bert/mri/aparc+aseg.mgz" --gm --o "$SUBJECTS_DIR/bert/mri/gm.nii";
  if [ ! -f $SUBJECTS_DIR/bert/mri/gm.nii ]; then
    echo "There was an error. Freesurfer could not create gm.nii from aparc+aseg.mgz";
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

function getTransformationMatrices {
  mri_info --vox2ras-tkr ${SUBJECTS_DIR}/func/task-HcpMotor_acq-ap_bold.nii --o ${SUBJECTS_DIR}/func/vox2ras-tkr.csv
}
if [ "$dataToUse" = 'U' ]; then 
  runFreesurferReconAll;
  getAparcAsecNii;
  getROILabels;
  getTransformationMatrices;
elif [ "$dataToUse" = 'P' ]; then 
  getAparcAsecNii;
  getROILabels;
  getTransformationMatrices;
else
  echo  "You must enter either U or P.";
  exit;
fi;