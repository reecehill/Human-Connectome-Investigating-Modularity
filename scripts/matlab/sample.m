function sample()
clear ft_hastoolbox;
restoredefaultpath;
savepath;
addpath('toolboxes/AlongTractStats');
addpath(genpath('toolboxes/SurfStat'));
addpath('toolboxes/FieldTrip');
ft_defaults;
ft_hastoolbox('spm12',1);
ft_hastoolbox('iso2mesh',1);
ft_hastoolbox('gifti',1);
close all;


subjectId = '100206';
downsample = 'yes';
pathToFile = '../../data/subjects/100206';
type = 1;
condition = 'lh';

adj_matrix = matfile(['../../data/subjects/',subjectId,'/matrices.mat']).adj_matrix;
%adj_matrix_ds = matfile('../../data/subjects/100610/whole_brain_FreeSurferDKT_Cortical.mat');
load(['../../data/subjects/',subjectId,'/edgeList.mat']);
load(['../../data/subjects/',subjectId,'/labelSRF.mat']);
load(['../../data/subjects/',subjectId,'/matrices.mat']);
load(['../../data/subjects/',subjectId,'/trsfmTrk.mat']);
load(['../../data/subjects/',subjectId,'/optimal_struc_modules.mat']);

[roiL_ids, roiR_ids] = getROIIds(pathToFile, downsample, "lh.L_precentral", "rh.R_precentral");
roiR_ids = roiR_ids - length(lo_glpfaces(:,1));
usePreStatsModules = false;
if(usePreStatsModules)
    roiStrucModulesL = readmatrix(['../../data/subjects/',subjectId,'/exported_modules/left_structural_modules.csv'])';
    roiStrucModulesR =  readmatrix(['../../data/subjects/',subjectId,'/exported_modules/right_structural_modules.csv'])';
    allStrucModulesL = readmatrix(['../../data/subjects/',subjectId,'/exported_modules/all_left_structural_modules.csv'])';
    allStrucModulesR = readmatrix(['../../data/subjects/',subjectId,'/exported_modules/all_right_structural_modules.csv'])';
    roiFuncModulesL_lf = readmatrix(['../../data/subjects/',subjectId,'/exported_modules/left_',condition,'_functional_modules.csv'])';
    roiFuncModulesR_lf = readmatrix(['../../data/subjects/',subjectId,'/exported_modules/right_',condition,'_functional_modules.csv'])';
else
    allStrucModulesL = ones(size(lo_glpfaces(:,1)))*-1;
    allStrucModulesR = ones(size(lo_grpfaces(:,1)))*-1;
    roiStrucModulesL = readmatrix(['../../data/subjects/',subjectId,'/statistics/left_hemisphere/datasets/cleaned_mapped_left_structural_modules.csv']);
    roiStrucModulesR =  readmatrix(['../../data/subjects/',subjectId,'/statistics/right_hemisphere/datasets/cleaned_mapped_right_structural_modules.csv']);
    allStrucModulesL(roiL_ids(roiStrucModulesL(:,1))) = roiStrucModulesL(:,2);
    allStrucModulesR(roiR_ids(roiStrucModulesR(:,1))) = roiStrucModulesR(:,2);
    %allStrucModulesL = readmatrix(['../../data/subjects/',subjectId,'/exported_modules/all_left_structural_modules.csv'])';
    %allStrucModulesR = readmatrix(['../../data/subjects/',subjectId,'/exported_modules/all_right_structural_modules.csv'])';


    allFuncModulesL_lf = ones(size(lo_glpfaces(:,1)))*-1;
    allFuncModulesR_lf = ones(size(lo_grpfaces(:,1)))*-1;
    roiFuncModulesL_lf = readmatrix(['../../data/subjects/',subjectId,'/statistics/left_hemisphere/datasets/cleaned_mapped_left_',condition,'_functional_modules.csv']);
    roiFuncModulesR_lf = readmatrix(['../../data/subjects/',subjectId,'/statistics/right_hemisphere/datasets/cleaned_mapped_right_',condition,'_functional_modules.csv']);
    allFuncModulesL_lf(roiL_ids(roiFuncModulesL_lf(:,1))) = roiFuncModulesL_lf(:,2);
    allFuncModulesR_lf(roiR_ids(roiFuncModulesR_lf(:,1))) = roiFuncModulesR_lf(:,2);
end


