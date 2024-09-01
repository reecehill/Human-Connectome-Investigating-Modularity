function [facesROI,faceToNodeMap] = loopROIAndAssignLabels(ROI_startIndex, ROI_endIndex, faces, ROIfacevert)

    % This function moves scalar values from NODES to FACE CENTROIDS.
    % The face receives the value if 2 or more nodes have the value.
        facesROI={};
        faceToNodeMap={};
        for roi=ROI_startIndex:ROI_endIndex
            nodeIds = ROIfacevert(roi).faces(:,1);

            % Get the faces attached to these nodes
            attachedFaces = ismember(faces(:,1:3),nodeIds);

            % Number of nodes per face that share nodeValue.
            x = sum(attachedFaces(:,1:3),2);

            % Face ids with >=2 nodes of same value.
            minNOfSharedNodes = 2;
            ROIfacevert(roi).ffaces=find(x>=minNOfSharedNodes); %by Xue
            
            nbffaces=length(ROIfacevert(roi).ffaces);
            
            % Face id to include roi.
            facesROI{roi} = [faces(ROIfacevert(roi).ffaces,:), ones(nbffaces,1)*roi];

            % A matrix that lists the nodeIds that gave the face its value
            % (useful for conversion back).
            matrixOfIds = NaN(size(attachedFaces));
            matrixOfIds(attachedFaces==1) = faces(attachedFaces);
            matrixOfIds = [[1:length(matrixOfIds)]' matrixOfIds];
            matrixOfIds(sum(isnan(matrixOfIds), 2) >= minNOfSharedNodes, :) = [];
            faceToNodeMap{roi} = matrixOfIds;
        end
        facesROI=cat(1,facesROI{:});
        faceToNodeMap=cat(1,faceToNodeMap{:});
end