%% THIS SCRIPT NEEDS WORK TO BE ABLE TO WORK ON FLOAT NUMBERS.

function [mat] = getThreeDimensions(x,y,z)
% Min and max values
xmin = min(x)
xmax = max(x);
ymin = min(y);
ymax = max(y);
zmin = min(z);
zmax = max(z);

ind = sub2ind([xmax,ymax], x, y);
mat(ind) = z;
end