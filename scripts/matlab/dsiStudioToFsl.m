function dsiStudioToFsl()
    %% Convert DSIStudio studio coordinates into that viewable in FSL and FS.

    tracks = niftiinfo('../../data/subjects/100610/T1w/Diffusion/1m0.tt.nii.gz');
    T1w = niftiinfo('../../data/subjects/100610/T1w/T1w_acpc_dc_restore_brain.nii.gz');
    tracks.Transform.T = T1w.Transform.T;

    tracksVol = niftiread(tracks);
    tracksVolFlippedXAxis = flip(tracksVol, 1);
    tracksVolFlippedYAxis = flip(tracksVol, 2);

    niftiwrite(tracksVolFlippedXAxis, '../../data/subjects/100610/T1w/Diffusion/1m0_flippedY.tt.nii.gz', tracks);

    tracks = niftiinfo('../../data/subjects/100610/T1w/Diffusion/whole_brain_in_T1w_restore_brain_mni.tt.nii.gz');
    T1w = niftiinfo('../../data/subjects/100610/MNINonLinear/T1w_restore_brain.nii.gz');
    tracks.Transform.T = T1w.Transform.T;

    tracksVol = niftiread(tracks);
    tracksVolFlippedXAxis = flip(tracksVol, 1);
    tracksVolFlippedYAxis = flip(tracksVol, 2);

    niftiwrite(tracksVolFlippedXAxis, '../../data/subjects/100610/T1w/Diffusion/1m0_flippedY_mni.tt.nii.gz', tracks);
    %niftiwrite(tracksVolFlippedYAxis, '../../data/subjects/100610/T1w/Diffusion/1m0_flippedX.tt.nii.gz', tracks);
end