%load(['../../data/subjects/',subjectId,'/modulesByFace.mat']);
[inflated_lo_glpfaces, inflated_lo_grpfaces, inflated_lo_glpvertex, inflated_lo_grpvertex, filenames, subfilenames, inflated_lo_ROIfacevert]  = loadMesh([pathToFile,'/MNINonLinear/fsaverage_LR32k/',subjectId,'.L.very_inflated_MSMAll.32k_fs_LR.surf.gii'],[pathToFile,'/MNINonLinear/fsaverage_LR32k/',subjectId,'.R.very_inflated_MSMAll.32k_fs_LR.surf.gii'],pathToFile,subjectId,type);
[flat_lo_glpfaces, flat_lo_grpfaces, flat_lo_glpvertex, flat_lo_grpvertex, filenames, subfilenames, flat_lo_ROIfacevert]  = loadMesh([pathToFile,'/MNINonLinear/fsaverage_LR32k/',subjectId,'.L.flat.32k_fs_LR.surf.gii'],[pathToFile,'/MNINonLinear/fsaverage_LR32k/',subjectId,'.R.flat.32k_fs_LR.surf.gii'],pathToFile,subjectId,type);
highestLhLabelId = find(contains(filenames,'lh.'), 1, 'last' );
lowestLhLabelId = find(contains(filenames,'lh.'), 1, 'first' );
highestRhLabelId = find(contains(filenames,'rh.'), 1, 'last' );
lowestRhLabelId = find(contains(filenames,'rh.'), 1, 'first' );
[~,flat_lo_faceToNodeMapLH] = loopROIAndAssignLabels(lowestLhLabelId, highestLhLabelId, flat_lo_glpfaces, flat_lo_ROIfacevert);
[~,flat_lo_faceToNodeMapRH] = loopROIAndAssignLabels(lowestRhLabelId, highestRhLabelId, flat_lo_grpfaces, flat_lo_ROIfacevert);
  

figure;
title("Weighted adjacency matrix - Remote + Local");
allFileNames = [filenames subfilenames];
downsample=true;
if(downsample)
    labelIds=[lo_faceROIidL(:,1); lo_faceROIidR(:,1); double(max(lo_faceROIidR(:,1)))+lo_faceROIidSubCor];
else
    labelIds=[hi_faceROIidL(:,1); hi_faceROIidR(:,1); double(max(hi_faceROIidR(:,1)))+hi_faceROIidSubCor];
end
indicesOfLabelledFaces = labelIds >= 1; %ignore NaNs
plottedLabelIds = labelIds(indicesOfLabelledFaces);
plottedLabelsNames=allFileNames(plottedLabelIds);
[plottedLabelNamesSorted, I] =sort(string(plottedLabelsNames), 'ascend');
nFibres = int2str(sum(adj_matrix_wei(I, I), "all") / 2);
subtitle(['Whole brain in MNINonLinear space; seeded by whole brain; sorted by labels (ascend); ', nFibres, ' fibres;']);
plottedLabelIdsSorted=plottedLabelIds(I);
hold on;
grid on;
c = colorbar;
c.Label.String = 'Number of connections';
hold on;
grid on;
plottedLabelsNames=plottedLabelNamesSorted;
showTicksPer=100000;
xticks(1:(showTicksPer/50):length(plottedLabelsNames));
yticks(1:(showTicksPer/50):length(plottedLabelsNames));
xticklabels(plottedLabelsNames(1:(showTicksPer/50):end));
yticklabels(plottedLabelsNames(1:(showTicksPer/50):end));
hemisphereL_start = find(ismember(plottedLabelIdsSorted(:,1),find(contains(allFileNames,"lh."))), 1, "first" );
hemisphereL_end = find(ismember(plottedLabelIdsSorted(:,1),find(contains(allFileNames,"lh."))), 1, "last" );
hemisphereL_length = hemisphereL_end-hemisphereL_start;
hemisphereR_start = find(ismember(plottedLabelIdsSorted(:,1),find(contains(allFileNames,"rh."))), 1, "first" );
hemisphereR_end = find(ismember(plottedLabelIdsSorted(:,1),find(contains(allFileNames,"rh."))), 1, "last" );
hemisphereR_length = hemisphereR_end-hemisphereR_start;
miscellaneous_start = 1;
miscellaneous_end = hemisphereL_start-1;
miscellaneous_length = miscellaneous_end-miscellaneous_start;
roiL_start = min(roiL_ids);
roiL_end = max(roiL_ids);
roiL_length = roiL_end-roiL_start;
roiR_start = min(roiR_ids);
roiR_end = max(roiR_ids);
roiR_length = roiR_end-roiR_start;
rectangle('Position',[[hemisphereL_start, hemisphereL_start], hemisphereL_length, hemisphereL_length], 'FaceColor', [0 0 0 0.05], 'EdgeColor', [0 0 0 0.2]);
rectangle('Position',[[hemisphereR_start, hemisphereR_start], hemisphereR_length, hemisphereR_length], 'FaceColor', [0 0 0 0.05], 'EdgeColor', [0 0 0 0.2]);
rectangle('Position',[[miscellaneous_start, miscellaneous_start], miscellaneous_length, miscellaneous_length], 'FaceColor', [0 0 0 0.05], 'EdgeColor', [0 0 0 0.2]);
rectangle('Position',[[roiL_start, roiL_start], roiL_length, roiL_length], 'FaceColor', [1 0 0 0.1], 'EdgeColor', [1 0 0 0.2]);
rectangle('Position',[[roiR_start roiR_start], roiR_length, roiR_length], 'FaceColor', [1 0 0 0.1], 'EdgeColor', [1 0 0 0.2]);
grid off
cspy(adj_matrix_wei(I,I),'ColorMap','jet','MarkerSize',5);
legends = [];
legends = [legends, line(NaN,NaN,'LineWidth',4,'LineStyle','-','Color',[1 0 0 0.4])];
legends = [legends, line(NaN,NaN,'LineWidth',4,'LineStyle','-','Color',[0 0 0 0.05])];
legends = [legends, line(NaN,NaN,'LineWidth',4,'LineStyle','-','Color',[0 0 1 1])];
legend(legends,'Precentral Gyri','Hemispheres','Edge');

