function [ROIfacevert, filenames, subfilenames, nbROI] = getROIByFaceVertex(pathToFile,subjectId)
    % Function that stores the vertices (or maybe face) location of each anatomical label.
    % NB: Note that subcortical regions are unsupported.

    
    filenames=dir([pathToFile,'/MNINonLinear/',subjectId,'/label/label_type2/']);
    filenames={filenames(3:end).name};
    subfilenames={...
        'lh.cerebellum','lh.thalamus','lh.caudate','lh.putamen','lh.pallidum','lh.amygdala','lh.hippocampus','lh.accumbens',...
        'rh.thalamus','rh.caudate','rh.putamen','rh.pallidum','rh.amygdala','rh.hippocampus','rh.accumbens','rh.cerebellum',...
        'Brain-stem'};
    nbROI=length(filenames);
%     nROISub=length(subfilenames);
    parfor i=1:nbROI
        ROIfacevert(i,1).id=filenames(i);
        ROIfacevert(i,1).faces=importfile([pathToFile,'/MNINonLinear/',subjectId,'/label/label_type2/',filenames{i}]);  
    end
%     parfor i=1:nROISub
%         ROIfacevert(nbROI+i,1).id=subfilenames(i);
%         ROIfacevert(nbROI+i,1).faces=importfile([pathToFile,'/MNINonLinear/',subjectId,'/label/label_type2/',subfilenames{i}]);  
%     end
end