function processResults(pathToParticipants)
set(0, 'DefaultLineLineWidth', 2);
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
temp(find(ismember(temp.subjectId,'sub-002')),:).subjectId(:) = {'sub-02'}
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

filteredNStrucModules = [];
filteredNFuncModules = [];

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
    for subjectId=transpose(subjects)
        intersections = temp(find(ismember(temp.subjectId,subjectId) & ismember(temp.condition,conditionIndex)),:);
        [score,intersectionWithHighestScore] = max(intersections.normalisedOverlapsS);
        intersection = intersections(intersectionWithHighestScore,:);
        functionalModuleToGet = intersection.funcModuleId;
        functionalModuleIntersections = temp(find(ismember(temp.subjectId,subjectId) & ismember(temp.condition,conditionIndex) & ismember(temp.funcModuleId,functionalModuleToGet)),:);
        countingStrucModules.subjectId = subjectId;
        countingStrucModules.qty = length(unique(functionalModuleIntersections.strucModuleId));
        countingStrucModules.conditionIndex = conditionIndex;
        filteredNStrucModules = [filteredNStrucModules; countingStrucModules];
        
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

figure;boxplot(nFmriByCondition,'Colors',"b","Labels",["Left Hand", "Right Hand", "Left Foot", "Right Foot", "Tongue"]);title("Distribution of quantity of functional and structural modules");
hold on;plot(NaN,NaN,'DisplayName','Functional (f_y)','Color',"b");plot(NaN,NaN,'DisplayName','Structural (s_x)','Color',"r");
legend;boxplot(nStrucByCondition,'Widths',0.2,'Colors',"r","Labels",["Left Hand", "Right Hand", "Light Foot", "Right Foot", "Tongue"]);
ylabel('Number of modules');
savefig(gcf,[pathToParticipants '/figures/nFmriAndStrucModulesPerCondition'],'compact');

textLabels = ["(1) Left Hand", "(2) Right Hand", "(3) Left Foot", "(4) Right Foot", "(5) Tongue"];
meanQty = groupsummary(struct2table(filteredNStrucModules).qty,struct2table(filteredNStrucModules).conditionIndex,'mean');
figure;title("Distribution of number of structural modules per motor task")
boxchart(categorical(textLabels([filteredNStrucModules.conditionIndex])),[filteredNStrucModules.qty],'HandleVisibility','off');
hold on;
rectangle('Position',[0,0,1.5,10],'FaceColor',[0.9 0.9 0.9],'EdgeColor','none','HandleVisibility','off');
rectangle('Position',[1.5,0,1,10], 'FaceColor',[0.99 0.99 0.99],'EdgeColor','none','HandleVisibility','off');
rectangle('Position',[2.5,0,1,10],'FaceColor',[0.9 0.9 0.9],'EdgeColor','none','HandleVisibility','off');
rectangle('Position',[3.5,0,1,10], 'FaceColor',[0.99 0.99 0.99],'EdgeColor','none','HandleVisibility','off');
rectangle('Position',[4.5,0,1,10],'FaceColor',[0.9 0.9 0.9],'EdgeColor','none','HandleVisibility','off');
boxchart(categorical(textLabels([filteredNStrucModules.conditionIndex])),[filteredNStrucModules.qty],'DisplayName','Data');
set(gca,'FontSize',16);
xlim([categorical(textLabels(1)), categorical(textLabels(5))]);
ylabel('Number of structural modules');
hold on
plot(meanQty,'-o','DisplayName','Mean')
hold off
legend;
savefig(gcf,[pathToParticipants '/figures/nFmriModulesAllConditions'],'compact');


figure;boxplot(nFmriModules);title("Distribution of number of fMRI modules per subject (conditions combined).")
savefig(gcf,[pathToParticipants '/figures/nFmriModulesAllConditions'],'compact');

figure;boxplot(nStrucModules);title("Distribution of number of structural modules per subject (conditions combined)")
savefig(gcf,[pathToParticipants '/figures/nStrucModulesAllConditions'],'compact');


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

%ALL MOTOR TASKS JOINED
figure;
title('Weighted mean coverage of f_* over s_x for all motor tasks');
label = categorical(repmat({'All'},size(weightedMeanOverlapTable)));
mean1 = mean([weightedMeanOverlapTable.meanOverlap]);
std1 = std([weightedMeanOverlapTable.meanOverlap]);
n = length([weightedMeanOverlapTable.meanOverlap]);


