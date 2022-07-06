#!/bin/bash
export FS_LICENSE=$1
export FREESURFER_HOME=/usr/local/freesurfer
source $FREESURFER_HOME/SetUpFreeSurfer.sh
export pathto_participants=$2
export dataToUse=$3

function runFreesurferReconAll {
  ### recon-all to processing data
  mri_convert "${SUBJECTS_DIR}/${subj}_T1.nii.gz" "${SUBJECTS_DIR}/${subj}_T1.nii"
  recon-all -i "${SUBJECTS_DIR}/${subj}_T1.nii" -s ${subj} -all
}
### get aparc+aseg.nii
function getAparcAsecNii {
  mri_convert $SUBJECTS_DIR/bert/mri/aparc+aseg.mgz $SUBJECTS_DIR/bert/mri/aparc+aseg.nii;
}

function getROILabels {
  ### get 68 ROI labels based on pial file
# The pial file is provided by FreeSurfer.
mri_annotation2label --subject "bert" --hemi lh --surf pial --outdir $SUBJECTS_DIR/bert/label/label_type2
mri_annotation2label --subject "bert" --hemi rh --surf pial --outdir $SUBJECTS_DIR/bert/label/label_type2

### get 68 ROI labels based on pial.surf.gii file
# The HCP dataset provides both pial.surf.gii AND alongside pial.  
#mri_annotation2label --subject "bert" --hemi lh --surf pial.surf.gii --outdir $SUBJECTS_DIR/bert/label/label_type1
#mri_annotation2label --subject "bert" --hemi rh --surf pial.surf.gii --outdir $SUBJECTS_DIR/bert/label/label_type1
}


cd $pathto_participants
i=0
for subj in $(cat $pathto_participants/file_list_HCP_all_subset.txt);do
((i += 1))

  export SUBJECTS_DIR=$pathto_participants/$subj/T1

  if [ "$dataToUse" = 'u' ]; then 
    runFreesurferReconAll;
    getAparcAsecNii;
    getROILabels;
  elif [ "$dataToUse" = 'p' ]; then 
    getAparcAsecNii;
    getROILabels;
  else
    echo "You must enter either u or p."
  fi;

done
