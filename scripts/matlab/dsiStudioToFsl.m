function dsiStudioToFsl()
addpath('toolboxes/FieldTrip');
ft_defaults;
addpath('toolboxes/AlongTractStats');
addpath(genpath('toolboxes/SurfStat'));
    %% Convert DSIStudio studio coordinates into that viewable in FSL and FS.
   tracks = niftiinfo('../../data/subjects/100610/T1w/Diffusion/1m0_new.tt.nii.gz');
    T1w = niftiinfo('../../data/subjects/100610/MNINonLinear/T1w_restore_brain.nii.gz');
    tracks.Transform.T = T1w.Transform.T;

    tracksVol = niftiread(tracks);
    tracksFlippedY = flip(tracksVol, 2);
    niftiwrite(tracksFlippedY, '../../data/subjects/100610/T1w/Diffusion/1m0_flippedY_noflippedX.tt.nii', tracks, 'Compressed',true);

end