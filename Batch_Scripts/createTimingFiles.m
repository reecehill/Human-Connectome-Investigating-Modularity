function createTimingFiles(pathToParticipants, subject)

    if ~exist([pathToParticipants '/' subject '/data/func/timing_files'], 'dir')
       mkdir([pathToParticipants '/' subject '/data/func/timing_files'])
    end

% Taken from: https://github.com/andrewjahn/SPM_Scripts/blob/master/convertOnsetTimes.m
% As cited by: https://andysbrainbook.readthedocs.io/en/latest/SPM/SPM_Short_Course/SPM_Statistics/SPM_05_Creating_Timing_Files.html
% %---------------------%
% % Convert Onset Times %
% %---------------------%
% 
% % Converts timing files from BIDS format into a two-column format that can
% % be read by SPM
% 
% % The columns are:
% % 1. Onset (in seconds); and
% % 2. Duration (in seconds
% 
% 
% % Run this script from the directory that contains all of your subjects
% % (i.e., the Flanker directory)
    %cd(['sub-' subject '/func']) % Navigate to the subject's directory

    
    Run1_onsetTimes = tdfread([pathToParticipants '/' subject '/data/func/task-HcpMotor_acq-ap_events.tsv'],"\t"); % Read onset times file
    Run1_onsetTimes.trial_type = string(Run1_onsetTimes.trial_type); % Convert char array to string array, to make logical comparisons easier

    Run1_left_hand = [];
    Run1_right_hand = [];
    Run1_left_foot = [];
    Run1_right_foot = [];
    Run1_tongue = [];

    for i = 1:length(Run1_onsetTimes.onset)
        if strtrim(Run1_onsetTimes.trial_type(i,:)) == 'left_hand'
            Run1_left_hand = [Run1_left_hand; Run1_onsetTimes.onset(i,:) Run1_onsetTimes.duration(i,:)];
        elseif strtrim(Run1_onsetTimes.trial_type(i,:)) == 'right_hand'
            Run1_right_hand = [Run1_right_hand; Run1_onsetTimes.onset(i,:) Run1_onsetTimes.duration(i,:)];
        elseif strtrim(Run1_onsetTimes.trial_type(i,:)) == 'left_foot'
            Run1_left_foot = [Run1_left_foot; Run1_onsetTimes.onset(i,:) Run1_onsetTimes.duration(i,:)];
        elseif strtrim(Run1_onsetTimes.trial_type(i,:)) == 'right_foot'
            Run1_right_foot = [Run1_right_foot; Run1_onsetTimes.onset(i,:) Run1_onsetTimes.duration(i,:)];
        elseif strtrim(Run1_onsetTimes.trial_type(i,:)) == 'tongue'
            Run1_tongue = [Run1_tongue; Run1_onsetTimes.onset(i,:) Run1_onsetTimes.duration(i,:)];
        end
    end




    % Save timing files into text files

    save([pathToParticipants '/' subject '/data/func/timing_files/' 'left_hand.txt'], 'Run1_left_hand', '-ASCII');
    save([pathToParticipants '/' subject '/data/func/timing_files/' 'right_hand.txt'], 'Run1_right_hand', '-ASCII');
    save([pathToParticipants '/' subject '/data/func/timing_files/' 'left_foot.txt'], 'Run1_left_foot', '-ASCII');
    save([pathToParticipants '/' subject '/data/func/timing_files/' 'right_foot.txt'], 'Run1_right_foot', '-ASCII');
    save([pathToParticipants '/' subject '/data/func/timing_files/' 'tongue.txt'], 'Run1_tongue', '-ASCII');

    % Go back to Flanker directory

    % cd ../..

end