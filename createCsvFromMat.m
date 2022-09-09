function createCsvFromMat(pathToParticipants, subject)
clearvars -except pathToParticipants subject
addpath('../');
SPM = load([pathToParticipants '/' subject '/1stlevel/SPM.mat']);
nConditions = length(SPM.SPM.xCon);

for conditionIndex=[1:nConditions]
    clearvars -except pathToParticipants subject conditionIndex
    load([pathToParticipants '/' subject '/moduleResults/collectionOfMetrics__' num2str(conditionIndex) '.mat'])

    %% Left AND right hemisphere
    if(~isempty(leftCollectionOfMetrics))
    [leftCollectionOfMetrics(:).subjectId] = deal(subject);
    end
    if(~isempty(rightCollectionOfMetrics))
    [rightCollectionOfMetrics(:).subjectId] = deal(subject);
    end

    % Convert struct to table, but drop the faceIdsOfOverlap.
    table = [leftCollectionOfMetrics rightCollectionOfMetrics];
    if(~isempty(table))
    [table(:).faceIdsOfOverlap]= deal([]);
    
    writetable(struct2table(table, "AsArray",true), [pathToParticipants '/' subject '/moduleResults/collectionOfMetrics_' num2str(conditionIndex) '.csv']);
    
    writetable(struct2table(table, "AsArray",true), [pathToParticipants '/allSubjectsCollectionOfMetrics_' num2str(conditionIndex) '.csv'], "WriteMode","append");

    %writetable(struct2table(table), [pathToParticipants '/' subject '/moduleResults/collectionOfMetrics_' num2str(conditionIndex) '.csv'])
    end
end
end