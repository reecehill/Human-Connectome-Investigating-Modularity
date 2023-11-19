
%GIFTI pial.label.gii -> .pial
mris_convert ./data/subjects/100610/MNINonLinear/fsaverage_LR59k/100610.R.pial.59k_fs_LR.surf.gii ./data/subjects/100610/MNINonLinear/rh.pial

%GIFTI label.gii+surface.gii -> aparc.annot
mris_convert --annot ./data/subjects/100610/MNINonLinear/fsaverage_LR59k/100610.R.aparc.59k_fs_LR.label.gii ./data/subjects/100610/MNINonLinear/fsaverage_LR59k/100610.R.pial.59k_fs_LR.surf.gii ./data/subjects/100610/MNINonLinear/rh.aparc.annot

%aparc.annot -> label_files
mri_annotation2label --subject 100610 --hemi rh --surf pial --outdir ./data/subjects/100610/MNINonLinear/100610/label/label_type2 --annotation ./data/subjects/100610/MNINonLinear/rh.aparc.annot --sd ./data/subjects/100610/MNINonLinear