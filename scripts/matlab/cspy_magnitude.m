function [] = cspy_magnitude(varargin)
%CSPY Visualize sparsity pattern with dynamic marker sizes.
%   Modified to scale MarkerSize based on the magnitude of matrix values.

if nargin == 0
    return;
end
islevels = 0;
levels = 0;
MAP = 0;
markerSize = 0;
marker = 0;
ischannels = 0;
xdir = 0;
ydir = 0;

for i=2:2:nargin
    switch(lower(char(varargin(i))))
        case 'marker'
            marker = varargin(i+1);
            if iscell(marker)
                marker = marker{:};
            end
        case 'markersize'
            markerSize = cell2mat(varargin(i+1));
        case 'levels'
            levels = cell2mat(varargin(i+1));
            islevels = 1;
        case 'colormap'
            MAP = char(varargin(i+1));
        case 'channels'
            ischannels = char(varargin(i+1));
        case 'ydir'
            ydir = lower(char(varargin(i+1)));
        case 'xdir'
            xdir = lower(char(varargin(i+1)));
    end
end

matrix = cell2mat(varargin(1));

%% Default values
if ~ischannels || ~strcmp('on', ischannels)
    ischannels = 0;
else
    ischannels = 1;
end

channels = size(matrix, 3);
if ~ischannels
    if channels == 3
        matrix = rgb2gray(matrix);
        channels = 1;
    end
end
plotsdim = ceil(sqrt(channels));
if ~MAP
    MAP = 'lines';
end
if ~markerSize
    markerSize = 10;
end
if isempty(marker) || (~iscell(marker) && ~marker)
    marker = '.';
end

if ~ydir
    ydir = 'reverse';
end

if ~xdir
    xdir = 'normal';
end

if length(levels) > 1 && length(levels) ~= channels
    levels = ceil(mean(levels));
end
%%
for j = 1:channels
    if channels > 1
        matrix2d = matrix(:, :, j);
    else
        matrix2d = matrix;
    end
    if ~nnz(matrix2d)
        continue;
    end
    if channels > 1
        subplot(plotsdim, plotsdim, j);
    end

    [y, x, z] = find(matrix2d);
    minvalue = min(z);
    maxvalue = max(z);

    if ~islevels
        levels = ceil(maxvalue - minvalue + 1);
    end

    if length(levels) > 1
        clevels = levels(j);
    else
        clevels = levels;
    end

    step = (maxvalue - minvalue) / clevels;
    colors = eval(strcat(MAP, '(', num2str(clevels), ')'));

    colormap(colors);
    if size(matrix2d, 1) == size(matrix2d, 2)
        axis square;
    end
    if clevels > 1 && maxvalue - minvalue > 1
        colorbar;
        clim([minvalue maxvalue]);
    end

    xlim([1, size(matrix2d, 2)]);
    ylim([1, size(matrix2d, 1)]);
    xlabel(['nz = ' num2str(nnz(matrix2d))])
    hold on;

    % Normalize z values for MarkerSize scaling
    normalizedZ = (z - minvalue) / (maxvalue - minvalue);
    scaledMarkerSize = markerSize * (1 + normalizedZ); % Scale dynamically

for i = 1:clevels
    step_init = minvalue + (i - 1) * step;
    step_end = minvalue + i * step;
    if i == clevels
        ids = find(z >= step_init & z <= step_end);
    else
        ids = find(z >= step_init & z < step_end);
    end
    if length(marker) == clevels
        cmarker = char(marker(i));
    else
        cmarker = char(marker(1));
    end

    % Plot each point individually to scale MarkerSize dynamically
    for k = 1:length(ids)
        plot(x(ids(k)), y(ids(k)), cmarker, 'MarkerSize', scaledMarkerSize(ids(k)), 'Color', colors(i, :));
        hold on;
    end

    set(gca, 'XDir', xdir);
    set(gca, 'YDir', ydir);
    set(gca, 'XAxisLocation', 'top');
end
end

end
