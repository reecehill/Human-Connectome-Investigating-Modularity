function [optimalGamma] = findOptimalGamma(pathToParticipants, subject, adjacencyMatrix, startGamma, endGamma, visualiseData)
strucAxes = [];
randAxes = [];

allGammas = startGamma:0.02:endGamma;
%allIterations = 1:1:25;
allIterations = 1:1:2;
Q_corts = zeros([max(allIterations),1]);
Q_rands = zeros([max(allIterations),1]);
Q_max = zeros([length(allGammas),1]);

%% Create random adjancency matrix.
numberOfEdgesToCreate = nnz(adjacencyMatrix); %number of non-zero elements
densityOfRandomMatrix = numberOfEdgesToCreate / numel(adjacencyMatrix);
adjacencyMatrixDims = size(adjacencyMatrix);
randomAdjacencyMatrix = sprand(adjacencyMatrixDims(1),adjacencyMatrixDims(2), densityOfRandomMatrix);
if(visualiseData)
    figure("Name","Given adjacency matrix");
    strucAxes = plot(0,0);
    figure("Name","Random");
    randAxes = plot(0,0);
end

%% Trial all iterations for cortical data...
%gammaIndex = 1;
for gamma=allGammas
    gammaIndex = gamma == allGammas;
    parfor iterationIndex=allIterations
        disp(['Sorting cortex (ROI) into modules: gamma=' num2str(gamma) ', iteration #' num2str(iterationIndex) '/' num2str(max(allIterations))]);
        Q0 = -1; Q1 = 0;            % initialize modularity values
        while Q1-Q0>1e-5           % while modularity increases
            Q0 = Q1;                % perform community detection
            [~, Q1] = sortIntoModules(adjacencyMatrix, gamma);
            Q_corts(iterationIndex) = Q1;
            if(visualiseData)
                set(strucAxes,'XData',[get(strucAxes,'XData') iterationIndex],'YData',[get(strucAxes,'YData') Q1-Q0]);
                drawnow;
            end

        end

        disp(['Sorting cortex (Random) into modules: gamma=' num2str(gamma) ', iteration #' num2str(iterationIndex) '/' num2str(max(allIterations))]);
        Q0 = -1; Q1 = 0;            % initialize modularity values
        while Q1-Q0>1e-5           % while modularity increases
            Q0 = Q1;                % perform community detection
            [~, Q1] = sortIntoModules(randomAdjacencyMatrix, gamma);
            Q_rands(iterationIndex) = Q1;
            if(visualiseData)
                set(randAxes,'XData',[get(randAxes,'XData') iterationIndex],'YData',[get(randAxes,'YData') Q1-Q0]);
                drawnow;
            end
        end
    end

    Q_corts_mean = mean(Q_corts);
    Q_rand_mean = mean(Q_rands);
    Q_max(gammaIndex) = Q_corts_mean - Q_rand_mean;
    if(visualiseData)
        set(strucAxes,'XData',[0],'YData',[0]);
        set(randAxes,'XData',[0],'YData',[0]);
    end
    %gammaIndex =+ 1;
end

%% Gamma that returned the largest modularity
optimalGamma = allGammas(Q_max == max(Q_max));
end