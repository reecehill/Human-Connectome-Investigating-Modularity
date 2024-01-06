function [edgeListRemote,edgeListLocal,lpcentroids,rpcentroids,subCoor]=makeEdgeList(pathToFile,downsample)
clear ft_hastoolbox;
%restoredefaultpath;
gcp;
addpath('toolboxes/AlongTractStats');
addpath(genpath('toolboxes/SurfStat'));
addpath('toolboxes/FieldTrip');
ft_defaults;
ft_hastoolbox('spm12',1);
ft_hastoolbox('iso2mesh',1);
ft_hastoolbox('gifti',1);

disp('step3: check if there are fibres connected between node pairs')

%% load the data that was output by loadLabels.m
disp('loading labelSRF.mat');
fileToLoad=[pathToFile,'/labelSRF.mat'];
load(fileToLoad, "glpfaces", "glpvertex", "grpfaces", "grpvertex", "nfl", "nfr", "nvl", "nvr", "subCoor"); % not used: "faceROIidL", "faceROIidR", "filenames", "subROIid", "subfilenames" 

%% load the data that was output by conversion.m
disp('loading trsfmTrk.mat');
fileToLoad=[pathToFile,'/trsfmTrk.mat'];
load(fileToLoad, "trk_type", "trkEP"); %"trk_len": not used
%% get lengths of data

nbTracts=length(trkEP);
%% get centres of triangles
disp('computing centroids');
if strcmp(downsample,'no') % method for no downsample
    lpcentroids=meshcentroid(glpvertex,glpfaces);
    rpcentroids=meshcentroid(grpvertex,grpfaces);
    glpfacesLen=length(glpfaces);
    grpFacesLen=length(grpfaces);
    %nbFaces=size(grpfaces,1)+size(glpfaces,1);
else
    lpcentroids=meshcentroid(nvl,nfl);
    rpcentroids=meshcentroid(nvr,nfr);
    nfllen=length(nfl);
    nfrlen=length(nfr);
    %nbFaces=size(nfr,1)+size(nfl,1);
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
subCoorFirstCol = subCoor(:,1);
subCoorSecCol = subCoor(:,2);
subCoorThirdCol = subCoor(:,3);
fprintf('Building Remote connection elist:\n');
fprintf(['\n' repmat('.',1,round(nbTracts/100000)) '\n\n']);

buildRemote = 1;
if(buildRemote == 1)
    startps = trkEP(:, 1:3);
    endps = trkEP(:,4:6);
    milestones = round(nbTracts * (0:0.1:1));
    parfor k=1:nbTracts  
        if ismember(k,milestones)
            disp((k/nbTracts)*100+"%");
        end
        
        if trk_type(k,3) ~=0
            % This moves the start and end points of the tracts to the
            % nearest centroids on the resampled/original mesh (downsampled dependent). 
            startp=startps(k,:);
            endp=endps(k,:);
            dsl=(lpCentroidsFirstCol-startp(1)).^2 + (lpCentroidsSecCol-startp(2)).^2 + (lpCentroidsThirdCol-startp(3)).^2 ;
            dsr=(rpCentroidsFirstCol-startp(1)).^2 + (rpCentroidsSecCol-startp(2)).^2 + (rpCentroidsThirdCol-startp(3)).^2 ;
            del=(lpCentroidsFirstCol-endp(1)).^2 + (lpCentroidsSecCol-endp(2)).^2 + (lpCentroidsThirdCol-endp(3)).^2 ;
            der=(rpCentroidsFirstCol-endp(1)).^2 + (rpCentroidsSecCol-endp(2)).^2 + (rpCentroidsThirdCol-endp(3)).^2 ;
            dss=(subCoorFirstCol-startp(1)).^2 + (subCoorSecCol-startp(2)).^2 + (subCoorThirdCol-startp(3)).^2 ;
            des =(subCoorFirstCol-endp(1)).^2 + (subCoorSecCol-endp(2)).^2 + (subCoorThirdCol-endp(3)).^2 ;
            
            endpoints=[del;der;des];
            startpoints=[dsl;dsr;dss];
            [C,I]=min([endpoints,startpoints]);
            edgeListRemote(k,:)=[I,sqrt(C),k];             
        end
    end
    disp(".");
    disp("Done building remote edge list");
    toc
    edgeListRemote(edgeListRemote(:,5)==0,:)=[];
