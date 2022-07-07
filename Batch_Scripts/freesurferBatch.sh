#!/bin/bash
export FS_LICENSE=$1
export FREESURFER_HOME=/usr/local/freesurfer
source $FREESURFER_HOME/SetUpFreeSurfer.sh
export pathToParticipants=$2
export subjectId=$3
export dataToUse=$4
export subjectsDir="$pathToParticipants/$subjectId/T1w";
cd $pathToParticipants

function runFreesurferReconAll {
  ### recon-all to processing data
  mri_convert "$subjectsDir/T1.nii.gz" "$subjectsDir/T1.nii"
  recon-all -i "$subjectsDir/T1.nii" -s $subjectId -all
}
### get aparc+aseg.nii
getAparcAsecNii() {
  # $1 = $subjectsDir
  echo  "Called getAparcAsecNii";
  mri_convert "$subjectsDir/bert/mri/aparc+aseg.mgz" "$subjectsDir/bert/mri/aparc+aseg.nii"
  if [ ! -f $subjectsDir/bert/mri/aparc+aseg.nii ]; then
    echo "There was an error. Freesurfer did not convert aparc+aseg.mgz -> .nii.";
    exit 0;
  fi
}

getROILabels() {
  # $1 = $subjectsDir

  ### get 68 ROI labels based on pial file
  echo  "Called getROILabels"
  echo  "$subjectsDir";
  # The pial file is provided by FreeSurfer.
  mri_annotation2label --subject "bert" --hemi lh --surf pial --outdir $subjectsDir/bert/label/label_type2
  mri_annotation2label --subject "bert" --hemi rh --surf pial --outdir $subjectsDir/bert/label/label_type2

### get 68 ROI labels based on pial.surf.gii file
# The HCP dataset provides both pial.surf.gii AND alongside pial.  
#mri_annotation2label --subject "bert" --hemi lh --surf pial.surf.gii --outdir $subjectsDir/bert/label/label_type1
#mri_annotation2label --subject "bert" --hemi rh --surf pial.surf.gii --outdir $subjectsDir/bert/label/label_type1
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