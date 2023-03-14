function updatedProcessResults(pathToParticipants)
if ~exist([pathToParticipants '\figures'],'dir')
    mkdir([pathToParticipants '\figures']);
end
close all;
subject = 'sub-01';

addpath('../');
SPM = load([pathToParticipants '/' subject '/1stlevel/SPM.mat']);
%nConditions = length(SPM.SPM.xCon);
nConditions = 5;

%% Append all results into one file.
delete([ pathToParticipants '/allSubjectsAndConditionsCollectionOfMetrics.csv']);
for conditionIndex=[1:nConditions]
    table = readtable([pathToParticipants '/allSubjectsCollectionOfMetrics_' num2str(conditionIndex) '.csv']);
    table.condition(:) = deal(conditionIndex);
    writetable(table, [pathToParticipants '/allSubjectsAndConditionsCollectionOfMetrics.csv'], "WriteMode","append");
end

temp = readtable([pathToParticipants '/allSubjectsAndConditionsCollectionOfMetrics.csv']);
results{1,conditionIndex} = temp;

% Results grouped
groupBySubjectAndCondition = findgroups(temp.subjectId, temp.condition);
temp.groupBySubjectAndCondition(:) = groupBySubjectAndCondition;
groupBySubject = findgroups(temp.subjectId);
temp.groupBySubject(:) = groupBySubject;

%% Add variables for normalisation
% B is same as AnC (aka intersection);
Bs = temp(:,:).overlapArea; %in mm
Cs = (Bs./temp(:,:).areaOverlapAsPercentOfFunc).*1; %in mm
As = (Bs./temp(:,:).areaOverlapAsPercentOfStruc).*1; %in mm
AuCs = (As+Cs)-Bs;
temp.A = As;
temp.C = Cs;
temp.AuC = AuCs;
% Overlap score (1=complete overlap)
overlapScores = Bs./AuCs;
normalisedOverlapsS = Bs./As;
normalisedOverlapsF = Bs./Cs;
temp.overlapScores = overlapScores;
temp.normalisedOverlapsS = normalisedOverlapsS;
temp.normalisedOverlapsF = normalisedOverlapsF;
temp.id(:) = [1:1:size(temp,1)];
%% Per subject processing
nFmriModules = [];
nStrucModules = [];
normalisedCoveragesBySubject = [];
overlapAreaBySubject = [];
normalisedCoveragesBySubject = [];
subjects = unique(temp.subjectId);
nSubjects = length(subjects);
for subject=1:nSubjects
    idsWithSubject{subject} = find(ismember(temp.subjectId,subjects{subject}));
    numberOfFmriModules = length(unique(temp(idsWithSubject{subject},:).funcModuleId));
    numberOfStrucModules = length(unique(temp(idsWithSubject{subject},:).strucModuleId));
    overlapAreas = temp(idsWithSubject{subject},:).overlapArea;
    overlapScores = temp(idsWithSubject{subject},:).overlapScores;
    nFmriModules = [nFmriModules numberOfFmriModules];
    nStrucModules = [nStrucModules numberOfStrucModules];
    overlapAreaBySubject = [padarray(overlapAreaBySubject,max((length(overlapAreas) - length(overlapAreaBySubject)),0), NaN, "post") padarray(overlapAreas,max((length(overlapAreaBySubject) - length(overlapAreas)),0), NaN, "post")];
    normalisedCoveragesBySubject = [padarray(normalisedCoveragesBySubject,max((length(overlapScores) - length(normalisedCoveragesBySubject)),0), NaN, "post") padarray(overlapScores,max((length(normalisedCoveragesBySubject) - length(overlapScores)),0), NaN, "post")];
end