end
% columns 1:2 are the edges to which they connect, columns 3:4 are the
% distance from the pial surface, column 5 is the track ID.

%% get local connection -- downsample or no downsample
disp('building local connection matrix');
count =1;
% adj_local=sparse(nbFaces,nbFaces);

% two method pointing to downsample or no downsample
if strcmp(downsample,'no') % method for no downsample
    edgeListLocalLH=zeros(glpfacesLen*3,2,'single');
    tic
    for i=1:glpfacesLen
        [faceNode_1,~]=find(glpfaces==glpfaces(i,1));
        [faceNode_2,~]=find(glpfaces==glpfaces(i,2));
        [faceNode_3,~]=find(glpfaces==glpfaces(i,3));
        faceNodes=[faceNode_1;faceNode_2;faceNode_3];
        [~, I] = unique(faceNodes, 'first');
        tmp = 1:length(faceNodes);
        tmp(I) = [];
        faceNodes=faceNodes(tmp);
        faceNodes(faceNodes==i)=[];
        if length(faceNodes) == 3
            edgeListLocalLH(count,:)=[i,faceNodes(1)];
            count=count+1;
            edgeListLocalLH(count,:)=[i,faceNodes(2)];
            count=count+1;
            edgeListLocalLH(count,:)=[i,faceNodes(3)];
            count=count+1;
        elseif  length(faceNodes) == 2
            edgeListLocalLH(count,:)=[i,faceNodes(1)];
            count=count+1;
            edgeListLocalLH(count,:)=[i,faceNodes(2)];
            count=count+1;
            edgeListLocalLH(count,:)=[i,0];
            count=count+1;
        elseif length(faceNodes) == 1
            edgeListLocalLH(count,:)=[i,faceNodes(1)];
            count=count+1;
            edgeListLocalLH(count,:)=[i,0];
            count=count+1;
            edgeListLocalLH(count,:)=[i,0];
            count=count+1;
        elseif isempty(faceNodes)
            edgeListLocalLH(count,:)=[i,0];
            count=count+1;
            edgeListLocalLH(count,:)=[i,0];
            count=count+1;
            edgeListLocalLH(count,:)=[i,0];
            count=count+1;
        end 
        clear faceNode_1 faceNode_2 faceNode_3 faceNodes I tmp
        if mod(i/1000,1)==0
            disp(num2str(glpfacesLen\i))
        end
    end
    toc
    edgeListLocalRH=zeros(grpFacesLen*3,2,'single');
    count=1;
    for i=1:grpFacesLen
        [faceNode_1,~]=find(grpfaces==grpfaces(i,1));
        [faceNode_2,~]=find(grpfaces==grpfaces(i,2));
        [faceNode_3,~]=find(grpfaces==grpfaces(i,3));
        faceNodes=[faceNode_1;faceNode_2;faceNode_3];
        [~, I] = unique(faceNodes, 'first');
        tmp = 1:length(faceNodes);
        tmp(I) = [];
        faceNodes=faceNodes(tmp);
        faceNodes(faceNodes==i)=[];
        if length(faceNodes) == 3
            edgeListLocalRH(count,:)=[i+glpfacesLen,faceNodes(1)+glpfacesLen];
            count=count+1;
            edgeListLocalRH(count,:)=[i+glpfacesLen,faceNodes(2)+glpfacesLen];
            count=count+1;
            edgeListLocalRH(count,:)=[i+glpfacesLen,faceNodes(3)+glpfacesLen];
            count=count+1;
        elseif length(faceNodes) == 2
            edgeListLocalRH(count,:)=[i+glpfacesLen,faceNodes(1)+glpfacesLen];
            count=count+1;
            edgeListLocalRH(count,:)=[i+glpfacesLen,faceNodes(2)+glpfacesLen];
            count=count+1;
            edgeListLocalRH(count,:)=[i+glpfacesLen,0];
            count=count+1;
        elseif length(faceNodes) == 1
            edgeListLocalRH(count,:)=[i+glpfacesLen,faceNodes(1)+glpfacesLen];
            count=count+1;
            edgeListLocalRH(count,:)=[i+glpfacesLen,0];
            count=count+1;
            edgeListLocalRH(count,:)=[i+glpfacesLen,0];
            count=count+1;
        elseif isempty(faceNodes)
            edgeListLocalRH(count,:)=[i+glpfacesLen,0];
            count=count+1;
            edgeListLocalRH(count,:)=[i+glpfacesLen,0];
            count=count+1;
            edgeListLocalRH(count,:)=[i+glpfacesLen,0];
            count=count+1;      
        end
        clear faceNode_1 faceNode_2 faceNode_3 faceNodes I tmp
        edgeListLocal=[edgeListLocalLH;edgeListLocalRH];
        edgeListLocal(edgeListLocal(:,2)==0,:)=[];
    end
