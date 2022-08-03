% Iterative community finetuning.
% W is the input connection matrix.
close all;
showTicksPer = 500;

adj_matrix = matfile('D:\Dissertation\Participants\sub-01\matlab-output-10-million\matrices.mat').adj_matrix;
load('D:\Dissertation\Participants\sub-01\matlab-output-10-million\labelSRF.mat');


filenames={'lh.bankssts.label';'lh.caudalanteriorcingulate.label';'lh.caudalmiddlefrontal.label';'lh.cuneus.label';'lh.entorhinal.label';'lh.frontalpole.label';'lh.fusiform.label';'lh.inferiorparietal.label';'lh.inferiortemporal.label';'lh.insula.label';'lh.isthmuscingulate.label';'lh.lateraloccipital.label';'lh.lateralorbitofrontal.label';'lh.lingual.label';'lh.medialorbitofrontal.label';'lh.middletemporal.label';'lh.paracentral.label';'lh.parahippocampal.label';'lh.parsopercularis.label';'lh.parsorbitalis.label';'lh.parstriangularis.label';'lh.pericalcarine.label';'lh.postcentral.label';'lh.posteriorcingulate.label';'lh.precentral.label';'lh.precuneus.label';'lh.rostralanteriorcingulate.label';'lh.rostralmiddlefrontal.label';'lh.superiorfrontal.label';'lh.superiorparietal.label';'lh.superiortemporal.label';'lh.supramarginal.label';'lh.temporalpole.label';'lh.transversetemporal.label';'rh.bankssts.label';'rh.caudalanteriorcingulate.label';'rh.caudalmiddlefrontal.label';'rh.cuneus.label';'rh.entorhinal.label';'rh.frontalpole.label';'rh.fusiform.label';'rh.inferiorparietal.label';'rh.inferiortemporal.label';'rh.insula.label';'rh.isthmuscingulate.label';'rh.lateraloccipital.label';'rh.lateralorbitofrontal.label';'rh.lingual.label';'rh.medialorbitofrontal.label';'rh.middletemporal.label';'rh.paracentral.label';'rh.parahippocampal.label';'rh.parsopercularis.label';'rh.parsorbitalis.label';'rh.parstriangularis.label';'rh.pericalcarine.label';'rh.postcentral.label';'rh.posteriorcingulate.label';'rh.precentral.label';'rh.precuneus.label';'rh.rostralanteriorcingulate.label';'rh.rostralmiddlefrontal.label';'rh.superiorfrontal.label';'rh.superiorparietal.label';'rh.superiortemporal.label';'rh.supramarginal.label';'rh.temporalpole.label';'rh.transversetemporal.label'};
subfilenames=transpose({'lh.thalamus'	'lh.caudate'	'lh.putamen'	'lh.pallidum'	'lh.amygdala'	'lh.hippocampus'	'lh.accumbens'	'lh.cerebellum'	'rh.thalamus'	'rh.caudate'	'rh.putamen'	'rh.pallidum'	'rh.amygdala'	'rh.hippocampus'	'rh.accumbens'	'rh.cerebellum'	'Brain-stem'});
allFilenames = [filenames;subfilenames];

regionNameIds = [faceROIidL; faceROIidR+34; subROIid+34+17];
allLabels = allFilenames(regionNameIds);

nodeIdsOfInterest = find(ismember(allLabels, ["lh.superiorfrontal.label","lh.superiorparietal.label"]));
labelsOfInterest = allLabels(nodeIdsOfInterest);

newMatrix = adj_matrix(nodeIdsOfInterest,nodeIdsOfInterest);


figure2 = figure;
plottedLabels = allLabels(1:showTicksPer:end);

spy(adj_matrix);
rectangle('Position',[min(nodeIdsOfInterest) min(nodeIdsOfInterest) length(nodeIdsOfInterest) length(nodeIdsOfInterest)])
xticks(1:showTicksPer:length(allLabels));
yticks(1:showTicksPer:length(allLabels));
xticklabels(plottedLabels);
yticklabels(plottedLabels);

figure1 = figure;
plottedLabels = labelsOfInterest(1:showTicksPer:end);
spy(newMatrix);
xticks(1:showTicksPer:length(allLabels));
yticks(1:showTicksPer:length(allLabels));

xticklabels(plottedLabels);
yticklabels(plottedLabels);

%% attempt module detection
% Iterative community finetuning.
%W is the input connection matrix.
W = newMatrix;
n  = size(W,1);             % number of nodes
%M  = 1:n;                   % initial community affiliations
Q0 = -1; Q1 = 0;            % initialize modularity values
while Q1-Q0>1e-5           % while modularity increases
    Q0 = Q1;                % perform community detection
    [M, Q1] = community_louvain(W, 1.5);
end
figure1 = figure;
hold on;

moduleIndex = min(M);
%For each module
cmap = hsv(length(M));
for i = transpose(M)
    % Get ids of nodes that are in this module.
    nodeIds = find(M == i);
    nodesByModule = zeros(size(newMatrix));
    nodesByModule(nodeIds, nodeIds) = 1;
    spy(nodesByModule);
    drawnow;
    x=get(gca,'children');
    lastX = length(x);
    color = [cmap(lastX,:)];
    set(x(lastX),'color',color);
end