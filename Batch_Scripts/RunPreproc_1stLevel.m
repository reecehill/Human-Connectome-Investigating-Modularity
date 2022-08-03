function RunPreproc_1stLevel(pathToParticipants, subject)
    % List of open inputs
    nrun = 1; % enter the number of runs here
    jobfile = {'D:\Dissertation\RunPreproc_1stLevel_job.m'};
    input = {pathToParticipants; subject};
    jobs = repmat(jobfile, 1, nrun);
    inputs = repmat(input, nrun);
    for crun = 1:nrun
    end
    spm('defaults', 'FMRI');
    spm_jobman('run', jobs, inputs{:});
end