figure;
title("Left Hemisphere - Precentral Gyrus");
ax = gca;
ax.XMinorTick = 'on';
ax.YMinorTick = 'on';
c = colorbar;
c.Label.String = 'Number of connections';
hold on;
xlabel('Node within ROI');
xticks(0:100:length(roiL_ids));
yticks(0:100:length(roiL_ids));
ylabel('Node within ROI');
cspy_magnitude(adj_matrix_wei(I(roiL_ids),I(roiL_ids)),'ColorMap','jet');

figure;
title("With structural modules")
subtitle("Whole brain in MNINonLinear space; seeded by ROI (precentral); sorted by modules (ascend)");
c = colorbar;
c.Label.String = 'Number of connections';
hold on;
ax = gca;
ax.XMinorTick = 'on';
ax.YMinorTick = 'on';
xlabel('Node within ROI');
xticks(0:100:length(roiL_ids));
yticks(0:100:length(roiL_ids));
ylabel('Node within ROI');

[strucModulesL_sorted, I_strucModulesL]= sort(roiStrucModulesL(:,2));
legends = [];
legendText = {};
legends = [legends, line(NaN,NaN,'LineWidth',4,'LineStyle','-','Color',[1 0 0 0.4])];
legends = [legends, line(NaN,NaN,'LineWidth',4,'LineStyle','-','Color',[0 0 0 0.05])];
legends = [legends, line(NaN,NaN,'LineWidth',4,'LineStyle','-','Color',[0 0 1 1])];
legendText = [legendText; 'Precentral Gyri'; 'Hemispheres'; 'Edge'];

cspy(adj_matrix_wei(I(roiL_ids(I_strucModulesL)),I(roiL_ids(I_strucModulesL))),'ColorMap','jet','MarkerSize',10);
for moduleId=1:max(strucModulesL_sorted)
    moduleIds = find(strucModulesL_sorted == moduleId);
    moduleStart = min(moduleIds);
    moduleEnd = max(moduleIds);
    moduleLength = moduleEnd-moduleStart;
    rectangle('Position',[[moduleStart, moduleStart], moduleLength, moduleLength], 'FaceColor', [1 0 0 0.1], 'EdgeColor', [1 0 0 0.2]);
    legends = [legends, line(NaN,NaN,'LineWidth',4,'LineStyle','-','Color',[1 0 0 0.1])];
    legendText = [legendText; ['Module #',num2str(moduleId)]];
end
legend(legends,legendText{:});

%% Structural modules on pial surface
graphOpts = {'FaceAlpha',1,'EdgeAlpha',0.04,'AlignVertexCenters','on','LineJoin','round','FaceLighting','gouraud'};
figure;
title("Structural modules on brain surface (precentral only) ");
hold on;
nModules_L = length(unique(allStrucModulesL));
nModules_R = length(unique(allStrucModulesR));
nModules = nModules_L + nModules_R;


plotsurf(lo_glpvertex,lo_glpfaces(~ismember(1:end,roiL_ids),:),'FaceAlpha',1,'EdgeAlpha',0.05,'FaceColor',[0.5 0 0]);
plotsurf(lo_grpvertex,lo_grpfaces(~ismember(1:end,roiR_ids),:),'FaceAlpha',1,'EdgeAlpha',0.05,'FaceColor',[0.5 0 0]);
plotsurf(lo_glpvertex,[lo_glpfaces(roiL_ids,:) allStrucModulesL(roiL_ids)],graphOpts{:});
plotsurf(lo_grpvertex,[lo_grpfaces(roiR_ids,:) allStrucModulesR(roiR_ids)],graphOpts{:});
campos(1.0e+03 * [-0.7198    1.0299    0.4153]);
lighting gouraud;
camlight;

figure;
title("Functional (left foot movement) modules on brain surface (precentral only) ");
hold on;

plotsurf(lo_glpvertex,lo_glpfaces(~ismember(1:end,roiL_ids),:),'FaceAlpha',1,'EdgeAlpha',0.05,'FaceColor',[0.5 0 0]);
plotsurf(lo_grpvertex,lo_grpfaces(~ismember(1:end,roiR_ids),:),'FaceAlpha',1,'EdgeAlpha',0.05,'FaceColor',[0.5 0 0]);
plotsurf(lo_glpvertex,[lo_glpfaces(roiL_ids,:) allFuncModulesL_lf(roiL_ids)],graphOpts{:});
plotsurf(lo_grpvertex,[lo_grpfaces(roiR_ids,:) allFuncModulesR_lf(roiR_ids)],graphOpts{:});
campos(1.0e+03 * [-0.7198    1.0299    0.4153]);
lighting gouraud;
camlight;

