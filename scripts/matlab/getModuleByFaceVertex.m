function [moduleFacevert_L,moduleFacevert_R, nbmodules] = getModuleByFaceVertex(pathToFile,subject)
    % Function that stores the vertices (or maybe face) location of each anatomical label.
    % NB: Note that subcortical regions are unsupported.

    L_cifti = ft_read_cifti([pathToFile,'/',subject,'/MNINonLinear/Results/tfMRI_MOTOR/tfMRI_MOTOR_hp200_s2_level2_MSMAll.feat/',subject,'_tfMRI_MOTOR_level2_hp200_s2_MSMAll_',subject,'_tfMRI_MOTOR_level2_LF_hp200_s2_MSMAll_ROI_L_clusters.dscalar.nii']);
    all_L_modules = L_cifti.dscalar(L_cifti.brainstructure==1);
    all_L_modules(isnan(all_L_modules)) = 0;
    R_cifti = ft_read_cifti([pathToFile,'/',subject,'/MNINonLinear/Results/tfMRI_MOTOR/tfMRI_MOTOR_hp200_s2_level2_MSMAll.feat/',subject,'_tfMRI_MOTOR_level2_hp200_s2_MSMAll_',subject,'_tfMRI_MOTOR_level2_LF_hp200_s2_MSMAll_ROI_R_clusters.dscalar.nii']);
    all_R_modules = R_cifti.dscalar(R_cifti.brainstructure==2);
    all_R_modules(isnan(all_R_modules)) = 0;

    L_modules = unique(all_L_modules);
    nbLmodules = length(L_modules);
    parfor moduleIndex=1:nbLmodules
        moduleFacevert_L(moduleIndex,1).id=moduleIndex;
        moduleFacevert_L(moduleIndex,1).faces=find(all_L_modules == L_modules(moduleIndex)); 
    end

    R_modules = unique(all_R_modules);
    nbRmodules = length(R_modules);
    parfor moduleIndex=1:nbRmodules
        % Modules in right hemisphere are offset by those in left.
        moduleFacevert_R(moduleIndex,1).id=moduleIndex;
        moduleFacevert_R(moduleIndex,1).faces=find(all_R_modules == R_modules(moduleIndex)); 
    end
    
    nbmodules = nbLmodules + nbRmodules;

end