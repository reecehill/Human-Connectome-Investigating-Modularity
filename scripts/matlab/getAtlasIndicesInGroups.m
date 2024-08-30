function [indices] = getAtlasIndicesInGroups(group)
    switch group
        % TODO: Correct the all indices!
        case 'ventricularSystem'
            indices = [14:15,24];
        case 'whiteMatter'
            ventricularSystemIndices = getAtlasIndicesInGroups('ventricularSystem');
            indices = [1:6,27:46,59:999,ventricularSystemIndices];
        case 'cortical'
            indices = [19,20];
        case 'subcortical'
            indices = [7:13,16:18,26:28,47:58,1001:1099,1101:1999,2001:2099,2101:2999];
        case 'unknown'
            indices = [0,21:23,25,1000,2000,3000,4000,1100,2100,3100,4100,11100,12100,13100,14100];
        case 'subColor'
            indices = [7, 8, 10, 11, 12, 13, 16, 17, 18, 26, 46, 47, 49, 50, 51, 52, 53, 54, 58];
        otherwise
            indices = [];
    end
end