%% Inflated image
figure;
title("Functional (left foot movement) modules on brain surface (precentral only) - inflated");
hold on;
nModules_L = length(unique(allFuncModulesL_lf));
nModules_R = length(unique(allFuncModulesR_lf));
nModules = nModules_L + nModules_R;

% Use flattened surface
plotsurf(inflated_lo_glpvertex,inflated_lo_glpfaces(~ismember(1:end,roiL_ids),:),'FaceAlpha',1,'EdgeAlpha',0.05,'FaceColor',[0.5 0 0]);
plotsurf(inflated_lo_grpvertex,inflated_lo_grpfaces(~ismember(1:end,roiR_ids),:),'FaceAlpha',1,'EdgeAlpha',0.05,'FaceColor',[0.5 0 0]);
plotsurf(inflated_lo_glpvertex,[inflated_lo_glpfaces(roiL_ids,:) allFuncModulesL_lf(roiL_ids)]);
plotsurf(inflated_lo_grpvertex,[inflated_lo_grpfaces(roiR_ids,:) allFuncModulesR_lf(roiR_ids)]);

campos(1.0e+03 * [-0.7198    1.0299    0.4153]);
lighting gouraud;
camlight;

figure;
title("Structural modules on brain surface (precentral only) - inflated");
hold on;
nModules_L = length(unique(allStrucModulesL));
nModules_R = length(unique(allStrucModulesR));
nModules = nModules_L + nModules_R;


% Use flattened surface
plotsurf(inflated_lo_glpvertex,inflated_lo_glpfaces(~ismember(1:end,roiL_ids),:),'FaceAlpha',1,'EdgeAlpha',0.05,'FaceColor',[0.5 0 0]);
plotsurf(inflated_lo_grpvertex,inflated_lo_grpfaces(~ismember(1:end,roiR_ids),:),'FaceAlpha',1,'EdgeAlpha',0.05,'FaceColor',[0.5 0 0]);
plotsurf(inflated_lo_glpvertex,[inflated_lo_glpfaces(roiL_ids,:) allStrucModulesL(roiL_ids)]);
plotsurf(inflated_lo_grpvertex,[inflated_lo_grpfaces(roiR_ids,:) allStrucModulesR(roiR_ids)]);

campos(1.0e+03 * [-1.1603    0.2411    0.5211]);
lighting gouraud;
camlight;

%% Superimpose functional onto structural data
figure;
title("Structural and functional modules (left foot) on brain surface (precentral only) - inflated");
hold on;
nModules_L = length(unique(allStrucModulesL)) + length(unique(allFuncModulesL_lf));
nModules_R = length(unique(allStrucModulesR)) + length(unique(allFuncModulesR_lf));
nModules = nModules_L + nModules_R;

% plotsurf(inflated_lo_glpvertex,inflated_lo_glpfaces(ismember(1:end,roiL_ids),:),'FaceAlpha',1,'EdgeAlpha',0.05,'FaceColor',[1 1 1],'DisplayName','L Precentral Gyrus without modules');
% plotsurf(inflated_lo_glpvertex,inflated_lo_glpfaces(~ismember(1:end,roiL_ids),:),'FaceAlpha',1,'EdgeAlpha',0.05,'FaceColor',[0.5 0 0],'DisplayName','Left Hemisphere');
plotsurf(inflated_lo_grpvertex,inflated_lo_grpfaces(ismember(1:end,roiR_ids),:),'FaceAlpha',1,'EdgeAlpha',0.05,'FaceColor',[1 1 1],'DisplayName','R Precentral Gyrus without modules');
plotsurf(inflated_lo_grpvertex,inflated_lo_grpfaces(~ismember(1:end,roiR_ids),:),'FaceAlpha',1,'EdgeAlpha',0.05,'FaceColor',[0.5 0 0],'DisplayName','Right Hemisphere');

nStrucModules_L = length(unique(allStrucModulesL));
nStrucModules_R = length(unique(allStrucModulesR));
nFuncModules_L = length(unique(allFuncModulesL_lf));
nFuncModules_R = length(unique(allFuncModulesR_lf));

colormap_lines = lines(nStrucModules_L + nFuncModules_L + nStrucModules_R + nFuncModules_R + 5);
legends = [];
legendText = {};

colorIndex = 1;
% for strucModuleIndex=0:nStrucModules_L
%     faceIndicesOfModule = find(allStrucModulesL == strucModuleIndex);
%     moduleColor = colormap_lines(colorIndex,:);
%     colorIndex = colorIndex + 1;
%     plotsurf(inflated_lo_glpvertex,[inflated_lo_glpfaces(faceIndicesOfModule,:) allStrucModulesL(faceIndicesOfModule)],'DisplayName',['Structural Module: #',num2str(strucModuleIndex)], 'FaceColor', moduleColor);
%     legends = [legends, patch(NaN,NaN,moduleColor)];
%     legendText = [legendText; ['(L) Structural Module: #' num2str(strucModuleIndex)]];
% end
for strucModuleIndex=0:nStrucModules_R
    faceIndicesOfModule = find(allStrucModulesR == strucModuleIndex);
    moduleColor = colormap_lines(colorIndex,:);
    colorIndex = colorIndex + 1;
    plotsurf(inflated_lo_grpvertex,[inflated_lo_grpfaces(faceIndicesOfModule,:) allStrucModulesR(faceIndicesOfModule)],'DisplayName',['Structural Module: #',num2str(strucModuleIndex)], 'FaceColor', moduleColor);
    legends = [legends, patch(NaN,NaN,moduleColor)];
    legendText = [legendText; ['(R) Structural Module: #' num2str(strucModuleIndex)]];