boxchart(label,[weightedMeanOverlapTable.meanOverlap],'HandleVisibility','off');
hold on;
rectangle('Position',[0,0,1.5,1],'FaceColor',[0.99 0.99 0.99],'EdgeColor','none','HandleVisibility','off');
boxchart(label,[weightedMeanOverlapTable.meanOverlap],'DisplayName','Data');
errorbar(mean1,std1./sqrt(n),'vertical','-o','LineWidth',3,'DisplayName','Mean');
set(gca,'FontSize',16);
legend;
ylabel(['Normalised overlap of $f_*$ and $s_x$','( $\overline {i}$ )'],'interpreter','latex','fontsize',15);
xlim([label(1), label(end)]);
ylim([0, 1]);


meanOverlap = groupsummary(struct2table(weightedMeanOverlapTable).meanOverlap,struct2table(weightedMeanOverlapTable).conditionIndex,'mean');
stdOverlap = groupsummary(struct2table(weightedMeanOverlapTable).meanOverlap,struct2table(weightedMeanOverlapTable).conditionIndex,'std');
n = groupsummary(struct2table(weightedMeanOverlapTable).meanOverlap,struct2table(weightedMeanOverlapTable).conditionIndex,'nnz');

figure; hold on; ylabel(['Normalised overlap of $f_*$ and $s_x$','( $\overline {i}$ )'],'interpreter','latex','fontsize',15);
title('Weighted mean coverage of f_* over s_x per motor task');
boxchart(categorical(textLabels([weightedMeanOverlapTable.conditionIndex])),[weightedMeanOverlapTable.meanOverlap],'HandleVisibility','off');
hold on;
rectangle('Position',[0,0,1.5,1],'FaceColor',[0.9 0.9 0.9],'EdgeColor','none','HandleVisibility','off');
rectangle('Position',[1.5,0,1,1], 'FaceColor',[0.99 0.99 0.99],'EdgeColor','none','HandleVisibility','off');
rectangle('Position',[2.5,0,1,1],'FaceColor',[0.9 0.9 0.9],'EdgeColor','none','HandleVisibility','off');
rectangle('Position',[3.5,0,1,1], 'FaceColor',[0.99 0.99 0.99],'EdgeColor','none','HandleVisibility','off');
rectangle('Position',[4.5,0,1,1],'FaceColor',[0.9 0.9 0.9],'EdgeColor','none','HandleVisibility','off');
boxchart(categorical(textLabels([weightedMeanOverlapTable.conditionIndex])),[weightedMeanOverlapTable.meanOverlap]);

%plot(meanOverlap, '-o');
errorbar(meanOverlap,stdOverlap./sqrt(n),'vertical','-o','LineWidth',3);
set(gca,'FontSize',16);
xlim([categorical(textLabels(1)), categorical(textLabels(5))]);

hold off
legend(["Data","Mean"]);
savefig(gcf,[pathToParticipants '/figures/weightedmeancoverage-fstar-sx-by-condition'],'compact');

meanF_y = groupsummary(temp.C,temp.condition,'mean');
meanS_x = groupsummary(temp.A,temp.condition,'mean');

figure; hold on; ylabel(['Size of all functional modules (mm)',' ( ${f_y}$ )'],'interpreter','latex','fontsize',15);
title('Size of all f_y per motor task');
boxchart(categorical(textLabels([temp.condition])),[temp.C]);
hold on;
plot(meanF_y, '-o');
hold off
legend(["Data","Mean"]);
savefig(gcf,[pathToParticipants '/figures/mean-f_y-distribution'],'compact');

rowsOfA.valuesToPlot = temp.A;
rowsOfA.condition = temp.condition;
rowsOfA.type = 's_x';
rowsOfC.valuesToPlot = temp.C;
rowsOfC.condition = temp.condition;
rowsOfC.type = 'f_y';

meanf_y_n_s_x = groupsummary(temp.overlapArea,temp.condition,'mean');

