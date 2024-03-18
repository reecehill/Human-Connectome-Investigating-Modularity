function batch_process(pathToFile,subjects,type,downsample,rate)
% pathToFile: path to all data folders
% subjects: the list of subjects
% type: two types of surface data:
%       1---lh(rh).pial.surf.gii
%       2---lh(rh).pial
% downsample: 'yes'-- downsample of surface 
%             'no'--- no downsample (default)
% rate:  downsample rate, default is 0.1, 90% left
disp(matlab.addons.installedAddons);
%start parallel pool.
gcp; 

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
addpath('toolboxes/AlongTractStats');
addpath(genpath('toolboxes/SurfStat'));
addpath('toolboxes/FieldTrip');
ft_defaults;
ft_hastoolbox('spm12',1);
ft_hastoolbox('iso2mesh',1);



sprintf('type=%d',type)


if ~exist('rate','var')
    rate = 0.1; % default
end

if ~exist('downsample','var')
    downsample = 'no'; % default is no downsample
end

if ~strcmp(downsample,'no') & ~strcmp(downsample,'yes')
  disp('wrong description of downsample, please type ''yes'' or ''no''.')
elseif strcmp(downsample,'yes')
    sprintf('downsample=%s, rate=%1f',downsample,rate)
elseif strcmp(downsample,'no')
    sprintf('downsample=%s',downsample) 
end

for i=1:length(subjects)
    gunzip([pathToFile num2str(subjects{i}) '/MNINonLinear/aparc+aseg.nii.gz']);
end

%% convert .trk file from DSI_studio to matrix containing endpoints converted to the same space, the trk_len and termination info (GM)
%  for i=1:length(subjects)
%      subject = subjects{i};
%      pathToSubjectData = [pathToFile,num2str(subject)];
%      [trkEP,trk_len,trk_type]=conversion_tt(pathToSubjectData,type);
%      filename=[pathToFile,num2str(subjects{i}),'/trsfmTrk.mat'];
%      save(filename,'trkEP','trk_len','trk_type','-v7.3');
%      clear trkEP trk_len trk_type
%  end

 
 %%  assign freesurfer ROI labels to each face
%  for i=1:length(subjects)
%      [faceROIidL,faceROIidR,hi_faceROIidL,hi_faceROIidR,filenames,subfilenames,glpfaces,grpfaces,glpvertex,grpvertex,nfl,nfr,nvl,nvr,subCoor,subROIid,hi_subCoor,hi_subROIid,lo_centroidsL,lo_centroidsR,hi_centroidsL,hi_centroidsR]=loadLabels([pathToFile,subjects{i}],subjects{i},type,downsample,rate);
%      filename=[pathToFile,subjects{i},'/labelSRF.mat'];
%      save(filename,'faceROIidL','faceROIidR','hi_faceROIidL','hi_faceROIidR','filenames','subfilenames','glpfaces','grpfaces','glpvertex','grpvertex','nfl','nfr','nvl','nvr','subCoor','subROIid','hi_subCoor','hi_subROIid','lo_centroidsL','lo_centroidsR','hi_centroidsL','hi_centroidsR','-v7.3');
%      clear faceROIidL faceROIidR filenames subfilenames glpfaces grpfaces glpvertex grpvertex nfl nfr nvl nvr subCoor subROIid
%  end

%% Make edgelist and other stuff
for i=1:length(subjects)
    [edgeListRemote,edgeListLocal,lpcentroids,rpcentroids,subCoor]=makeEdgeList([pathToFile,subjects{i}],downsample);
    filename=[pathToFile,subjects{i},'/edgeList.mat'];
    save(filename,'edgeListRemote','edgeListLocal','lpcentroids','rpcentroids','subCoor','-v7.3');
    clear edgeListRemote edgeListLocal;
end


%% Make adjacency matrices (low and hi res)
for i=1:length(subjects)
    [adj_local,adj_remote_bin,adj_remote_wei,adj_remote_len,lo_adj_wei,adj_matrix,lo_adj_cortical_wei,faceROI_all,faceROI_cortical]=getmatrices([pathToFile,subjects{i},'/'], downsample);
    filename=[pathToFile,subjects{i},'/matrices.mat'];
    save(filename,'adj_local','adj_remote_bin','adj_remote_wei','adj_remote_len','lo_adj_wei','adj_matrix','lo_adj_cortical_wei','faceROI_all','faceROI_cortical','-v7.3');
end

%% map coordinates into MNI space
for i=1:length(subjects)
    [Coor_MNI305,Coor_MNI152]=getMNIFromRasCoords([pathToFile,subjects{i},'/'],subjects{i},[lpcentroids;rpcentroids;subCoor],type);
    filename=[pathToFile,subjects{i},'/MNIcoor.mat'];
    save(filename,'Coor_MNI305','Coor_MNI152','-v7.3');
    clear lpcentroids rpcentroids subCoor;
end

disp("Finished using structural data in MATLAB.");
%quit;

%%DELETE BELOW
adj_matrix = matfile('../../data/subjects/100610/matrices.mat').adj_matrix;
%adj_matrix_ds = matfile('../../data/subjects/100610/whole_brain_FreeSurferDKT_Cortical.mat');
load('../../data/subjects/100610/edgeList.mat');
load('../../data/subjects/100610/labelSRF.mat');
load('../../data/subjects/100610/matrices.mat');
load('../../data/subjects/100610/trsfmTrk.mat');
allFileNames = [filenames; subfilenames']';
plottedLabels=allFileNames(faceROI_all);
[~, positionOfFirstLabel, ~] = unique(plottedLabels, "first");
[~, positionOfLastLabel, ~] = unique(plottedLabels, "last");
positionOfMiddleLabel = floor(mean([positionOfFirstLabel positionOfLastLabel], 2));
plottedLabelsFinal_all = sort(positionOfMiddleLabel);

figure;
title("Whole connectivity matrix.")
spy(adj_matrix);
hold on;
set(gca, 'Ytick',1:1:length(plottedLabelsFinal_all),'YTickLabel',plottedLabels(plottedLabelsFinal_all));
set(gca, 'Xtick',1:1:length(plottedLabelsFinal_all),'XTickLabel',plottedLabels(plottedLabelsFinal_all));
savefig('../../data/subjects/100610/whole_adjmatrix.fig');
saveas(gcf, '../../data/subjects/100610/whole_adjmatrix.png');
%%DELETE ABOVE


end



















