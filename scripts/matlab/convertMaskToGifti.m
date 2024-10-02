function convertMaskToGifti(pathToNiftiMask_compressed, pathToFieldTripDirectory)

    %% PARAMETERS - EXPLAINED
    % ==> pathToCompressedMask_nifti
    %       must be an absolute or relative path pointing to a file with 
    %       extension .nii.gz
    % ==> pathToFieldTripDirectory
    %       must be an absolute/relative path pointing to the FOLDER that
    %       contains Fieldtrip (see next section). 

    
    %% (!!!) Download Fieldtrip MATLAB package - do this before running script.
    % This script uses two MATLAB packages "Gifti" and "iso2mesh". You
    % _could_ install these separately (https://www.gllmflndn.com/software/matlab/gifti/) 
    % and (https://iso2mesh.sourceforge.net/) respectively... 
    % BUT - I recommend you just use FieldTrip (that contains the above); this toolbox also contains many
    % toolboxes within that may be useful to you later.

    % To save you time, this script will setup PATHS for you - you just
    % need to tell it where the FieldTrip folder is extracted to. So...

    % Download, unzip and move the Fieldtrip folder to somewhere 
    % memorable: before continuing -> 
    % Go to: https://www.fieldtriptoolbox.org/download.php
   
    % Now, you can run this script in MATLAB, e.g.,
    %    convertMaskToGifti('ovine_brain_segmentation.nii.gz','/home/tracy/MATLAB/Iso2Mesh');


    %% (1) Initialise
    % Load Fieldtrip.
    restoredefaultpath;
    addpath(pathToFieldTripDirectory);
    ft_defaults;

    % Load gifti package from Fieldtrip.
    ft_hastoolbox('gifti',1);

    % Load iso2mesh package from Fieldtrip.
    ft_hastoolbox('iso2mesh',1);
    
    %% (2) Decompress nifti (.nii.gz to .nii)
    pathToNiftiMask = gunzip(pathToNiftiMask_compressed);

    %% (3) Read decompressed nifti as volume
    nifti_vol = niftiread(string(pathToNiftiMask));
    nifti_header = niftiinfo(string(pathToNiftiMask));

    %% (4) Convert mask to mesh of nodes and faces
    % Set meshing options. For more info: https://iso2mesh.sourceforge.net/cgi-bin/index.cgi?Doc/FunctionList
    isovalues = [1];
    opt = [];
    opt.maxnode = 50000; %max 50k nodes per surface mesh.
    opt.radbound = 1; %max radius of the Delaunay sphere
    %opt.distbound: ?; %maximum deviation from the specified isosurfaces
    opt.keepratio = 0.1; % setting compression rate for each levelset
    method = 'cgalmesh' ; % 'cgalmesh' or 'simplify' -> see documentation for finetuning options.


    [nodes,faces,regions,holes]=v2s(nifti_vol,isovalues,opt,method);

    %% (5) Check the mesh for errors and automatically repair.
    opt = [];
    opt.dup = 1;
    opt.isolated = 1;
    opt.deep = 1;
    opt.meshfix = 1;
    [nodes,faces]=meshcheckrepair(nodes,faces,opt);

    %% (6) Reorder nodes in a single closed surface to ensure the norms of all triangles are pointing outward
    [nodes,faces]=surfreorient(nodes,faces);

    %% (7) Save nodes and faces as .gifti surface file
    % .gifti files can be opened by freeview (freesurfer), fsleyes, wb_view (workbench) and Matlab.

    new_surf = gifti;
    new_surf.mat = eye(4);

    % NB: the nodes' coordinates, when read, are automatically transformed (using mask nifti
    % transform matrix). This is done erroneously, and without correction 
    % node coordinates are incorrect when viewed in Freeview/FSL etc.
    % Therefore, I undo this transformation to re-align surface with atlas.
    % You may wish to manually verify alignment by visualisation.
    % Verification by direct comparison of coord raw values not advised
    % without transformation.
    nodes_t = [nodes ones([length(nodes) 1])] * (nifti_header.Transform.T^1);

    new_surf.vertices = nodes_t(:,1:3);
    new_surf.faces = faces(:,1:3);
    pathToSurfaceFile_new = './surfaceFile_transformed.surf.gii';
    save(new_surf,pathToSurfaceFile_new);


   
    % --------------------------------
    % ----- EXTRA SCRIPTS BELOW. -----
    % --------------------------------

    %% Save file for FreeSurfer
    % It's possible to use Freesurfer's function (write_surf()) to save a surface file. 
    % This is now omitted due to above format being widely accepted.


    %% Save file back to .vtk
    % For confirmation that the generation of surface mesh from mask isn't
    % crazy, you may wish to do this? Then you can compare.
    % Maybe try: https://uk.mathworks.com/matlabcentral/fileexchange/94993-vtktoolbox

    %% (+) Visualise nodes and faces
    % Producing these figures, especially with large meshes, may be
    % intensive operations.

    showFigureInMatlab = 1; % 1 = generate figures; 0 = do NOT.

    if (showFigureInMatlab)
        % Figure 1
        figure();
        hold on;
        title("Generated surface file (transformed)");
        subtitle("Visualising nodes and faces.")
        plotsurf(nodes_t,faces,'FaceColor',[1 0 0],'EdgeColor',[0 0 0],'EdgeAlpha',0.2);

    
        % Disable clipping
        ax = gca;
        ax.Clipping = "off";
        % Add lighting
        lighting gouraud;
        campos([-465 -600  440]);
        camlight;

        % Figure 2
        figure();
        hold on;
        title("Generated surface file (NOT transformed)");
        subtitle("Visualising nodes and faces.")
        plotsurf(nodes,faces,'FaceColor',[1 0 0],'EdgeColor',[0 0 0],'EdgeAlpha',0.2);

    
        % Disable clipping
        ax = gca;
        ax.Clipping = "off";
        % Add lighting
        lighting gouraud;
        campos([-465 -600  440]);
        camlight;

        % Figure 3.
        figure();
        hold on;
        title("Provided brain mask");
        subtitle("Visualising raw data - NOT nodes/faces.")
        isosurface(nifti_vol);
    
        % Disable clipping
        ax = gca;
        ax.Clipping = "off";
        % Add lighting
        lighting gouraud;
        campos([-465 -600  440]);
        camlight;
    end
    
    %% (+) Visualise surface in Freesurfer
    % Launch freeview from matlab. (Untested, only works on Linux). 
    !freeview -v pathToNiftiMask_compressed -f pathToSurfaceFile_new --viewport 3d &
end