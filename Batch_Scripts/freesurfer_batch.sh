#!/bin/bash
export FREESURFER_HOME=/usr/local/freesurfer
source $FREESURFER_HOME/SetUpFreeSurfer.sh
export pathto_participants=/mnt/c/Users/Reece/Documents/Dissertation/Data/Dissertation/Data/Participants

cd $pathto_participants
i=0
for subj in $(cat $pathto_participants/file_list_BSD_all_subset.txt);do
((i += 1))
export SUBJECTS_DIR=$pathto_participants/$subj/T1w/$subj
### recon-all to processing data
recon-all -i $SUBJECTS_DIR/T1.nii.gz -s bert -all
### get aparc+aseg.nii
mri_convert $SUBJECTS_DIR/bert/mri/aparc+aseg.mgz $SUBJECTS_DIR/bert/mri/aparc+aseg.nii
### get 68 ROI labels based on pial file
mri_annotation2label --subject bert --hemi lh --surf pial --outdir $SUBJECTS_DIR/bert/label/label_type2
mri_annotation2label --subject bert --hemi rh --surf pial --outdir $SUBJECTS_DIR/bert/label/label_type2
### get 68 ROI labels based on pial.surf.gii file
#mri_annotation2label --subject bert --hemi lh --surf pial.surf.gii --outdir $SUBJECTS_DIR/bert/label/label_type1
#mri_annotation2label --subject bert --hemi rh --surf pial.surf.gii --outdir $SUBJECTS_DIR/bert/label/label_type1

done
