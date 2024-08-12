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

adj_matrix = matfile('../../data/subjects/100307/matrices.mat').adj_matrix;
%adj_matrix_ds = matfile('../../data/subjects/100610/whole_brain_FreeSurferDKT_Cortical.mat');
load('../../data/subjects/100307/edgeList.mat');
load('../../data/subjects/100307/labelSRF.mat');
load('../../data/subjects/100307/matrices.mat');
load('../../data/subjects/100307/trsfmTrk.mat');


figure;
title("Weighted adjacency matrix - Remote + Local");
subtitle("Whole brain in MNINonLinear space; seeded by ROI (precentral)");
allFileNames = [filenames subfilenames];
downsample=true;
if(downsample)
    labelIds=[lo_faceROIidL(:,1); lo_faceROIidR(:,1); double(max(lo_faceROIidR(:,1)))+lo_subROIid];
else
    labelIds=[hi_faceROIidL(:,1); hi_faceROIidR(:,1); double(max(hi_faceROIidR(:,1)))+hi_subROIid];
end
indicesOfLabelledFaces = labelIds >= 1; %ignore NaNs
plottedLabelIds = labelIds(indicesOfLabelledFaces);
plottedLabelsNames=allFileNames(plottedLabelIds);
[plottedLabelNamesSorted, I] =sort(string(plottedLabelsNames), 'ascend');
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
roi = "lh.L_precentral";
roiIds = find(contains(allFileNames,roi));
roiL_ids = find(ismember(plottedLabelIdsSorted(:,1),roiIds));
roiL_start = min(roiL_ids);
roiL_end = max(roiL_ids);
roiL_length = roiL_end-roiL_start;
roi = "rh.R_precentral";
roiIds = find(contains(allFileNames,roi));
roiR_ids = find(ismember(plottedLabelIdsSorted(:,1),roiIds));
roiR_start = min(roiR_ids);
roiR_end = max(roiR_ids);
roiR_length = roiR_end-roiR_start;
rectangle('Position',[[hemisphereL_start, hemisphereL_start], hemisphereL_length, hemisphereL_length], 'FaceColor', [0 0 0 0.05], 'EdgeColor', [0 0 0 0.2]);
rectangle('Position',[[hemisphereR_start, hemisphereR_start], hemisphereR_length, hemisphereR_length], 'FaceColor', [0 0 0 0.05], 'EdgeColor', [0 0 0 0.2]);
rectangle('Position',[[miscellaneous_start, miscellaneous_start], miscellaneous_length, miscellaneous_length], 'FaceColor', [0 0 0 0.05], 'EdgeColor', [0 0 0 0.2]);
rectangle('Position',[[roiL_start, roiL_start], roiL_length, roiL_length], 'FaceColor', [1 0 0 0.1], 'EdgeColor', [1 0 0 0.2]);
rectangle('Position',[[roiR_start roiR_start], roiR_length, roiR_length], 'FaceColor', [1 0 0 0.1], 'EdgeColor', [1 0 0 0.2]);

cspy(adj_matrix_wei(I,I),'ColorMap','jet','MarkerSize',10);
roiLine = line(NaN,NaN,'LineWidth',4,'LineStyle','-','Color',[1 0 0 0.4]);
hLine = line(NaN,NaN,'LineWidth',4,'LineStyle','-','Color',[0 0 0 0.05]);
spyLine = line(NaN,NaN,'LineWidth',4,'LineStyle','-','Color',[0 0 1 1]);
legend([hLine, roiLine, spyLine],'Hemispheres','Precentral Gyri','Edge');

figure;
title("Left ROI only")
hold on;
cspy(adj_matrix_wei(I(roiL_ids),I(roiL_ids)),'ColorMap','jet','MarkerSize',10);

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
openfig('../../data/subjects/100610/tracts_aparc_xyz.fig');
hold on;
mycifti = ft_read_cifti('../../data/subjects/100610/MNINonLinear/Results/tfMRI_MOTOR/tfMRI_MOTOR_hp200_s2_level2.feat/100610_tfMRI_MOTOR_level2_hp200_s2.dscalar.nii')
scatter3(mycifti.pos(:,1), mycifti.pos(:,2), mycifti.pos(:,3), [], mycifti.x100610_tfmri_motor_level2_lf_hp200_s2);





%%Diffusion
load('../../data/subjects/100610/labelSRF.mat', "nvl", "nvr", "nfl", "nfr", "faceROIidL", "faceROIidR");
adj_matrix = matfile('../../data/subjects/100610/matrices.mat').adj_matrix;
%adj_matrix_L = adj_matrix(find(faceROIidL), find(faceROIidL)); %TODO: label25=precentral_L


adj_matrix_L = adj_matrix(find(faceROIidL==25), find(faceROIidL==25)); %TODO: label25=precentral_L
adj_matrix_R = adj_matrix(find(faceROIidR==(59-34)), find(faceROIidR==(59-34)));  %TODO: 59-34 = precentral_R
[leftOptimalGamma] = findOptimalGamma('../../data/subjects', '100610', adj_matrix_L, 1, 1, 1);
filename=['../../data/subjects/100610/moduleResults/leftOptimalGamma.mat'];
save(filename,'leftOptimalGamma','-v7.3');

[nfl(find(faceROIidL==25),4), L_Q1] = sortIntoModules(adj_matrix_L, leftOptimalGamma);

%[nfl(faceROIidL,4), L_Q1] = sortIntoModules(adj_matrix_L, leftOptimalGamma);
filename=['../../data/subjects/100610/moduleResults/leftStructuralModules.mat'];
leftStructuralModules = nfl(faceROIidL,4);
save(filename,'leftStructuralModules','-v7.3');
close all;
% figure;
% plotsurf(right_pial_59k.vertices,right_pial_59k.faces,mycifti.x100610_tfmri_motor_level2_lf_hp200_s2(mycifti.brainstructure==2));
% hold on;
% plotsurf(left_pial_59k.vertices,left_pial_59k.faces,mycifti.x100610_tfmri_motor_level2_lf_hp200_s2(mycifti.brainstructure==1));

figure;
plotsurf(l.coord', l.tri, mycifti.x100610_tfmri_motor_level2_lf_hp200_s2(mycifti.brainstructure==1));
hold on;
plotsurf(r.coord', r.tri, mycifti.x100610_tfmri_motor_level2_lf_hp200_s2(mycifti.brainstructure==2));

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

load('../../data/subjects/100610/labelSRF.mat', "nvl", "nvr", "nfl", "nfr", "faceROIidL", "faceROIidR");

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