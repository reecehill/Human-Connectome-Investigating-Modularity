function [strucModules, Q1] = sortIntoModules(adjacencyMatrix, gamma)
    %% attempt module detection
    % Iterative community finetuning.
    % W is the input connection matrix.
    %n  = size(adjacencyMatrix,1);             % number of nodes
    %M  = 1:n;                   % initial community affiliations
    Q0 = -1; Q1 = 0;            % initialize modularity values
    while Q1-Q0>1e-5           % while modularity increases
        Q0 = Q1;                % perform community detection
        [strucModules, Q1] = community_louvain(adjacencyMatrix, gamma);
    end
end