end

% for funcModuleIndex=1:nFuncModules_L
%     faceIndicesOfModule = allFuncModulesL_lf == funcModuleIndex;
%     moduleColor = colormap_lines(colorIndex,:);
%     colorIndex = colorIndex + 1;
%     edgesOfModules = surfedge(inflated_lo_glpfaces(faceIndicesOfModule,:));
%     plotedges(inflated_lo_glpvertex(:,1:3), edgesOfModules, 'linewidth',2, 'linestyle','-','DisplayName',['Functional Module: #' num2str(funcModuleIndex)],'Marker','o','MarkerSize',3,'AlignVertexCenters','on','HandleVisibility','off', 'Color', moduleColor);
%     legends = [legends, line(NaN,NaN,'LineWidth',4,'LineStyle','-','Color',moduleColor)];
%     legendText = [legendText; ['Functional Module: #' num2str(funcModuleIndex)]];
% end
for funcModuleIndex=1:nFuncModules_R
    faceIndicesOfModule = allFuncModulesR_lf == funcModuleIndex;
    moduleColor = colormap_lines(colorIndex,:);
    colorIndex = colorIndex + 1;
    edgesOfModules = surfedge(inflated_lo_grpfaces(faceIndicesOfModule,:));
    plotedges(inflated_lo_grpvertex(:,1:3), edgesOfModules, 'linewidth',3, 'linestyle','-','DisplayName',['Functional Module: #' num2str(funcModuleIndex)],'Marker','o','MarkerSize',3,'AlignVertexCenters','on','HandleVisibility','off', 'Color', moduleColor);
    legends = [legends, line(NaN,NaN,'LineWidth',3,'LineStyle','-','Color',moduleColor)];
    legendText = [legendText; ['Functional Module: #' num2str(funcModuleIndex)]];
end
campos(1.0e+03 * [1.0518    0.1297    0.7534]);
lighting gouraud;
material dull
camlight;
legend(legends,legendText{:});
zoom on;
axis off
ax = gca;
ax.Clipping = "off";

disp(['Stopped executing after line: ', num2str(dbstack().line)]); % Display current line
disp("Due to incompatible scripts.")
return

%% Superimposed modules on flat surface
figure;
title("Structural and functional modules (left foot) on brain surface (precentral only) - flat");
hold on;
legends = [];
legendText = {};

nodeStrucModules_L = mapFaceValuesToNodes(allStrucModulesL,flat_lo_glpvertex,flat_lo_faceToNodeMapLH);
nodeStrucModules_R = mapFaceValuesToNodes(allStrucModulesR,flat_lo_grpvertex,flat_lo_faceToNodeMapRH);
nodeStrucModules_R(isnan(nodeStrucModules_R)) = -1;
nodeFuncModules_L = mapFaceValuesToNodes(allFuncModulesL_lf,flat_lo_glpvertex,flat_lo_faceToNodeMapLH);
nodeFuncModules_R = mapFaceValuesToNodes(allFuncModulesR_lf,flat_lo_grpvertex,flat_lo_faceToNodeMapRH);
nodeRoiIds_L = mapFaceValuesToNodes(lo_faceROIidL(:,1),flat_lo_glpvertex,flat_lo_faceToNodeMapLH);
nodeRoiIds_R = mapFaceValuesToNodes(lo_faceROIidR(:,1),flat_lo_grpvertex,flat_lo_faceToNodeMapRH);

%plotsurf(flat_lo_glpvertex,flat_lo_glpfaces(~ismember(1:end,nodeRoiIds_L),:),'FaceAlpha',1,'EdgeAlpha',0.05,'FaceColor',[0.5 0 0],'DisplayName','Left Hemisphere');

nStrucModules_L = length(unique(nodeStrucModules_L));
nStrucModules_R = length(unique(nodeStrucModules_R));
nFuncModules_L = length(unique(nodeFuncModules_L));
nFuncModules_R = length(unique(nodeFuncModules_R));


colormap_lines = lines(nStrucModules_L + nFuncModules_L + nStrucModules_R + nFuncModules_R);

