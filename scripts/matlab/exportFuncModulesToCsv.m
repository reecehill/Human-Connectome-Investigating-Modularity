function [] = exportFuncModulesToCsv(pathToFile,subject,downsample,conditions)
conditions = textscan(conditions(2:end-1), '%s','Delimiter',{',',char("'")},'MultipleDelimsAsOne',true); % Used to enable conversion of character array (from python) to cell string array
conditions = conditions{:};
disp('loading labelSRF.mat');
fileToLoad=[pathToFile,'/labelSRF.mat'];
load(fileToLoad, ...
    'hi_faceROIidL','hi_faceROIidR', 'hi_faceROIidSubCor', ...
    'lo_faceROIidL','lo_faceROIidR', 'lo_faceROIidSubCor' ,...
    'lo_glpfaces', 'lo_grpfaces',...
    'filenames', 'subfilenames'...
    ); % not used: "faceROIidL", "faceROIidR", "filenames", "subROIid", "subfilenames"

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

useROI=true;
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

for conditionIndex=1:length(conditions)
    condition = char(conditions(conditionIndex));
    modulesByFace = struct();

    % Left hemisphere functional modules
    [moduleFacevert_L ,moduleFacevert_R, ~] = getModuleByFaceVertex(pathToFile,subject,upper(condition));

    minModule_L = min(cat(1,moduleFacevert_L.id));
    maxModule_L = max(cat(1,moduleFacevert_L.id));
    [lo_faceModuleL,~] = loopROIAndAssignLabels(minModule_L, maxModule_L, lo_glpfaces, moduleFacevert_L);
    lo_faceModuleL = lo_faceModuleL(:,4);

    % Right hemisphere functional modules
    minModule_R = min(cat(1,moduleFacevert_R.id));
    maxModule_R = max(cat(1,moduleFacevert_R.id));
    [lo_faceModuleR,~] = loopROIAndAssignLabels(minModule_R, maxModule_R, lo_grpfaces, moduleFacevert_R);
    lo_faceModuleR = lo_faceModuleR(:,4);


    modulesByFace.left_functional_modulesByAllId(:,1) = lo_faceModuleL;
    modulesByFace.right_functional_modulesByAllId(:,1) = lo_faceModuleR;
    modulesByFace.left_functional_modulesByROIId = modulesByFace.left_functional_modulesByAllId(roiL_ids);
    modulesByFace.right_functional_modulesByROIId = modulesByFace.right_functional_modulesByAllId(roiR_ids-length(faceROI_L));

    % Convert NaN to -1
    leftNaNValues = isnan(modulesByFace.left_functional_modulesByROIId(:,1));
    modulesByFace.left_functional_modulesByROIId(leftNaNValues,1) = -1;
    rightNaNValues = isnan(modulesByFace.right_functional_modulesByROIId(:,1));
    modulesByFace.right_functional_modulesByROIId(rightNaNValues,1) = -1;

    % Convert to string.
    modulesByFace.left_functional_modulesByROIId = string(modulesByFace.left_functional_modulesByROIId(:,1));
    modulesByFace.right_functional_modulesByROIId = string(modulesByFace.right_functional_modulesByROIId(:,1));

    % Write structural and functional (filtered by condition) to .csv
    writematrix(modulesByFace.left_functional_modulesByROIId',[pathToFile,'/exported_modules/left_',condition,'_functional_modules.csv'],"Delimiter",',',"QuoteStrings","all",'WriteMode', 'overwrite');
    writematrix(modulesByFace.right_functional_modulesByROIId',[pathToFile,'/exported_modules/right_',condition,'_functional_modules.csv'],"Delimiter","comma","QuoteStrings","all",'WriteMode', 'overwrite');
end
end