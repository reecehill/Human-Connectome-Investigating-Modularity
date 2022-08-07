function convertIntensityToCoordinates(pathToParticipants, subject) 
    %% Load in conditions
    SPM = load([pathToParticipants '/' subject '/1stlevel/SPM.mat']);
    nConditions = length(SPM.SPM.xCon);
    
    for conditionIndex=[1:nConditions]
        %% Load voxels from SPM fMRI results report (binarised data)
        % For all of the contrasts produced by SPM, get the MNI co-ordinates of
        % voxels that were identified as being above a threshold of activation (binary).
        binarisedVoxels = spm_vol([pathToParticipants '/' subject '/1stlevel/spmT_000' num2str(conditionIndex) '_allClusters.nii']);
        [intensitiesPerVoxel, funcXyzCoordinatesmm] = spm_read_vols(binarisedVoxels);
        funcXyzCoordinatesmm = transpose(funcXyzCoordinatesmm); % transpose to match struct data.


        %% Sort voxels into "modules"
        % Here, a module is found by grouping adjacent active voxels together if their
        % faces, edges, or corners touch with another voxel that is active (=1).
        % For more: https://uk.mathworks.com/help/images/ref/bwlabeln.html
        fmriModules = bwlabeln(intensitiesPerVoxel, 26);
        nModules = max(fmriModules, [], 'all');
        filename=[pathToParticipants '/' subject '/1stlevel/fMRIModules_000' num2str(conditionIndex) '.mat'];
        save(filename,'intensitiesPerVoxel','funcXyzCoordinatesmm','fmriModules','nModules','-v7.3');
    end
end