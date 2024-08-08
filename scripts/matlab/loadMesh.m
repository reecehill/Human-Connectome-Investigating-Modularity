function [glpfaces, grpfaces, glpvertex, grpvertex, filenames, subfilenames, ROIfacevert] = loadMesh(pathToLMesh,pathToRMesh,pathToFile,subjectId,type)
[ROIfacevert, filenames, subfilenames] = getROIByFaceVertex(pathToFile,subjectId);
if(type==1)
    disp('load lh(rh).pial.surf.gii as surface')
    giftilh=gifti(pathToLMesh); % ... surf.gii
    glpfaces      = giftilh.faces;
    glpvertex     = giftilh.vertices;
    giftirh=gifti(pathToRMesh); % ... surf.gii
    grpfaces      = giftirh.faces;
    grpvertex     = giftirh.vertices;
    clear giftilh giftirh;
elseif (type==2)
    % load hi-res surface - pial
    disp('load lh(rh).pial as surface')
    l=SurfStatReadSurf(pathToLMesh); % ... lh.pial
    r=SurfStatReadSurf(pathToRMesh); % ... rh.pial
    glpfaces = l.tri; %118,580x3 int32 (each row is the ID of the 3 nodes of the face)
    glpvertex = l.coord'; %59292x3 double (each row are the coordinates of a node; row id = node ID)
    grpfaces = r.tri; %118,580x3 int32 (each row is the ID of the 3 nodes of the face)
    grpvertex = r.coord'; %59292x3 double (each row are the coordinates of a node; row id = node ID)
    clear l r;
else
    disp("Type is neither 1 nor 2.")
end
end