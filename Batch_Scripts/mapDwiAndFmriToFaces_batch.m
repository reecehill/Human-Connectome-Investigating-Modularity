function mapDwiAndFmriToFaces_batch(pathToParticipants, subject)
addpath('../');
SPM = load([pathToParticipants '/' subject '/1stlevel/SPM.mat']);
nConditions = length(SPM.SPM.xCon);
for conditionIndex=[1:nConditions]
    mapDwiAndFmriToFaces(pathToParticipants,subject,conditionIndex,0);
end
end