elseif strcmp(downsample,'yes') % method for downsample data
    tic
    % Loop through each face of the downsample mesh
    % nfl(1) = [nodeId1, nodeId2, nodeId3];
    count=1;
    for i=1:nfllen
        [faceNode_1,~]=find(nfl==nfl(i,1)); % via current face's first node
        [faceNode_2,~]=find(nfl==nfl(i,2)); % via current face's second node
        [faceNode_3,~]=find(nfl==nfl(i,3)); % via current face's third node

        %x = linear indices of all faces containing a node with face ID == i.
        faceNodes = [faceNode_1; faceNode_2; faceNode_3];
        

        % Get the face that shares TWO or more nodes. (i.e, adjacent face - as
        % they're triangular).
        % NOTE: a "face" is defined by its three nodes.
        
        [~, I] = unique(faceNodes, "first");
        tmp = 1:length(faceNodes);
        tmp(I) = []; % remove indices of values that are unique. tmp is now a vector of indices of nodeIds that are repeated.
        faceNodes=faceNodes(tmp); % get the nodeIds that are repeated
        faceNodes(faceNodes==i)=[]; % where the node ID is from the current face, exclude it.
        
        edgeListLocalLH(i,:)=[i,faceNodes(1)]; % x(1) = nodeIds that connect to the current face via the face's first node.
        edgeListLocalLH(i+1,:)=[i,faceNodes(2)]; % x(2) = nodeIds that connect to the current face via the face's second node.
        edgeListLocalLH(i+2,:)=[i,faceNodes(3)]; % x(3) = nodeIds that connect to the current face via the face's third node.
        %clear faceNode_1 faceNode_2 faceNode_3 faceNodes I tmp
        if mod(i/1000,1)==0
            disp(num2str(nfllen\i))
        end
    end
    toc
    edgeListLocalRH=zeros(nfrlen*3,2,'single');
    count=1;
    for i=1:nfrlen
        [faceNode_1,~]=find(nfr==nfr(i,1));
        [faceNode_2,~]=find(nfr==nfr(i,2));
        [faceNode_3,~]=find(nfr==nfr(i,3));
        faceNodes=[faceNode_1;faceNode_2;faceNode_3];
        [~, I] = unique(faceNodes, 'first');
        tmp = 1:length(faceNodes);
        tmp(I) = [];
        faceNodes=faceNodes(tmp);
        faceNodes(faceNodes==i)=[];
        edgeListLocalRH(count,:)=[i+nfrlen,faceNodes(1)+nfrlen];
        count=count+1;
        edgeListLocalRH(count,:)=[i+nfrlen,faceNodes(2)+nfrlen];
        count=count+1;
        edgeListLocalRH(count,:)=[i+nfrlen,faceNodes(3)+nfrlen];
        count=count+1;
        clear faceNode_1 faceNode_2 faceNode_3 faceNodes I tmp
        if mod(i/1000,1)==0
            disp(num2str(nfrlen\i))
        end
    end
    edgeListLocal=[edgeListLocalLH;edgeListLocalRH];
end

% adj_local=sparse(edgeListLocal(:,1),edgeListLocal(:,2),ones(length(edgeListLocalLH(:,1)),1),nbFaces,nbFaces);
clear edgeListLocalLH edgeListLocalRH 
end