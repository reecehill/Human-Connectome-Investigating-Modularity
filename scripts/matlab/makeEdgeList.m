function [...
    edgeListRemote,...
    edgeListLocal,...
    lpcentroids,...
    rpcentroids...
    ]=makeEdgeList(pathToFile,downsample)
disp("------");
disp("Start of edgeList.m")
tic
disp("------");
clear ft_hastoolbox;
restoredefaultpath;
%gcp;
%addpath('toolboxes/AlongTractStats');
%addpath(genpath('toolboxes/SurfStat'));
addpath('toolboxes/FieldTrip');
ft_defaults;
%ft_hastoolbox('spm12',1);
ft_hastoolbox('iso2mesh',1);
%ft_hastoolbox('gifti',1);

disp('step3: check if there are fibres connected between node pairs')

%% load the data that was output by loadLabels.m
disp('loading labelSRF.mat');
fileToLoad=[pathToFile,'/labelSRF.mat'];
load(fileToLoad, "hi_glpfaces", "hi_glpvertex", "hi_grpfaces", "hi_grpvertex", "lo_glpfaces", "lo_grpfaces", "lo_glpvertex", "lo_grpvertex", "lo_subCoor"); % not used: "faceROIidL", "faceROIidR", "filenames", "subROIid", "subfilenames"

%% load the data that was output by conversion.m
disp('loading trsfmTrk.mat');
fileToLoad=[pathToFile,'/trsfmTrk.mat'];
load(fileToLoad, "trk_type", "trkEP"); %"trk_len": not used
%% get lengths of data

nbTracts=length(trkEP);
%% get centres of triangles
disp('computing centroids');
if strcmp(downsample,'no') % method for no downsample
    lpcentroids=meshcentroid(hi_glpvertex,hi_glpfaces);
    rpcentroids=meshcentroid(hi_grpvertex,hi_grpfaces);
    % nbFaces=size(hi_grpfaces,1)+size(hi_glpfaces,1);
else
    lpcentroids=meshcentroid(lo_glpvertex,lo_glpfaces);
    rpcentroids=meshcentroid(lo_grpvertex,lo_grpfaces);
    % nbFaces=size(lo_grpfaces,1)+size(lo_glpfaces,1);
end

%% make edge list for remote connections
edgeListRemote=zeros(nbTracts,5,'single');
% parfor k=1:nbTracts
tic
lpCentroidsFirstCol = lpcentroids(:,1);
lpCentroidsSecCol = lpcentroids(:,2);
lpCentroidsThirdCol = lpcentroids(:,3);
rpCentroidsFirstCol = rpcentroids(:,1);
rpCentroidsSecCol = rpcentroids(:,2);
rpCentroidsThirdCol = rpcentroids(:,3);
subCoorFirstCol = lo_subCoor(:,1);
subCoorSecCol = lo_subCoor(:,2);
subCoorThirdCol = lo_subCoor(:,3);
allPoints = [lpcentroids; rpcentroids; lo_subCoor];
disp('Building Remote connection elist:\n');
buildRemote = 1;
if(buildRemote == 1)
    startps = trkEP(:, 1:3);
    endps = trkEP(:,4:6);
    [indexOfClosestPoints_start, distFromQueryPointToData_start] = knnsearch(allPoints,startps,'K',1,'Distance','euclidean');
    [indexOfClosestPoints_end, distFromQueryPointToData_end] = knnsearch(allPoints,endps,'K',1,'Distance','euclidean');
    edgeListRemote = [indexOfClosestPoints_end, indexOfClosestPoints_start, distFromQueryPointToData_end,distFromQueryPointToData_start];
    edgeListRemote(:,5) = 1:1:length(edgeListRemote);
    edgeListRemote(edgeListRemote(:,5)==0,:)=[];
    disp("Done building remote edge list");
    toc
    
end
% columns 1:2 are the nodes to which they connect, columns 3:4 are the
% distance from the pial surface, column 5 is the track ID.

%% get local connection -- downsample or no downsample

% adj_local=sparse(nbFaces,nbFaces);
% two method pointing to downsample or no downsample
if strcmp(downsample,'no') % method for no downsample
    tic
    disp("Building left hemisphere's local edges.")
    [edgeListLocalLH] = getEdgeListLocal(hi_glpfaces);
    disp("Done building left hemisphere's local edges.")
    toc

    tic
    disp("Building right hemisphere's local edges.")
    [edgeListLocalRH] = getEdgeListLocal(hi_grpfaces,length(hi_glpfaces));
    disp("Done building right hemisphere's local edges.")
    toc
elseif strcmp(downsample,'yes') % method for downsample data
    disp("Building left hemisphere's local edges.")
    tic
    [edgeListLocalLH] = getEdgeListLocal(lo_glpfaces);
    disp("Done building left hemisphere's local edges.")
    toc

    disp("Building right hemisphere's local edges.")
    tic
    [edgeListLocalRH] = getEdgeListLocal(lo_grpfaces,length(lo_glpfaces));
    disp("Done building right hemisphere's local edges.")
    toc
end

edgeListLocal=[...
    edgeListLocalLH;
    edgeListLocalRH;
    ];

% Should boundary faces be removed completely?
%edgeListLocal(edgeListLocal(:,2)==0)=[];

% adj_local=sparse(edgeListLocal(:,1),edgeListLocal(:,2),ones(length(edgeListLocalLH(:,1)),1),nbFaces,nbFaces);
clear edgeListLocalLH edgeListLocalRH

disp("------");
disp("Finished with edgeList.m")
toc
disp("------");
end
function [edgeListLocal_hemisphere] = getEdgeListLocal(faces, countFrom)
% countFrom (int) is added to each node ID, rather than counting from 0.
% Used for Right hemisphere.
arguments
    faces
    countFrom = 0
end
endedgeListLocal_hemisphere = countFrom+edgeneighbors(faces(:,1:3)); %each row...
% index is the faceID, and each column is the adjacent face triangle (three).
facesList = countFrom+(1:1:length(faces))';
edgeListLocal_hemisphere = sortrows([ ...
    facesList endedgeListLocal_hemisphere(:,1); ...
    facesList endedgeListLocal_hemisphere(:,2); ...
    facesList endedgeListLocal_hemisphere(:,3) ...
    ],1);

%edgeListLocal_hemisphere(edgeListLocal_hemisphere(:,2)==0,:)=[];
end