function convertIntensityToCoordinates(pathToParticipants, subject)

%% Load in conditions
nConditions = 5., %Todo - automate this.

for conditionIndex=[1:nConditions]
    addpath(genpath('toolboxes/spm12'));

    %% Load voxels from preprocessed fMRI results report (binarised data)
    % For all of the contrasts produced by SPM, get the MNI co-ordinates of
    % voxels that were identified as being above a threshold of (zero) activation (binary).
    %binarisedVoxels = spm_vol([pathToParticipants '/' subject '/1stlevel/spmT_000' num2str(conditionIndex) '_allClustersBinary.nii']);

    intensitiesPerVoxel = ft_read_cifti('/home/reece/HCIM/core/Human-Connectome-Investigating-Modularity/data/subjects/100610/MNINonLinear/Results/tfMRI_MOTOR/tfMRI_MOTOR_hp200_s2_level2_MSMAll.feat/100610_tfMRI_MOTOR_level2_hp200_s2_MSMAll.dscalar.nii').x100610_tfmri_motor_level2_lf_hp200_s2_msmall;
    
    left_pial_32k = gifti('/home/reece/HCIM/core/Human-Connectome-Investigating-Modularity/data/subjects/100610/MNINonLinear/fsaverage_LR32k/100610.L.pial_MSMAll.32k_fs_LR.surf.gii').vertices;
    right_pial_32k = gifti('/home/reece/HCIM/core/Human-Connectome-Investigating-Modularity/data/subjects/100610/MNINonLinear/fsaverage_LR32k/100610.R.pial_MSMAll.32k_fs_LR.surf.gii').vertices;

    funcXyzCoordinatesmm = [left_pial_32k;right_pial_32k]; % transpose to match struct data format.


    %% Sort voxels into "modules"
    % Here, a module is found by grouping adjacent active voxels together if their
    % faces, edges, or corners touch with another voxel that is active (>0).
    % For more: https://uk.mathworks.com/help/images/ref/bwlabeln.html
    fmriModules = bwlabeln(intensitiesPerVoxel, 18);
    nModules = max(fmriModules, [], 'all');
    filename=[pathToParticipants '/' subject '/1stlevel/fMRIModules_000' num2str(conditionIndex) '.mat'];
    save(filename,'intensitiesPerVoxel','funcXyzCoordinatesmm','fmriModules','nModules','-v7.3');
    disp("SPM output has been sorted into modules and saved.");
end
end