colorIndex = 1;
% for strucModuleIndex=1:nStrucModules_L
%     faceIndicesOfModule = find(nodeStrucModules_L == strucModuleIndex);
%     moduleColor = colormap_lines(colorIndex,:);
%     colorIndex = colorIndex + 1;
%     plotsurf(flat_lo_glpvertex,[flat_lo_glpfaces(faceIndicesOfModule,:) nodeStrucModules_L(faceIndicesOfModule,1)],'DisplayName',['Structural Module: #',num2str(strucModuleIndex)], 'FaceColor', moduleColor);
% end
for strucModuleIndex=1:nStrucModules_R
    faceIndicesOfModule = find(nodeStrucModules_R == strucModuleIndex);
    moduleColor = colormap_lines(colorIndex,:);
    colorIndex = colorIndex + 1;
    plotsurf(flat_lo_grpvertex,[flat_lo_grpfaces(faceIndicesOfModule,:) nodeStrucModules_R(faceIndicesOfModule,1)],'DisplayName',['Structural Module: #',num2str(strucModuleIndex)], 'FaceColor', moduleColor);
    legends = [legends, line(NaN,NaN,'LineWidth',4,'LineStyle','-','Color',moduleColor)];
    legendText = [legendText; ['Structural Module: #' num2str(strucModuleIndex)]];
end


% for funcModuleIndex=1:nFuncModules_L
%     faceIndicesOfModule = allFuncModulesL_lf == funcModuleIndex;
%     moduleColor = colormap_lines(colorIndex,:);
%     colorIndex = colorIndex + 1;
%     edgesOfModules = surfedge(inflated_lo_glpfaces(faceIndicesOfModule,:));
%     plotedges(inflated_lo_glpvertex(:,1:3), edgesOfModules, 'linewidth',10, 'linestyle','-','DisplayName',['Functional Module: #' num2str(funcModuleIndex)],'Marker','o','MarkerSize',3,'AlignVertexCenters','on','HandleVisibility','off', 'Color', moduleColor);
% end
for funcModuleIndex=1:nFuncModules_R
    faceIndicesOfModule = allFuncModulesR_lf == funcModuleIndex;
    moduleColor = colormap_lines(colorIndex,:);
    colorIndex = colorIndex + 1;
    edgesOfModules = surfedge(flat_lo_grpfaces(faceIndicesOfModule,:));
    plotedges(flat_lo_grpvertex(:,1:3), edgesOfModules, 'linewidth',2, 'linestyle','-','DisplayName',['Functional Module: #' num2str(funcModuleIndex)],'Marker','o','MarkerSize',3,'AlignVertexCenters','on','HandleVisibility','off', 'Color', moduleColor);
    legends = [legends, line(NaN,NaN,'LineWidth',3,'LineStyle','-','Color',moduleColor)];
    legendText = [legendText; ['Functional Module: #' num2str(funcModuleIndex)]];
end
campos(1.0e+03 * [0.0088    0.0414    3.0932]);
lighting gouraud;
material dull
camlight;
legend(legends,legendText{:});
zoom on;
camva(11);
axis off
ax = gca;
ax.Clipping = "off";

%% Load in gifti data from fMRI
mycifti = ft_read_cifti(['../../data/subjects','/',subjectId,'/MNINonLinear/Results/tfMRI_MOTOR/tfMRI_MOTOR_hp200_s2_level2_MSMAll.feat/',subjectId,'_tfMRI_MOTOR_level2_hp200_s2_MSMAll.dscalar.nii']);
fieldName = ['x', subjectId, '_tfmri_motor_level2_avg_',condition,'_hp200_s2_msmall'];
verticesL_rawfMRIvalues = mycifti.(fieldName)(mycifti.brainstructure==1,:);
% Assign vertices values to face centroids (meaned).
face_fMRI_nodeValues(:,:) = verticesL_rawfMRIvalues(lo_grpfaces(:,:));
face_fMRIValuesL = mean(face_fMRI_nodeValues,2, "omitnan");
face_fMRIValuesL_sorted = face_fMRIValuesL(I(roiL_ids(strucModulesL_sorted)));
% Convert fMRI values into something that can be plotted


fMRIvalues_matrix = speye(length(face_fMRIValuesL_sorted), length(face_fMRIValuesL_sorted));
%TODO: This shouldnt be necessary.
face_fMRIValuesL_sorted_thresholded=face_fMRIValuesL_sorted>1;
fMRIvalues_matrix(fMRIvalues_matrix>0) = face_fMRIValuesL_sorted_thresholded(I_strucModulesL);

