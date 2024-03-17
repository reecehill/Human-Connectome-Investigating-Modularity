function [glpfaces, grpfaces, glpvertex, grpvertex, filenames, subfilenames, ROIfacevert, nbROI] = load164kMesh(pathToFile,subjectId,type)

ROIfacevert = getROIByFaceVertex();
if type==1
    disp('load lh(rh).pial.surf.gii as surface')
    giftilh=gifti([pathToFile,'/MNINonLinear/',subjectId,'.L.pial_MSMAll.164k_fs_LR.surf.gii']);
    glpfaces      = giftilh.faces;
    glpvertex     = giftilh.vertices;
    giftirh=gifti([pathToFile,'/MNINonLinear/',subjectId,'.R.pial_MSMAll.164k_fs_LR.surf.gii']);
    grpfaces      = giftirh.faces;
    grpvertex     = giftirh.vertices;
    clear giftilh giftirh;
elseif type==2
    % load hi-res surface - pial
    disp('load lh(rh).pial as surface')
    
    l=SurfStatReadSurf([pathToFile,'/MNINonLinear/',subjectId,'/surf/lh.pial']);
    r=SurfStatReadSurf([pathToFile,'/MNINonLinear/',subjectId,'/surf/rh.pial']);
    glpfaces = l.tri; %118,580x3 int32 (each row is the ID of the 3 nodes of the face)
    glpvertex = l.coord'; %59292x3 double (each row are the coordinates of a node; row id = node ID)
    grpfaces = r.tri; %118,580x3 int32 (each row is the ID of the 3 nodes of the face)
    grpvertex = r.coord'; %59292x3 double (each row are the coordinates of a node; row id = node ID)
    clear l r;
end
end