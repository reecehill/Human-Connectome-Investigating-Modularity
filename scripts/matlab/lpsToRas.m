function lpsToRas(inputFilePath)
    nifti = niftiread(inputFilePath);
    nifti_info = niftiinfo(inputFilePath);
    nifti = flip(nifti,1);
    nifti = flip(nifti,2);

    niftiwrite(nifti, [inputFilePath '.new.nii.gz'], nifti_info);
    print("de");
    ok;
end