tableOfAC.valuesToPlot = [temp.A; temp.C; temp.overlapArea];
types = [repmat({'s_x'},length(temp.A),1); repmat({'f_y'},length(temp.C),1); repmat({'(s_x \cap  f_y)'},length(temp.overlapArea),1)];
tableOfAC.types = types;
tableOfAC.conditions = [temp.condition; temp.condition; temp.condition];
figure; hold on; ylabel(['Surface area size (mm^2)'],'fontsize',15);
title('Size of all modules per motor task');
boxchart(categorical(textLabels([tableOfAC.conditions])),[tableOfAC.valuesToPlot],'GroupByColor',[tableOfAC.types],'HandleVisibility','off');
hold on;
rectangle('Position',[0.05,1,1.5,10^4],'FaceColor',[0.9 0.9 0.9],'EdgeColor','none','HandleVisibility','off');
rectangle('Position',[1.5,1,1.5,10^4], 'FaceColor',[0.99 0.99 0.99],'EdgeColor','none','HandleVisibility','off');
rectangle('Position',[2.5,1,1.5,10^4],'FaceColor',[0.9 0.9 0.9],'EdgeColor','none','HandleVisibility','off');
rectangle('Position',[3.5,1,1.5,10^4], 'FaceColor',[0.99 0.99 0.99],'EdgeColor','none','HandleVisibility','off');
rectangle('Position',[4.5,1,1.5,10^4],'FaceColor',[0.9 0.9 0.9],'EdgeColor','none','HandleVisibility','off');
boxchart(categorical(textLabels([tableOfAC.conditions])),[tableOfAC.valuesToPlot],'GroupByColor',[tableOfAC.types]);
xlim([categorical(textLabels(1)), categorical(textLabels(5))]);

plot([1,2,3,4,5],meanF_y, '-o','DisplayName','Mean f_y');
plot([1,2,3,4,5]+(1/3),meanS_x, '-o','DisplayName','Mean s_x');
plot([1,2,3,4,5]-(1/3),meanf_y_n_s_x, '-o','DisplayName','Mean (s_x \cap f_y)');
plot([1,2,3,4,5]-(1/3),meanf_y_n_s_x.*meanQty, '-.o','DisplayName','Mean (s_x \cap f_y)_{scaled}');
set(gca, 'YScale', 'log');
set(gca,'FontSize',16);
lgd = legend;
lgd.Location = 'north';
lgd.Orientation = 'horizontal';
savefig(gcf,[pathToParticipants '/figures/mean-s_x-and-f_y-distribution'],'compact');

figure; hold on; ylabel(['Size of all structural modules (mm)',' ( ${s_x}$ )'],'interpreter','latex','fontsize',15);
title('Size of all s_x per motor task');
boxchart(categorical(textLabels([temp.condition])),[temp.A]);
hold on;
plot(meanS_x, '-o');
hold off
legend(["Data","Mean"]);
savefig(gcf,[pathToParticipants '/figures/mean-s_x-distribution'],'compact');

meanOverlapBySubject = groupsummary(struct2table(weightedMeanOverlapTable).meanOverlap,struct2table(weightedMeanOverlapTable).subjectId,'mean');
figure; hold on; ylabel(['Normalised overlap of $f_*$ and $s_x$','( $\overline {i}$ )'],'interpreter','latex','fontsize',15);
title('Weighted mean coverage of f_* over s_x per subject');
boxchart(categorical([weightedMeanOverlapTable.subjectId]),[weightedMeanOverlapTable.meanOverlap]);
hold on;
plot(meanOverlapBySubject, '-o');
hold off
legend(["Data","Mean"]);
savefig(gcf,[pathToParticipants '/figures/weightedmeancoverage-fstar-sx-by-subject'],'compact');


allOverlapsBySubject = groupsummary(temp.normalisedOverlapsS,temp.condition,'mean');
figure; hold on; ylabel(['Normalised overlap of $f_y$ and $s_x$','( $i$ )'],'interpreter','latex','fontsize',15);
title('All coverage of f_y over s_x per subject by condition');
boxchart(categorical(textLabels([temp.condition])),[temp.normalisedOverlapsS], 'GroupByColor',temp.subjectId,'HandleVisibility','off');
hold on;
rectangle('Position',[0,0,1.5,1],'FaceColor',[0.9 0.9 0.9],'EdgeColor','none','HandleVisibility','off');
rectangle('Position',[1.5,0,1,1], 'FaceColor',[0.99 0.99 0.99],'EdgeColor','none','HandleVisibility','off');
rectangle('Position',[2.5,0,1,1],'FaceColor',[0.9 0.9 0.9],'EdgeColor','none','HandleVisibility','off');
rectangle('Position',[3.5,0,1,1], 'FaceColor',[0.99 0.99 0.99],'EdgeColor','none','HandleVisibility','off');
rectangle('Position',[4.5,0,1,1],'FaceColor',[0.9 0.9 0.9],'EdgeColor','none','HandleVisibility','off');
boxchart(categorical(textLabels([temp.condition])),[temp.normalisedOverlapsS], 'GroupByColor',temp.subjectId);
plot(allOverlapsBySubject, '-o','DisplayName','Task mean');
xlim([categorical(textLabels(1)), categorical(textLabels(5))]);
%Add plot of f_* i values
plot(meanOverlap,'-s','DisplayName','Task mean (optimised, f_* )');

