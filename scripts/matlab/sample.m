function sample()
addpath(genpath('toolboxes/FieldTrip'));
%t1_r = niftiread('../../data/subjects/100610/T1w/T1w_acpc_dc.nii.gz');
t1_r_mni152 = niftiread('../../data/subjects/100610/MNINonLinear/T1w_restore_brain.nii.gz');

%diff_r = niftiread('../../data/subjects/100610/T1w/Diffusion/data.nii.gz');
diff_r_mni152 = '?'

left_pial_59k = gifti('../../data/subjects/100610/MNINonLinear/fsaverage_LR59k/100610.L.pial_MSMAll.59k_fs_LR.surf.gii')
left_pial_labels =  gifti('../../data/subjects/100610/MNINonLinear/fsaverage_LR59k/100610.L.aparc.59k_fs_LR.label.gii');
right_pial_59k = gifti('../../data/subjects/100610/MNINonLinear/fsaverage_LR59k/100610.R.pial_MSMAll.59k_fs_LR.surf.gii')

mycifti = ft_read_cifti('../../data/subjects/100610/MNINonLinear/Results/tfMRI_MOTOR/tfMRI_MOTOR_hp200_s2_level2_MSMAll.feat/100610_tfMRI_MOTOR_level2_hp200_s2_MSMAll.dscalar.nii')
close all;
figure;
plotsurf(right_pial_59k.vertices,right_pial_59k.faces,mycifti.x100610_tfmri_motor_level2_lf_hp200_s2_msmall(mycifti.brainstructure==2));
hold on;
plotsurf(left_pial_59k.vertices,left_pial_59k.faces,mycifti.x100610_tfmri_motor_level2_lf_hp200_s2_msmall(mycifti.brainstructure==1));

end