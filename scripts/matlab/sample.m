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

adj_matrix = matfile('../../data/subjects/100610/matrices.mat').adj_matrix;
%adj_matrix_ds = matfile('../../data/subjects/100610/whole_brain_FreeSurferDKT_Cortical.mat');
load('../../data/subjects/100610/edgeList.mat');
load('../../data/subjects/100610/labelSRF.mat');
load('../../data/subjects/100610/matrices.mat');
load('../../data/subjects/100610/trsfmTrk.mat');
%load('../../data/subjects/100610/MNIcoor.mat');

allFileNames = [filenames; subfilenames']';
plottedLabels=allFileNames(faceROI_all);
[~, positionOfFirstLabel, ~] = unique(plottedLabels, "first");
[~, positionOfLastLabel, ~] = unique(plottedLabels, "last");
positionOfMiddleLabel = floor(mean([positionOfFirstLabel positionOfLastLabel], 2));
plottedLabelsFinal_all = sort(positionOfMiddleLabel);

figure;
title("Adjacency matrix: matrices.mat")
spy(adj_matrix);
hold on;
set(gca, 'Ytick',plottedLabelsFinal_all,'YTickLabel',plottedLabels(plottedLabelsFinal_all));
set(gca, 'Xtick',plottedLabelsFinal_all,'XTickLabel',plottedLabels(plottedLabelsFinal_all));

% showTicksPer=100000;
% xticks(1:(showTicksPer/50):length(plottedLabels));
% yticks(1:(showTicksPer/50):length(plottedLabels));
% xticklabels(plottedLabels(1:(showTicksPer/50):end));
% yticklabels(plottedLabels(1:(showTicksPer/50):end));
savefig('../../data/subjects/100610/adjmatrix_reduction_164k.fig');


%t1_r = niftiread('../../data/subjects/100610/T1w/T1w_acpc_dc.nii.gz');
t1_r_mni152 = niftiread('../../data/subjects/100610/MNINonLinear/T1w_restore_brain.nii.gz');

%diff_r = niftiread('../../data/subjects/100610/T1w/Diffusion/data.nii.gz');
diff_r_mni152 = '?'

l=SurfStatReadSurf(['../../data/subjects/100610/MNINonLinear/100610/surf/lh.pial']);
r=SurfStatReadSurf(['../../data/subjects/100610/MNINonLinear/100610/surf/rh.pial']);

left_pial_59k = gifti('../../data/subjects/100610/MNINonLinear/fsaverage_LR32k/100610.L.pial.32k_fs_LR.surf.gii');
left_pial_labels =  gifti('../../data/subjects/100610/MNINonLinear/fsaverage_LR32k/100610.L.aparc.32k_fs_LR.label.gii');
right_pial_59k = gifti('../../data/subjects/100610/MNINonLinear/fsaverage_LR32k/100610.R.pial.32k_fs_LR.surf.gii');


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