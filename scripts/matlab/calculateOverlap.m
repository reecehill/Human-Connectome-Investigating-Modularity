function [leftCollectionOfMetrics, rightCollectionOfMetrics] = calculateOverlap(pathToParticipants, subject, conditions, visualiseData)
addpath('toolboxes/FieldTrip');
ft_defaults;
%ft_hastoolbox('spm12',1);
ft_hastoolbox('iso2mesh',1);
subject = subject
load([pathToParticipants,'/labelSRF.mat']);

conditions = textscan(conditions(2:end-1), '%s','Delimiter',{',',char("'")},'MultipleDelimsAsOne',true); % Used to enable conversion of character array (from python) to cell string array
conditions = conditions{:};

for conditionIndex=1:length(conditions)
    conditionName = char(conditions(conditionIndex));
    disp(['Calculating overlap for all conditions' conditionName]);
    load([pathToParticipants,'/moduleResults/allBrainData__',conditionName,'.mat']);

    %% LEFT HEMISPHERE
    leftOverlappingFaces = find(allBrainData.leftHemisphere.surf.faces(:,6) == 1);
    leftOffset = max(allBrainData.leftHemisphere.surf.faces(:,5))+1;
    allBrainData.leftHemisphere.surf.faces(allBrainData.leftHemisphere.surf.faces(:,5)>0,5) = allBrainData.leftHemisphere.surf.faces(allBrainData.leftHemisphere.surf.faces(:,5)>0,5) + leftOffset;
    allBrainData.leftHemisphere.surf.faces(:,7) = allBrainData.leftHemisphere.surf.faces(:,4) + allBrainData.leftHemisphere.surf.faces(:,5);

    %globalFunctionalModules = transpose(unique(allBrainData.leftHemisphere.surf.faces(allBrainData.leftHemisphere.surf.faces(:,5)>0,5)));

    leftStructuralModules = allBrainData.leftHemisphere.surf.faces(:,4);
    for moduleIndex=1:length(unique(leftStructuralModules))
        moduleName = leftStructuralModules(moduleIndex);
        %% For each module, get its outline.
        % Edges are defined by two indexes - the two nodes they connect.
        leftStrucModuleFacesIndexes{moduleIndex} = find(allBrainData.leftHemisphere.surf.faces(:,4) == moduleName);
        leftStrucModuleFacesBiggerThan1Indexes{moduleIndex} = length(find(allBrainData.leftHemisphere.surf.faces(:,4) == moduleName)) > 1;
        leftStrucModuleNodeIndexesTemp = allBrainData.leftHemisphere.surf.faces(leftStrucModuleFacesIndexes{moduleIndex},1:3);
        leftStrucModuleNodeIndexes = unique(leftStrucModuleNodeIndexesTemp(:));
        leftStrucModuleAreaMm{moduleIndex} = sum(elemvolume(allBrainData.leftHemisphere.surf.nodes(:,1:3),allBrainData.leftHemisphere.surf.faces(leftStrucModuleFacesIndexes{moduleIndex},1:3)));
        allBrainData.leftHemisphere.surf.nodes(leftStrucModuleNodeIndexes,4) = moduleIndex;
        [strucEdges{moduleIndex},~]=surfedge(allBrainData.leftHemisphere.surf.faces(leftStrucModuleFacesIndexes{moduleIndex},1:3));
    end

    leftFuncModuleIndexes = transpose(unique(allBrainData.leftHemisphere.surf.faces(leftOverlappingFaces,5)));
    %funcModuleIndexes = transpose(unique(allBrainData.leftHemisphere.surf.faces(allBrainData.leftHemisphere.surf.faces(:,5)>0,5)));

    for funcModuleIndex=1:length(leftFuncModuleIndexes)
        funcModuleName = leftFuncModuleIndexes(funcModuleIndex);
        leftFuncModuleFacesIndexes{funcModuleIndex} = intersect(leftOverlappingFaces,find(allBrainData.leftHemisphere.surf.faces(:,5) == funcModuleName));
        leftFuncModuleAreaMm{funcModuleIndex} = sum(elemvolume(allBrainData.leftHemisphere.surf.nodes(:,1:3),allBrainData.leftHemisphere.surf.faces(leftFuncModuleFacesIndexes{funcModuleIndex},1:3)));

        leftGlobalFuncModuleFacesIndexes{funcModuleIndex}= find(allBrainData.leftHemisphere.surf.faces(:,5) == funcModuleName);
        leftGlobalFuncModuleAreaMm{funcModuleIndex} = sum(elemvolume(allBrainData.leftHemisphere.surf.nodes(:,1:3),allBrainData.leftHemisphere.surf.faces(leftFuncModuleFacesIndexes{funcModuleIndex},1:3)));

        leftFuncModuleNodeIndexesTemp = allBrainData.leftHemisphere.surf.faces(leftFuncModuleFacesIndexes{funcModuleIndex},1:3);
        leftFuncModuleNodeIndexes{funcModuleIndex} = unique(leftFuncModuleNodeIndexesTemp(:));
        [leftFuncEdges{funcModuleIndex},~]=surfedge(allBrainData.leftHemisphere.surf.faces(leftFuncModuleFacesIndexes{funcModuleIndex},(1:3)));
    end

    %% Calculating overlap
    readmatrix([pathToParticipants,'/exported_modules/left_structural_modules.csv']);
    allCsvFiles = dir(fullfile([pathToParticipants,'/exported_modules'], '*.csv'));
    allModules = struct();
    for k = 1:length(allCsvFiles)
        allModules(k).name = allCsvFiles(k).name(1:end-4);
        allModules(k).moduleGroup = readmatrix([pathToParticipants,'/exported_modules/', allCsvFiles(k).name]);
    end


    leftOverlapMatrix = {};
    leftModuleCounter=0;
    for funcModuleIndex=1:length(leftFuncModuleIndexes)
        funcModuleName = leftFuncModuleIndexes(funcModuleIndex);
        leftModuleCounter = leftModuleCounter+1;
        % This gets all face ids - even those outside the ROI.
        leftFuncFaceIds = find(allBrainData.leftHemisphere.surf.faces(:,5) == funcModuleName);
        leftStrucModuleIds = transpose(unique(allBrainData.leftHemisphere.surf.faces(intersect(leftOverlappingFaces,leftFuncFaceIds),4)));
        for strucModuleIndex=1:length(leftStrucModuleIds)
            strucModuleName=leftStrucModuleIds(strucModuleIndex);
            leftStrucFaceIds = find(allBrainData.leftHemisphere.surf.faces(:,4) == strucModuleName);
            metrics.funcModuleId = funcModuleName;
            metrics.strucModuleId = strucModuleName;
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

    rightStructuralModules = allBrainData.rightHemisphere.surf.faces(:,4);
    for moduleIndex=1:length(unique(rightStructuralModules))
        moduleName = rightStructuralModules(moduleIndex);
        %% For each module, get its outline.
        % Edges are defined by two indexes - the two nodes they connect.
        rightStrucModuleFacesIndexes{moduleIndex} = find(allBrainData.rightHemisphere.surf.faces(:,4) == moduleName);
        rightStrucModuleFacesBiggerThan1Indexes{moduleIndex} = length(find(allBrainData.rightHemisphere.surf.faces(:,4) == moduleName)) > 1;
        rightStrucModuleNodeIndexesTemp = allBrainData.rightHemisphere.surf.faces(rightStrucModuleFacesIndexes{moduleIndex},1:3);
        rightStrucModuleNodeIndexes = unique(rightStrucModuleNodeIndexesTemp(:));
        rightStrucModuleAreaMm{moduleIndex} = sum(elemvolume(allBrainData.rightHemisphere.surf.nodes(:,1:3),allBrainData.rightHemisphere.surf.faces(rightStrucModuleFacesIndexes{moduleIndex},1:3)));
        allBrainData.rightHemisphere.surf.nodes(rightStrucModuleNodeIndexes,4) = moduleIndex;
        [strucEdges{moduleIndex},~]=surfedge(allBrainData.rightHemisphere.surf.faces(rightStrucModuleFacesIndexes{moduleIndex},1:3));
    end

    rightFuncModuleIndexes = transpose(unique(allBrainData.rightHemisphere.surf.faces(rightOverlappingFaces,5)));
    %funcModuleIndexes = transpose(unique(allBrainData.rightHemisphere.surf.faces(allBrainData.rightHemisphere.surf.faces(:,5)>0,5)));

    for funcModuleIndex=1:length(unique(rightFuncModuleIndexes))
        funcModuleName=rightFuncModuleIndexes(funcModuleIndex);
        rightFuncModuleFacesIndexes{funcModuleIndex} = intersect(rightOverlappingFaces,find(allBrainData.rightHemisphere.surf.faces(:,5) == funcModuleName));
        rightFuncModuleAreaMm{funcModuleIndex} = sum(elemvolume(allBrainData.rightHemisphere.surf.nodes(:,1:3),allBrainData.rightHemisphere.surf.faces(rightFuncModuleFacesIndexes{funcModuleIndex},1:3)));

        rightGlobalFuncModuleFacesIndexes{funcModuleIndex}= find(allBrainData.rightHemisphere.surf.faces(:,5) == funcModuleName);
        rightGlobalFuncModuleAreaMm{funcModuleIndex} = sum(elemvolume(allBrainData.rightHemisphere.surf.nodes(:,1:3),allBrainData.rightHemisphere.surf.faces(rightFuncModuleFacesIndexes{funcModuleIndex},1:3)));

        rightFuncModuleNodeIndexesTemp = allBrainData.rightHemisphere.surf.faces(rightFuncModuleFacesIndexes{funcModuleIndex},1:3);
        rightFuncModuleNodeIndexes{funcModuleIndex} = unique(rightFuncModuleNodeIndexesTemp(:));
        [rightFuncEdges{funcModuleIndex},~]=surfedge(allBrainData.rightHemisphere.surf.faces(rightFuncModuleFacesIndexes{funcModuleIndex},(1:3)));
    end

    %% Calculating overlap
    rightOverlapMatrix = {};
    rightModuleCounter=0;
    for funcModuleIndex=1:length(unique(rightFuncModuleIndexes))
        funcModuleName=rightFuncModuleIndexes(funcModuleIndex);
        rightModuleCounter = rightModuleCounter+1;
        % This gets all face ids - even those outside the ROI.
        rightFuncFaceIds = find(allBrainData.rightHemisphere.surf.faces(:,5) == funcModuleName);
        rightStrucModuleIds = transpose(unique(allBrainData.rightHemisphere.surf.faces(intersect(rightOverlappingFaces,rightFuncFaceIds),4)));
        for strucModuleIndex=1:length(unique(rightStrucModuleIds))
            strucModuleName = rightStrucModuleIds(strucModuleIndex);
            rightStrucFaceIds = find(allBrainData.rightHemisphere.surf.faces(:,4) == strucModuleName);
            metrics.funcModuleId = funcModuleIndex;
            metrics.strucModuleId = strucModuleName;
            metrics.faceIdsOfOverlap = intersect(rightFuncFaceIds,rightStrucFaceIds);
            metrics.overlapArea = sum(elemvolume(allBrainData.rightHemisphere.surf.nodes(:,1:3),allBrainData.rightHemisphere.surf.faces(metrics.faceIdsOfOverlap,1:3)));
            metrics.areaOverlapAsPercentOfFunc = metrics.overlapArea / rightFuncModuleAreaMm{funcModuleIndex};
            metrics.areaOverlapAsPercentOfStruc = metrics.overlapArea / rightStrucModuleAreaMm{strucModuleIndex};
            rightOverlapMatrix = [rightOverlapMatrix; metrics];
            clear metrics;
        end
    end
    rightCollectionOfMetrics = cat(2,rightOverlapMatrix{:});


    filename=[pathToParticipants  '/moduleResults/collectionOfMetrics__' conditionName '.mat'];
    save(filename,'leftCollectionOfMetrics','rightCollectionOfMetrics','-v7.3');
    disp("Script ran successfully.");


    if(visualiseData == 1)
        %% Visualisations
        figure;
        xlabel('Left-Right');
        ylabel('Anterior-Posterior');
        zlabel('Inferior-Superior');
        hold on;
        ax = gca;               % get the current axis
        ax.Clipping = 'off';    % turn clipping off
        title("Left motor homonculus parcellated into triangular nodes");
        %plotsurf(allBrainData.leftHemisphere.surf.nodes,allBrainData.leftHemisphere.surf.faces(:,1:3),'DisplayName','Left hemisphere','FaceAlpha',0.5,'EdgeColor','black','EdgeAlpha',0.05,'FaceColor','white');
        plotsurf(allBrainData.leftHemisphere.surf.nodes,allBrainData.leftHemisphere.surf.faces(find(allBrainData.leftHemisphere.surf.faces(:,4) > 0),1:3),'DisplayName','Left hemisphere','FaceAlpha',0.5,'EdgeColor','black','EdgeAlpha',0.05,'FaceColor','white');

        leftStrucModuleIds = transpose(unique(allBrainData.leftHemisphere.surf.faces(intersect(leftOverlappingFaces,leftFuncFaceIds),4)));
        leftColormap_hsv = hsv(double(max(leftStrucModuleIds)));
        for moduleIndex=1:length(leftStrucModuleIds)
            color = leftColormap_hsv(moduleIndex,:);
            plotsurf(allBrainData.leftHemisphere.surf.nodes(:,1:3),allBrainData.leftHemisphere.surf.faces(leftStrucModuleFacesIndexes{moduleIndex},1:3),'DisplayName',['Structural Module: #' num2str(moduleIndex)],'EdgeAlpha',0.3,'FaceColor',[color]);
            %plotedges(allBrainData.leftHemisphere.surf.nodes(:,1:3), strucEdges{moduleIndex},'linewidth',randi(5,1),'Color',[color 0.9],'linestyle','-','DisplayName',['Structural Module: #' num2str(moduleIndex)]);
        end

        leftColormap_jet = jet(length(leftFuncModuleIndexes));
        count = 0;
        for funcModuleIndex=1:length(unique(leftFuncModuleIndexes))
            count = count+1;
            color = leftColormap_jet(count,:);
            %plotsurf(allBrainData.leftHemisphere.surf.nodes(:,1:3),allBrainData.leftHemisphere.surf.faces(intersect(leftOverlappingFaces,funcModuleFacesIndexes{funcModuleIndex}),1:3),'DisplayName',['Functional Module: #' num2str(funcModuleIndex)],'EdgeAlpha',0.3,'FaceColor',colormap_jet(funcModuleIndex,:));
            plotedges(allBrainData.leftHemisphere.surf.nodes(:,1:3), leftFuncEdges{funcModuleIndex},'linewidth',3,'Color',[color],'linestyle','-','DisplayName',['Functional Module: #' num2str(funcModuleIndex)],'Marker','o','MarkerSize',3,'AlignVertexCenters','on','HandleVisibility','off');
            plot(NaN,NaN,'linewidth',5,'Color',color,'DisplayName',['Functional Module: #' num2str(funcModuleIndex)],'Marker','o','MarkerSize',3)
        end

        camlight;
        lighting gouraud;
        legend;

        figure;
        xlabel('Left-Right');
        ylabel('Anterior-Posterior');
        zlabel('Inferior-Superior');
        hold on;
        ax = gca;               % get the current axis
        ax.Clipping = 'off';    % turn clipping off
        title("Right motor homonculus parcellated into triangular nodes");
        %plotsurf(allBrainData.leftHemisphere.surf.nodes,allBrainData.leftHemisphere.surf.faces(:,1:3),'DisplayName','Left hemisphere','FaceAlpha',0.5,'EdgeColor','black','EdgeAlpha',0.05,'FaceColor','white');
        plotsurf(allBrainData.rightHemisphere.surf.nodes,allBrainData.rightHemisphere.surf.faces(find(allBrainData.rightHemisphere.surf.faces(:,4) > 0),1:3),'DisplayName','Right hemisphere','FaceAlpha',0.5,'EdgeColor','black','EdgeAlpha',0.05,'FaceColor','white');

        rightStrucModules = allBrainData.rightHemisphere.surf.faces(:,4);
        rightColormap_hsv = hsv(length(unique(rightStrucModules)));
        for moduleIndex=1:length(unique(rightStrucModules))
            color = rightColormap_hsv(moduleIndex,:);
            plotsurf(allBrainData.rightHemisphere.surf.nodes(:,1:3),allBrainData.rightHemisphere.surf.faces(rightStrucModuleFacesIndexes{moduleIndex},1:3),'DisplayName',['Structural Module: #' num2str(moduleIndex)],'EdgeAlpha',0.3,'FaceColor',color);
        end

        rightColormap_jet = jet(length(rightFuncModuleIndexes));
        count = 0;
        for funcModuleIndex=1:length(unique(rightFuncModuleIndexes))
            count = count+1;
            color = rightColormap_jet(count,:);
            %plotsurf(allBrainData.leftHemisphere.surf.nodes(:,1:3),allBrainData.leftHemisphere.surf.faces(intersect(leftOverlappingFaces,funcModuleFacesIndexes{funcModuleIndex}),1:3),'DisplayName',['Functional Module: #' num2str(funcModuleIndex)],'EdgeAlpha',0.3,'FaceColor',colormap_jet(funcModuleIndex,:));
            plotedges(allBrainData.rightHemisphere.surf.nodes(:,1:3), rightFuncEdges{funcModuleIndex},'linewidth',3,'Color',color,'linestyle','-','DisplayName',['Functional Module: #' num2str(funcModuleIndex)],'Marker','o','MarkerSize',3,'AlignVertexCenters','on','HandleVisibility','off');
            plot(NaN,NaN,'linewidth',5,'Color',color,'DisplayName',['Functional Module: #' num2str(funcModuleIndex)],'Marker','o','MarkerSize',3)
        end
        camlight;
        lighting gouraud;
        legend;


        figure;
        hold on;
        title("Independent view of each structural module from left hemisphere");
        modulesWith1OrMoreFaces = cat(2,leftStrucModuleFacesBiggerThan1Indexes{:});
        tiledlayout(ceil(sum(modulesWith1OrMoreFaces)/3),3,'TileSpacing','None','Padding','None');

        leftStrucModuleIds = transpose(unique(allBrainData.leftHemisphere.surf.faces(intersect(leftOverlappingFaces,leftFuncFaceIds),4)));
        for moduleIndex=1:length(leftStrucModuleIds)
            if(modulesWith1OrMoreFaces(moduleIndex) == 1)
                ax = nexttile;               % get the current axis
                hold on;
                ax.Clipping = 'off';    % turn clipping offcamlight;
                light(ax,'Position',[0 0 0]);
                light(ax,'Position',[200 200 200]);
                light(ax,'Position',[-100 70 0]);
                lighting(ax, 'gouraud');
                plotsurf(allBrainData.leftHemisphere.surf.nodes(:,1:3),...
                    allBrainData.leftHemisphere.surf.faces(leftStrucModuleFacesIndexes{moduleIndex},(1:3)),'DisplayName',['Structural Module: ' moduleIndex],'EdgeAlpha',0.3,'FaceColor',leftColormap_hsv(moduleIndex,:));
            end
        end

        figure;
        hold on;
        title("Independent view of each structural module from right hemisphere");
        rightModulesWith1OrMoreFaces = cat(2,rightStrucModuleFacesBiggerThan1Indexes{:});
        tiledlayout(ceil(sum(rightModulesWith1OrMoreFaces)/3),3,'TileSpacing','None','Padding','None');

        rightStrucModuleIds = transpose(unique(allBrainData.rightHemisphere.surf.faces(intersect(rightOverlappingFaces,rightFuncFaceIds),4)));
        for moduleIndex=1:length(rightStrucModuleIds)
            if(rightModulesWith1OrMoreFaces(moduleIndex) == 1)
                ax = nexttile;               % get the current axis
                hold on;
                ax.Clipping = 'off';    % turn clipping offcamlight;
                light(ax,'Position',[0 0 0]);
                light(ax,'Position',[200 200 200]);
                light(ax,'Position',[-100 70 0]);
                lighting(ax, 'gouraud');
                plotsurf(allBrainData.rightHemisphere.surf.nodes(:,1:3),...
                    allBrainData.rightHemisphere.surf.faces(rightStrucModuleFacesIndexes{moduleIndex},(1:3)),'DisplayName',['Structural Module: ' moduleIndex],'EdgeAlpha',0.3,'FaceColor',rightColormap_hsv(moduleIndex,:));
            end
        end
    end
end

end