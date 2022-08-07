function RunPreproc_1stLevel_job(pathToParticipants, subject)
    if ~exist([pathToParticipants '/' subject '/1stlevel'], 'dir')
       mkdir([pathToParticipants '/' subject '/1stlevel'])
    end
    %-----------------------------------------------------------------------
    % Job saved on 31-Jul-2022 16:21:17 by cfg_util (rev $Rev: 7345 $)
    % spm SPM - SPM12 (7771)
    % cfg_basicio BasicIO - Unknown
    %-----------------------------------------------------------------------
    matlabbatch{1}.cfg_basicio.file_dir.file_ops.cfg_named_file.name = 'HcpMotorFiles';
    matlabbatch{1}.cfg_basicio.file_dir.file_ops.cfg_named_file.files = {{[pathToParticipants '\' subject '\data\func\task-HcpMotor_acq-ap_bold.nii.gz']}};
    matlabbatch{2}.cfg_basicio.file_dir.file_ops.cfg_gunzip_files.files(1) = cfg_dep('Named File Selector: HcpMotorFiles(1) - Files', substruct('.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','files', '{}',{1}));
    matlabbatch{2}.cfg_basicio.file_dir.file_ops.cfg_gunzip_files.outdir = {''};
    matlabbatch{2}.cfg_basicio.file_dir.file_ops.cfg_gunzip_files.keep = true;
    matlabbatch{3}.spm.spatial.realign.estwrite.data{1}(1) = cfg_dep('Gunzip Files: Gunzipped Files', substruct('.','val', '{}',{2}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('()',{':'}));
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
    matlabbatch{4}.spm.temporal.st.scans{1}(1) = cfg_dep('Realign: Estimate & Reslice: Resliced Images (Sess 1)', substruct('.','val', '{}',{3}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','sess', '()',{1}, '.','rfiles'));
    matlabbatch{4}.spm.temporal.st.nslices = 93;
    matlabbatch{4}.spm.temporal.st.tr = 2;
    matlabbatch{4}.spm.temporal.st.ta = 1.97849462365591;
    matlabbatch{4}.spm.temporal.st.so = [0 1.0225 0.0625 1.085 0.1275 1.15 0.1925 1.2125 0.255 1.2775 0.32 1.34 0.3825 1.405 0.4475 1.47 0.51 1.5325 0.575 1.5975 0.6375 1.66 0.7025 1.725 0.765 1.7875 0.83 1.8525 0.895 1.915 0.9575 0 1.0225 0.0625 1.085 0.1275 1.15 0.1925 1.2125 0.255 1.2775 0.32 1.34 0.3825 1.405 0.4475 1.47 0.51 1.5325 0.575 1.5975 0.6375 1.66 0.7025 1.725 0.765 1.7875 0.83 1.8525 0.895 1.915 0.9575 0 1.0225 0.0625 1.085 0.1275 1.15 0.1925 1.2125 0.255 1.2775 0.32 1.34 0.3825 1.405 0.4475 1.47 0.51 1.5325 0.575 1.5975 0.6375 1.66 0.7025 1.725 0.765 1.7875 0.83 1.8525 0.895 1.915 0.9575];
    matlabbatch{4}.spm.temporal.st.refslice = 0;
    matlabbatch{4}.spm.temporal.st.prefix = 'a';
    matlabbatch{5}.spm.spatial.coreg.estwrite.ref(1) = cfg_dep('Realign: Estimate & Reslice: Mean Image', substruct('.','val', '{}',{3}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','rmean'));
    matlabbatch{5}.spm.spatial.coreg.estwrite.source = {[pathToParticipants '\' subject '\data\anat\T1w.nii,1']};
    matlabbatch{5}.spm.spatial.coreg.estwrite.other = {''};
    matlabbatch{5}.spm.spatial.coreg.estwrite.eoptions.cost_fun = 'nmi';
    matlabbatch{5}.spm.spatial.coreg.estwrite.eoptions.sep = [4 2];
    matlabbatch{5}.spm.spatial.coreg.estwrite.eoptions.tol = [0.02 0.02 0.02 0.001 0.001 0.001 0.01 0.01 0.01 0.001 0.001 0.001];
    matlabbatch{5}.spm.spatial.coreg.estwrite.eoptions.fwhm = [7 7];
    matlabbatch{5}.spm.spatial.coreg.estwrite.roptions.interp = 4;
    matlabbatch{5}.spm.spatial.coreg.estwrite.roptions.wrap = [0 0 0];
    matlabbatch{5}.spm.spatial.coreg.estwrite.roptions.mask = 0;
    matlabbatch{5}.spm.spatial.coreg.estwrite.roptions.prefix = 'r';
    matlabbatch{6}.spm.spatial.preproc.channel.vols(1) = cfg_dep('Coregister: Estimate & Reslice: Coregistered Images', substruct('.','val', '{}',{5}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','cfiles'));
    matlabbatch{6}.spm.spatial.preproc.channel.biasreg = 0.001;
    matlabbatch{6}.spm.spatial.preproc.channel.biasfwhm = 60;
    matlabbatch{6}.spm.spatial.preproc.channel.write = [0 1];
    matlabbatch{6}.spm.spatial.preproc.tissue(1).tpm = {'C:\Program Files\MATLAB\R2021b\spm12\tpm\TPM.nii,1'};
    matlabbatch{6}.spm.spatial.preproc.tissue(1).ngaus = 1;
    matlabbatch{6}.spm.spatial.preproc.tissue(1).native = [1 0];
    matlabbatch{6}.spm.spatial.preproc.tissue(1).warped = [0 0];
    matlabbatch{6}.spm.spatial.preproc.tissue(2).tpm = {'C:\Program Files\MATLAB\R2021b\spm12\tpm\TPM.nii,2'};
    matlabbatch{6}.spm.spatial.preproc.tissue(2).ngaus = 1;
    matlabbatch{6}.spm.spatial.preproc.tissue(2).native = [1 0];
    matlabbatch{6}.spm.spatial.preproc.tissue(2).warped = [0 0];
    matlabbatch{6}.spm.spatial.preproc.tissue(3).tpm = {'C:\Program Files\MATLAB\R2021b\spm12\tpm\TPM.nii,3'};
    matlabbatch{6}.spm.spatial.preproc.tissue(3).ngaus = 2;
    matlabbatch{6}.spm.spatial.preproc.tissue(3).native = [1 0];
    matlabbatch{6}.spm.spatial.preproc.tissue(3).warped = [0 0];
    matlabbatch{6}.spm.spatial.preproc.tissue(4).tpm = {'C:\Program Files\MATLAB\R2021b\spm12\tpm\TPM.nii,4'};
    matlabbatch{6}.spm.spatial.preproc.tissue(4).ngaus = 3;
    matlabbatch{6}.spm.spatial.preproc.tissue(4).native = [1 0];
    matlabbatch{6}.spm.spatial.preproc.tissue(4).warped = [0 0];
    matlabbatch{6}.spm.spatial.preproc.tissue(5).tpm = {'C:\Program Files\MATLAB\R2021b\spm12\tpm\TPM.nii,5'};
    matlabbatch{6}.spm.spatial.preproc.tissue(5).ngaus = 4;
    matlabbatch{6}.spm.spatial.preproc.tissue(5).native = [1 0];
    matlabbatch{6}.spm.spatial.preproc.tissue(5).warped = [0 0];
    matlabbatch{6}.spm.spatial.preproc.tissue(6).tpm = {'C:\Program Files\MATLAB\R2021b\spm12\tpm\TPM.nii,6'};
    matlabbatch{6}.spm.spatial.preproc.tissue(6).ngaus = 2;
    matlabbatch{6}.spm.spatial.preproc.tissue(6).native = [0 0];
    matlabbatch{6}.spm.spatial.preproc.tissue(6).warped = [0 0];
    matlabbatch{6}.spm.spatial.preproc.warp.mrf = 1;
    matlabbatch{6}.spm.spatial.preproc.warp.cleanup = 1;
    matlabbatch{6}.spm.spatial.preproc.warp.reg = [0 0.001 0.5 0.05 0.2];
    matlabbatch{6}.spm.spatial.preproc.warp.affreg = 'mni';
    matlabbatch{6}.spm.spatial.preproc.warp.fwhm = 0;
    matlabbatch{6}.spm.spatial.preproc.warp.samp = 3;
    matlabbatch{6}.spm.spatial.preproc.warp.write = [0 1];
    matlabbatch{6}.spm.spatial.preproc.warp.vox = NaN;
    matlabbatch{6}.spm.spatial.preproc.warp.bb = [NaN NaN NaN
                                                  NaN NaN NaN];
    matlabbatch{7}.spm.spatial.normalise.write.subj.def(1) = cfg_dep('Segment: Forward Deformations', substruct('.','val', '{}',{6}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','fordef', '()',{':'}));
    matlabbatch{7}.spm.spatial.normalise.write.subj.resample(1) = cfg_dep('Slice Timing: Slice Timing Corr. Images (Sess 1)', substruct('.','val', '{}',{4}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('()',{1}, '.','files'));
    matlabbatch{7}.spm.spatial.normalise.write.woptions.bb = [-78 -112 -70
                                                              78 76 85];
    matlabbatch{7}.spm.spatial.normalise.write.woptions.vox = [2 2 2];
    matlabbatch{7}.spm.spatial.normalise.write.woptions.interp = 4;
    matlabbatch{7}.spm.spatial.normalise.write.woptions.prefix = 'w';
    matlabbatch{8}.spm.spatial.smooth.data(1) = cfg_dep('Normalise: Write: Normalised Images (Subj 1)', substruct('.','val', '{}',{7}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('()',{1}, '.','files'));
    matlabbatch{8}.spm.spatial.smooth.fwhm = [8 8 8];
    matlabbatch{8}.spm.spatial.smooth.dtype = 0;
    matlabbatch{8}.spm.spatial.smooth.im = 0;
    matlabbatch{8}.spm.spatial.smooth.prefix = 's';
    matlabbatch{9}.spm.stats.fmri_spec.dir = {[pathToParticipants '/' subject '\1stlevel']};
    matlabbatch{9}.spm.stats.fmri_spec.timing.units = 'secs';
    matlabbatch{9}.spm.stats.fmri_spec.timing.RT = 2;
    matlabbatch{9}.spm.stats.fmri_spec.timing.fmri_t = 16;
    matlabbatch{9}.spm.stats.fmri_spec.timing.fmri_t0 = 8;
    matlabbatch{9}.spm.stats.fmri_spec.sess.scans(1) = cfg_dep('Smooth: Smoothed Images', substruct('.','val', '{}',{8}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','files'));
    matlabbatch{9}.spm.stats.fmri_spec.sess.cond(1).name = 'left_hand';
    %%
    leftHandTimingFile = importdata([pathToParticipants '/' subject '\data\func\timing_files\left_hand.txt']);
    matlabbatch{9}.spm.stats.fmri_spec.sess.cond(1).onset = leftHandTimingFile(:,1);
    matlabbatch{9}.spm.stats.fmri_spec.sess.cond(1).duration = leftHandTimingFile(:,2);
    %%
    matlabbatch{9}.spm.stats.fmri_spec.sess.cond(1).tmod = 0;
    matlabbatch{9}.spm.stats.fmri_spec.sess.cond(1).pmod = struct('name', {}, 'param', {}, 'poly', {});
    matlabbatch{9}.spm.stats.fmri_spec.sess.cond(1).orth = 1;
    matlabbatch{9}.spm.stats.fmri_spec.sess.cond(2).name = 'right_hand';
    
    rightHandTimingFile = importdata([pathToParticipants '/' subject '\data\func\timing_files\right_hand.txt']);
    matlabbatch{9}.spm.stats.fmri_spec.sess.cond(2).onset = rightHandTimingFile(:,1);
    matlabbatch{9}.spm.stats.fmri_spec.sess.cond(2).duration = rightHandTimingFile(:,2);
    %%
    
    %%
    matlabbatch{9}.spm.stats.fmri_spec.sess.cond(2).tmod = 0;
    matlabbatch{9}.spm.stats.fmri_spec.sess.cond(2).pmod = struct('name', {}, 'param', {}, 'poly', {});
    matlabbatch{9}.spm.stats.fmri_spec.sess.cond(2).orth = 1;
    matlabbatch{9}.spm.stats.fmri_spec.sess.cond(3).name = 'left_foot';
    %%
    leftFootTimingFile = importdata([pathToParticipants '/' subject '\data\func\timing_files\left_foot.txt']);
    matlabbatch{9}.spm.stats.fmri_spec.sess.cond(3).onset = leftFootTimingFile(:,1);
    matlabbatch{9}.spm.stats.fmri_spec.sess.cond(3).duration = leftFootTimingFile(:,2);
    
    %%
    matlabbatch{9}.spm.stats.fmri_spec.sess.cond(3).tmod = 0;
    matlabbatch{9}.spm.stats.fmri_spec.sess.cond(3).pmod = struct('name', {}, 'param', {}, 'poly', {});
    matlabbatch{9}.spm.stats.fmri_spec.sess.cond(3).orth = 1;
    matlabbatch{9}.spm.stats.fmri_spec.sess.cond(4).name = 'right_foot';
    rightFootTimingFile = importdata([pathToParticipants '/' subject '\data\func\timing_files\right_foot.txt']);
    matlabbatch{9}.spm.stats.fmri_spec.sess.cond(4).onset = rightFootTimingFile(:,1);
    matlabbatch{9}.spm.stats.fmri_spec.sess.cond(4).duration = rightFootTimingFile(:,2);

    %%
    matlabbatch{9}.spm.stats.fmri_spec.sess.cond(4).tmod = 0;
    matlabbatch{9}.spm.stats.fmri_spec.sess.cond(4).pmod = struct('name', {}, 'param', {}, 'poly', {});
    matlabbatch{9}.spm.stats.fmri_spec.sess.cond(4).orth = 1;
    matlabbatch{9}.spm.stats.fmri_spec.sess.cond(5).name = 'tongue';
    %%
    tongueTimingFile = importdata([pathToParticipants '/' subject '\data\func\timing_files\tongue.txt']);
    matlabbatch{9}.spm.stats.fmri_spec.sess.cond(5).onset = tongueTimingFile(:,1);
    matlabbatch{9}.spm.stats.fmri_spec.sess.cond(5).duration = tongueTimingFile(:,2);
    
    matlabbatch{9}.spm.stats.fmri_spec.sess.cond(5).tmod = 0;
    matlabbatch{9}.spm.stats.fmri_spec.sess.cond(5).pmod = struct('name', {}, 'param', {}, 'poly', {});
    matlabbatch{9}.spm.stats.fmri_spec.sess.cond(5).orth = 1;
    matlabbatch{9}.spm.stats.fmri_spec.sess.multi = {''};
    matlabbatch{9}.spm.stats.fmri_spec.sess.regress = struct('name', {}, 'val', {});
    matlabbatch{9}.spm.stats.fmri_spec.sess.multi_reg = {''};
    matlabbatch{9}.spm.stats.fmri_spec.sess.hpf = 128;
    matlabbatch{9}.spm.stats.fmri_spec.fact = struct('name', {}, 'levels', {});
    matlabbatch{9}.spm.stats.fmri_spec.bases.hrf.derivs = [0 0];
    matlabbatch{9}.spm.stats.fmri_spec.volt = 1;
    matlabbatch{9}.spm.stats.fmri_spec.global = 'None';
    matlabbatch{9}.spm.stats.fmri_spec.mthresh = 0.8;
    matlabbatch{9}.spm.stats.fmri_spec.mask = {''};
    matlabbatch{9}.spm.stats.fmri_spec.cvi = 'AR(1)';
    matlabbatch{10}.spm.stats.fmri_est.spmmat(1) = cfg_dep('fMRI model specification: SPM.mat File', substruct('.','val', '{}',{9}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','spmmat'));
    matlabbatch{10}.spm.stats.fmri_est.write_residuals = 1;
    matlabbatch{10}.spm.stats.fmri_est.method.Classical = 1;
    matlabbatch{11}.spm.stats.con.spmmat(1) = cfg_dep('Model estimation: SPM.mat File', substruct('.','val', '{}',{10}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','spmmat'));
    matlabbatch{11}.spm.stats.con.consess{1}.tcon.name = 'left_hand';
    matlabbatch{11}.spm.stats.con.consess{1}.tcon.weights = [1 -1 -1 -1 -1];
    matlabbatch{11}.spm.stats.con.consess{1}.tcon.sessrep = 'sess';
    matlabbatch{11}.spm.stats.con.consess{2}.tcon.name = 'right_hand';
    matlabbatch{11}.spm.stats.con.consess{2}.tcon.weights = [-1 1 -1 -1 -1];
    matlabbatch{11}.spm.stats.con.consess{2}.tcon.sessrep = 'sess';
    matlabbatch{11}.spm.stats.con.consess{3}.tcon.name = 'left_foot';
    matlabbatch{11}.spm.stats.con.consess{3}.tcon.weights = [-1 -1 1 -1 -1];
    matlabbatch{11}.spm.stats.con.consess{3}.tcon.sessrep = 'sess';
    matlabbatch{11}.spm.stats.con.consess{4}.tcon.name = 'right_foot';
    matlabbatch{11}.spm.stats.con.consess{4}.tcon.weights = [-1 -1 -1 1 -1];
    matlabbatch{11}.spm.stats.con.consess{4}.tcon.sessrep = 'sess';
    matlabbatch{11}.spm.stats.con.consess{5}.tcon.name = 'tongue';
    matlabbatch{11}.spm.stats.con.consess{5}.tcon.weights = [-1 -1 -1 -1 1];
    matlabbatch{11}.spm.stats.con.consess{5}.tcon.sessrep = 'sess';
    matlabbatch{11}.spm.stats.con.delete = 0;

    matlabbatch{12}.spm.stats.results.spmmat = {[pathToParticipants '/' subject '\1stlevel\SPM.mat']};
    matlabbatch{12}.spm.stats.results.conspec.titlestr = '';
    matlabbatch{12}.spm.stats.results.conspec.contrasts = Inf;
    matlabbatch{12}.spm.stats.results.conspec.threshdesc = 'none';
    matlabbatch{12}.spm.stats.results.conspec.thresh = 0.01;
    matlabbatch{12}.spm.stats.results.conspec.extent = 0;
    matlabbatch{12}.spm.stats.results.conspec.conjunction = 1;
    matlabbatch{12}.spm.stats.results.conspec.mask.none = 1;
    matlabbatch{12}.spm.stats.results.units = 1;
    matlabbatch{12}.spm.stats.results.export{1}.binary.basename = 'allClusters';

    spm('defaults', 'FMRI');
    spm_jobman('run', matlabbatch);
end