function dsiStudioToFsl()
addpath('toolboxes/FieldTrip');
ft_defaults;
addpath('toolboxes/AlongTractStats');
addpath(genpath('toolboxes/SurfStat'));
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

   tracks = niftiinfo('../../data/subjects/100610/T1w/Diffusion/1m0.tt.nii.gz');
    T1w = niftiinfo('../../data/subjects/100610/MNINonLinear/T1w_restore_brain.nii.gz');
    tracks.Transform.T = T1w.Transform.T;

    tracksVol = niftiread(tracks);
    tracksFlippedY = flip(tracksVol, 2);
    tracksFlippedX = flip(tracksFlippedY, 1);

    niftiwrite(tracksFlippedY, '../../data/subjects/100610/T1w/Diffusion/1m0_flippedY_noflippedX.tt.nii.gz', tracks);

    %% Tracks version
    [trackHeader, tracksVol] = trk_read('../../data/subjects/100610/T1w/Diffusion/1m0.trk');
    T1w = niftiinfo('../../data/subjects/100610/MNINonLinear/T1w_restore_brain.nii.gz');
    % trackHeader.vox_to_ras = T1w.Transform.T;

    trackHeader.hdr_size = int32(1000);
    trackIndex = 1;
    copyTracksVol = tracksVol;
    for track=1:1:length(tracksVol)
        copyTracksVol(trackIndex).matrix = [tracksVol(trackIndex).matrix(:,1), tracksVol(trackIndex).matrix(:,2) * -1, tracksVol(trackIndex).matrix(:,3) ];
    end
    trk_write(trackHeader, tracksVol, '../../data/subjects/100610/T1w/Diffusion/whole_brain_in_T1w_restore_brain_flippedY_noflippedX_unedited.trk');
    trk_write(trackHeader, copyTracksVol, '../../data/subjects/100610/T1w/Diffusion/whole_brain_in_T1w_restore_brain_flippedY_noflippedX.trk');

    %% Convert MNI T1w header to pretend its not MNI (so DSI Studio uses normalisation)
    T1wMNI = niftiinfo('../../data/subjects/100610/MNINonLinear/T1w_restore_brain.nii.gz');
    T1wMNIVol = niftiread(T1wMNI);
    T1wMNI.raw.sform_code = 3;
    T1wMNI.raw.qform_code = 3;
    niftiwrite(T1wMNIVol, '../../data/subjects/100610/MNINonLinear/T1w_moddedheader.native.nii', T1wMNI, 'Compressed',true,'Version','NIfTI2');
end