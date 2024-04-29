function findStructuralModularity(pathToParticipants,subject,conditionIndex,visualiseData)
%% Parameters
    roiLabels = ["L_precentral.label"]; % only supports single values for now.
%% Load external parameters
    adj_matrix = matfile([pathToParticipants '/' subject '/matrices.mat']).adj_matrix;
    load([pathToParticipants '/' subject '/labelSRF.mat'],"nvl","nvr","nfl","nfr","glpfaces","glpvertex","grpfaces","grpvertex","faceROIidL","faceROIidR","subROIid","filenames","subfilenames");
    load([pathToParticipants '/' subject '/edgeList.mat'], "lpcentroids","rpcentroids","subCoor");
    %load([pathToParticipants '/' subject '/MNIcoor.mat'],"Coor_MNI152");
    %load([pathToParticipants '/' subject '/1stlevel/fMRIModules_000' num2str(conditionIndex) '.mat'], "fmriModules");

%% Integrate/handle labels into dataset.
    allBrainData.leftHemisphere.labels.ids = faceROIidL;
    allBrainData.rightHemisphere.labels.ids = faceROIidR;
    allBrainData.leftHemisphere.labels.names = filenames( allBrainData.leftHemisphere.labels.ids);
    allBrainData.rightHemisphere.labels.names = filenames( allBrainData.rightHemisphere.labels.ids);
    allBrainData.subCortical.labels.names = transpose(subfilenames(subROIid));

%% Initialize
    % ROI Anatomical Data
    % Add region of interest data (face IDs and centroids).
    roiStructuralData.leftHemisphere.surf.faceIdsOfAllBrain = find(ismember(allBrainData.leftHemisphere.labels.names,strcat('lh.',roiLabels)));
    roiStructuralData.leftHemisphere.adjacencyMatrix = adj_matrix(roiStructuralData.leftHemisphere.surf.faceIdsOfAllBrain,roiStructuralData.leftHemisphere.surf.faceIdsOfAllBrain);
%% ROI Structural Data
    disp('Sorting DWI data into modules...');

    if(size(roiStructuralData.leftHemisphere.adjacencyMatrix,1) > 0)
        if(isfile([pathToParticipants '/' subject '/moduleResults/leftStructuralModules.mat']))
            load([pathToParticipants '/' subject '/moduleResults/leftStructuralModules.mat'], "leftStructuralModules");
            [allBrainData.leftHemisphere.surf.faces(roiStructuralData.leftHemisphere.surf.faceIdsOfAllBrain,4)] = leftStructuralModules;
        else
            if(isfile([pathToParticipants '/' subject '/moduleResults/leftOptimalGamma.mat']))
                load([pathToParticipants '/' subject '/moduleResults/leftOptimalGamma.mat'], "leftOptimalGamma");
                allBrainData.leftHemisphere.optimalGamma = leftOptimalGamma;
            else
                %[leftOptimalGamma] = findOptimalGamma(pathToParticipants, subject, roiStructuralData.leftHemisphere.adjacencyMatrix, 0.6, 1.4, visualiseData)
                [leftOptimalGamma] = findOptimalGamma(pathToParticipants, subject, roiStructuralData.leftHemisphere.adjacencyMatrix, 0.4, 0.42, visualiseData)
                allBrainData.leftHemisphere.optimalGamma = leftOptimalGamma;
                filename=[pathToParticipants '/' subject '/moduleResults/leftOptimalGamma.mat'];
                save(filename,'leftOptimalGamma','-v7.3');
            end
            [allBrainData.leftHemisphere.surf.faces(roiStructuralData.leftHemisphere.surf.faceIdsOfAllBrain,4), allBrainData.leftHemisphere.Q1] = sortIntoModules(roiStructuralData.leftHemisphere.adjacencyMatrix, allBrainData.leftHemisphere.optimalGamma);
            filename=[pathToParticipants '/' subject '/moduleResults/leftStructuralModules.mat'];
            leftStructuralModules = allBrainData.leftHemisphere.surf.faces(roiStructuralData.leftHemisphere.surf.faceIdsOfAllBrain,4);
            save(filename,'leftStructuralModules','-v7.3');
        end
    else
        allBrainData.leftHemisphere.optimalGamma = [];
    end


    if(size(roiStructuralData.rightHemisphere.adjacencyMatrix,1) > 0)
        if(isfile([pathToParticipants '/' subject '/moduleResults/rightStructuralModules.mat']))
            load([pathToParticipants '/' subject '/moduleResults/rightStructuralModules.mat'], "rightStructuralModules");
            [allBrainData.rightHemisphere.surf.faces(roiStructuralData.rightHemisphere.surf.faceIdsOfAllBrain,4)] = rightStructuralModules;
        else
            if(isfile([pathToParticipants '/' subject '/moduleResults/rightOptimalGamma.mat']))
                load([pathToParticipants '/' subject '/moduleResults/rightOptimalGamma.mat'], "rightOptimalGamma");
                allBrainData.rightHemisphere.optimalGamma = rightOptimalGamma;
            else
                [rightOptimalGamma] = findOptimalGamma(pathToParticipants, subject, roiStructuralData.rightHemisphere.adjacencyMatrix, 0.6, 1.4, visualiseData)
                %[rightOptimalGamma] = findOptimalGamma(pathToParticipants, subject, roiStructuralData.rightHemisphere.adjacencyMatrix, 0.7, 0.8, visualiseData)
                allBrainData.rightHemisphere.optimalGamma = rightOptimalGamma;
                filename=[pathToParticipants '/' subject '/moduleResults/rightOptimalGamma.mat'];
                save(filename,'rightOptimalGamma','-v7.3');
            end
            [allBrainData.rightHemisphere.surf.faces(roiStructuralData.rightHemisphere.surf.faceIdsOfAllBrain,4), allBrainData.rightHemisphere.Q1] = sortIntoModules(roiStructuralData.rightHemisphere.adjacencyMatrix, allBrainData.rightHemisphere.optimalGamma);
            filename=[pathToParticipants '/' subject '/moduleResults/rightStructuralModules.mat'];
            rightStructuralModules = allBrainData.rightHemisphere.surf.faces(roiStructuralData.rightHemisphere.surf.faceIdsOfAllBrain,4);
            save(filename,'rightStructuralModules','-v7.3');
        end
    else
        allBrainData.rightHemisphere.optimalGamma = [];
    end
end