function convertIntensityToCoordinates(pathToParticipants,subjectId)
adj_matrix = matfile([pathToParticipants '/' subjectId '/matrices.mat']).adj_matrix;
load([pathToParticipants '/' subjectId '/labelSRF.mat'],"nvl","nvr","nfl","nfr","glpfaces","glpvertex","grpfaces","grpvertex","faceROIidL","faceROIidR","subROIid","filenames","subfilenames");
    allBrainData.leftHemisphere.labels.ids = faceROIidL;
    allBrainData.rightHemisphere.labels.ids = faceROIidR;
    allBrainData.leftHemisphere.labels.names = filenames( allBrainData.leftHemisphere.labels.ids);
    allBrainData.rightHemisphere.labels.names = filenames( allBrainData.rightHemisphere.labels.ids);
    allBrainData.subCortical.labels.names = transpose(subfilenames(subROIid));

disp('Sorting DWI data into modules...');
disp("Left hemisphere:")

[leftOptimalGamma] = findOptimalGamma(pathToParticipants, subjectId, ...
    roiStructuralData.leftHemisphere.adjacencyMatrix, 0.6, 1.4, visualiseData)

end