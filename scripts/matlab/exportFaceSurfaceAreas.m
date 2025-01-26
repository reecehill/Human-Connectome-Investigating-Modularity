function [] = exportFaceSurfaceAreas(pathToFile,downsample)
addpath('toolboxes/FieldTrip');
ft_defaults;
ft_hastoolbox('iso2mesh',1);

disp('loading labelSRF.mat');
fileToLoad=[pathToFile,'/labelSRF.mat'];
load(fileToLoad, ...
    'lo_glpfaces', 'lo_grpfaces',...
    'lo_glpvertex', 'lo_grpvertex',...
    'lo_faceROIidL','lo_faceROIidR', 'lo_faceROIidSubCor',...
    'filenames', 'subfilenames'...
    );

faceROI_L=lo_faceROIidL(:,1);
%faceROI_R=lo_faceROIidR(:,1);

[roiL_ids, roiR_ids] = getROIIds(pathToFile, downsample, 'lh.L_precentral', 'rh.R_precentral');

lo_faceSurfaceAreas_L = elemvolume(lo_glpvertex,lo_glpfaces(roiL_ids,1:3));
lo_faceSurfaceAreas_R = elemvolume(lo_grpvertex,lo_grpfaces(roiR_ids-length(faceROI_L),1:3));

% Convert to string.
lo_faceSurfaceAreas_L = string(lo_faceSurfaceAreas_L);
lo_faceSurfaceAreas_R = string(lo_faceSurfaceAreas_R);

% Write to .csv
writematrix(lo_faceSurfaceAreas_L',[pathToFile,'/face_surface_areas/left_sa_by_face.csv'],"Delimiter",',',"QuoteStrings","all",'WriteMode', 'overwrite');
writematrix(lo_faceSurfaceAreas_R',[pathToFile,'/face_surface_areas/right_sa_by_face.csv'],"Delimiter",',',"QuoteStrings","all",'WriteMode', 'overwrite');

disp("Written face surface areas.");

end