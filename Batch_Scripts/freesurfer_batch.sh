#!/bin/bash
export FS_LICENSE=/mnt/c/Users/Reece/Documents/Dissertation/freesurfer/license.txt
export FREESURFER_HOME=/usr/local/freesurfer
source $FREESURFER_HOME/SetUpFreeSurfer.sh
export pathto_participants=/mnt/c/Users/Reece/Documents/Dissertation/Main/Participants


cd $pathto_participants
i=0
for subj in $(cat $pathto_participants/file_list_HCP_all_subset.txt);do
((i += 1))
export SUBJECTS_DIR=$pathto_participants/$subj/T1w

# Get T1.nii from T1.mgz, but do NOT place in same directory. 
mri_convert $SUBJECTS_DIR/$subj/mri/T1.mgz $SUBJECTS_DIR/T1.nii.gz


### recon-all to processing data
recon-all -i $SUBJECTS_DIR/T1.nii.gz -s $subj -all
### get aparc+aseg.nii
mri_convert $SUBJECTS_DIR/$subj/mri/aparc+aseg.mgz $SUBJECTS_DIR/$subj/mri/aparc+aseg.nii
### get 68 ROI labels based on pial file
mri_annotation2label --subject $subj --hemi lh --surf pial --outdir $SUBJECTS_DIR/$subj/label/label_type2
mri_annotation2label --subject $subj --hemi rh --surf pial --outdir $SUBJECTS_DIR/$subj/label/label_type2
### get 68 ROI labels based on pial.surf.gii file
#mri_annotation2label --subject $subj --hemi lh --surf pial.surf.gii --outdir $SUBJECTS_DIR/$subj/label/label_type1
#mri_annotation2label --subject $subj --hemi rh --surf pial.surf.gii --outdir $SUBJECTS_DIR/$subj/label/label_type1

done
