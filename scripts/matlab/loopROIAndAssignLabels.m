function [facesROI] = loopROIAndAssignLabels(ROI_startIndex, ROI_endIndex, faces, ROIfacevert)

    % This function moves scalar values from NODES to FACE CENTROIDS.
    % The face receives the value if 2 or more nodes have the value.
        facesROI={};
        for roi=ROI_startIndex:ROI_endIndex
            nodeIds = ROIfacevert(roi).faces(:,1);

            % Get the faces attached to these nodes
            attachedFaces = ismember(faces(:,1:3),nodeIds);

            % Number of nodes per face that share nodeValue.
            x = sum(attachedFaces(:,1:3),2);

            % Face ids with >=2 nodes of same value.
            ROIfacevert(roi).ffaces=find(x>=2); %by Xue
            
            nbffaces=length(ROIfacevert(roi).ffaces);
            
            % Face id to include roi.
            facesROI{roi} = [faces(ROIfacevert(roi).ffaces,:), ones(nbffaces,1)*roi];
        end
        facesROI=cat(1,facesROI{:});
end