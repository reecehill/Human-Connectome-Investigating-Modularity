function [moduleFacevert_L,moduleFacevert_R, nbmodules] = getModuleByFaceVertex(pathToFile,subject,conditionName)
    % Function that stores the vertices (or maybe face) location of each anatomical label.
    % NB: Note that subcortical regions are unsupported.

    L_cifti = ft_read_cifti([pathToFile,'/MNINonLinear/Results/tfMRI_MOTOR/tfMRI_MOTOR_hp200_s2_level2_MSMAll.feat/',subject,'_tfMRI_MOTOR_level2_hp200_s2_MSMAll_',subject,'_tfMRI_MOTOR_level2_',conditionName,'_hp200_s2_MSMAll_ROI_L_clusters.dscalar.nii']);
    all_L_modules = L_cifti.dscalar(L_cifti.brainstructure==1);
    % The fMRI modules begin from 1 onwards. 0 is no module.
    all_L_modules(all_L_modules==0) = -1;
    all_L_modules(isnan(all_L_modules)) = -1;

    R_cifti = ft_read_cifti([pathToFile,'/MNINonLinear/Results/tfMRI_MOTOR/tfMRI_MOTOR_hp200_s2_level2_MSMAll.feat/',subject,'_tfMRI_MOTOR_level2_hp200_s2_MSMAll_',subject,'_tfMRI_MOTOR_level2_',conditionName,'_hp200_s2_MSMAll_ROI_R_clusters.dscalar.nii']);
    all_R_modules = R_cifti.dscalar(R_cifti.brainstructure==2); % add 1 as python indexing begins from zero.;
    all_R_modules(all_R_modules==0) = -1;
    all_R_modules(isnan(all_R_modules)) = -1;

    L_modules = unique(all_L_modules);
    nbLmodules = length(L_modules);
    parfor moduleIndex=1:nbLmodules
        moduleName = L_modules(moduleIndex);
        moduleFacevert_L(moduleIndex,1).id=moduleName;
        moduleFacevert_L(moduleIndex,1).faces=find(all_L_modules == moduleName); 
    end

    R_modules = unique(all_R_modules);
    nbRmodules = length(R_modules);
    parfor moduleIndex=1:nbRmodules
        moduleName = R_modules(moduleIndex);
        moduleFacevert_R(moduleIndex,1).id=moduleName;
        moduleFacevert_R(moduleIndex,1).faces=find(all_R_modules == moduleName); 
    end
    
    nbmodules = nbLmodules + nbRmodules;

end