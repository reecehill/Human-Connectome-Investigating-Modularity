function [] = exportStrucModulesToCsv(pathToFile,subject,downsample)

disp('loading modules.mat');
useROI = true;
fileToLoad=[pathToFile,'/optimal_struc_modules.mat'];
load(fileToLoad, ...
    "modules"...
    );
%% Structural modules
disp('loading labelSRF.mat');
fileToLoad=[pathToFile,'/labelSRF.mat'];
load(fileToLoad, ...
    'lo_centroidsL', 'lo_centroidsR',......
    'lo_faceROIidL', 'lo_faceROIidR',...
    'hi_faceROIidL', 'hi_faceROIidR',...
    'lo_faceROIidSubCor', 'hi_faceROIidSubCor',...
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

% Convert NaN to -1
leftNaNValues = isnan(modulesByFace.left_structural_modulesByROIId(:,2));
modulesByFace.left_structural_modulesByROIId(leftNaNValues,2) = -1;
rightNaNValues = isnan(modulesByFace.right_structural_modulesByROIId(:,2));
modulesByFace.right_structural_modulesByROIId(rightNaNValues,2) = -1;

% Convert to string and drop index.
modulesByFace.left_structural_modulesByROIId = string(modulesByFace.left_structural_modulesByROIId(:,2));
modulesByFace.right_structural_modulesByROIId = string(modulesByFace.right_structural_modulesByROIId(:,2));

writematrix(modulesByFace.left_structural_modulesByROIId',[pathToFile,'/exported_modules/left_structural_modules.csv'],"Delimiter",',',"QuoteStrings","all",'WriteMode', 'overwrite');
writematrix(modulesByFace.right_structural_modulesByROIId',[pathToFile,'/exported_modules/right_structural_modules.csv'],"Delimiter","comma","QuoteStrings","all",'WriteMode', 'overwrite');
writematrix(modulesByFace.left_structural_modulesByAllId(:,2)',[pathToFile,'/exported_modules/all_left_structural_modules.csv'],"Delimiter",',',"QuoteStrings","all",'WriteMode', 'overwrite');
writematrix(modulesByFace.right_structural_modulesByAllId(:,2)',[pathToFile,'/exported_modules/all_right_structural_modules.csv'],"Delimiter","comma","QuoteStrings","all",'WriteMode', 'overwrite');


% Additionally, write centroid coordinates to csv.
writematrix(string(lo_centroidsL(roiL_ids,1:3)),[pathToFile,'/left_coordinatesByROIId.csv'],"Delimiter","comma","QuoteStrings","all",'WriteMode', 'overwrite');
writematrix(string(lo_centroidsR(roiR_ids-length(faceROI_L),1:3)),[pathToFile,'/right_coordinatesByROIId.csv'],"Delimiter","comma","QuoteStrings","all",'WriteMode', 'overwrite');

end