function [faceModules_struc] = assignModulesToStructuralFaces(pathToFile,subject,downsample)
disp('loading communities.mat');
useROI = true;
fileToLoad=[pathToFile,'/',subject,'/optimal_modules.mat'];
load(fileToLoad, ...
    "modules",...
    "optimal_gamma"...
    );

disp('loading labelSRF.mat');
fileToLoad=[pathToFile,'/',subject,'/labelSRF.mat'];
load(fileToLoad, ...
    'lo_faceROIidL', 'lo_faceROIidR',...
    'hi_faceROIidL', 'hi_faceROIidR',...
    'lo_subROIid',...
    'hi_subROIid',...
    'filenames',...
    'subfilenames'); % not used: "faceROIidL", "faceROIidR", "filenames", "subROIid", "subfilenames"


if strcmp(downsample,'no') % method for no downsample
    faceROI_L=hi_faceROIidL(:,1);
    faceROI_R=hi_faceROIidR(:,1);
    labelIds=[hi_faceROIidL(:,1); hi_faceROIidR(:,1); double(max(hi_faceROIidR(:,1)))+hi_subROIid];
    %faceROI_L=[hi_faceROIidL(:,1); hi_faceROIidR(:,1); hi_subROIid+length(filenames)];
else
    labelIds=[lo_faceROIidL(:,1); lo_faceROIidR(:,1); double(max(lo_faceROIidR(:,1)))+lo_subROIid];
    faceROI_L=lo_faceROIidL(:,1);
    faceROI_R=lo_faceROIidR(:,1);
    %faceROI_all=[lo_faceROIidL(:,1); lo_faceROIidR(:,1); lo_subROIid+length(filenames)];
end

if(useROI)
    % If ROI is used, then the faceIDs are going to relative to the
    % ROI. We must now scale them up to the whole hemisphere.
    indicesOfLabelledFaces = labelIds >= 1; %ignore NaNs
    plottedLabelIds = labelIds(indicesOfLabelledFaces);
    allFileNames = [filenames subfilenames];
    plottedLabelsNames=allFileNames(plottedLabelIds);
    [~, I] =sort(string(plottedLabelsNames), 'ascend');
    plottedLabelIdsSorted=plottedLabelIds(I);
    roi = "lh.L_precentral";
    roiIds = find(contains(allFileNames,roi));
    roiL_ids = find(ismember(plottedLabelIdsSorted(:,1),roiIds));
    roi = "rh.R_precentral";
    roiIds = find(contains(allFileNames,roi));
    roiR_ids = find(ismember(plottedLabelIdsSorted(:,1),roiIds));
end

modulesByFace = struct();
moduleSets = fieldnames(modules);
for moduleSetIndex=1:length(moduleSets)
    moduleName = moduleSets(moduleSetIndex);
    moduleSet = modules.(moduleName{:});
    nModules = length(moduleSet);
    nFaces = length([moduleSet{:}]);
    modulesByFace.([moduleName{:},'_modulesByROIId']) = zeros(nFaces,2);
    modulesByFace.([moduleName{:},'_modulesByROIId'])(:,1) = 1:1:nFaces;
    modulesByFace.([moduleName{:},'_modulesByAllId']) = zeros(length(labelIds),2);
    modulesByFace.([moduleName{:},'_modulesByAllId'])(:,1) = 1:1:length(labelIds);

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
            module_allIds = roiR_ids(moduleSet{moduleIndex}+1); %add 1 as python starts counting from zero.            
        else
            disp("ERROR: Module file does not contain left or right modules.")
        end
        modulesByFace.([moduleName{:},'_modulesByAllId'])(module_allIds,2) = moduleIndex;
        
    end
    %modulesByFace.([moduleName{:},'_modulesByAllId'])(modulesByFace.([moduleName{:},'_modulesByAllId'])(:,2)==0,:) = [];
end




filename=[pathToFile,'/',subject,'/modulesByFace.mat'];
save(filename,...
    'modulesByFace',...
    '-v7');
end