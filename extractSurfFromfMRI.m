addpath('C:\Users\Reece\AppData\Roaming\MathWorks\MATLAB Add-Ons\Collections\AlongTractStats');
addpath('C:\Users\Reece\AppData\Roaming\MathWorks\MATLAB Add-Ons\Collections\Gifti');
addpath('C:\Users\Reece\AppData\Roaming\MathWorks\MATLAB Add-Ons\Collections\Iso2Mesh');
addpath(genpath('C:\Users\Reece\AppData\Roaming\MathWorks\MATLAB Add-Ons\Collections\SurfStat'));
addpath(genpath('C:\Program Files\MATLAB\R2021b\spm12'));
addpath('C:\Users\Reece\AppData\Roaming\MathWorks\MATLAB Add-Ons\Collections\FieldTrip');
% 
% 
% img = niftiread('D:\Dissertation\Participants\sub-002\1stlevel\allClustersBinary.nii');
% %[node,elem,face]=vol2surf(img,1:size(img,1),1:size(img,2),1:size(img,3),[],100,1);
% k = v2m(img,[],'simplify','simplify')
% 

FV = gifti('D:\Dissertation\Participants\sub-002\1stlevel\spmT_0002_allClustersBinary.surf.gii');
figure;
%$shape = alphaShape(FV.faces(:,1),FV.faces(:,2),FV.faces(:,3));
trisurf(FV.faces,FV.vertices(:,1),FV.vertices(:,2),FV.vertices(:,3));
write_surf('freesurfer.surf',FV.vertices,FV.faces)
fg = spm_figure('GetWin','Graphics');
ax = axes('Parent',fg);
p  = patch(FV, 'Parent',ax,...
    'FaceColor', [0.8 0.7 0.7], 'FaceVertexCData', [],...
    'EdgeColor', 'none',...
    'FaceLighting', 'phong',...
    'SpecularStrength' ,0.7, 'AmbientStrength', 0.1,...
    'DiffuseStrength', 0.7, 'SpecularExponent', 10);