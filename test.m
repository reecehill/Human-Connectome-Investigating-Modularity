clc
clear

pathToFile='/home/campus.ncl.ac.uk/b7071887/Xchen/Demo_batch_high_resolution/HCP_';
subjects = '100307';

%% do not downsample surface, surface is pial.surf.gii
% batch_process(pathToFile,subjects,1,'no');

%% downsample surface , surface is pial.surf.gii, default downsample ratio is 0.1
batch_process(pathToFile,subjects,1,'yes',0.1);

%% no downsample surface, surface is pial
% batch_process(pathToFile,subjects,2,'no');