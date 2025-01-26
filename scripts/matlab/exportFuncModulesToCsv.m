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

faceROI_L=lo_faceROIidL(:,1);
%faceROI_R=lo_faceROIidR(:,1);
[roiL_ids, roiR_ids] = getROIIds(pathToFile, downsample, 'lh.L_precentral', 'rh.R_precentral');

for conditionIndex=1:length(conditions)
    condition = char(conditions(conditionIndex));
    modulesByFace = struct();

    % Left hemisphere functional modules
    [moduleFacevert_L ,moduleFacevert_R, ~] = getModuleByFaceVertex(pathToFile,subject,upper(condition));

    allModules_L = unique(cat(1,moduleFacevert_L.id));
    [lo_faceModuleL,~] = loopROIAndAssignLabels(1, length(allModules_L), lo_glpfaces, moduleFacevert_L);
    lo_faceModuleL = lo_faceModuleL(:,4);

    % Right hemisphere functional modules
    allModules_R = unique(cat(1,moduleFacevert_R.id));
    [lo_faceModuleR,~] = loopROIAndAssignLabels(1,  length(allModules_R), lo_grpfaces, moduleFacevert_R);
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