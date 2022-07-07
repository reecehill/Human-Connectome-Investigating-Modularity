#!/bin/bash
export pathToData=/home/campus.ncl.ac.uk/b7071887/Xchen/Demo_high_resolution
export pathToDsiStudio=C:\Users\Reece\Documents\Dissertation\dsi_studio_win
cd $pathToDsiStudio/dsi_studio_64

i=0
for subj in $(cat $pathToData/batch_files/file_list_HCP_all_subset.txt);do
    ((i += 1))
#### generate SRC files from nifti images (.src)
$pathToDsiStudio/build/dsi_studio --action=src --source=$pathToData/$subj/data.nii.gz --bval=$pathToData/$subj/bvals --bvec=$pathToData/$subj/bvecs --output=$pathToData/$subj/data.src.gz

#### image reconstruction (.fib.gz)
$pathToDsiStudio/build/dsi_studio --action=rec --thread=4 --source=$pathToData/$subj/data.src.gz --method=4 --param0=1.25 --scheme_balance=1 --check_btable=1 --csf_calibration=1 --output_rdi=0 --output_dif=0

#### fiber tracking (.trk.gz)
$pathToDsiStudio/build/dsi_studio --action=trk --source=$pathToData/$subj/data.src.gz.odf8.f5.bal.csfc.012fy.gqi.1.25.fib.gz --fiber_count=1000000 --initial_dir=0 --thread_count=4 --seed_plan=0 --interpolation=0 --random_seed=1 --step_size=0.625 --turning_angle=60 --smoothing=0 --min_length=10 --max_length=300 --method=0 --ref=$pathToData/$subj/mri/aparc+aseg.nii --output=$pathToData/$subj/1m0.trk.gz

$pathToDsiStudio/build/dsi_studio --action=trk --source=$pathToData/$subj/data.src.gz.odf8.f5.bal.csfc.012fy.gqi.1.25.fib.gz --fiber_count=1000000 --initial_dir=0 --thread_count=4 --seed_plan=0 --interpolation=0 --random_seed=1 --step_size=0.625 --turning_angle=60 --smoothing=0 --min_length=10 --max_length=300 --method=0 --ref=$pathToData/$subj/mri/aparc+aseg.nii --output=$pathToData/$subj/1m1.trk.gz

$pathToDsiStudio/build/dsi_studio --action=trk --source=$pathToData/$subj/data.src.gz.odf8.f5.bal.csfc.012fy.gqi.1.25.fib.gz --fiber_count=1000000 --initial_dir=0 --thread_count=4 --seed_plan=0 --interpolation=0 --random_seed=1 --step_size=0.625 --turning_angle=60 --smoothing=0 --min_length=10 --max_length=300 --method=0 --ref=$pathToData/$subj/mri/aparc+aseg.nii --output=$pathToData/$subj/1m2.trk.gz

$pathToDsiStudio/build/dsi_studio --action=trk --source=$pathToData/$subj/data.src.gz.odf8.f5.bal.csfc.012fy.gqi.1.25.fib.gz --fiber_count=1000000 --initial_dir=0 --thread_count=4 --seed_plan=0 --interpolation=0 --random_seed=1 --step_size=0.625 --turning_angle=60 --smoothing=0 --min_length=10 --max_length=300 --method=0 --ref=$pathToData/$subj/mri/aparc+aseg.nii --output=$pathToData/$subj/1m3.trk.gz

$pathToDsiStudio/build/dsi_studio --action=trk --source=$pathToData/$subj/data.src.gz.odf8.f5.bal.csfc.012fy.gqi.1.25.fib.gz --fiber_count=1000000 --initial_dir=0 --thread_count=4 --seed_plan=0 --interpolation=0 --random_seed=1 --step_size=0.625 --turning_angle=60 --smoothing=0 --min_length=10 --max_length=300 --method=0 --ref=$pathToData/$subj/mri/aparc+aseg.nii --output=$pathToData/$subj/1m4.trk.gz

