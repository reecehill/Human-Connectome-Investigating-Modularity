function cloneNiftiHeaders(pathToNiftiInput,pathToNiftiRef,pathToNiftiOutput)
% This function copies the qform_code and sform_code of one nifti image to another nifti.
% i.e., It replaces the "space tag" of T1w (MNI) with that of aparc+aseg ("unknown").
% This forces DSIStudio and other compatible downstream software to align
% the input nifti the same way it would the target. Essentially, it is a
% hack to ensure both files are treated equally during registration.
% See table for scode code values: https://nipy.org/nibabel/nifti_images.html
refHeader = niftiinfo(pathToNiftiRef);
inputHeader = niftiinfo(pathToNiftiInput);
inputVol = niftiread(pathToNiftiInput);
inputHeader.raw.qform_code = refHeader.raw.qform_code;
inputHeader.raw.sform_code = refHeader.raw.sform_code;

if(endsWith(pathToNiftiOutput,".nii.gz"))
    niftiwrite(inputVol, erase(pathToNiftiOutput,".nii.gz"), inputHeader, "Compressed",true);
elseif(endsWith(pathToNiftiOutput,".nii"))
    niftiwrite(inputVol, erase(pathToNiftiOutput,".nii"), inputHeader, "Compressed",false);
else
    error('pathToNiftiOutput must end with either .nii.gz or .nii');
end
end