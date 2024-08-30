function [faceModules_struc] = assignModulesToStructuralFaces(pathToFile,subject,downsample)
disp('loading communities.mat');
useROI = true;
fileToLoad=[pathToFile,'/',subject,'/optimal_modules.mat'];
load(fileToLoad, ...
    "modules",...
    "optimal_gamma"...
    );

%% Structural modules
disp('loading labelSRF.mat');
fileToLoad=[pathToFile,'/',subject,'/labelSRF.mat'];
load(fileToLoad, ...
    'lo_glpfaces','lo_grpfaces',...
    'hi_glpfaces','hi_grpfaces',...
    'hi_glpvertex','hi_grpvertex',...
    'lo_glpvertex','lo_grpvertex',...
    'lo_faceROIidL', 'lo_faceROIidR',...
    'hi_faceROIidL', 'hi_faceROIidR',...
    'lo_faceROIidSubCor',...
    'hi_faceROIidSubCor',...
    'filenames',...
    'subfilenames'); % not used: "faceROIidL", "faceROIidR", "filenames", "subROIid", "subfilenames"


if strcmp(downsample,'no') % method for no downsample
    faceROI_L=hi_faceROIidL(:,1);
    faceROI_R=hi_faceROIidR(:,1);
    labelIds=[hi_faceROIidL(:,1); hi_faceROIidR(:,1); double(max(hi_faceROIidR(:,1)))+hi_faceROIidSubCor];
    %faceROI_L=[hi_faceROIidL(:,1); hi_faceROIidR(:,1); hi_faceROIidSubCor+length(filenames)];
else
    labelIds=[lo_faceROIidL(:,1); lo_faceROIidR(:,1); double(max(lo_faceROIidR(:,1)))+lo_faceROIidSubCor];
    faceROI_L=lo_faceROIidL(:,1);
    faceROI_R=lo_faceROIidR(:,1);
    %faceROI_all=[lo_faceROIidL(:,1); lo_faceROIidR(:,1); lo_faceROIidSubCor+length(filenames)];
end

if(useROI)
    % If ROI is used, then the faceIDs are going to relative to the
    % ROI. We must now scale them up to the whole hemisphere.
    allFileNames = [filenames subfilenames];
    
    roi = "lh.L_precentral";
    roiIds = find(contains(allFileNames,roi));
    roiL_ids = find(ismember(labelIds(:,1),roiIds));

    roi = "rh.R_precentral";
    roiIds = find(contains(allFileNames,roi));
    roiR_ids = find(ismember(labelIds(:,1),roiIds));
end

modulesByFace = struct();
moduleSets = fieldnames(modules);
for moduleSetIndex=1:length(moduleSets)
    moduleName = moduleSets(moduleSetIndex);
    moduleSet = modules.(moduleName{:});
    nModules = length(moduleSet);
    nFaces = length([moduleSet{:}]);
    if(contains(moduleName{:},'left'))
        modulesByFace.([moduleName{:},'_modulesByROIId']) = zeros(nFaces,2);
        modulesByFace.([moduleName{:},'_modulesByROIId'])(:,1) = roiL_ids;
        modulesByFace.([moduleName{:},'_modulesByAllId']) = zeros(length(faceROI_L),2);
        modulesByFace.([moduleName{:},'_modulesByAllId'])(:,1) = 1:1:length(faceROI_L);
    elseif(contains(moduleName{:},'right'))
        modulesByFace.([moduleName{:},'_modulesByROIId']) = zeros(nFaces,2);
        modulesByFace.([moduleName{:},'_modulesByROIId'])(:,1) = roiR_ids;
        modulesByFace.([moduleName{:},'_modulesByAllId']) = zeros(length(faceROI_R),2);
        modulesByFace.([moduleName{:},'_modulesByAllId'])(:,1) = 1:1:length(faceROI_R);
    else
        disp("ERROR: Module name incorrectly set")
    end

    for moduleIndex=1:1:nModules
        % Set module assignment by ROI face ID (from zero).
        module_roiIds = moduleSet{moduleIndex}+1; %add 1 as python starts counting from zero.
        modulesByFace.([moduleName{:},'_modulesByROIId'])(module_roiIds,2) = moduleIndex;

        % Set module assignment by all face IDs.
        if(contains(moduleName{:},'left'))
            % ROI is of left.
            module_allIds = roiL_ids(moduleSet{moduleIndex}+1); %add 1 as python starts counting from zero.
        elseif(contains(moduleName{:},'right'))
            % ROI is of right.
            %TODO: Labels arrive with rh offset by length of lh labels. Does
            %this make sense?
            module_allIds = roiR_ids(moduleSet{moduleIndex}+1)-length(faceROI_L); %add 1 as python starts counting from zero.            
        else
            disp("ERROR: Module file does not contain left or right modules.")
        end
        
        modulesByFace.([moduleName{:},'_modulesByAllId'])(module_allIds,2) = moduleIndex;
        
    end
    %modulesByFace.([moduleName{:},'_modulesByAllId'])(modulesByFace.([moduleName{:},'_modulesByAllId'])(:,2)==0,:) = [];
