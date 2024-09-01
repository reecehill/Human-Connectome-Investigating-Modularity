function [faceModules_struc] = assignModulesToStructuralFaces(pathToFile,subject,downsample)
disp('loading modules.mat');
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
        'lo_faceROIidL', 'lo_faceROIidR',...
        'hi_faceROIidL', 'hi_faceROIidR',...
        'lo_glpfaces', 'lo_grpfaces',...
        'hi_glpfaces', 'hi_grpfaces',...
        'lo_glpvertex', 'lo_grpvertex',...
        'hi_glpvertex', 'hi_grpvertex',...
        'lo_centroidsSubCor',  'hi_centroidsSubCor',...
        'lo_faceROIidSubCor', 'hi_faceROIidSubCor',...
        'lo_faceToNodeMapLH', 'lo_faceToNodeMapRH',...
        'hi_faceToNodeMapLH', 'hi_faceToNodeMapRH',...
        'lo_centroidsL', 'lo_centroidsR',...
        'hi_centroidsL', 'hi_centroidsR',...
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
[L_facesROI,L_faceToNodeMap] = loopROIAndAssignLabels(minModule_L, maxModule_L, lo_glpfaces, moduleFacevert_L);
[~,~,indicesWithModule_L] = intersect(L_facesROI(:,1:3),lo_glpfaces(:,1:3),'rows','stable');
lo_faceModuleL = lo_glpfaces;
lo_faceModuleL(:,4) = -1;
lo_faceModuleL(indicesWithModule_L,4) = L_facesROI(:,4);
lo_faceModuleL(lo_faceModuleL(:,4)==-1,4) = 0;
lo_faceModuleL = lo_faceModuleL(:,4);


minModule_R = min(cat(1,moduleFacevert_R.id));
maxModule_R = max(cat(1,moduleFacevert_R.id));
[R_facesROI,L_faceToNodeMap] = loopROIAndAssignLabels(minModule_R, maxModule_R, lo_grpfaces, moduleFacevert_R);
[~,~,indicesWithModule_R] = intersect(R_facesROI(:,1:3),lo_grpfaces(:,1:3),'rows','stable');
lo_faceModuleR = lo_grpfaces;
lo_faceModuleR(:,4) = -1;
lo_faceModuleR(indicesWithModule_R,4) = R_facesROI(:,4);
lo_faceModuleR(lo_faceModuleR(:,4)==-1,4) = 0;
lo_faceModuleR = lo_faceModuleR(:,4);


modulesByFace.left_functional_modulesByAllId(:,1) = [1:1:length(L_facesROI)];
modulesByFace.left_functional_modulesByAllId(:,2) = lo_faceModuleL;
modulesByFace.right_functional_modulesByAllId(:,1) = [1:1:length(R_facesROI)];
modulesByFace.right_functional_modulesByAllId(:,2) = lo_faceModuleR;

%% Create dscalar of structural and functional modules.
sampleCifti = ft_read_cifti([pathToFile,'/',subject,'/MNINonLinear/Results/tfMRI_MOTOR/tfMRI_MOTOR_hp200_s2_level2_MSMAll.feat/',subject,'_tfMRI_MOTOR_level2_hp200_s2_MSMAll.dscalar.nii'], 'readdata',true,'mapname','array');
newCifti = sampleCifti;
newCifti.dscalar = NaN([length(sampleCifti.dscalar) 1]);
newCifti.mapname = cell([1,1]);
nStrucModules_L = length(unique(modulesByFace.left_structural_modulesByAllId(:,2)));
nFuncModules_L = length(unique(modulesByFace.left_functional_modulesByAllId(:,2)));

% Add structural modules to cifti
newCifti.dscalar(newCifti.brainstructure==1,1) = mapFaceValuesToNodes(modulesByFace.left_structural_modulesByAllId(:,2),lo_glpvertex,lo_faceToNodeMapLH);
newCifti.dscalar(newCifti.brainstructure==2,1) =   mapFaceValuesToNodes(modulesByFace.right_structural_modulesByAllId(:,2),lo_grpvertex,lo_faceToNodeMapRH);
%newCifti.dscalar(isnan(newCifti.dscalar(:,1))) = 0;
newCifti.mapname{1} = 'structural_modules';
ft_write_cifti([pathToFile,'/',subject,'/MNINonLinear/Results/tfMRI_MOTOR/tfMRI_MOTOR_hp200_s2_level2_MSMAll.feat/',subject,'_structuralModules'], newCifti, 'parameter', 'dscalar','writesurface',false);



filename=[pathToFile,'/',subject,'/modulesByFace.mat'];
save(filename,...
    'modulesByFace',...
    '-v7');
end