%% Per condition processing
numberOfFmriModulesByCondition = [];
numberOfStrucModulesByCondition = [];
for conditionIndex=1:1:5
    idsWithConditions{conditionIndex} = find(ismember(temp.condition,conditionIndex));
    var = splitapply(@(x1)[length(unique(x1))],temp(idsWithConditions{conditionIndex},:).funcModuleId,findgroups(temp(idsWithConditions{conditionIndex},:).subjectId));
    var1 = padarray(var, nSubjects-length(var),NaN,"post");
    nFmriByCondition(:,conditionIndex) = [numberOfFmriModulesByCondition; var1];
    var = splitapply(@(x1)[length(unique(x1))],temp(idsWithConditions{conditionIndex},:).strucModuleId,findgroups(temp(idsWithConditions{conditionIndex},:).subjectId));
    var1 = padarray(var, nSubjects-length(var),NaN,"post");
    nStrucByCondition(:,conditionIndex) = [numberOfStrucModulesByCondition; var1];
    % For condition X, split it into groups of participants (i.e., nSubjects).
end

%% METHOD ONE
% Select by largest overlapping area for each subject
idsWithMaxB = find(ismember(temp.overlapArea,splitapply(@max,temp.overlapArea,groupBySubjectAndCondition)));
maximalValuesPerConditionForLargestMm = [];
maximalValuesPerConditionForLargestScore = [];
for conditionIndex=[1:nConditions]
    idsWithCondition{conditionIndex} = find(temp.condition==conditionIndex);
    maximalValuesPerSubjectForLargestMm = splitapply(@max,temp(idsWithCondition{conditionIndex},:).overlapArea,findgroups(temp(idsWithCondition{conditionIndex},:).subjectId));
    maximalValuesPerSubjectForLargestScore = splitapply(@(x1,y)[y(find(max(x1)))],temp(idsWithCondition{conditionIndex},:).overlapArea, temp(idsWithCondition{conditionIndex},:).overlapScores,findgroups(temp(idsWithCondition{conditionIndex},:).subjectId));
    maximalValuesPerConditionForLargestMm(:,conditionIndex) = [maximalValuesPerSubjectForLargestMm; zeros(nSubjects-size(maximalValuesPerSubjectForLargestMm,1),1)];
    maximalValuesPerConditionForLargestScore(:,conditionIndex) = [maximalValuesPerSubjectForLargestScore; zeros(nSubjects-size(maximalValuesPerSubjectForLargestScore,1),1)];

end

%% METHOD TWO
idsWithMaxOverlapScoresByParticipantByCondition = find(ismember(temp.overlapScores,splitapply(@max,temp.overlapScores,groupBySubjectAndCondition)));
idsWithMaxOverlapScoresByParticipant = find(ismember(temp.overlapScores,splitapply(@max,temp.overlapScores,groupBySubject)));

%% Coverage by highest overlap score
for conditionIndex=[1:nConditions]
    idsWithCondition{conditionIndex} = find(temp.condition==conditionIndex);
    maximalValues = splitapply(@max,temp(idsWithCondition{conditionIndex},:).overlapScores,findgroups(temp(idsWithCondition{conditionIndex},:).subjectId));
    normalisedCoveragesForAllParticipantsByCondition(:,conditionIndex) = [maximalValues; zeros(nSubjects-size(maximalValues,1),1)];
end
normalisedCoveragesForAllParticipantAndConditions = temp(idsWithMaxOverlapScoresByParticipantByCondition,:).overlapScores;
normalisedCoveragesForAllParticipants =  temp(idsWithMaxOverlapScoresByParticipant,:).overlapScores;

weightedMeanOverlapTable = [];

%% METHOD 3
% Coverage by weighted mean

