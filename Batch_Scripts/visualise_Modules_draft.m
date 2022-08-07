clear;
close all;
load('D:\Dissertation\Participants\sub-002\1stlevel\fMRIModules_0001.mat');
figure;

for moduleIndex = 1:nModules
    [x, y, z] = ind2sub(size(modules), find(modules== moduleIndex));
    plot3(x, y, z, '.');
    hold on;
end