strucValues_matrix = speye(length(face_fMRIValuesL_sorted), length(face_fMRIValuesL_sorted));
strucValues_matrix(strucValues_matrix>0) = modulesByFace.left_structural_modulesByROIId(I_strucModulesL,2);
figure; 
ax = gca;
ax(2) = copyobj(ax(1), ax(1).Parent);
linkaxes([ax(1),ax(2)])
title("Modules of fMRI and Structural along diagonal")
hold on;
cspy(strucValues_matrix, 'ColorMap', 'jet', 'Levels', max(strucValues_matrix,[],'all'), 'MarkerSize',40, 'Marker', '.', 'Parent', ax(1));
hold on;
axes(ax(2));
cspy(fMRIvalues_matrix, 'ColorMap','copper','Levels', max(fMRIvalues_matrix,[],'all'), 'MarkerSize',20, 'Marker', '.', 'Parent', ax(2));
hold on;
set(ax(1), 'Colormap', jet);
set(ax(2), 'Colormap', copper);
ax(2).Visible = 'off';
ax(2).XTick = [];
ax(2).YTick = [];
colormap_lines(ax(1), jet(max(strucValues_matrix,[],'all')));
colormap_lines(ax(2), copper(max(fMRIvalues_matrix,[],'all')));
c1 = colorbar(ax(1),'Position',[.05 .11 .0675 .815], 'Limits', [min(strucValues_matrix,[],'all'),max(strucValues_matrix,[],'all')]);
c1.Label.String = 'Module id (structural)';
c2 = colorbar(ax(2),'Position',[.88 .11 .0675 .815], 'Limits', [min(fMRIvalues_matrix,[],'all'),max(fMRIvalues_matrix,[],'all')]);
c2.Label.String = 'Module id (functional)';
set([ax(1),ax(2)],'Position',[.17 .11 .685 .815]);

figure;
title("With structural modules - only strongly connected nodes ")
subtitle("Whole brain in MNINonLinear space; seeded by ROI (precentral); sorted by modules (ascend)");
hold on;
legends = [];
legendText = {};
legends = [legends, line(NaN,NaN,'LineWidth',4,'LineStyle','-','Color',[1 0 0 0.4])];
legends = [legends, line(NaN,NaN,'LineWidth',4,'LineStyle','-','Color',[0 0 0 0.05])];
legends = [legends, line(NaN,NaN,'LineWidth',4,'LineStyle','-','Color',[0 0 1 1])];
legendText = [legendText; 'Precentral Gyri'; 'Hemispheres'; 'Edge'];

indicesOfLabelledFaces = labelIds >= 1; %ignore NaNs
plottedLabelIds = labelIds(indicesOfLabelledFaces);
plottedLabelsNames=allFileNames(plottedLabelIds);
[plottedLabelNamesSorted, I] =sort(string(plottedLabelsNames), 'ascend');
plottedLabelIdsSorted=plottedLabelIds(I);
[strucModulesL_sorted, I_strucModulesL]= sort(modulesByFace.left_structural_modulesByROIId(:,2));
c = colorbar;
c.Label.String = 'Number of connections';
adj_matrix_wei_hubs_only = sparse(length(adj_matrix_wei), length(adj_matrix_wei));
largestWeightsInMatrix = find(adj_matrix_wei>(0.1*max(adj_matrix_wei,[],'all')));
adj_matrix_wei_hubs_only(largestWeightsInMatrix) = adj_matrix_wei(largestWeightsInMatrix);

cspy(adj_matrix_wei_hubs_only(I(roiL_ids(I_strucModulesL)),I(roiL_ids(I_strucModulesL))),'ColorMap','jet','MarkerSize',10);
for moduleId=1:max(strucModulesL_sorted)
    moduleIds = find(strucModulesL_sorted == moduleId);
    moduleStart = min(moduleIds);
    moduleEnd = max(moduleIds);
    moduleLength = moduleEnd-moduleStart;
    rectangle('Position',[[moduleStart, moduleStart], moduleLength, moduleLength], 'FaceColor', [1 0 0 0.1], 'EdgeColor', [1 0 0 0.2]);
    legends = [legends, line(NaN,NaN,'LineWidth',4,'LineStyle','-','Color',[1 0 0 0.1])];
    legendText = [legendText; ['Module #',num2str(moduleId)]];
end
legend(legends,legendText{:});


%% Plot ROI region only
figure;
title("Only Precentral gyri (left and right)");
hold on;
grid on;
roi = "precentral";
roiIds = find(contains(allFileNames,roi));
indicesInROI = [roi_L,roi_R];
roiL_start = find(ismember(hi_faceROIidL(:,1),roiIds), 1, "first" );
roiL_length = length(find(ismember(hi_faceROIidL(:,1),roiIds)));
roiR_start = find(ismember(hi_faceROIidR(:,1),roiIds), 1, "first" );
roiR_length = length(find(ismember(hi_faceROIidL(:,1),roiIds)));

labelsInROI = plottedLabels(indicesInROI);
rectangle('Position',[[roiL_start roiL_start], roiL_length,roiL_length], 'FaceColor', [1 0 0 0.4], 'EdgeColor', [0 0 0 0.01]);
rectangle('Position',[[roiR_start roiR_start], roiR_length,roiR_length], 'FaceColor', [1 0 0 0.4], 'EdgeColor', [0 0 0 0.01]);
spy(adj_matrix(indicesInROI,indicesInROI));
showTicksPer=100000;
xticks(1:(showTicksPer/50):length(labelsInROI));
yticks(1:(showTicksPer/50):length(labelsInROI));
xticklabels(labelsInROI(1:(showTicksPer/50):end));
yticklabels(labelsInROI(1:(showTicksPer/50):end));


