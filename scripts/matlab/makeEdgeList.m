function [...
    edgeListRemote,...
    edgeListLocal...
    ]=makeEdgeList(pathToFile,downsample,restrictToRoi)
% NOTE: This function can only make one edgeList per run. If you want an
% edgeList for low-resolution, then it must be ran with such parameter.
% (Other functions may make both lo_ and hi_glpfaces, for instance.
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
load(fileToLoad, "filenames","lo_faceROIidL","lo_faceROIidR","hi_faceROIidL","hi_faceROIidR", "hi_glpfaces", "hi_glpvertex", "hi_grpfaces", "hi_grpvertex", "lo_glpfaces", "lo_grpfaces", "lo_glpvertex", "lo_grpvertex", "lo_centroidsSubCor", "hi_centroidsSubCor", "hi_centroidsL", "hi_centroidsR","lo_centroidsL", "lo_centroidsR"); % not used: "faceROIidL", "faceROIidR", "filenames", "subROIid", "subfilenames"

%% load the data that was output by conversion.m
disp('loading trsfmTrk.mat');
fileToLoad=[pathToFile,'/trsfmTrk.mat'];
load(fileToLoad, "trk_type", "trkEP_full"); %"trk_len": not used
%% get lengths of data

nbTracts=length(trkEP_full);
%% get centres of triangles
disp('computing centroids');

if strcmp(downsample,'no') % method for no downsample
    %allCentroids is just allPoints but not filtered.
    allCentroids = [...
        hi_centroidsL; ...
        hi_centroidsR;...
        hi_centroidsSubCor];
else
    allCentroids = [...
        lo_centroidsL; ...
        lo_centroidsR;...
        lo_centroidsSubCor];
end
%Add index to fourth column.
allCentroids(:,4) = 1:1:length(allCentroids);

if(restrictToRoi==1)
    % NOTE: Incompatible with subcortical ROIs.
    roi = "precentral";
    roiIds = find(contains(filenames,roi));
    if strcmp(downsample,'no') % method for no downsample
        selectedFacesL = find(ismember(hi_faceROIidL(:,1),roiIds));
        selectedFacesR = find(ismember(hi_faceROIidR(:,1),roiIds));
        allPoints = allCentroids([selectedFacesL; length(hi_faceROIidL)+selectedFacesR],1:4);
    else
        selectedFacesL = find(ismember(lo_faceROIidL(:,1),roiIds));
        selectedFacesR = find(ismember(lo_faceROIidR(:,1),roiIds));
        allPoints = allCentroids([selectedFacesL; length(lo_faceROIidL)+selectedFacesR],1:4);
    end
else
    allPoints = allCentroids;
end



%% make edge list for remote connections
edgeListRemote=zeros(nbTracts,4,'single');
% parfor k=1:nbTracts
tic
disp('Building Remote connection elist:\n');
buildRemote = 1;
if(buildRemote == 1)
    startps = trkEP_full(:, 1:3);
    endps = trkEP_full(:,4:6);
    [indexOfClosestAllPoints_start, distFromQueryPointToData_start] = knnsearch(allPoints(:,1:3),startps,'K',1,'Distance','euclidean');
    [indexOfClosestAllPoints_end, distFromQueryPointToData_end] = knnsearch(allPoints(:,1:3),endps,'K',1,'Distance','euclidean');

    indexOfAllCentroids_start = allCentroids(allPoints(indexOfClosestAllPoints_start,4),4);
    indexOfAllCentroids_end = allCentroids(allPoints(indexOfClosestAllPoints_end,4),4);

    edgeListRemote = [indexOfAllCentroids_end, indexOfAllCentroids_start, distFromQueryPointToData_end,distFromQueryPointToData_start];

    edgeListRemote(:,5) = 1:1:length(edgeListRemote);

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

edgeListLocal_hemisphere(edgeListLocal_hemisphere(:,2)==0,:)=[];
end