method3atable = [];
for conditionIndex=[1:nConditions]
    subjects=unique(temp(idsWithCondition{conditionIndex},:).subjectId);
    % METHOD 3A
    % Loop through functional modules, and calculate their mean i. 
    for subjectId=transpose(subjects)
        functionalModuleIds = unique(temp(find(ismember(temp.subjectId,subjectId) & ismember(temp.condition,conditionIndex)),:).funcModuleId);
        method3atablepre = [];
        for funcModuleId=transpose(functionalModuleIds)
            intersections = temp(find(ismember(temp.subjectId,subjectId) & ismember(temp.condition,conditionIndex) & ismember(temp.funcModuleId,funcModuleId)),:);
            i = sum(intersections.normalisedOverlapsS.*intersections.normalisedOverlapsF)/sum(intersections.normalisedOverlapsF);
            method3arow.subjectId = subjectId;
            method3arow.conditionId = conditionIndex;
            method3arow.funcModuleId = funcModuleId;
            method3arow.i = i;
            method3atablepre = [method3atablepre; method3arow];
        end
       % Keep only highest scoring funcModule for each participant and condition.
    highestrow = find(max([method3atablepre(:).i]));
    method3atable = [method3atable; method3atablepre(highestrow)]; 
    end
    
    
    

    %METHOD 3B
    % Select the functional module rowID with the highest score.

    [t,highestScoringFuncModuleIndex] = splitapply(@(subjectIds,intersections,normalisedOverlapsS) max(normalisedOverlapsS),temp(idsWithCondition{conditionIndex},:).subjectId,temp(idsWithCondition{conditionIndex},:).funcModuleId,temp(idsWithCondition{conditionIndex},:).normalisedOverlapsS,findgroups(temp(idsWithCondition{conditionIndex},:).subjectId));
    for subjectId=transpose(subjects)
        intersections = temp(find(ismember(temp.subjectId,subjectId) & ismember(temp.condition,conditionIndex)),:);
        [score,intersectionWithHighestScore] = max(intersections.normalisedOverlapsS);
        intersection = intersections(intersectionWithHighestScore,:);
        functionalModuleToGet = intersection.funcModuleId;
        functionalModuleIntersections = temp(find(ismember(temp.subjectId,subjectId) & ismember(temp.condition,conditionIndex) & ismember(temp.funcModuleId,functionalModuleToGet)),:);
        % Follow diss equations
        numerator = sum(functionalModuleIntersections.normalisedOverlapsS.*functionalModuleIntersections.normalisedOverlapsF);
        denominator = sum(functionalModuleIntersections.normalisedOverlapsF);
        meanOverlap = numerator/denominator;
        row.subjectId = subjectId;
        row.conditionIndex = conditionIndex;
        row.meanOverlap = meanOverlap;
        weightedMeanOverlapTable = [weightedMeanOverlapTable; row];
    end
    weightedMeanOverlapPerCondition(:,conditionIndex) = [weightedMeanOverlapTable(find(ismember([weightedMeanOverlapTable.conditionIndex],conditionIndex))).meanOverlap]
end


%% Graphing
% Distribution of number of modules by condition
figure;boxplot(nStrucByCondition,"Labels",["L Hand", "R Hand", "L Foot", "R Foot", "Tongue"]);title("Distribution of number of structural modules per condition for all subjects.");
savefig(gcf,[pathToParticipants '/figures/nStrucModulesPerCondition'],'compact');
figure;boxplot(nFmriByCondition,"Labels",["L Hand", "R Hand", "L Foot", "R Foot", "Tongue"]);title("Distribution of number of functional modules per condition for all subjects.");
savefig(gcf,[pathToParticipants '/figures/nFmriModulesPerCondition'],'compact');

figure;boxplot(nFmriByCondition,'Colors',"b","Labels",["L Hand", "R Hand", "L Foot", "R Foot", "Tongue"]);title("Distribution of number of functional modules per condition for all subjects.");
hold on;plot(NaN,NaN,'DisplayName','Number of fMRI clusters','Color',"b");plot(NaN,NaN,'DisplayName','Number of Structural modules','Color',"r");
legend;boxplot(nStrucByCondition,'Widths',0.2,'Colors',"r","Labels",["L Hand", "R Hand", "L Foot", "R Foot", "Tongue"]);
savefig(gcf,[pathToParticipants '/figures/nFmriAndStrucModulesPerCondition'],'compact');


figure;boxplot(nFmriModules);title("Distribution of number of fMRI modules per subject (conditions combined).")
savefig(gcf,[pathToParticipants '/figures/nFmriModulesAllConditions'],'compact');

figure;boxplot(nStrucModules);title("Distribution of number of structural modules per subject (conditions combined)")
savefig(gcf,[pathToParticipants '/figures/nStrucModulesAllConditions'],'compact');

figure;boxchart([filteredNStrucModules.conditionIndex],[filteredNStrucModules.qty],"Labels",["L Hand", "R Hand", "L Foot", "R Foot", "Tongue"]);title("Distribution of number of fMRI modules per subject (conditions combined).")
savefig(gcf,[pathToParticipants '/figures/nFmriModulesAllConditions'],'compact');



