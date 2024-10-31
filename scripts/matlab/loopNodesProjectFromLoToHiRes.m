function [hi_nodes_scalar] = loopNodesProjectFromLoToHiRes(lo_nodes,hi_nodes,lo_nodes_values)
nHiNodes = size(hi_nodes,1);
nMissingFmriData = 0;
matchedNodes = zeros(nHiNodes,7);
hi_nodes_scalar=zeros(nHiNodes,size(lo_nodes_values,2));
for k=1:nHiNodes
    % Print progress.
    if mod(k/1000,1)==0
        display(num2str(nHiNodes\k))
    end

    currentnode=hi_nodes(k,:); %current node's coordinates
    %Euclidean distances (vector double) between current face and all mesh centroids
    ds=((currentnode(:,1)-lo_nodes(:,1)).^2 + (currentnode(:,2)-lo_nodes(:,2)).^2 + (currentnode(:,3)-lo_nodes(:,3)).^2 );

    % ID of the mesh centroid that is closest to current face's
    % centroid.
    [distance,closestVertex_id]=min(ds);
    matchedNodes(k,:) = [currentnode lo_nodes(closestVertex_id,:) distance];
    % Replace ID (as above) with the fMRI value of the closest centroid.
    try
        hi_nodes_scalar(k,:)=lo_nodes_values(closestVertex_id,:);
    catch
        % Nearest face is not cortical.
        hi_nodes_scalar(k,:)=NaN;
        nMissingFmriData = nMissingFmriData+1;
    end
end
if(nMissingFmriData>0)
    disp(nMissingFmriData+" vertices with an unknown/missing fMRI data value encountered. They were skipped.");
end