end



%% Functional modules

[moduleFacevert_L ,moduleFacevert_R, nbmodules] = getModuleByFaceVertex(pathToFile,subject);

minModule_L = min(cat(1,moduleFacevert_L.id));
maxModule_L = max(cat(1,moduleFacevert_L.id));
[L_facesROI] = loopROIAndAssignLabels(minModule_L, maxModule_L, lo_glpfaces, moduleFacevert_L);

minModule_R = min(cat(1,moduleFacevert_R.id));
maxModule_R = max(cat(1,moduleFacevert_R.id));
[R_facesROI] = loopROIAndAssignLabels(minModule_R, maxModule_R, lo_grpfaces, moduleFacevert_R);

modulesByFace.left_functional_modulesByAllId(:,1) = [1:1:length(L_facesROI)];
modulesByFace.left_functional_modulesByAllId(:,2) = L_facesROI(:,4);
modulesByFace.right_functional_modulesByAllId(:,1) = [1:1:length(R_facesROI)];
modulesByFace.right_functional_modulesByAllId(:,2) = R_facesROI(:,4);


fmriCifti_L = ft_read_cifti([pathToFile,'/',subject,'/MNINonLinear/Results/tfMRI_MOTOR/tfMRI_MOTOR_hp200_s2_level2_MSMAll.feat/',subject,'_tfMRI_MOTOR_level2_hp200_s2_MSMAll_',subject,'_tfMRI_MOTOR_level2_LF-AVG_hp200_s2_MSMAll.dscalar.nii']);
strucCifti_mock = struct();
strucCifti_mock.dscalar = modulesByFace.left_structural_modulesByAllId(:,2);
strucCifti_mock.pos=[lo_glpvertex; lo_grpvertex];
strucCifti_mock.dimord='pos';
strucCifti_mock.tri=[lo_glpfaces; lo_grpfaces];
%strucCifti_mock.brainstructure = strucCifti_mock.brainstructure(1:length(strucCifti_mock.pos));
%ft_write_cifti([pathToFile,'/',subject,'/MNINonLinear/Results/tfMRI_MOTOR/tfMRI_MOTOR_hp200_s2_level2_MSMAll.feat/',subject,'_tfMRI_MOTOR_level2_hp200_s2_MSMAll_',subject,'_tfMRI_MOTOR_level2_LF-AVG_hp200_s2_MSMAll_structuralModules.dscalar.nii'], strucCifti_mock, 'parameter', 'dscalar','writesurface',false);

fmriModules(:,1) = 1:1:length(fmriCifti_L.dscalar);
fmriModules(:,2) = fmriCifti_L.dscalar;

%TODO: In progress, trying to get fmri values to align with structural when
%visualised.
% gifti_L = gifti([pathToFile,'/',subject,'/MNINonLinear/fsaverage_LR32k/100307.L.pial_MSMAll.32k_fs_LR.surf.gii']);
% gifti_R = gifti([pathToFile,'/',subject,'/MNINonLinear/fsaverage_LR32k/100307.R.pial_MSMAll.32k_fs_LR.surf.gii']);
% nfl = gifti_L.faces;
% nfr = gifti_R.faces;
% nvl = gifti_L.vertices;
% nvr = gifti_R.vertices;
% totalVertices = length(nvl) + length(nvr);
% totalVertices_downsampled = length(lo_glpvertex) + length(lo_grpvertex);
% totalFmriDataPoints = length(fmriModules);
% 
% 
% fmriModules(isnan(fmriModules)) = 0;


filename=[pathToFile,'/',subject,'/modulesByFace.mat'];
save(filename,...
    'modulesByFace',...
    '-v7');
end