$pathToDsiStudio/build/dsi_studio --action=trk --source=$pathToData/$subj/data.src.gz.odf8.f5.bal.csfc.012fy.gqi.1.25.fib.gz --fiber_count=1000000 --initial_dir=0 --thread_count=4 --seed_plan=0 --interpolation=0 --random_seed=1 --step_size=0.625 --turning_angle=60 --smoothing=0 --min_length=10 --max_length=300 --method=0 --ref=$pathToData/$subj/mri/aparc+aseg.nii --output=$pathToData/$subj/1m5.trk.gz

$pathToDsiStudio/build/dsi_studio --action=trk --source=$pathToData/$subj/data.src.gz.odf8.f5.bal.csfc.012fy.gqi.1.25.fib.gz --fiber_count=1000000 --initial_dir=0 --thread_count=4 --seed_plan=0 --interpolation=0 --random_seed=1 --step_size=0.625 --turning_angle=60 --smoothing=0 --min_length=10 --max_length=300 --method=0 --ref=$pathToData/$subj/mri/aparc+aseg.nii --output=$pathToData/$subj/1m6.trk.gz

$pathToDsiStudio/build/dsi_studio --action=trk --source=$pathToData/$subj/data.src.gz.odf8.f5.bal.csfc.012fy.gqi.1.25.fib.gz --fiber_count=1000000 --initial_dir=0 --thread_count=4 --seed_plan=0 --interpolation=0 --random_seed=1 --step_size=0.625 --turning_angle=60 --smoothing=0 --min_length=10 --max_length=300 --method=0 --ref=$pathToData/$subj/mri/aparc+aseg.nii --output=$pathToData/$subj/1m7.trk.gz

$pathToDsiStudio/build/dsi_studio --action=trk --source=$pathToData/$subj/data.src.gz.odf8.f5.bal.csfc.012fy.gqi.1.25.fib.gz --fiber_count=1000000 --initial_dir=0 --thread_count=4 --seed_plan=0 --interpolation=0 --random_seed=1 --step_size=0.625 --turning_angle=60 --smoothing=0 --min_length=10 --max_length=300 --method=0 --ref=$pathToData/$subj/mri/aparc+aseg.nii --output=$pathToData/$subj/1m8.trk.gz

$pathToDsiStudio/build/dsi_studio --action=trk --source=$pathToData/$subj/data.src.gz.odf8.f5.bal.csfc.012fy.gqi.1.25.fib.gz --fiber_count=1000000 --initial_dir=0 --thread_count=4 --seed_plan=0 --interpolation=0 --random_seed=1 --step_size=0.625 --turning_angle=60 --smoothing=0 --min_length=10 --max_length=300 --method=0 --ref=$pathToData/$subj/mri/aparc+aseg.nii --output=$pathToData/$subj/1m9.trk.gz

#### unzip .trk.gz to .trk which can be open in matlab
gunzip $pathToData/$subj/1m0.trk.gz
gunzip $pathToData/$subj/1m1.trk.gz
gunzip $pathToData/$subj/1m2.trk.gz
gunzip $pathToData/$subj/1m3.trk.gz
gunzip $pathToData/$subj/1m4.trk.gz
gunzip $pathToData/$subj/1m5.trk.gz
gunzip $pathToData/$subj/1m6.trk.gz
gunzip $pathToData/$subj/1m7.trk.gz
gunzip $pathToData/$subj/1m8.trk.gz
gunzip $pathToData/$subj/1m9.trk.gz

#### delete orignal .trk.gz files
rm -f $pathToData/$subj/1m0.trk.gz
rm -f $pathToData/$subj/1m1.trk.gz
rm -f $pathToData/$subj/1m2.trk.gz
rm -f $pathToData/$subj/1m3.trk.gz
rm -f $pathToData/$subj/1m4.trk.gz
rm -f $pathToData/$subj/1m5.trk.gz
rm -f $pathToData/$subj/1m6.trk.gz
rm -f $pathToData/$subj/1m7.trk.gz
rm -f $pathToData/$subj/1m8.trk.gz
rm -f $pathToData/$subj/1m9.trk.gz
done
