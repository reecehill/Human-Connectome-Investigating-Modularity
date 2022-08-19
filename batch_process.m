function batch_process(pathToFile,subjects,type,downsample,rate)
% pathToFile: path to all data folders
% subjects: the list of subjects
% type: two types of surface data:
%       1---lh(rh).pial.surf.gii
%       2---lh(rh).pial
% downsample: 'yes'-- downsample of surface 
%             'no'--- no downsample (default)
% rate:  downsample rate, default is 0.1, 90% left

% Ensure numbers are numbers and not char
if(isa(type, "char"))
    type = str2double(type);
end
if(isa(rate, "char"))
    rate = str2double(rate);
end

disp(subjects);
subjects={subjects};
clear ft_hastoolbox;
restoredefaultpath;
addpath('C:\Users\Reece\AppData\Roaming\MathWorks\MATLAB Add-Ons\Collections\AlongTractStats');
addpath('C:\Users\Reece\AppData\Roaming\MathWorks\MATLAB Add-Ons\Collections\Gifti');
addpath('C:\Users\Reece\AppData\Roaming\MathWorks\MATLAB Add-Ons\Collections\Iso2Mesh');
addpath(genpath('C:\Users\Reece\AppData\Roaming\MathWorks\MATLAB Add-Ons\Collections\SurfStat'));
addpath(genpath('C:\Program Files\MATLAB\R2021b\spm12'));
addpath('C:\Users\Reece\AppData\Roaming\MathWorks\MATLAB Add-Ons\Collections\FieldTrip');
ft_defaults;


sprintf('type=%d',type)


if ~exist('rate','var')
    rate = 0.1; % default
end

if ~exist('downsample','var')
    downsample = 'no'; % default is no downsample
end

if ~strcmp(downsample,'no') & ~strcmp(downsample,'yes')
  display('wrong description of downsample, please type ''yes'' or ''no''.')
elseif strcmp(downsample,'yes')
    sprintf('downsample=%s, rate=%1f',downsample,rate)
elseif strcmp(downsample,'no')
    sprintf('downsample=%s',downsample) 
end

% convert .trk file from DSI_studio to matrix containing endpoints converted to the same space, the trk_len and termination info (GM)
 
%  for i=1:length(subjects)
%      subject = subjects{i}
%      pathToSubjectData = [pathToFile,num2str(subject)]
%      [trkEP,trk_len,trk_type]=conversion(pathToSubjectData,type);
%      filename=[pathToFile,num2str(subjects{i}),'/trsfmTrk.mat'];
%      save(filename,'trkEP','trk_len','trk_type','-v7.3');
%      clear trkEP trk_len trk_type
%  end
 %%  assign freesurfer ROI labels to each face
 
%  for i=1:length(subjects)
%      [faceROIidL,faceROIidR,filenames,subfilenames,glpfaces,grpfaces,glpvertex,grpvertex,nfl,nfr,nvl,nvr,subCoor,subROIid]=loadLabels([pathToFile,subjects{i}],type,downsample,rate);
%  %     [faceROIidL,faceROIidR,filenames,glpfaces,grpfaces,glpvertex,grpvertex,nfl,nfr,nvl,nvr]=loadLabels([pathToFile,subjects{i}]);
%      % save data
%      filename=[pathToFile,subjects{i},'/labelSRF.mat'];
%      save(filename,'faceROIidL','faceROIidR','filenames','subfilenames','glpfaces','grpfaces','glpvertex','grpvertex','nfl','nfr','nvl','nvr','subCoor','subROIid','-v7.3');
%      clear faceROIidL faceROIidR filenames subfilenames glpfaces grpfaces glpvertex grpvertex nfl nfr nvl nvr subCoor subROIid
%  end

%% Make edgelist and other stuff
for i=1:length(subjects)
    [edgeListRemote,edgeListLocal,lpcentroids,rpcentroids,subCoor]=makeEdgeList([pathToFile,subjects{i}],downsample);
    filename=[pathToFile,subjects{i},'/edgeList.mat'];
    save(filename,'edgeListRemote','edgeListLocal','lpcentroids','rpcentroids','subCoor','-v7.3');
    clear edgeListRemote,edgeListLocal;
end

%% Make adjacency matrices (low and hi res)
for i=1:length(subjects)
    [adj_local,adj_remote_bin,adj_remote_wei,adj_remote_len,lo_adj_wei,adj_matrix,lo_adj_cortical_wei,faceROI_all,faceROI_cortical]=getmatrices([pathToFile,subjects{i},'/']);
    filename=[pathToFile,subjects{i},'/matrices.mat'];
    save(filename,'adj_local','adj_remote_bin','adj_remote_wei','adj_remote_len','lo_adj_wei','adj_matrix','lo_adj_cortical_wei','faceROI_all','faceROI_cortical','-v7.3');
end

%% map coordinates into MNI space
for i=1:length(subjects)
    [Coor_MNI305,Coor_MNI152]=getMNIFromRasCoords([pathToFile,subjects{i}],[lpcentroids;rpcentroids;subCoor],type);
    filename=[pathToFile,subjects{i},'/MNIcoor.mat'];
    save(filename,'Coor_MNI305','Coor_MNI152','-v7.3');
    clear lpcentroids,rpcentroids,subCoor;
end

display(["Finished using structural data in MATLAB."]);
quit;
end


















