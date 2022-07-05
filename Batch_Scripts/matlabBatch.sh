#!/bin/bash
export pathto_data=/home/campus.ncl.ac.uk/b7071887/Xchen/Demo_high_resolution
cd $pathto_data

### batch_process(pathToFile,subjects,type,downsample,rate)
### type=1, using pial.surf.nii file; type=2, using pial file
### downsample='yes', downsample surface coordinates; downsample='no', no downsample(default)
### rate is downsample rate,default is 0.1
export type=1
export downsample='yes'
export rate=0.1

i=0
for subj in $(cat $pathto_data/batch_files/file_list_HCP_all_subset.txt);do
((i += 1))
matlab -nodisplay -nosplas -r "try, batch_process('$pathto_data/','$subj',$type,'$downsample',$rate);end;"
done
