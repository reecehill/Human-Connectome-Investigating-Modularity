#!/bin/bash
export FS_LICENSE=$1
export FREESURFER_HOME=/usr/local/freesurfer
source $FREESURFER_HOME/SetUpFreeSurfer.sh
export pathToParticipants=$2
export subjectId=$3
export SUBJECTS_DIR="$pathToParticipants/$subjectId/data";
cd $pathToParticipants;

  tkregister2 --mov "${SUBJECTS_DIR}/func/sartask-HcpMotor_acq-ap_bold.nii" --s ${subjectId}/data/  --noedit --regheader --reg "${SUBJECTS_DIR}/func/register.dat" --targ "${SUBJECTS_DIR}/bert/mri/orig.mgz"; 
