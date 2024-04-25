function [voxelIndices] = boundByAtlasDimensions(voxelIndices, atlasDim)
% Where a voxel indice is now (marginally) outside atlasDim (+/- 1), usually
% due to rounding or exploration, bring it back in by one.
% VoxelIndices: 3xk matrix
% atlasDim: 1x3 matrix (e.g., 255, 361, 255)
atlasDim_t = atlasDim';
for k=1:size(voxelIndices,2)
    voxelIndiceRow = voxelIndices(:,k);

    if(any(voxelIndiceRow-atlasDim_t > 1) || any(voxelIndiceRow < 0))
        error("When running boundByAtlasDimensions, a voxel "+sprintf('[%d %d %d]',voxelIndiceRow)+" was found that " + ...
            "was >1 indice outside atlas dimensions "+sprintf('[%d %d %d]',atlasDim)+". Is the labelled " + ...
            "image correctly aligned with the tracks?");
    end

    voxelsAboveRange = voxelIndiceRow-atlasDim_t==1;
    voxelIndiceRow(voxelsAboveRange) = atlasDim_t(voxelsAboveRange);

    voxelsBelowRange = voxelIndiceRow==0;
    voxelIndiceRow(voxelsBelowRange) = 1;

    voxelIndices(:,k) = voxelIndiceRow;
end

end