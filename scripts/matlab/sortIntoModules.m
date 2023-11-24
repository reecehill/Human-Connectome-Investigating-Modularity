function [modules, Q1] = sortIntoModules(adjacencyMatrix, gamma)
 addpath('toolboxes/FieldTrip/');
 ft_defaults;
 ft_hastoolbox('bct',1);
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