hold off
legend;
savefig(gcf,[pathToParticipants '/figures/all-coverage-fy-sx-per-subject-by-condition'],'compact');

allOverlapsByCondition = groupsummary(temp.normalisedOverlapsS,temp.subjectId,'mean');
figure; hold on; ylabel(['Normalised overlap of $f_y$ and $s_x$','( $i$ )'],'interpreter','latex','fontsize',15);
title('All coverage of f_y over s_x per condition by subject');
boxchart(categorical(temp.subjectId),[temp.normalisedOverlapsS], 'GroupByColor',categorical(textLabels([temp.condition])),'HandleVisibility','off');
hold on;
rectangle('Position',[0,0,1.5,1],'FaceColor',[0.9 0.9 0.9],'EdgeColor','none','HandleVisibility','off');
rectangle('Position',[1.5,0,1,1], 'FaceColor',[0.99 0.99 0.99],'EdgeColor','none','HandleVisibility','off');
rectangle('Position',[2.5,0,1,1],'FaceColor',[0.9 0.9 0.9],'EdgeColor','none','HandleVisibility','off');
rectangle('Position',[3.5,0,1,1], 'FaceColor',[0.99 0.99 0.99],'EdgeColor','none','HandleVisibility','off');
rectangle('Position',[4.5,0,1,1],'FaceColor',[0.9 0.9 0.9],'EdgeColor','none','HandleVisibility','off');
rectangle('Position',[5.5,0,1,1], 'FaceColor',[0.99 0.99 0.99],'EdgeColor','none','HandleVisibility','off');
rectangle('Position',[6.5,0,1,1],'FaceColor',[0.9 0.9 0.9],'EdgeColor','none','HandleVisibility','off');
rectangle('Position',[7.5,0,1,1], 'FaceColor',[0.99 0.99 0.99],'EdgeColor','none','HandleVisibility','off');
rectangle('Position',[8.5,0,1,1],'FaceColor',[0.9 0.9 0.9],'EdgeColor','none','HandleVisibility','off');
rectangle('Position',[9.5,0,1,1], 'FaceColor',[0.99 0.99 0.99],'EdgeColor','none','HandleVisibility','off');
rectangle('Position',[10.5,0,1,1],'FaceColor',[0.9 0.9 0.9],'EdgeColor','none','HandleVisibility','off');
rectangle('Position',[11.5,0,1,1], 'FaceColor',[0.99 0.99 0.99],'EdgeColor','none','HandleVisibility','off');
boxchart(categorical(temp.subjectId),[temp.normalisedOverlapsS], 'GroupByColor',categorical(textLabels([temp.condition])));
plot(allOverlapsByCondition, '-o','DisplayName','Subject mean');

%Add plot of f_* i values
plot(meanOverlapBySubject,'-s','DisplayName','Subject mean (optimised, f_* )');

xlim([categorical({'sub-01'}), categorical({'sub-14'})]);
hold off
legend;
savefig(gcf,[pathToParticipants '/figures/all-coverage-fy-sx-per-condition-by-subject'],'compact');


scaledmeanf_y_n_s_x_s = meanf_y_n_s_x .* meanQty;
figure; hold on; ylabel(['Size of all intersections (mm)',' ( ${f_y \cap s_x}$ )'],'interpreter','latex','fontsize',15);
title('Size of all (f_y ∩ s_x) per motor task');
boxchart(categorical(textLabels([temp.condition])),[temp.overlapArea], "HandleVisibility","off");
hold on;
rectangle('Position',[0,0,1.5,700],'FaceColor',[0.9 0.9 0.9],'EdgeColor','none','HandleVisibility','off');
rectangle('Position',[1.5,0,1,700], 'FaceColor',[0.99 0.99 0.99],'EdgeColor','none','HandleVisibility','off');
rectangle('Position',[2.5,0,1,700],'FaceColor',[0.9 0.9 0.9],'EdgeColor','none','HandleVisibility','off');
rectangle('Position',[3.5,0,1,700], 'FaceColor',[0.99 0.99 0.99],'EdgeColor','none','HandleVisibility','off');
rectangle('Position',[4.5,0,1,700],'FaceColor',[0.9 0.9 0.9],'EdgeColor','none','HandleVisibility','off');
boxchart(categorical(textLabels([temp.condition])),[temp.overlapArea]);

plot(meanf_y_n_s_x, '-o');
plot(scaledmeanf_y_n_s_x_s, '-s');
hold off
legend(["Data","Mean","Scaled Mean"]);
savefig(gcf,[pathToParticipants '/figures/f_y_n_s_x-distribution'],'compact');





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



