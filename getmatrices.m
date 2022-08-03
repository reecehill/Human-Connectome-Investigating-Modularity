function [adj_local,adj_remote_bin,adj_remote_wei,adj_remote_len,lo_adj_wei,adj_matrix,lo_adj_cortical_wei,faceROI_all,faceROI_cortical]=getmatrices(pathToFile)

display('step4: get finally connectivity matrices')

disp('loading labelSRF.mat')
load([pathToFile,'/labelSRF.mat'])
disp('loading edgeList.mat')
load([pathToFile,'/edgeList.mat'])
disp('loading trsfmTrk.mat');
load([pathToFile,'/trsfmTrk.mat']);


%% get lengths of data
nfllen=length(nfl); % number of (indexes for each triangle's angle, left hemisphere) - downsampled version
nfrlen=length(nfr); % as above, but right hemisphere.
nsublen = size(subCoor,1); % number of (co-ordinates of all sub-cortical regions)

nbFaces=size(nfr,1)+size(nfl,1)+nsublen; % number of triangles in left hemi, right hemi, and subcortical regions.


%% make local connection matrix
adj_local=sparse( ...
    double(edgeListLocal(:,1)), ...
    double(edgeListLocal(:,2)), ...
    ones(length(edgeListLocal(:,1)),1), ...
    nbFaces, ...
    nbFaces);


%% make binary connection matrix
disp('making adj_remote_bin')

adj_remote_bin=sparse(double(edgeListRemote(:,1)),double(edgeListRemote(:,2)),ones(length(edgeListRemote(:,1)),1),nbFaces,nbFaces);
adj_remote_bin=adj_remote_bin+adj_remote_bin';
adj_remote_bin(adj_remote_bin>0)=1;
%% make adj_remote_wei
disp('making adj_remote_wei')

adj_remote_wei=sparse(double(edgeListRemote(:,1)),double(edgeListRemote(:,2)),ones(length(edgeListRemote(:,1)),1),nbFaces,nbFaces);
adj_remote_wei=adj_remote_wei+adj_remote_wei';

%% make adj_matrix combining local and long rang connction matrix
adj_matrix = adj_remote_bin + adj_local;
adj_matrix(adj_matrix>0) = 1;


%% make adj_remote_len
disp('making adj_remote_len')

adj_remote_len=sparse(double(edgeListRemote(:,1)),double(edgeListRemote(:,2)),double(trk_len(edgeListRemote(:,5))),nbFaces,nbFaces);
adj_remote_len=adj_remote_len+adj_remote_len';
% adj_remote_bin(adj_remote_bin>0)=1;
[x,y,v]=find(adj_remote_len~=0);
lenx=length(x);
for i=1:lenx
adj_remote_len(x(i),y(i))=adj_remote_len(x(i),y(i))./adj_remote_wei(x(i),y(i));
end

%% make lo res matrix(68 corticals + 14 subcortical + rh/lh.cerebellum + brain-stem = 85)
disp('making lo_adj include all regions')

lo_adj_wei=zeros(85,85);
faceROI_all=[faceROIidL;faceROIidR+34;subROIid+68];
ROIlen = max(faceROI_all);
for i=1:ROIlen
    ilocs=find(faceROI_all==i);
    for j=1:ROIlen
        jlocs=find(faceROI_all==j);
        lo_adj_wei(i,j)=sum(sum(adj_remote_wei(ilocs,jlocs)));
    end 
end

disp('making lo_adj only include cortical regions')
lo_adj_cortical_wei=zeros(68,68);
faceROI_cortical=[faceROIidL;faceROIidR+34];
ROIlen = max(faceROI_cortical);
for i=1:ROIlen
    ilocs=find(faceROI_cortical==i);
    for j=1:ROIlen
        jlocs=find(faceROI_cortical==j);
        lo_adj_cortical_wei(i,j)=sum(sum(adj_remote_wei(ilocs,jlocs)));
    end 
end

end