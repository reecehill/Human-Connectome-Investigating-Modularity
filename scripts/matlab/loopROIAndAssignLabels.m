function [facesROI,faceToNodeMap] = loopROIAndAssignLabels(ROI_startIndex, ROI_endIndex, faces, ROIfacevert)

    % This function moves scalar values from NODES to FACE CENTROIDS.
    % The face receives the value if 2 or more nodes have the value.
        %facesROI = {};    
        facesROI=double(faces);
        facesROI(:,4)=NaN;

        % 1st column is index, next three are the nodes that gave the face
        % its value. If two columns are empty, then a single node was
        % responsible etc. 
        faceToNodeMap=NaN([length(faces),4]);
        faceToNodeMap(:,1) = 1:1:length(faces);


        allRois = unique([ROIfacevert(:).id]);
        firstRoiIndex = find(allRois==ROI_startIndex);
        lastRoiIndexx = find(allRois==ROI_endIndex);
        minNOfSharedNodes = 2;
        maxNOfSharedNodes = 3; % As a triangle has 3 nodes.

        for roiIndex=firstRoiIndex:lastRoiIndexx
            roiName = allRois(roiIndex);
            nodeIds = ROIfacevert(roiIndex).faces(:,1);

            % Get the faces attached to these nodes
            % A logical mx3 matrix, where 1 = "node has roi and is
            % connected to this face"
            attachedFaces = ismember(faces(:,1:3),nodeIds);

            % Number of nodes per face that share nodeValue.
            x = sum(attachedFaces(:,1:3),2);

            % Face ids with >=x nodes of same value.

            for nSharedNodes = minNOfSharedNodes:maxNOfSharedNodes
                faceIdsSetWithNodeValue = find(x==nSharedNodes);
    
                % Node ids contributing to face value
                %TODO: Simplify this to better make use of array indexing
                % Add plus one to column as first column is index!
                faceToNodeMap(attachedFaces(faceIdsSetWithNodeValue,1),1+1) = faces(attachedFaces(faceIdsSetWithNodeValue,1),1);
                faceToNodeMap(attachedFaces(faceIdsSetWithNodeValue,2),2+1) = faces(attachedFaces(faceIdsSetWithNodeValue,2),2);
                faceToNodeMap(attachedFaces(faceIdsSetWithNodeValue,3),3+1) = faces(attachedFaces(faceIdsSetWithNodeValue,3),3);
                
               

                %% Set variables.
                % Face id to include roi.
                facesROI(faceIdsSetWithNodeValue,4) = roiName;
            end

        end     
     disp("Number of faces without a value projected from " + int2str(minNOfSharedNodes) + " or more nodes: " + int2str(sum(isnan(facesROI(:,4)))))

     % Henceforth, unlabelled modules are denoted with -1 not NaN.
     facesROI(isnan(facesROI(:,4)),4)=-1;
end