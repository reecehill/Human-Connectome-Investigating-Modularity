function [strucModules, Q1, optimalGamma] = sortIntoModules(structuralAdjacencyMatrix, startGamma, endGamma, visualiseData)
strucAxes = [];
randAxes = [];

allGammas = startGamma:0.02:endGamma;
allIterations = 1:1:3;
Q_corts = zeros([max(allIterations),1]);
Q_rands = zeros([max(allIterations),1]);
Q_max = zeros([length(allGammas),1]);

%% Create random adjancency matrix.
numberOfEdgesToCreate = nnz(structuralAdjacencyMatrix); %number of non-zero elements
densityOfRandomMatrix = numberOfEdgesToCreate / numel(structuralAdjacencyMatrix);
structuralAdjacencyMatrixDims = size(structuralAdjacencyMatrix);
randomAdjacencyMatrix = sprand(structuralAdjacencyMatrixDims(1),structuralAdjacencyMatrixDims(2), densityOfRandomMatrix);
if(visualiseData)
    figure("Name","Structural");
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
            [~, Q1] = community_louvain(structuralAdjacencyMatrix, gamma);
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
            [~, Q1] = community_louvain(randomAdjacencyMatrix, gamma);
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

function [modules,Q1] = runLouvainAlgorithm(adjacencyMatrix, gamma)
    disp('Running louvain algorithm...')
    %% attempt module detection
    % Iterative community finetuning.
    % W is the input connection matrix.
    %n  = size(adjacencyMatrix,1);             % number of nodes
    %M  = 1:n;                   % initial community affiliations
    Q0 = -1; Q1 = 0;            % initialize modularity values
    while Q1-Q0>1e-5           % while modularity increases
        Q0 = Q1;                % perform community detection
        [modules, Q1] = community_louvain(adjacencyMatrix, gamma);
    end
end

%% Redo the value for gamma that returned the largest modularity
optimalGamma = allGammas(Q_max == max(Q_max));
[strucModules,Q1] = runLouvainAlgorithm(structuralAdjacencyMatrix,optimalGamma);

end