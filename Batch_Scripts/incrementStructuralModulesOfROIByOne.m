% This code finds the faces of a region of interest, and increments their
% module group by one. This is because in later code, a module of zero is
% assumed to mean the face is not a part of the ROI. This code is isolated
% from the main script, as the script was updated to do this automatically.


function incrementStructuralModulesOfROIByOne(pathToParticipants, subject, conditionIndex)
%clearvars -except pathToParticipants subject conditionIndex

%% Parameters
roiLabels = ["precentral.label"]; % only supports single values for now.


load([pathToParticipants '\' subject '\moduleResults\allBrainData__' num2str(conditionIndex) '.mat'], "allBrainData");




%% ROI Anatomical Data
% Get region of interest data (face IDs and centroids).
roiStructuralData.leftHemisphere.surf.faceIdsOfAllBrain = find(ismember(allBrainData.leftHemisphere.labels.names,strcat('lh.',roiLabels)));
roiStructuralData.rightHemisphere.surf.faceIdsOfAllBrain = find(ismember(allBrainData.rightHemisphere.labels.names,strcat('rh.',roiLabels)));

%% See what the ROI area is.
figure;
title("ROI - Structural modules of the precentral gyrus");
hold on;
xlabel('Left-Right');
ylabel('Anterior-Posterior');
zlabel('Inferior-Superior');
hold on;
ax = gca;               % get the current axis
ax.Clipping = 'off';    % turn clipping off
camlight;
lightangle(-45,30);
lightangle(100,0);
lightangle(0,0);
lightangle(100,100);
lighting gouraud;
plotsurf(allBrainData.leftHemisphere.surf.nodes,allBrainData.leftHemisphere.surf.faces(find(allBrainData.leftHemisphere.surf.faces(:,4) == 0),1:4),'DisplayName','Left hemisphere','EdgeColor','#575757','EdgeAlpha',0.2,'FaceColor','#d69696','Marker','o','MarkerSize',1);
plotsurf(allBrainData.rightHemisphere.surf.nodes,allBrainData.rightHemisphere.surf.faces(find(allBrainData.rightHemisphere.surf.faces(:,4) == 0),1:4),'DisplayName','Right hemisphere','EdgeColor','#575757','EdgeAlpha',0.2,'FaceColor','#d69696','Marker','o','MarkerSize',1);
plotsurf(allBrainData.leftHemisphere.surf.nodes,allBrainData.leftHemisphere.surf.faces(roiStructuralData.leftHemisphere.surf.faceIdsOfAllBrain,1:4),'DisplayName','Structural module','EdgeColor','#575757','EdgeAlpha',0.2,'Marker','o','MarkerSize',1,'FaceLighting','none','FaceColor','red');
plotsurf(allBrainData.rightHemisphere.surf.nodes,allBrainData.rightHemisphere.surf.faces(roiStructuralData.rightHemisphere.surf.faceIdsOfAllBrain,1:4),'DisplayName','Structural module','EdgeColor','#575757','EdgeAlpha',0.2,'Marker','o','MarkerSize',1,'FaceLighting','none','FaceColor','green');
legend;
view(190,25);



% For all ROI faces, increment the structural module by one.
allBrainData.leftHemisphere.surf.faces(roiStructuralData.leftHemisphere.surf.faceIdsOfAllBrain,4) = allBrainData.leftHemisphere.surf.faces(roiStructuralData.leftHemisphere.surf.faceIdsOfAllBrain,4) + 1;
allBrainData.rightHemisphere.surf.faces(roiStructuralData.rightHemisphere.surf.faceIdsOfAllBrain,4) = allBrainData.rightHemisphere.surf.faces(roiStructuralData.rightHemisphere.surf.faceIdsOfAllBrain,4) + 1;




% Save new file
filename=[pathToParticipants '/' subject '/moduleResults/new_allBrainData__' num2str(conditionIndex) '.mat'];
%save(filename,'allBrainData');
save(filename,'allBrainData','-v7.3');

disp(["Condition " num2str(conditionIndex) " has had its structural modules increased by one."]);


figure;
title("Structural modules of the precentral gyrus");
hold on;
xlabel('Left-Right');
ylabel('Anterior-Posterior');
zlabel('Inferior-Superior');
hold on;
ax = gca;               % get the current axis
ax.Clipping = 'off';    % turn clipping off
camlight;
lightangle(-45,30);
lightangle(100,0);
lightangle(0,0);
lightangle(100,100);
lighting gouraud;
plotsurf(allBrainData.leftHemisphere.surf.nodes,allBrainData.leftHemisphere.surf.faces(find(allBrainData.leftHemisphere.surf.faces(:,4) == 0),1:4),'DisplayName','Left hemisphere','EdgeColor','#575757','EdgeAlpha',0.2,'FaceColor','#d69696','Marker','o','MarkerSize',1);
plotsurf(allBrainData.rightHemisphere.surf.nodes,allBrainData.rightHemisphere.surf.faces(find(allBrainData.rightHemisphere.surf.faces(:,4) == 0),1:4),'DisplayName','Right hemisphere','EdgeColor','#575757','EdgeAlpha',0.2,'FaceColor','#d69696','Marker','o','MarkerSize',1);
plotsurf(allBrainData.leftHemisphere.surf.nodes,allBrainData.leftHemisphere.surf.faces(find(allBrainData.leftHemisphere.surf.faces(:,4) > 0),1:4),'DisplayName','Structural module','EdgeColor','#575757','EdgeAlpha',0.2,'Marker','o','MarkerSize',1,'FaceLighting','none');
plotsurf(allBrainData.rightHemisphere.surf.nodes,allBrainData.rightHemisphere.surf.faces(find(allBrainData.rightHemisphere.surf.faces(:,4) > 0),1:4),'DisplayName','Structural module','EdgeColor','#575757','EdgeAlpha',0.2,'Marker','o','MarkerSize',1,'FaceLighting','none');
legend;
view(190,25);
end