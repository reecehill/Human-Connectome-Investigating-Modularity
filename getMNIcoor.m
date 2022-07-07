function [Coor_MNI305,Coor_MNI152]=getMNIcoor(pathToFile,type)

display('step5: get high resolution coordinates in MNI space')

disp('loading edgeList.mat')
load([pathToFile,'/edgeList.mat'])

%% all node coordinates
Coor = [lpcentroids;rpcentroids;subCoor];
nlen = size(Coor,1);


%% load linear transformation matrix
[TalairachXFM] = freesurfer_read_talxfm([pathToFile,'T1w/bert/mri/transforms/talairach.xfm']);

ft_defaults
mri=ft_read_mri([pathToFile,'T1w/bert/mri/aparc+aseg.nii']);
Norig = mri.hdr.vox2ras;
Torig = mri.hdr.tkrvox2ras;

if type==1  % pial.surf.nii
    transform = TalairachXFM; % transformaiton matrix 
elseif type==2 % pial
    transform = TalairachXFM*Norig*inv(Torig); % from voxel slices to tk surface RAS coordinates.
else
    display('wrong type of surface')
end

%% MNI305 space
In = [Coor ones(nlen,1)]';
Out = transform*In;
Coor_MNI305 = Out(1:3,:)';

%% MNI152 space
transform305_152 = [  0.9975   -0.0073    0.0176   -0.0429
           0.0146    1.0009   -0.0024    1.5496
          -0.0130   -0.0093    0.9971    1.1840];
In = [Coor_MNI305 ones(nlen,1)]';
Out = transform305_152*In;
Coor_MNI152 = Out(1:3,:)';



















end