function [] = exportRoiIds(pathToFile,downsample)

[roiL_ids, roiR_ids] = getROIIds(pathToFile, downsample, 'lh.L_precentral', 'rh.R_precentral');

% Stringify
roiL_ids = string(roiL_ids);
roiR_ids = string(roiR_ids);

% Write to .csv
writematrix(roiL_ids',[pathToFile,'/left_ROIids.csv'],"Delimiter",',',"QuoteStrings","all",'WriteMode', 'overwrite');
writematrix(roiR_ids',[pathToFile,'/right_ROIids.csv'],"Delimiter",',',"QuoteStrings","all",'WriteMode', 'overwrite');
disp("Written ROI ids.");
end