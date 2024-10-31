function [] = exportStrucFuncModulesToCifti()
%% Create dscalar of structural and functional modules.
sampleCifti = ft_read_cifti([pathToFile,'/',subject,'/MNINonLinear/Results/tfMRI_MOTOR/tfMRI_MOTOR_hp200_s2_level2_MSMAll.feat/',subject,'_tfMRI_MOTOR_level2_hp200_s2_MSMAll.dscalar.nii'], 'readdata',true,'mapname','array');
newCifti = sampleCifti;
newCifti.dscalar = NaN([length(sampleCifti.dscalar) 1]);
newCifti.mapname = cell([1,1]);
nStrucModules_L = length(unique(modulesByFace.left_structural_modulesByAllId(:,2)));
nFuncModules_L = length(unique(modulesByFace.left_functional_modulesByAllId(:,2)));

% Add structural modules to cifti
newCifti.dscalar(newCifti.brainstructure==1,1) = mapFaceValuesToNodes(modulesByFace.left_structural_modulesByAllId(:,2),lo_glpvertex,lo_faceToNodeMapLH);
newCifti.dscalar(newCifti.brainstructure==2,1) = mapFaceValuesToNodes(modulesByFace.right_structural_modulesByAllId(:,2),lo_grpvertex,lo_faceToNodeMapRH);
newCifti.dscalar(isnan(newCifti.dscalar(:,1))) = -1;

newCifti.mapname{1} = 'structural_modules';
ft_write_cifti([pathToFile,'/',subject,'/MNINonLinear/Results/tfMRI_MOTOR/tfMRI_MOTOR_hp200_s2_level2_MSMAll.feat/',subject,'_structuralModules'], newCifti, 'parameter', 'dscalar','writesurface',false);

end