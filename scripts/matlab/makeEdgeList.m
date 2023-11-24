function [edgeListRemote,edgeListLocal,lpcentroids,rpcentroids,subCoor]=makeEdgeList(pathToFile,downsample)
clear ft_hastoolbox;
restoredefaultpath;
addpath('toolboxes/AlongTractStats');
addpath('toolboxes/Gifti');
addpath('toolboxes/Iso2Mesh');
addpath(genpath('toolboxes/SurfStat'));
addpath(genpath('toolboxes/spm12'));
addpath('toolboxes/FieldTrip');
ft_defaults;

display('step3: check if there are fibres connected between node pairs')

%% load the data that was output by loadLabels.m
disp('loading labelSRF.mat');
fileToLoad=[pathToFile,'/labelSRF.mat'];
load(fileToLoad);

%% load the data that was output by conversion.m
disp('loading trsfmTrk.mat');
fileToLoad=[pathToFile,'/trsfmTrk.mat'];
load(fileToLoad, "trk_type", "trk_len", "trkEP");
%% get lengths of data

nbTracts=length(trkEP);
%% get centres of triangles
disp('computing centroids');
if strcmp(downsample,'no') % method for no downsample
    lpcentroids=meshcentroid(glpvertex,glpfaces);
    rpcentroids=meshcentroid(grpvertex,grpfaces);
    glpfacesLen=length(glpfaces);
    grpFacesLen=length(grpfaces);
    nbFaces=size(grpfaces,1)+size(glpfaces,1);
else
    lpcentroids=meshcentroid(nvl,nfl);
    rpcentroids=meshcentroid(nvr,nfr);
    nfllen=length(nfl);
    nfrlen=length(nfr);
    nbFaces=size(nfr,1)+size(nfl,1);
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
fprintf('Building Remove connection elist:\n');
fprintf(['\n' repmat('.',1,round(nbTracts/100000)) '\n\n']);

buildRemote = 1;
if(buildRemote == 1)
    parfor k=1:nbTracts    
        if mod(k/1000,1)==0
        %disp(num2str(nbTracts\k))
        end
        if mod(k/100000,1)==0
        %disp(num2str(nbTracts\k))
        fprintf('\b|\n');
        end
        
        if trk_type(k,3) ~=0
            % This moves the start and end points of the tracts to the
            % nearest centroids on the resampled/original mesh (downsampled dependent). 
            startp=trkEP(k,1:3);
            endp=trkEP(k,4:6);
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
    toc
    edgeListRemote(find(edgeListRemote(:,5)==0),:)=[];
end
% columns 1:2 are the edges to which they connect, columns 3:4 are the
% distance from the pial surface, column 5 is the track ID.

%% get local connection -- downsample or no downsample
disp('building local connection matrix');

% adj_local=sparse(nbFaces,nbFaces);
count=1;
% two method pointing to downsample or no downsample
if strcmp(downsample,'no') % method for no downsample
    edgeListLocalLH=zeros(glpfacesLen*3,2,'single');
    tic
    for i=1:glpfacesLen
        [x1,~]=find(glpfaces==glpfaces(i,1));
        [x2,~]=find(glpfaces==glpfaces(i,2));
        [x3,~]=find(glpfaces==glpfaces(i,3));
        x=[x1;x2;x3];
        [~, I] = unique(x, 'first');
        tmp = 1:length(x);
        tmp(I) = [];
        x=x(tmp);
        x(x==i)=[];
        if length(x) == 3
            edgeListLocalLH(count,:)=[i,x(1)];
            count=count+1;
            edgeListLocalLH(count,:)=[i,x(2)];
            count=count+1;
            edgeListLocalLH(count,:)=[i,x(3)];
            count=count+1;
        elseif  length(x) == 2
            edgeListLocalLH(count,:)=[i,x(1)];
            count=count+1;
            edgeListLocalLH(count,:)=[i,x(2)];
            count=count+1;
            edgeListLocalLH(count,:)=[i,0];
            count=count+1;
        elseif length(x) == 1
            edgeListLocalLH(count,:)=[i,x(1)];
            count=count+1;
            edgeListLocalLH(count,:)=[i,0];
            count=count+1;
            edgeListLocalLH(count,:)=[i,0];
            count=count+1;
        elseif length(x) == 0
            edgeListLocalLH(count,:)=[i,0];
            count=count+1;
            edgeListLocalLH(count,:)=[i,0];
            count=count+1;
            edgeListLocalLH(count,:)=[i,0];
            count=count+1;
        end 
        clear x1 x2 x3 x I tmp
        if mod(i/1000,1)==0
            disp(num2str(glpfacesLen\i))
        end
    end
    toc
    edgeListLocalRH=zeros(grpFacesLen*3,2,'single');
    count=1;
    for i=1:grpFacesLen
        [x1,~]=find(grpfaces==grpfaces(i,1));
        [x2,~]=find(grpfaces==grpfaces(i,2));
        [x3,~]=find(grpfaces==grpfaces(i,3));
        x=[x1;x2;x3];
        [~, I] = unique(x, 'first');
        tmp = 1:length(x);
        tmp(I) = [];
        x=x(tmp);
        x(x==i)=[];
        if length(x) == 3
            edgeListLocalRH(count,:)=[i+glpfacesLen,x(1)+glpfacesLen];
            count=count+1;
            edgeListLocalRH(count,:)=[i+glpfacesLen,x(2)+glpfacesLen];
            count=count+1;
            edgeListLocalRH(count,:)=[i+glpfacesLen,x(3)+glpfacesLen];
            count=count+1;
        elseif length(x) == 2
            edgeListLocalRH(count,:)=[i+glpfacesLen,x(1)+glpfacesLen];
            count=count+1;
            edgeListLocalRH(count,:)=[i+glpfacesLen,x(2)+glpfacesLen];
            count=count+1;
            edgeListLocalRH(count,:)=[i+glpfacesLen,0];
            count=count+1;
        elseif length(x) == 1
            edgeListLocalRH(count,:)=[i+glpfacesLen,x(1)+glpfacesLen];
            count=count+1;
            edgeListLocalRH(count,:)=[i+glpfacesLen,0];
            count=count+1;
            edgeListLocalRH(count,:)=[i+glpfacesLen,0];
            count=count+1;
        elseif length(x) == 0
            edgeListLocalRH(count,:)=[i+glpfacesLen,0];
            count=count+1;
            edgeListLocalRH(count,:)=[i+glpfacesLen,0];
            count=count+1;
            edgeListLocalRH(count,:)=[i+glpfacesLen,0];
            count=count+1;      
        end
        clear x1 x2 x3 x I tmp
        edgeListLocal=[edgeListLocalLH;edgeListLocalRH];
        edgeListLocal(find(edgeListLocal(:,2)==0),:)=[];
    end
