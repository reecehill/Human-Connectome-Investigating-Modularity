function findStructuralModularity_new(pathToParticipants,subjectId)
addpath('toolboxes/bct');
gcp;
adj_matrix = matfile([pathToParticipants '/' subjectId '/matrices.mat']).adj_matrix;
load([pathToParticipants '/' subjectId '/labelSRF.mat'],...
    'lo_faceROIidL', 'lo_faceROIidR',...
    'hi_faceROIidL', 'hi_faceROIidR',...
    'lo_glpfaces', 'lo_grpfaces',...
    'hi_glpfaces', 'hi_grpfaces',...
    'lo_glpvertex', 'lo_grpvertex',...
    'hi_glpvertex', 'hi_grpvertex',...
    'lo_centroidsSubCor',  'hi_centroidsSubCor',...
    'lo_faceROIidSubCor', 'hi_faceROIidSubCor', ...
    "filenames","subfilenames");

disp('Sorting DWI data into modules...');
disp("Left hemisphere:")
visualiseData = false;

downsample=true;
if(downsample)
    labelIds=[lo_faceROIidL(:,1); lo_faceROIidR(:,1); double(max(lo_faceROIidR(:,1)))+lo_faceROIidSubCor];
else
    labelIds=[hi_faceROIidL(:,1); hi_faceROIidR(:,1); double(max(hi_faceROIidR(:,1)))+hi_faceROIidSubCor];
end

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

[nnzIds_row, nnzIds_col, ~] = find(adj_matrix(I([roiL_ids; roiR_ids]),I([roiL_ids; roiR_ids])));

[leftOptimalGamma] = findOptimalGamma(pathToParticipants, subjectId, ...
    adj_matrix(...
    nnzIds_row, ...
    nnzIds_col ...
    ), 0.6, 0.62, visualiseData);
disp(leftOptimalGamma);
end