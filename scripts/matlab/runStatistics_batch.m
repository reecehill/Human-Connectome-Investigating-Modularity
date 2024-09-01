function runStatistics_batch(pathToParticipants,subject)
    nConditions = 5; %TODO do not hardcode this
    % for conditionIndex=1:nConditions
        calculateOverlap(pathToParticipants,subject,conditionIndex,0);
        %calculateEditDistance(pathToParticipants,subject,conditionIndex);
    end
end