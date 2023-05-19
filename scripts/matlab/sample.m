function sample()
t1_r = niftiread('../../data/subjects/100610/T1w/T1w_acpc_dc.nii.gz');
t1_r_mni152 = niftiread('../../data/subjects/100610/MNINonLinear/T1w.nii.gz');

diff_r = niftiread('../../data/subjects/100610/T1w/Diffusion/data.nii.gz');
diff_r_mni152 = '?'

left_pial_32k = gifti('/home/reece/HCIM/core/Human-Connectome-Investigating-Modularity/data/subjects/100610/MNINonLinear/fsaverage_LR32k/100610.L.pial_MSMAll.32k_fs_LR.surf.gii')
right_pial_32k = gifti('/home/reece/HCIM/core/Human-Connectome-Investigating-Modularity/data/subjects/100610/MNINonLinear/fsaverage_LR32k/100610.R.pial_MSMAll.32k_fs_LR.surf.gii')

mycifti = ft_read_cifti('/home/reece/HCIM/core/Human-Connectome-Investigating-Modularity/data/subjects/100610/MNINonLinear/Results/tfMRI_MOTOR/tfMRI_MOTOR_hp200_s2_level2_MSMAll.feat/100610_tfMRI_MOTOR_level2_hp200_s2_MSMAll.dscalar.nii')

figure;
plotsurf(right_pial_32k.vertices,right_pial_32k.faces,mycifti.x100610_tfmri_motor_level2_lf_hp200_s2_msmall(mycifti.brainstructure==2))
end