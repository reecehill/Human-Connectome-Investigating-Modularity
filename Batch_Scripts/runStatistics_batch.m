function runStatistics_batch(pathToParticipants)
addpath('../');
subjects = { 'sub-01', 'sub-002', 'sub-04','sub-05','sub-06','sub-07','sub-08','sub-09','sub-11','sub-12','sub-13','sub-14'};
for n=1:length(subjects)
    subject = subjects(n);
    subject = subject{1};
    SPM = load([pathToParticipants '/' subject '/1stlevel/SPM.mat']);
    nConditions = length(SPM.SPM.xCon);

    

    for conditionIndex=[1:nConditions]
        %calculateOverlap(pathToParticipants,subject,conditionIndex,0);
        calculateEditDistance(pathToParticipants,subject,conditionIndex);
    end

end
end