function [roiL_ids, roiR_ids] = getROIIds(pathToFile, downsample, roiFilename_L, roiFilename_R)
fileToLoad=[pathToFile,'/labelSRF.mat'];
load(fileToLoad, ...
    'hi_faceROIidL','hi_faceROIidR', 'hi_faceROIidSubCor', ...
    'lo_faceROIidL','lo_faceROIidR', 'lo_faceROIidSubCor' ,...
    'filenames', 'subfilenames'...
    ); % not used: "faceROIidL", "faceROIidR", "filenames", "subROIid", "subfilenames"

if strcmp(downsample,'no') % method for no downsample
    faceROI_L=hi_faceROIidL(:,1);
    %faceROI_R=hi_faceROIidR(:,1);
    labelIds=[hi_faceROIidL(:,1); hi_faceROIidR(:,1); double(max(hi_faceROIidR(:,1)))+hi_faceROIidSubCor];
    %faceROI_L=[hi_faceROIidL(:,1); hi_faceROIidR(:,1); hi_faceROIidSubCor+length(filenames)];
else
    labelIds=[lo_faceROIidL(:,1); lo_faceROIidR(:,1); double(max(lo_faceROIidR(:,1)))+lo_faceROIidSubCor];
    faceROI_L=lo_faceROIidL(:,1);
    %faceROI_R=lo_faceROIidR(:,1);
    %faceROI_all=[lo_faceROIidL(:,1); lo_faceROIidR(:,1); lo_faceROIidSubCor+length(filenames)];
end

useROI=true;
if(useROI)
    % If ROI is used, then the faceIDs are going to be relative to the
    % ROI. We must now scale them up to the whole hemisphere.
    allFileNames = [filenames subfilenames];
    
    roiIds_L = find(contains(allFileNames,roiFilename_L));
    roiL_ids = find(ismember(labelIds(:,1),roiIds_L));

    roiIds_R = find(contains(allFileNames,roiFilename_R));
    roiR_ids = find(ismember(labelIds(:,1),roiIds_R));
end
end