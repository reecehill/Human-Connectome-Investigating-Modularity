#!/bin/bash
export FS_LICENSE=$1
export FREESURFER_HOME=/usr/local/freesurfer
source $FREESURFER_HOME/SetUpFreeSurfer.sh
export pathto_participants=$2


cd $pathto_participants
i=0
for subj in $(cat $pathto_participants/file_list_HCP_all_subset.txt);do
((i += 1))


export SUBJECTS_DIR=$pathto_participants/$subj/unprocessed/3T/T1w_MPR1

### recon-all to processing data
mri_convert "${SUBJECTS_DIR}/${subj}_3T_T1w_MPR1.nii.gz" "${SUBJECTS_DIR}/${subj}_3T_T1w_MPR1.nii"
recon-all -i "${SUBJECTS_DIR}/${subj}_3T_T1w_MPR1.nii" -s "bert" -all
exit;


### get aparc+aseg.nii
mri_convert $SUBJECTS_DIR/bert/mri/aparc+aseg.mgz $SUBJECTS_DIR/bert/mri/aparc+aseg.nii
### get 68 ROI labels based on pial file
mri_annotation2label --subject "bert" --hemi lh --surf pial --outdir $SUBJECTS_DIR/bert/label/label_type2
mri_annotation2label --subject "bert" --hemi rh --surf pial --outdir $SUBJECTS_DIR/bert/label/label_type2
### get 68 ROI labels based on pial.surf.gii file
#mri_annotation2label --subject "bert" --hemi lh --surf pial.surf.gii --outdir $SUBJECTS_DIR/bert/label/label_type1
#mri_annotation2label --subject "bert" --hemi rh --surf pial.surf.gii --outdir $SUBJECTS_DIR/bert/label/label_type1

done