elseif strcmp(downsample,'yes') % method for downsample data
    tic
    % Loop through each face of the downsample mesh
    % nfl(1) = [nodeId1, nodeId2, nodeId3];
    for i=1:nfllen
        % x1 = linear indices of the faces that share a node with current face.
        [x1,~]=find(nfl==nfl(i,1)); % via current face's first node
        [x2,~]=find(nfl==nfl(i,2)); % via current face's second node
        [x3,~]=find(nfl==nfl(i,3)); % via current face's third node

        %x = linear indices of all faces containing a node with ID == i.
        x=[x1;x2;x3];

        %I = indices of x that contain unique values.
        [~, I] = unique(x, 'first');
        tmp = 1:length(x);
        tmp(I) = []; % remove indices of values that are unique. tmp is now a vector of indices of nodeIds that are repeated.
        x=x(tmp); % get the nodeIds that are repeated
        x(x==i)=[]; % where the node ID is from the current face, exclude it.
        edgeListLocalLH(count,:)=[i,x(1)]; % x(1) = nodeIds that connect to the current face via the face's first node.
        count=count+1;
        edgeListLocalLH(count,:)=[i,x(2)]; % x(2) = nodeIds that connect to the current face via the face's second node.
        count=count+1;
        edgeListLocalLH(count,:)=[i,x(3)]; % x(3) = nodeIds that connect to the current face via the face's third node.
        count=count+1;
        clear x1 x2 x3 x I tmp
        if mod(i/1000,1)==0
            disp(num2str(nfllen\i))
        end
    end
    toc
    edgeListLocalRH=zeros(nfrlen*3,2,'single');
    count=1;
    for i=1:nfrlen
        [x1,~]=find(nfr==nfr(i,1));
        [x2,~]=find(nfr==nfr(i,2));
        [x3,~]=find(nfr==nfr(i,3));
        x=[x1;x2;x3];
        [~, I] = unique(x, 'first');
        tmp = 1:length(x);
        tmp(I) = [];
        x=x(tmp);
        x(x==i)=[];
        edgeListLocalRH(count,:)=[i+nfllen,x(1)+nfllen];
        count=count+1;
        edgeListLocalRH(count,:)=[i+nfllen,x(2)+nfllen];
        count=count+1;
        edgeListLocalRH(count,:)=[i+nfllen,x(3)+nfllen];
        count=count+1;
        clear x1 x2 x3 x I tmp
        if mod(i/1000,1)==0
            disp(num2str(nfrlen\i))
        end
    end
    edgeListLocal=[edgeListLocalLH;edgeListLocalRH];
end

% adj_local=sparse(edgeListLocal(:,1),edgeListLocal(:,2),ones(length(edgeListLocalLH(:,1)),1),nbFaces,nbFaces);
clear edgeListLocalLH edgeListLocalRH 


end