% Distribution of participant's data
figure;boxplot(overlapAreaBySubject,'Labels',[1:1:nSubjects]);title("Distribution of modules' overlap areas (mm) (per subject per condition; all activations).");
savefig(gcf,[pathToParticipants '/figures/boxplotAllOverlapMmPerCondition'],'compact');

% Method 1
figure;boxplot(temp(idsWithMaxB,:).areaOverlapAsPercentOfStruc);title("Distribution of B/A");hold on;plot(mean(temp(idsWithMaxB,:).areaOverlapAsPercentOfStruc), 'dg')
savefig(gcf,[pathToParticipants '/figures/boxplotAreaOverlapAsPercentOfStruc'],'compact');

figure;boxplot(maximalValuesPerConditionForLargestMm,'Labels',{'1','2','3','4','5'});title("Distribution of modules Bs with largest overlap area (mm) (per subject per condition).")
savefig(gcf,[pathToParticipants '/figures/boxplotHighestOverlapMmPerCondition'],'compact');

figure;boxplot(maximalValuesPerConditionForLargestScore,'Labels',{'1','2','3','4','5'});title("Distribution of modules scores with largest overlap area (mm) (per subject per condition).")
savefig(gcf,[pathToParticipants '/figures/boxplotHighestOverlapScorePerCondition'],'compact');


% Method 2
figure;boxplot(normalisedCoveragesForAllParticipants);ylim([0 1]);title("Distribution of modules that show maximal overlap (with all conditions joined into one per subject)")
savefig(gcf,[pathToParticipants '/figures/boxplotNormalisedMaximalCoverageCombined'],'compact');

figure;boxplot(normalisedCoveragesForAllParticipantAndConditions);ylim([0 1]);title("Distribution of modules that show maximal overlap (maximum is selected per-subject per-condition).")
savefig(gcf,[pathToParticipants '/figures/boxplotNormalisedMaximalCoverageCombinedMaximal'],'compact');

meansForSubjects = mean(normalisedCoveragesForAllParticipantsByCondition,2);
meansForConditions = mean(normalisedCoveragesForAllParticipantsByCondition,1);
labels = { ...
    append("L Hand mean: ",num2str(meansForConditions(1))), ...
    append("R Hand mean: ",num2str(meansForConditions(2))), ...
    append("L Foot mean: ",num2str(meansForConditions(3))), ...
    append("R Foot mean:",num2str(meansForConditions(4))), ...
    append("Tongue mean: ",num2str(meansForConditions(5))) ...
    };

figure;boxplot(normalisedCoveragesForAllParticipantsByCondition,'Labels',{labels});ylim([0 1]);title("Distribution of modules that show maximal overlap (maximum is selected per-subject per-condition).")
savefig(gcf,[pathToParticipants '/figures/boxplotNormalisedMaximalCoverageByCondition'],'compact');

% Method 3b (weighted mean)
%figure;boxplot([weightedMeanOverlapTable(:).meanOverlap]);ylim([0 1]);title("Distribution of modules that show maximal overlap (with all conditions joined into one per subject)")
%savefig(gcf,[pathToParticipants '/figures/boxplotNormalisedMaximalCoverageCombined-method3a'],'compact');

meansForSubjects = mean(weightedMeanOverlapPerCondition,2);
meansForConditions = mean(weightedMeanOverlapPerCondition,1);
labels = { ...
    append("L Hand mean: ",num2str(meansForConditions(1))), ...
    append("R Hand mean: ",num2str(meansForConditions(2))), ...
    append("L Foot mean: ",num2str(meansForConditions(3))), ...
    append("R Foot mean:",num2str(meansForConditions(4))), ...
    append("Tongue mean: ",num2str(meansForConditions(5))) ...
    };

figure;boxplot(weightedMeanOverlapPerCondition,'Labels',{labels});ylim([0 1]);title("**Distribution of modules that show maximal overlap (maximum is selected per-subject per-condition). 3a")
savefig(gcf,[pathToParticipants '/figures/boxplotNormalisedMaximalCoverageByCondition-3a'],'compact');

end