%% Plot fMRI and structural/diffusion data over each other
openfig(['../../data/subjects/',subjectId,'/tracts_aparc_xyz.fig']);
hold on;
mycifti = ft_read_cifti(['../../data/subjects/',subjectId,'/MNINonLinear/Results/tfMRI_MOTOR/tfMRI_MOTOR_hp200_s2_level2_MSMAll.feat/',subjectId,'_tfMRI_MOTOR_level2_hp200_s2_MSMAll.clusters.dscalar.nii'])
fieldValue = ['x',subjectId,'_tfmri_motor_level2_',condition,'_hp200_s2'];
scatter3(mycifti.pos(:,1), mycifti.pos(:,2), mycifti.pos(:,3), [], mycifti.(fieldValue));





%%Diffusion
load(['../../data/subjects/',subjectId,'/labelSRF.mat'], "nvl", "nvr", "nfl", "nfr", "faceROIidL", "faceROIidR");
adj_matrix = matfile(['../../data/subjects/',subjectId,'/matrices.mat']).adj_matrix;
%adj_matrix_L = adj_matrix(find(faceROIidL), find(faceROIidL)); %TODO: label25=precentral_L


adj_matrix_L = adj_matrix(find(faceROIidL==25), find(faceROIidL==25)); %TODO: label25=precentral_L
adj_matrix_R = adj_matrix(find(faceROIidR==(59-34)), find(faceROIidR==(59-34)));  %TODO: 59-34 = precentral_R
[leftOptimalGamma] = findOptimalGamma('../../data/subjects', subjectId, adj_matrix_L, 1, 1, 1);
filename=['../../data/subjects/',subjectId,'/moduleResults/leftOptimalGamma.mat'];
save(filename,'leftOptimalGamma','-v7.3');

[nfl(find(faceROIidL==25),4), L_Q1] = sortIntoModules(adj_matrix_L, leftOptimalGamma);

%[nfl(faceROIidL,4), L_Q1] = sortIntoModules(adj_matrix_L, leftOptimalGamma);
filename=['../../data/subjects/',subjectId,'/moduleResults/leftStructuralModules.mat'];
leftStructuralModules = nfl(faceROIidL,4);
save(filename,'leftStructuralModules','-v7.3');
close all;
% figure;
% plotsurf(right_pial_59k.vertices,right_pial_59k.faces,mycifti.x100610_tfmri_motor_level2_lf_hp200_s2(mycifti.brainstructure==2));
% hold on;
% plotsurf(left_pial_59k.vertices,left_pial_59k.faces,mycifti.x100610_tfmri_motor_level2_lf_hp200_s2(mycifti.brainstructure==1));

figure;
fieldValue = ['x',subjectId,'_tfmri_motor_level2_',condition,'_hp200_s2'];
plotsurf(l.coord', l.tri, mycifti.(fieldValue)(mycifti.brainstructure==1));
hold on;
plotsurf(r.coord', r.tri, mycifti.(fieldValue)(mycifti.brainstructure==2));

figure;
plotsurf(nvl, nfl(nfl(:,4) == 0, 1:3), 'DisplayName', "Left hemisphere (no modules)", 'EdgeAlpha',0.3,'FaceColor',[0.1 0.1 0.1],'FaceAlpha',0.5);
hold on;
%plotsurf(nvr, nfr);
nfl = double([nfl leftStructuralModules]);
leftColormap_hsv = hsv(max(nfl(:,4)));
for moduleIndex=1:max(nfl(:,4))
    color = leftColormap_hsv(moduleIndex,:);
    plotsurf(nvl,nfl((nfl(:,4) == moduleIndex),1:3),'DisplayName',['Structural Module: #' num2str(moduleIndex)],'EdgeAlpha',0.3,'FaceColor',[color]);
    %plotedges(allBrainData.leftHemisphere.surf.nodes(:,1:3), strucEdges{moduleIndex},'linewidth',randi(5,1),'Color',[color 0.9],'linestyle','-','DisplayName',['Structural Module: #' num2str(moduleIndex)]);
end
legend;


adj_matrix_L = adj_matrix(find(faceROIidL), find(faceROIidL)); %TODO: label25=precentral_L
figure;

load(['../../data/subjects/',subjectId,'/labelSRF.mat'], "nvl", "nvr", "nfl", "nfr", "faceROIidL", "faceROIidR");

% adj_matrix = matfile('../../data/subjects/100610/matrices.mat').adj_matrix;
% load('../../data/subjects/100610/edgeList.mat');
% load('../../data/subjects/100610/labelSRF.mat');
% load('../../data/subjects/100610/matrices.mat');
% load('../../data/subjects/100610/trsfmTrk.mat');
% load('../../data/subjects/100610/MNIcoor.mat');

%%allFileNames = [filenames; subfilenames']';
%%plottedLabels=allFileNames(faceROI_all);
        xticks(1:(showTicksPer/50):length(plottedLabels));
        yticks(1:(showTicksPer/50):length(plottedLabels));
        xticklabels(plottedLabels(1:(showTicksPer/50):end));
        yticklabels(plottedLabels(1:(showTicksPer/50):end));
[x,y,z] = adjacency_plot_und(adj_matrix_L,nfl(:,1:3));
plot3(x,y,z);
legend;
end