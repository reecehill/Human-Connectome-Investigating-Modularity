function [leftCollectionOfMetrics, rightCollectionOfMetrics] = calculateOverlap(pathToParticipants, subject, conditionIndex, visualiseData)
clearvars -except pathToParticipants subject conditionIndex visualiseData;
addpath('C:\Users\Reece\AppData\Roaming\MathWorks\MATLAB Add-Ons\Collections\Iso2Mesh');
load([pathToParticipants '\' subject '\moduleResults\allBrainData__' num2str(conditionIndex) '.mat'], "allBrainData");
disp(['Calculating overlap for condition' conditionIndex]);

%% LEFT HEMISPHERE
leftOverlappingFaces = find(allBrainData.leftHemisphere.surf.faces(:,6) == 1);
leftOffset = max(allBrainData.leftHemisphere.surf.faces(:,5))+1;
allBrainData.leftHemisphere.surf.faces(allBrainData.leftHemisphere.surf.faces(:,5)>0,5) = allBrainData.leftHemisphere.surf.faces(allBrainData.leftHemisphere.surf.faces(:,5)>0,5) + leftOffset;
allBrainData.leftHemisphere.surf.faces(:,7) = allBrainData.leftHemisphere.surf.faces(:,4) + allBrainData.leftHemisphere.surf.faces(:,5);

%globalFunctionalModules = transpose(unique(allBrainData.leftHemisphere.surf.faces(allBrainData.leftHemisphere.surf.faces(:,5)>0,5)));

maxLeftStructuralModule = max(allBrainData.leftHemisphere.surf.faces(:,4),[],'all');
for moduleIndex=1:maxLeftStructuralModule
    %% For each module, get its outline.
    % Edges are defined by two indexes - the two nodes they connect.
    leftStrucModuleFacesIndexes{moduleIndex} = find(allBrainData.leftHemisphere.surf.faces(:,4) == moduleIndex);
    leftStrucModuleFacesBiggerThan1Indexes{moduleIndex} = length(find(allBrainData.leftHemisphere.surf.faces(:,4) == moduleIndex)) > 1;
    leftStrucModuleNodeIndexesTemp = allBrainData.leftHemisphere.surf.faces(leftStrucModuleFacesIndexes{moduleIndex},1:3);
    leftStrucModuleNodeIndexes = unique(leftStrucModuleNodeIndexesTemp(:));
    leftStrucModuleAreaMm{moduleIndex} = sum(elemvolume(allBrainData.leftHemisphere.surf.nodes(:,1:3),allBrainData.leftHemisphere.surf.faces(leftStrucModuleFacesIndexes{moduleIndex},1:3)));
    allBrainData.leftHemisphere.surf.nodes(leftStrucModuleNodeIndexes,4) = moduleIndex;
    [strucEdges{moduleIndex},~]=surfedge(allBrainData.leftHemisphere.surf.faces(leftStrucModuleFacesIndexes{moduleIndex},1:3));
end

leftFuncModuleIndexes = transpose(unique(allBrainData.leftHemisphere.surf.faces(leftOverlappingFaces,5)));
%funcModuleIndexes = transpose(unique(allBrainData.leftHemisphere.surf.faces(allBrainData.leftHemisphere.surf.faces(:,5)>0,5)));

for funcModuleIndex=leftFuncModuleIndexes
    leftFuncModuleFacesIndexes{funcModuleIndex} = intersect(leftOverlappingFaces,find(allBrainData.leftHemisphere.surf.faces(:,5) == funcModuleIndex));
    leftFuncModuleAreaMm{funcModuleIndex} = sum(elemvolume(allBrainData.leftHemisphere.surf.nodes(:,1:3),allBrainData.leftHemisphere.surf.faces(leftFuncModuleFacesIndexes{funcModuleIndex},1:3)));

    leftGlobalFuncModuleFacesIndexes{funcModuleIndex}= find(allBrainData.leftHemisphere.surf.faces(:,5) == funcModuleIndex);
    leftGlobalFuncModuleAreaMm{funcModuleIndex} = sum(elemvolume(allBrainData.leftHemisphere.surf.nodes(:,1:3),allBrainData.leftHemisphere.surf.faces(leftFuncModuleFacesIndexes{funcModuleIndex},1:3)));

    leftFuncModuleNodeIndexesTemp = allBrainData.leftHemisphere.surf.faces(leftFuncModuleFacesIndexes{funcModuleIndex},1:3);
    leftFuncModuleNodeIndexes{funcModuleIndex} = unique(leftFuncModuleNodeIndexesTemp(:));
    [leftFuncEdges{funcModuleIndex},~]=surfedge(allBrainData.leftHemisphere.surf.faces(leftFuncModuleFacesIndexes{funcModuleIndex},(1:3)));
end

%% Calculating overlap
leftOverlapMatrix = [{}];
leftModuleCounter=0;
for funcModuleIndex=leftFuncModuleIndexes
    leftModuleCounter = leftModuleCounter+1;
    % This gets all face ids - even those outside the ROI.
    leftFuncFaceIds = find(allBrainData.leftHemisphere.surf.faces(:,5) == funcModuleIndex);
    leftStrucModuleIds = transpose(unique(allBrainData.leftHemisphere.surf.faces(intersect(leftOverlappingFaces,leftFuncFaceIds),4)));
    for strucModuleIndex=leftStrucModuleIds
        leftStrucFaceIds = find(allBrainData.leftHemisphere.surf.faces(:,4) == strucModuleIndex);
        metrics.funcModuleId = funcModuleIndex;
        metrics.strucModuleId = strucModuleIndex;
        metrics.faceIdsOfOverlap = intersect(leftFuncFaceIds,leftStrucFaceIds);
        metrics.overlapArea = sum(elemvolume(allBrainData.leftHemisphere.surf.nodes(:,1:3),allBrainData.leftHemisphere.surf.faces(metrics.faceIdsOfOverlap,1:3)));
        metrics.areaOverlapAsPercentOfFunc = metrics.overlapArea / leftFuncModuleAreaMm{funcModuleIndex};
        metrics.areaOverlapAsPercentOfStruc = metrics.overlapArea / leftStrucModuleAreaMm{strucModuleIndex};
        leftOverlapMatrix = [leftOverlapMatrix; metrics];
        clear metrics;
    end
end
leftCollectionOfMetrics = cat(2,leftOverlapMatrix{:});




%% RIGHT HEMISPHERE
rightOverlappingFaces = find(allBrainData.rightHemisphere.surf.faces(:,6) == 1);
rightOffset = max(allBrainData.rightHemisphere.surf.faces(:,5))+1;
allBrainData.rightHemisphere.surf.faces(allBrainData.rightHemisphere.surf.faces(:,5)>0,5) = allBrainData.rightHemisphere.surf.faces(allBrainData.rightHemisphere.surf.faces(:,5)>0,5) + rightOffset;
allBrainData.rightHemisphere.surf.faces(:,7) = allBrainData.rightHemisphere.surf.faces(:,4) + allBrainData.rightHemisphere.surf.faces(:,5);

%globalFunctionalModules = transpose(unique(allBrainData.rightHemisphere.surf.faces(allBrainData.rightHemisphere.surf.faces(:,5)>0,5)));

maxRightStructuralModule = max(allBrainData.rightHemisphere.surf.faces(:,4),[],'all');
for moduleIndex=1:maxRightStructuralModule
    %% For each module, get its outline.
    % Edges are defined by two indexes - the two nodes they connect.
    rightStrucModuleFacesIndexes{moduleIndex} = find(allBrainData.rightHemisphere.surf.faces(:,4) == moduleIndex);
    rightStrucModuleFacesBiggerThan1Indexes{moduleIndex} = length(find(allBrainData.rightHemisphere.surf.faces(:,4) == moduleIndex)) > 1;
    rightStrucModuleNodeIndexesTemp = allBrainData.rightHemisphere.surf.faces(rightStrucModuleFacesIndexes{moduleIndex},1:3);
    rightStrucModuleNodeIndexes = unique(rightStrucModuleNodeIndexesTemp(:));
    rightStrucModuleAreaMm{moduleIndex} = sum(elemvolume(allBrainData.rightHemisphere.surf.nodes(:,1:3),allBrainData.rightHemisphere.surf.faces(rightStrucModuleFacesIndexes{moduleIndex},1:3)));
    allBrainData.rightHemisphere.surf.nodes(rightStrucModuleNodeIndexes,4) = moduleIndex;
    [strucEdges{moduleIndex},~]=surfedge(allBrainData.rightHemisphere.surf.faces(rightStrucModuleFacesIndexes{moduleIndex},1:3));
end

rightFuncModuleIndexes = transpose(unique(allBrainData.rightHemisphere.surf.faces(rightOverlappingFaces,5)));
%funcModuleIndexes = transpose(unique(allBrainData.rightHemisphere.surf.faces(allBrainData.rightHemisphere.surf.faces(:,5)>0,5)));

for funcModuleIndex=rightFuncModuleIndexes
    rightFuncModuleFacesIndexes{funcModuleIndex} = intersect(rightOverlappingFaces,find(allBrainData.rightHemisphere.surf.faces(:,5) == funcModuleIndex));
    rightFuncModuleAreaMm{funcModuleIndex} = sum(elemvolume(allBrainData.rightHemisphere.surf.nodes(:,1:3),allBrainData.rightHemisphere.surf.faces(rightFuncModuleFacesIndexes{funcModuleIndex},1:3)));

    rightGlobalFuncModuleFacesIndexes{funcModuleIndex}= find(allBrainData.rightHemisphere.surf.faces(:,5) == funcModuleIndex);
    rightGlobalFuncModuleAreaMm{funcModuleIndex} = sum(elemvolume(allBrainData.rightHemisphere.surf.nodes(:,1:3),allBrainData.rightHemisphere.surf.faces(rightFuncModuleFacesIndexes{funcModuleIndex},1:3)));

    rightFuncModuleNodeIndexesTemp = allBrainData.rightHemisphere.surf.faces(rightFuncModuleFacesIndexes{funcModuleIndex},1:3);
    rightFuncModuleNodeIndexes{funcModuleIndex} = unique(rightFuncModuleNodeIndexesTemp(:));
    [rightFuncEdges{funcModuleIndex},~]=surfedge(allBrainData.rightHemisphere.surf.faces(rightFuncModuleFacesIndexes{funcModuleIndex},(1:3)));
end

%% Calculating overlap
rightOverlapMatrix = [{}];
rightModuleCounter=0;
for funcModuleIndex=rightFuncModuleIndexes
    rightModuleCounter = rightModuleCounter+1;
    % This gets all face ids - even those outside the ROI.
    rightFuncFaceIds = find(allBrainData.rightHemisphere.surf.faces(:,5) == funcModuleIndex);
    rightStrucModuleIds = transpose(unique(allBrainData.rightHemisphere.surf.faces(intersect(rightOverlappingFaces,rightFuncFaceIds),4)));
    for strucModuleIndex=rightStrucModuleIds
        rightStrucFaceIds = find(allBrainData.rightHemisphere.surf.faces(:,4) == strucModuleIndex);
        metrics.funcModuleId = funcModuleIndex;
        metrics.strucModuleId = strucModuleIndex;
        metrics.faceIdsOfOverlap = intersect(rightFuncFaceIds,rightStrucFaceIds);
        metrics.overlapArea = sum(elemvolume(allBrainData.rightHemisphere.surf.nodes(:,1:3),allBrainData.rightHemisphere.surf.faces(metrics.faceIdsOfOverlap,1:3)));
        metrics.areaOverlapAsPercentOfFunc = metrics.overlapArea / rightFuncModuleAreaMm{funcModuleIndex};
        metrics.areaOverlapAsPercentOfStruc = metrics.overlapArea / rightStrucModuleAreaMm{strucModuleIndex};
        rightOverlapMatrix = [rightOverlapMatrix; metrics];
        clear metrics;
    end
end
rightCollectionOfMetrics = cat(2,rightOverlapMatrix{:});


filename=[pathToParticipants '/' subject '/moduleResults/collectionOfMetrics__' num2str(conditionIndex) '.mat'];
%save(filename,'leftCollectionOfMetrics','rightCollectionOfMetrics','-v7.3');
save(filename,'leftCollectionOfMetrics','rightCollectionOfMetrics');

%% Save data to csv
    if(~isempty(leftCollectionOfMetrics))
    [leftCollectionOfMetrics(:).subjectId] = deal(subject);
    end
    if(~isempty(rightCollectionOfMetrics))
    [rightCollectionOfMetrics(:).subjectId] = deal(subject);
    end
table = [leftCollectionOfMetrics rightCollectionOfMetrics];
if(~isempty(table))
    [table(:).faceIdsOfOverlap]= deal([]);
    writetable(struct2table(table, "AsArray",true), [pathToParticipants '/' subject '/moduleResults/collectionOfMetrics_' num2str(conditionIndex) '.csv']); 
    writetable(struct2table(table, "AsArray",true), [pathToParticipants '/allSubjectsCollectionOfMetrics_' num2str(conditionIndex) '.csv'], "WriteMode","append");
end


disp("Script ran successfully.");



    %% Visualisations

        if(~visualiseData==1)
        close all;
        end
        disp("Calculate overlap finished...")
end