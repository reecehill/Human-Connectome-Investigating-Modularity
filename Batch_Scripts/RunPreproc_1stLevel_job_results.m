function RunPreproc_1stLevel_job_results(pathToParticipants, subject)
addpath 'C:\Users\Reece\Documents\Dissertation\Main\Batch_Scripts';
addpath 'C:\Users\Reece\Documents\Dissertation\Main';
addpath(genpath('C:\Program Files\MATLAB\R2021b\spm12'));
close all;
clearvars -except pathToParticipants subject;
try

        %% Define fMRI model
     if ~exist([pathToParticipants '/' subject '/1stlevel/SPM.mat'], 'file')
             matlabbatch{1}.spm.stats.fmri_spec.dir = {[pathToParticipants '/' subject '\1stlevel']};
    matlabbatch{1}.spm.stats.fmri_spec.timing.units = 'secs';
    matlabbatch{1}.spm.stats.fmri_spec.timing.RT = 2;
    matlabbatch{1}.spm.stats.fmri_spec.timing.fmri_t = 16;
    matlabbatch{1}.spm.stats.fmri_spec.timing.fmri_t0 = 8;
    matlabbatch{1}.spm.stats.fmri_spec.sess.scans = {[pathToParticipants '/' subject '/data/func/sartask-HcpMotor_acq-ap_bold.nii']};

    % LEFT HAND
    matlabbatch{1}.spm.stats.fmri_spec.sess.cond(1).name = 'left_hand';
    leftHandTimingFile = importdata([pathToParticipants '/' subject '\data\func\timing_files\left_hand.txt']);
    matlabbatch{1}.spm.stats.fmri_spec.sess.cond(1).onset = leftHandTimingFile(:,1);
    matlabbatch{1}.spm.stats.fmri_spec.sess.cond(1).duration = leftHandTimingFile(:,2);
    matlabbatch{1}.spm.stats.fmri_spec.sess.cond(1).tmod = 0;
    matlabbatch{1}.spm.stats.fmri_spec.sess.cond(1).pmod = struct('name', {}, 'param', {}, 'poly', {});
    matlabbatch{1}.spm.stats.fmri_spec.sess.cond(1).orth = 1;

    % RIGHT HAND
    matlabbatch{1}.spm.stats.fmri_spec.sess.cond(2).name = 'right_hand';
    rightHandTimingFile = importdata([pathToParticipants '/' subject '\data\func\timing_files\right_hand.txt']);
    matlabbatch{1}.spm.stats.fmri_spec.sess.cond(2).onset = rightHandTimingFile(:,1);
    matlabbatch{1}.spm.stats.fmri_spec.sess.cond(2).duration = rightHandTimingFile(:,2);
    matlabbatch{1}.spm.stats.fmri_spec.sess.cond(2).tmod = 0;
    matlabbatch{1}.spm.stats.fmri_spec.sess.cond(2).pmod = struct('name', {}, 'param', {}, 'poly', {});
    matlabbatch{1}.spm.stats.fmri_spec.sess.cond(2).orth = 1;

    % LEFT FOOT
    matlabbatch{1}.spm.stats.fmri_spec.sess.cond(3).name = 'left_foot';
    leftFootTimingFile = importdata([pathToParticipants '/' subject '\data\func\timing_files\left_foot.txt']);
    matlabbatch{1}.spm.stats.fmri_spec.sess.cond(3).onset = leftFootTimingFile(:,1);
    matlabbatch{1}.spm.stats.fmri_spec.sess.cond(3).duration = leftFootTimingFile(:,2);
    matlabbatch{1}.spm.stats.fmri_spec.sess.cond(3).tmod = 0;
    matlabbatch{1}.spm.stats.fmri_spec.sess.cond(3).pmod = struct('name', {}, 'param', {}, 'poly', {});
    matlabbatch{1}.spm.stats.fmri_spec.sess.cond(3).orth = 1;

    % RIGHT FOOT
    matlabbatch{1}.spm.stats.fmri_spec.sess.cond(4).name = 'right_foot';
    rightFootTimingFile = importdata([pathToParticipants '/' subject '\data\func\timing_files\right_foot.txt']);
    matlabbatch{1}.spm.stats.fmri_spec.sess.cond(4).onset = rightFootTimingFile(:,1);
    matlabbatch{1}.spm.stats.fmri_spec.sess.cond(4).duration = rightFootTimingFile(:,2);
    matlabbatch{1}.spm.stats.fmri_spec.sess.cond(4).tmod = 0;
    matlabbatch{1}.spm.stats.fmri_spec.sess.cond(4).pmod = struct('name', {}, 'param', {}, 'poly', {});
    matlabbatch{1}.spm.stats.fmri_spec.sess.cond(4).orth = 1;

    % TONGUE
    matlabbatch{1}.spm.stats.fmri_spec.sess.cond(5).name = 'tongue';
    tongueTimingFile = importdata([pathToParticipants '/' subject '\data\func\timing_files\tongue.txt']);
    matlabbatch{1}.spm.stats.fmri_spec.sess.cond(5).onset = tongueTimingFile(:,1);
    matlabbatch{1}.spm.stats.fmri_spec.sess.cond(5).duration = tongueTimingFile(:,2);
    matlabbatch{1}.spm.stats.fmri_spec.sess.cond(5).tmod = 0;
    matlabbatch{1}.spm.stats.fmri_spec.sess.cond(5).pmod = struct('name', {}, 'param', {}, 'poly', {});
    matlabbatch{1}.spm.stats.fmri_spec.sess.cond(5).orth = 1;

    % MISC.
    matlabbatch{1}.spm.stats.fmri_spec.sess.multi = {''};
    matlabbatch{1}.spm.stats.fmri_spec.sess.regress = struct('name', {}, 'val', {});
    matlabbatch{1}.spm.stats.fmri_spec.sess.multi_reg = {''};
    matlabbatch{1}.spm.stats.fmri_spec.sess.hpf = 128;
    matlabbatch{1}.spm.stats.fmri_spec.fact = struct('name', {}, 'levels', {});
    matlabbatch{1}.spm.stats.fmri_spec.bases.hrf.derivs = [0 0];
    matlabbatch{1}.spm.stats.fmri_spec.volt = 1;
    matlabbatch{1}.spm.stats.fmri_spec.global = 'None';
    matlabbatch{1}.spm.stats.fmri_spec.mthresh = 0.8;
    matlabbatch{1}.spm.stats.fmri_spec.mask = {''};
    matlabbatch{1}.spm.stats.fmri_spec.cvi = 'AR(1)';
     else
                 matlabbatch{1}.cfg_basicio.run_ops.call_matlab.inputs{1}.evaluated = 'Skipped a module.';
        matlabbatch{1}.cfg_basicio.run_ops.call_matlab.outputs = {};
        matlabbatch{1}.cfg_basicio.run_ops.call_matlab.fun = 'display';
     end

    %% Estimate fMRI model
    matlabbatch{2}.spm.stats.fmri_est.spmmat(1) = {[pathToParticipants '/' subject '/1stlevel/SPM.mat']};
    matlabbatch{2}.spm.stats.fmri_est.write_residuals = 0;
    matlabbatch{2}.spm.stats.fmri_est.method.Classical = 1;

    %% Contrast manager
    matlabbatch{3}.spm.stats.con.spmmat(1) = cfg_dep('Model estimation: SPM.mat File', substruct('.','val', '{}',{2}, '.','val', '{}',{2}, '.','val', '{}',{2}), substruct('.','spmmat'));
    matlabbatch{3}.spm.stats.con.consess{1}.tcon.name = 'left_hand';
    matlabbatch{3}.spm.stats.con.consess{1}.tcon.weights = [1 0 0 0 0]; %[1 -1 -1 -1 -1]
    matlabbatch{3}.spm.stats.con.consess{1}.tcon.sessrep = 'sess';
    matlabbatch{3}.spm.stats.con.consess{2}.tcon.name = 'right_hand';
    matlabbatch{3}.spm.stats.con.consess{2}.tcon.weights = [0 1 0 0 0]; %[-1 1 -1 -1 -1]
    matlabbatch{3}.spm.stats.con.consess{2}.tcon.sessrep = 'sess';
    matlabbatch{3}.spm.stats.con.consess{3}.tcon.name = 'left_foot';
    matlabbatch{3}.spm.stats.con.consess{3}.tcon.weights = [0 0 1 0 0]; %[-1 -1 1 -1 -1]
    matlabbatch{3}.spm.stats.con.consess{3}.tcon.sessrep = 'sess';
    matlabbatch{3}.spm.stats.con.consess{4}.tcon.name = 'right_foot';
    matlabbatch{3}.spm.stats.con.consess{4}.tcon.weights = [0 0 0 1 0]; %[-1 -1 -1 1 -1]
    matlabbatch{3}.spm.stats.con.consess{4}.tcon.sessrep = 'sess';
    matlabbatch{3}.spm.stats.con.consess{5}.tcon.name = 'tongue';
    matlabbatch{3}.spm.stats.con.consess{5}.tcon.weights = [0 0 0 0 1]; %[-1 -1 -1 -1 1]
    matlabbatch{3}.spm.stats.con.consess{5}.tcon.sessrep = 'sess';
    matlabbatch{3}.spm.stats.con.delete = 0;

    %% Normalise the coregistered mask to MNI space (for use in results report).
    %     matlabbatch{3}.spm.spatial.normalise.write.subj.def(1) = cfg_dep('Segment: Forward Deformations', substruct('.','val', '{}',{3}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','fordef', '()',{':'}));
    %     matlabbatch{3}.spm.spatial.normalise.write.subj.resample(1) = {[pathToParticipants '/' subject '\data\bert\mri\rgm.nii,1']};
    %     matlabbatch{3}.spm.spatial.normalise.write.woptions.bb = [-78 -112 -70
    %         78 76 85];
    %     matlabbatch{3}.spm.spatial.normalise.write.woptions.vox = [2 2 2];
    %     matlabbatch{3}.spm.spatial.normalise.write.woptions.interp = 4;
    %     matlabbatch{3}.spm.spatial.normalise.write.woptions.prefix = 'w';
    matlabbatch{4}.cfg_basicio.run_ops.call_matlab.inputs{1}.evaluated = 'Skipped a module.';
    matlabbatch{4}.cfg_basicio.run_ops.call_matlab.outputs = {};
    matlabbatch{4}.cfg_basicio.run_ops.call_matlab.fun = 'display';


    %% Results report
    matlabbatch{5}.spm.stats.results.spmmat = {[pathToParticipants '/' subject '\1stlevel\SPM.mat']};
    matlabbatch{5}.spm.stats.results.conspec.titlestr = '';
    matlabbatch{5}.spm.stats.results.conspec.contrasts = Inf;
    matlabbatch{5}.spm.stats.results.conspec.threshdesc = 'FWE';
    matlabbatch{5}.spm.stats.results.conspec.thresh = 0.05;
    matlabbatch{5}.spm.stats.results.conspec.extent = 0;
    matlabbatch{5}.spm.stats.results.conspec.conjunction = 1;
    matlabbatch{5}.spm.stats.results.conspec.mask.image.name = {[pathToParticipants '/' subject '\data\bert\mri\realigned_precentral_gyrus.nii,1']};
    matlabbatch{5}.spm.stats.results.conspec.mask.image.mtype = 0;
    matlabbatch{5}.spm.stats.results.units = 1;
    matlabbatch{5}.spm.stats.results.export{1}.binary.basename = 'allClustersBinary';

    spm('defaults', 'FMRI');
    spm_jobman('run', matlabbatch);
    sound(sin(1:1000)); pause(0.2); sound(sin(1:1000));
    disp("Performing final step: saving output for next step in pipeline...");
    convertIntensityToCoordinates(pathToParticipants, subject);
    
catch ME
    sound(tan(1:1000)); pause(0.2); sound(tan(1:1000));
    rethrow(ME);
end
end