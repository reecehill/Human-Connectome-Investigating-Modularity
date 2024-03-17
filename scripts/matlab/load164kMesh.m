function [glpfaces, grpfaces, glpvertex, grpvertex, filenames, subfilenames, ROIfacevert, nbROI] = load164kMesh(pathToFile,subjectId,type)

filenames={'lh.L_unknown.label';'lh.L_bankssts.label';'lh.L_caudalanteriorcingulate.label';'lh.L_caudalmiddlefrontal.label';'lh.L_cuneus.label';'lh.L_entorhinal.label';'lh.L_frontalpole.label';'lh.L_fusiform.label';'lh.L_inferiorparietal.label';'lh.L_inferiortemporal.label';'lh.L_insula.label';'lh.L_isthmuscingulate.label';'lh.L_lateraloccipital.label';'lh.L_lateralorbitofrontal.label';'lh.L_lingual.label';'lh.L_medialorbitofrontal.label';'lh.L_middletemporal.label';'lh.L_paracentral.label';'lh.L_parahippocampal.label';'lh.L_parsopercularis.label';'lh.L_parsorbitalis.label';'lh.L_parstriangularis.label';'lh.L_pericalcarine.label';'lh.L_postcentral.label';'lh.L_posteriorcingulate.label';'lh.L_precentral.label';'lh.L_precuneus.label';'lh.L_rostralanteriorcingulate.label';'lh.L_rostralmiddlefrontal.label';'lh.L_superiorfrontal.label';'lh.L_superiorparietal.label';'lh.L_superiortemporal.label';'lh.L_supramarginal.label';'lh.L_temporalpole.label';'lh.L_transversetemporal.label';'rh.R_unknown.label';'rh.R_bankssts.label';'rh.R_caudalanteriorcingulate.label';'rh.R_caudalmiddlefrontal.label';'rh.R_cuneus.label';'rh.R_entorhinal.label';'rh.R_frontalpole.label';'rh.R_fusiform.label';'rh.R_inferiorparietal.label';'rh.R_inferiortemporal.label';'rh.R_insula.label';'rh.R_isthmuscingulate.label';'rh.R_lateraloccipital.label';'rh.R_lateralorbitofrontal.label';'rh.R_lingual.label';'rh.R_medialorbitofrontal.label';'rh.R_middletemporal.label';'rh.R_paracentral.label';'rh.R_parahippocampal.label';'rh.R_parsopercularis.label';'rh.R_parsorbitalis.label';'rh.R_parstriangularis.label';'rh.R_pericalcarine.label';'rh.R_postcentral.label';'rh.R_posteriorcingulate.label';'rh.R_precentral.label';'rh.R_precuneus.label';'rh.R_rostralanteriorcingulate.label';'rh.R_rostralmiddlefrontal.label';'rh.R_superiorfrontal.label';'rh.R_superiorparietal.label';'rh.R_superiortemporal.label';'rh.R_supramarginal.label';'rh.R_temporalpole.label';'rh.R_transversetemporal.label'};
subfilenames={'lh.thalamus','lh.caudate','lh.putamen','lh.pallidum','lh.amygdala','lh.hippocampus','lh.accumbens','lh.cerebellum','rh.thalamus','rh.caudate','rh.putamen','rh.pallidum','rh.amygdala','rh.hippocampus','rh.accumbens','rh.cerebellum','Brain-stem'};
nbROI=length(filenames);

if type==1
    disp('load lh(rh).pial.surf.gii as surface')
    parfor i=1:nbROI
        ROIfacevert(i,1).id=filenames(i);
        ROIfacevert(i,1).faces=importfile([pathToFile,'/MNINonLinear/',subjectId,'/label/label_type2/',filenames{i}]);  
    end
    giftilh=gifti([pathToFile,'/MNINonLinear/',subjectId,'.L.pial_MSMAll.164k_fs_LR.surf.gii']);
    glpfaces      = giftilh.faces;
    glpvertex     = giftilh.vertices;
    giftirh=gifti([pathToFile,'/MNINonLinear/',subjectId,'.R.pial_MSMAll.164k_fs_LR.surf.gii']);
    grpfaces      = giftirh.faces;
    grpvertex     = giftirh.vertices;
    clear giftilh giftirh;
elseif type==2
    parfor i=1:nbROI
        ROIfacevert(i,1).id=filenames(i);
        ROIfacevert(i,1).faces=importfile([pathToFile,'/MNINonLinear/',subjectId,'/label/label_type2/',filenames{i}]);    
    end
    % load hi-res surface - pial
    disp('load lh(rh).pial as surface')
    
    l=SurfStatReadSurf([pathToFile,'/MNINonLinear/',subjectId,'/surf/lh.pial']);
    r=SurfStatReadSurf([pathToFile,'/MNINonLinear/',subjectId,'/surf/rh.pial']);
    glpfaces = l.tri; %118,580x3 int32 (each row is the ID of the 3 nodes of the face)
    glpvertex = l.coord'; %59292x3 double (each row are the coordinates of a node; row id = node ID)
    grpfaces = r.tri; %118,580x3 int32 (each row is the ID of the 3 nodes of the face)
    grpvertex = r.coord'; %59292x3 double (each row are the coordinates of a node; row id = node ID)
    clear l r;
end
end