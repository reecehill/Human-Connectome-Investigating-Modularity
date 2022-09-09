#!/bin/bash
export FS_LICENSE=$1
export FREESURFER_HOME=/usr/local/freesurfer
source $FREESURFER_HOME/SetUpFreeSurfer.sh
export pathToParticipants=$2
export subjectId=$3
export SUBJECTS_DIR="$pathToParticipants/$subjectId/data";
cd $pathToParticipants;

#tkregister2 --mov "${SUBJECTS_DIR}/func/sartask-HcpMotor_acq-ap_bold.nii" --s ${subjectId}/data/  --noedit --regheader --reg "${SUBJECTS_DIR}/func/register.dat" --targ "${SUBJECTS_DIR}/bert/mri/orig.mgz"; 

# Get tranformation matrix that was used to go from mean fMRI image, to coregistered fMRI (fMRI gets moved, so that aligns with stationary T1 image)
tkregister2 --mov "${SUBJECTS_DIR}/func/meantask-HcpMotor_acq-ap_bold.nii" --s ${subjectId}/data/  --noedit --regheader --reg "${SUBJECTS_DIR}/func/register.dat" --targ "${SUBJECTS_DIR}/func/rmeantask-HcpMotor_acq-ap_bold.nii"

# TODO: Change this to just use the inverse of meanFmri->fMri
# Get transformation matrix that converts T1 to rT1 (into fMRI space)
tkregister2 --mov "${SUBJECTS_DIR}/bert/mri/T1.nii" --s ${subjectId}/data/  --noedit --regheader --reg "${SUBJECTS_DIR}/bert/mri/register.dat" --targ "${SUBJECTS_DIR}/bert/mri/rT1.nii"

# Since rT1 is in fMRI space, apply the transformation used T1->rT1 on the aparc+aseg and its precentral_gyrus mask, to ensure these can be used in fmri.
mri_vol2vol --mov "${SUBJECTS_DIR}/bert/mri/aparc+aseg.nii" --reg "${SUBJECTS_DIR}/bert/mri/register.dat" --o "${SUBJECTS_DIR}/bert/mri/realigned_aparc+aseg.nii" --no-resample --targ "${SUBJECTS_DIR}/bert/mri/rT1.nii"
mri_vol2vol --mov "${SUBJECTS_DIR}/bert/mri/precentral_gyrus.nii" --reg "${SUBJECTS_DIR}/bert/mri/register.dat" --o "${SUBJECTS_DIR}/bert/mri/realigned_precentral_gyrus.nii" --no-resample --targ "${SUBJECTS_DIR}/bert/mri/rT1.nii"