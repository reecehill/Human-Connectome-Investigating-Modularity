function getImages(pathToParticipants, subject)
close all;
textLabels = {'Left Hand','Right Hand','Left Foot','Right Foot','Tongue'};
if(isequal(subject,'sub-002'))
    subject1='sub-02';
else 
    subject1=subject;
end

newfig=figure;
p = uipanel('Title',['Participant: ' subject1],'FontSize',16,'BackgroundColor','w');
tcl=tiledlayout(p,2,5);

tcl.TileSpacing = 'none';
tcl.Padding = 'loose';
tcl.TileIndexing = 'columnmajor';
for conditionIndex=[1:5]
    %% Get left hemispheric images
    %for conditionIndex=[1:nConditions]
    genFigures(1,conditionIndex) = openfig([pathToParticipants '/' subject '/moduleResults/figures/' num2str(conditionIndex) '/left-precentral-gyrus-struc-and-func.fig']);
    pause(1);
    legend off;
    title(strjoin(string(({'Left precentral gyrus (',textLabels(conditionIndex),')'})),''));
    axis off;
    h = findobj('DisplayName','Left hemisphere');
    if(~isempty(h))
    delete(h(1));
    end
    h = findobj('type','light');
    if(~isempty(h))
    delete(h(:));
    end

    campos([ -559.7636  -52.6982  231.0349]);


    genFigures(2,conditionIndex) = openfig([pathToParticipants '/' subject '/moduleResults/figures/' num2str(conditionIndex) '/right-precentral-gyrus-struc-and-func.fig']);
    pause(1);
    legend off;
    title(strjoin(string(({'Right precentral gyrus (',textLabels(conditionIndex),')'})),''));
    campos([511.1604  -86.3331  344.2961]);
    
    h = findobj('DisplayName','Right hemisphere');
    if(~isempty(h))
    delete(h(1));
    end
    h = findobj('type','light');
    if(~isempty(h))
    delete(h(:));
    end
    
    axis off;
    h= [];
end




for i = 1:numel(genFigures)
    figure(genFigures(i));
    ax= gca;
    ax.Parent=tcl;
    ax.Layout.Tile=i;
    close(genFigures(i));
end

for i=1:length(tcl.Children)
    light(tcl.Children(i), 'Style','infinite','Position',campos(tcl.Children(i)));
    lighting(tcl.Children(i),'gouraud');
    material(tcl.Children(i),'dull');
end
set(gcf, 'Position', get(0, 'Screensize'));
set(gca, 'color', [1 1 0])
print(gcf,[pathToParticipants '/' subject '/moduleResults/figures/all-modules-both-hemispheres.svg'],'-dsvg');
end