function RunPreproc_1stLevel_job(pathToParticipants, subject)
addpath(genpath('toolboxes/spm12'));
close all;
clearvars -except pathToParticipants subject;
try
    %% Wipe results folder if exists. Then remake.
    if exist([pathToParticipants '/' subject '/1stlevel'], 'dir')
        delete([pathToParticipants '/' subject '/1stlevel/*']);
    end
    if ~exist([pathToParticipants '/' subject '/1stlevel'], 'dir')
        mkdir([pathToParticipants '/' subject '/1stlevel']);
    end

    %% Ensure fMRI is unzipped.
    if ~exist([pathToParticipants '/' subject '/data/func/task-HcpMotor_acq-ap_bold.nii'], 'file')
        gunzip([pathToParticipants '/' subject '/data/func/task-HcpMotor_acq-ap_bold.nii.gz'],[pathToParticipants '/' subject '/data/func']);
    end
    %-----------------------------------------------------------------------
    % Job saved on 31-Jul-2022 16:21:17 by cfg_util (rev $Rev: 7345 $)
    % spm SPM - SPM12 (7771)
    % cfg_basicio BasicIO - Unknown
    %-----------------------------------------------------------------------

    %% Name file. (?Possibly pointless, as only a single run)
    matlabbatch{1}.cfg_basicio.run_ops.call_matlab.inputs{1}.evaluated = 'Skipped a module.';
    matlabbatch{1}.cfg_basicio.run_ops.call_matlab.outputs = {};
    matlabbatch{1}.cfg_basicio.run_ops.call_matlab.fun = 'display';
    %matlabbatch{1}.cfg_basicio.file_dir.file_ops.cfg_named_file.name = 'HcpMotorFiles';
    %matlabbatch{1}.cfg_basicio.file_dir.file_ops.cfg_named_file.files = {{[pathToParticipants '\' subject '\data\func\task-HcpMotor_acq-ap_bold.nii.gz']}};
    %matlabbatch{1}.cfg_basicio.file_dir.file_ops.cfg_named_file.files = {{[pathToParticipants '\' subject '\data\func\artask-HcpMotor_acq-ap_bold.nii']}};

    %% Unzip fmri Data.
    %matlabbatch{2}.cfg_basicio.file_dir.file_ops.cfg_gunzip_files.files(1) = cfg_dep('Named File Selector: HcpMotorFiles(1) - Files', substruct('.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','files', '{}',{1}));
    %matlabbatch{2}.cfg_basicio.file_dir.file_ops.cfg_gunzip_files.outdir = {''};
    %matlabbatch{2}.cfg_basicio.file_dir.file_ops.cfg_gunzip_files.keep = true;
    matlabbatch{2}.cfg_basicio.run_ops.call_matlab.inputs{1}.evaluated = 'Skipped a module.';
    matlabbatch{2}.cfg_basicio.run_ops.call_matlab.outputs = {};
    matlabbatch{2}.cfg_basicio.run_ops.call_matlab.fun = 'display';


    %% Estimate and reslice
    if ~exist([pathToParticipants '/' subject '/data/func/rtask-HcpMotor_acq-ap_bold.nii'], 'file')
        matlabbatch{3}.spm.spatial.realign.estwrite.data{1}(1) = {[pathToParticipants '\' subject '\data\func\task-HcpMotor_acq-ap_bold.nii']};
        matlabbatch{3}.spm.spatial.realign.estwrite.eoptions.quality = 0.9;
        matlabbatch{3}.spm.spatial.realign.estwrite.eoptions.sep = 4;
        matlabbatch{3}.spm.spatial.realign.estwrite.eoptions.fwhm = 5;
        matlabbatch{3}.spm.spatial.realign.estwrite.eoptions.rtm = 1;
        matlabbatch{3}.spm.spatial.realign.estwrite.eoptions.interp = 2;
        matlabbatch{3}.spm.spatial.realign.estwrite.eoptions.wrap = [0 0 0];
        matlabbatch{3}.spm.spatial.realign.estwrite.eoptions.weight = '';
        matlabbatch{3}.spm.spatial.realign.estwrite.roptions.which = [2 1];
        matlabbatch{3}.spm.spatial.realign.estwrite.roptions.interp = 4;
        matlabbatch{3}.spm.spatial.realign.estwrite.roptions.wrap = [0 0 0];
        matlabbatch{3}.spm.spatial.realign.estwrite.roptions.mask = 1;
        matlabbatch{3}.spm.spatial.realign.estwrite.roptions.prefix = 'r';
    else
        matlabbatch{3}.cfg_basicio.run_ops.call_matlab.inputs{1}.evaluated = 'Skipped a module.';
        matlabbatch{3}.cfg_basicio.run_ops.call_matlab.outputs = {};
        matlabbatch{3}.cfg_basicio.run_ops.call_matlab.fun = 'display';
    end

    %% Slice timing
    if ~exist([pathToParticipants '/' subject '/data/func/artask-HcpMotor_acq-ap_bold.nii'], 'file')
        matlabbatch{4}.spm.temporal.st.scans{1}(1) = {[pathToParticipants '/' subject '/data/func/rtask-HcpMotor_acq-ap_bold.nii']};
        matlabbatch{4}.spm.temporal.st.nslices = 93;
        matlabbatch{4}.spm.temporal.st.tr = 2;
        matlabbatch{4}.spm.temporal.st.ta = 1.97849462365591;
        matlabbatch{4}.spm.temporal.st.so = [0 1.0225 0.0625 1.085 0.1275 1.15 0.1925 1.2125 0.255 1.2775 0.32 1.34 0.3825 1.405 0.4475 1.47 0.51 1.5325 0.575 1.5975 0.6375 1.66 0.7025 1.725 0.765 1.7875 0.83 1.8525 0.895 1.915 0.9575 0 1.0225 0.0625 1.085 0.1275 1.15 0.1925 1.2125 0.255 1.2775 0.32 1.34 0.3825 1.405 0.4475 1.47 0.51 1.5325 0.575 1.5975 0.6375 1.66 0.7025 1.725 0.765 1.7875 0.83 1.8525 0.895 1.915 0.9575 0 1.0225 0.0625 1.085 0.1275 1.15 0.1925 1.2125 0.255 1.2775 0.32 1.34 0.3825 1.405 0.4475 1.47 0.51 1.5325 0.575 1.5975 0.6375 1.66 0.7025 1.725 0.765 1.7875 0.83 1.8525 0.895 1.915 0.9575];
        matlabbatch{4}.spm.temporal.st.refslice = 0;
        matlabbatch{4}.spm.temporal.st.prefix = 'a';
    else
        matlabbatch{4}.cfg_basicio.run_ops.call_matlab.inputs{1}.evaluated = 'Skipped a module.';
        matlabbatch{4}.cfg_basicio.run_ops.call_matlab.outputs = {};
        matlabbatch{4}.cfg_basicio.run_ops.call_matlab.fun = 'display';
    end



    %% Coregister and reslice
        % Instance 1: we move T1 image and mask (precentral_gyrus) to coregister with mean fMRI image. Used for SPM masking.. 
    if ~exist([pathToParticipants '/' subject '/data/bert/mri/rT1.nii'], 'file')
        matlabbatch{5}.spm.spatial.coreg.estwrite.ref = {[pathToParticipants '\' subject '/data/func/artask-HcpMotor_acq-ap_bold.nii,1']};
        matlabbatch{5}.spm.spatial.coreg.estwrite.source(1) = {[pathToParticipants '/' subject '/data/bert/mri/T1.nii,1']};
        matlabbatch{5}.spm.spatial.coreg.estwrite.other = {''};
        matlabbatch{5}.spm.spatial.coreg.estwrite.eoptions.cost_fun = 'nmi';
        matlabbatch{5}.spm.spatial.coreg.estwrite.eoptions.sep = [4 2];
        matlabbatch{5}.spm.spatial.coreg.estwrite.eoptions.tol = [0.02 0.02 0.02 0.001 0.001 0.001 0.01 0.01 0.01 0.001 0.001 0.001];
        matlabbatch{5}.spm.spatial.coreg.estwrite.eoptions.fwhm = [7 7];
        matlabbatch{5}.spm.spatial.coreg.estwrite.roptions.interp = 4;
        matlabbatch{5}.spm.spatial.coreg.estwrite.roptions.wrap = [0 0 0];
        matlabbatch{5}.spm.spatial.coreg.estwrite.roptions.mask = 0;
        matlabbatch{5}.spm.spatial.coreg.estwrite.roptions.prefix = 'r';
    else
        matlabbatch{5}.cfg_basicio.run_ops.call_matlab.inputs{1}.evaluated = 'Skipped module 5.';
        matlabbatch{5}.cfg_basicio.run_ops.call_matlab.outputs = {};
        matlabbatch{5}.cfg_basicio.run_ops.call_matlab.fun = 'display';
    end

    % Instance 2: we move the mean fMRI image to match the T1 image. This
    % is important for tkregister2, which is ran separately later. 
    if ~exist([pathToParticipants '/' subject '/data/func/rmeantask-HcpMotor_acq-ap_bold.nii'], 'file')
        matlabbatch{6}.spm.spatial.coreg.estwrite.ref = {[pathToParticipants '\' subject '\data\bert\mri\T1.nii,1']};
        matlabbatch{6}.spm.spatial.coreg.estwrite.source(1) = {[pathToParticipants '/' subject '/data/func/meantask-HcpMotor_acq-ap_bold.nii,1']};
        matlabbatch{6}.spm.spatial.coreg.estwrite.other = {''};
        matlabbatch{6}.spm.spatial.coreg.estwrite.eoptions.cost_fun = 'nmi';
        matlabbatch{6}.spm.spatial.coreg.estwrite.eoptions.sep = [4 2];
        matlabbatch{6}.spm.spatial.coreg.estwrite.eoptions.tol = [0.02 0.02 0.02 0.001 0.001 0.001 0.01 0.01 0.01 0.001 0.001 0.001];
        matlabbatch{6}.spm.spatial.coreg.estwrite.eoptions.fwhm = [7 7];
        matlabbatch{6}.spm.spatial.coreg.estwrite.roptions.interp = 4;
        matlabbatch{6}.spm.spatial.coreg.estwrite.roptions.wrap = [0 0 0];
        matlabbatch{6}.spm.spatial.coreg.estwrite.roptions.mask = 0;
        matlabbatch{6}.spm.spatial.coreg.estwrite.roptions.prefix = 'r';
    else
        matlabbatch{6}.cfg_basicio.run_ops.call_matlab.inputs{1}.evaluated = 'Skipped a module.';
        matlabbatch{6}.cfg_basicio.run_ops.call_matlab.outputs = {};
        matlabbatch{6}.cfg_basicio.run_ops.call_matlab.fun = 'display';
    end

    %% Segmentation
    % matlabbatch{7}.spm.spatial.preproc.channel.vols(1) = cfg_dep('Coregister: Estimate & Reslice: Coregistered Images', substruct('.','val', '{}',{5}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','cfiles'));
    %     matlabbatch{7}.spm.spatial.preproc.channel.biasreg = 0.001;
    %     matlabbatch{7}.spm.spatial.preproc.channel.biasfwhm = 60;
    %     matlabbatch{7}.spm.spatial.preproc.channel.write = [0 1];
    %     matlabbatch{7}.spm.spatial.preproc.tissue(1).tpm = {'C:\Program Files\MATLAB\R2021b\spm12\tpm\TPM.nii,1'};
    %     matlabbatch{7}.spm.spatial.preproc.tissue(1).ngaus = 1;
    %     matlabbatch{7}.spm.spatial.preproc.tissue(1).native = [1 0];
    %     matlabbatch{7}.spm.spatial.preproc.tissue(1).warped = [0 0];
    %     matlabbatch{7}.spm.spatial.preproc.tissue(2).tpm = {'C:\Program Files\MATLAB\R2021b\spm12\tpm\TPM.nii,2'};
    %     matlabbatch{7}.spm.spatial.preproc.tissue(2).ngaus = 1;
    %     matlabbatch{7}.spm.spatial.preproc.tissue(2).native = [1 0];
    %     matlabbatch{7}.spm.spatial.preproc.tissue(2).warped = [0 0];
    %     matlabbatch{7}.spm.spatial.preproc.tissue(3).tpm = {'C:\Program Files\MATLAB\R2021b\spm12\tpm\TPM.nii,3'};
    %     matlabbatch{7}.spm.spatial.preproc.tissue(3).ngaus = 2;
    %     matlabbatch{7}.spm.spatial.preproc.tissue(3).native = [1 0];
    %     matlabbatch{7}.spm.spatial.preproc.tissue(3).warped = [0 0];
    %     matlabbatch{7}.spm.spatial.preproc.tissue(4).tpm = {'C:\Program Files\MATLAB\R2021b\spm12\tpm\TPM.nii,4'};
    %     matlabbatch{7}.spm.spatial.preproc.tissue(4).ngaus = 3;
    %     matlabbatch{7}.spm.spatial.preproc.tissue(4).native = [1 0];
    %     matlabbatch{7}.spm.spatial.preproc.tissue(4).warped = [0 0];
    %     matlabbatch{7}.spm.spatial.preproc.tissue(5).tpm = {'C:\Program Files\MATLAB\R2021b\spm12\tpm\TPM.nii,5'};
    %     matlabbatch{7}.spm.spatial.preproc.tissue(5).ngaus = 4;
    %     matlabbatch{7}.spm.spatial.preproc.tissue(5).native = [1 0];
    %     matlabbatch{7}.spm.spatial.preproc.tissue(5).warped = [0 0];
    %     matlabbatch{7}.spm.spatial.preproc.tissue(6).tpm = {'C:\Program Files\MATLAB\R2021b\spm12\tpm\TPM.nii,6'};
    %     matlabbatch{7}.spm.spatial.preproc.tissue(6).ngaus = 2;
    %     matlabbatch{7}.spm.spatial.preproc.tissue(6).native = [0 0];
    %     matlabbatch{7}.spm.spatial.preproc.tissue(6).warped = [0 0];
    %     matlabbatch{7}.spm.spatial.preproc.warp.mrf = 1;
    %     matlabbatch{7}.spm.spatial.preproc.warp.cleanup = 1;
    %     matlabbatch{7}.spm.spatial.preproc.warp.reg = [0 0.001 0.5 0.05 0.2];
    %     matlabbatch{7}.spm.spatial.preproc.warp.affreg = 'mni';
    %     matlabbatch{7}.spm.spatial.preproc.warp.fwhm = 0;
    %     matlabbatch{7}.spm.spatial.preproc.warp.samp = 3;
    %     matlabbatch{7}.spm.spatial.preproc.warp.write = [0 1];
    %     matlabbatch{7}.spm.spatial.preproc.warp.vox = NaN;
    %     matlabbatch{7}.spm.spatial.preproc.warp.bb = [NaN NaN NaN
    %         NaN NaN NaN];
    matlabbatch{7}.cfg_basicio.run_ops.call_matlab.inputs{1}.evaluated = 'Skipped a module.';
    matlabbatch{7}.cfg_basicio.run_ops.call_matlab.outputs = {};
    matlabbatch{7}.cfg_basicio.run_ops.call_matlab.fun = 'display';

    %     %% Normalise the fMRI to MNI space.
    %     matlabbatch{8}.spm.spatial.normalise.write.subj.def(1) = cfg_dep('Segment: Forward Deformations', substruct('.','val', '{}',{8}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','fordef', '()',{':'}));
    %     matlabbatch{8}.spm.spatial.normalise.write.subj.resample(1) = cfg_dep('Slice Timing: Slice Timing Corr. Images (Sess 1)', substruct('.','val', '{}',{4}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('()',{1}, '.','files'));
    %     matlabbatch{8}.spm.spatial.normalise.write.woptions.bb = [-78 -112 -70
    %         78 76 85];
    %     matlabbatch{8}.spm.spatial.normalise.write.woptions.vox = [2 2 2];
    %     matlabbatch{8}.spm.spatial.normalise.write.woptions.interp = 4;
    %     matlabbatch{8}.spm.spatial.normalise.write.woptions.prefix = 'w';
    matlabbatch{8}.cfg_basicio.run_ops.call_matlab.inputs{1}.evaluated = 'Skipped a module.';
    matlabbatch{8}.cfg_basicio.run_ops.call_matlab.outputs = {};
    matlabbatch{8}.cfg_basicio.run_ops.call_matlab.fun = 'display';

    %% Smooth normalised fMRI data.
    if ~exist([pathToParticipants '/' subject '/data/func/sartask-HcpMotor_acq-ap_bold.nii'], 'file')
        %matlabbatch{9}.spm.spatial.smooth.data(1) = cfg_dep('Normalise: Write: Normalised Images (Subj 1)', substruct('.','val', '{}',{9}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('()',{1}, '.','files'));
        %matlabbatch{9}.spm.spatial.smooth.data(1) = cfg_dep('Slice Timing: Slice Timing Corr. Images (Sess 1)', substruct('.','val', '{}',{4}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('()',{1}, '.','files'));
        matlabbatch{9}.spm.spatial.smooth.data = {[pathToParticipants '/' subject '/data/func/artask-HcpMotor_acq-ap_bold.nii']};
        %matlabbatch{9}.spm.spatial.smooth.data(1) = cfg_dep('Named File Selector: HcpMotorFiles(1) - Files', substruct('.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','files', '{}',{1}));
        matlabbatch{9}.spm.spatial.smooth.fwhm = [5 5 5]; %changed from 8 to 5 as per: https://europepmc.org/article/PMC/7856658#hbm25189-bib-0112
        matlabbatch{9}.spm.spatial.smooth.dtype = 0;
        matlabbatch{9}.spm.spatial.smooth.im = 0;
        matlabbatch{9}.spm.spatial.smooth.prefix = 's';
    else
        matlabbatch{9}.cfg_basicio.run_ops.call_matlab.inputs{1}.evaluated = 'Skipped a module.';
        matlabbatch{9}.cfg_basicio.run_ops.call_matlab.outputs = {};
        matlabbatch{9}.cfg_basicio.run_ops.call_matlab.fun = 'display';
    end



    disp("The preprocessing steps for SPM are finished.")

    spm('defaults', 'FMRI');
    spm_jobman('run', matlabbatch);

catch ME
    sound(tan(1:1000)); pause(0.2); sound(tan(1:1000));
    rethrow(ME);
end
end