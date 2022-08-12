[x,y,z] = ind2sub(size(intensitiesPerVoxel),1:1:numel(intensitiesPerVoxel));
xyz =transpose([x;y;z]);
colOfOnes = ones(size(xyz,1),1);
xyz = [xyz colOfOnes];
xyz = transpose(inv(rmmissing(Reg)) * tMov * xyz'); %nodes are now represented in mm rather than indice.
xyz(:,4) = []; %remove column of ones;


