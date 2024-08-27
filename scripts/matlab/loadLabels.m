function [...
    lo_faceROIidL,lo_faceROIidR,...
    hi_faceROIidL,hi_faceROIidR,...
    lo_glpfaces,lo_grpfaces,...
    hi_glpfaces,hi_grpfaces,...
    lo_glpvertex,lo_grpvertex,...
    hi_glpvertex,hi_grpvertex,...
    lo_subCoor,hi_subCoor,...
    lo_subROIid,hi_subROIid,...
    lo_centroidsL,lo_centroidsR,...
    hi_centroidsL,hi_centroidsR,...
    filenames,subfilenames...
    ]=...
    loadLabels(...
    pathToFile,subjectId,type,downsample,rate,...
    presetDownsampledSurface,presetDownsampledSurface_L,presetDownsampledSurface_R)

disp(presetDownsampledSurface);
disp(class(presetDownsampledSurface));
disp(presetDownsampledSurface_L);
disp(class(presetDownsampledSurface_L));
disp(presetDownsampledSurface_R);
disp(class(presetDownsampledSurface_R));
opt = struct(); opt.dup=true; opt.isolated=true; opt.intersect=true;
if ~exist('presetDownsampledSurface', 'var') ||  isempty(presetDownsampledSurface)
    presetDownsampledSurface = false;
end

addpath(genpath('toolboxes/SurfStat'));
addpath('toolboxes/FieldTrip');
ft_defaults;
ft_hastoolbox('spm12',1);
ft_hastoolbox('iso2mesh',1);
ft_hastoolbox('gifti',1);

%% load label info
disp('step2: load surface node coordinates and their denoted label')
atlas=ft_read_mri([pathToFile,'/MNINonLinear/aparc+aseg.nii.gz']);% load aparc+aseg.nii to get subcortical coordinates
[hi_glpfaces, hi_grpfaces, hi_glpvertex, hi_grpvertex, filenames, subfilenames, ROIfacevert]  = loadMesh([pathToFile,'/MNINonLinear/',subjectId,'.L.pial_MSMAll.164k_fs_LR.surf.gii'],[pathToFile,'/MNINonLinear/',subjectId,'.R.pial_MSMAll.164k_fs_LR.surf.gii'],pathToFile,subjectId,type);
if type==1
    RASmat = atlas.hdr.vox2ras; % vox2RAS: from voxel slices to scanner RAS coordinates (that is lh/rh.pial.surf.gii)
elseif type==2
    RASmat = atlas.hdr.tkrvox2ras; % from voxel slices to tk surface RAS coordinates (that is lh/rh.pial).
end


%% assign labels to LH hi-res
highestLhLabelId = find(contains(filenames,'lh.'), 1, 'last' );
lowestLhLabelId = find(contains(filenames,'lh.'), 1, 'first' );
hi_facesLH = loopROIAndAssignLabels(lowestLhLabelId,highestLhLabelId, hi_glpfaces, ROIfacevert);
hi_faceROIidL = hi_facesLH(:,4);

%% assign labels to RH hi-res
highestRhLabelId = find(contains(filenames,'rh.'), 1, 'last' );
lowestRhLabelId = find(contains(filenames,'rh.'), 1, 'first' );
hi_facesRH = loopROIAndAssignLabels(lowestRhLabelId, highestRhLabelId, hi_grpfaces, ROIfacevert);
hi_faceROIidR = hi_facesRH(:,4);

%% get subcortical coordinates and then map to pial space
hi_subROIid = []; hi_subCoor = []; lo_subROIid = [];lo_subCoor = [];
subColor = [10,11,12,13,18,17,26,7,8,49,50,51,52,54,53,58,46,47,16]; % freesurfer color index correspond to subfilenames, note: 47 and 8 are left cerebellum-white-matter
% and left cerebellum-cortex, two together are denoted as lh.cerebellum;
% likely, 46 and 47 together are denoted as rh.cerebellum; 16 is Brain-stem
ColorInd = atlas.anatomy;
all_subroi = cumsum(subColor ~=8 & subColor ~= 47); %if cerebellar cortex, the count is not increased.
parfor i = 1:length(subColor)
    color = subColor(i);
    subroi = all_subroi(i);

    % If not cerebellar cortex (L nor R)
    if color~=8 && color~=47
        [r,u,v] = ind2sub(size(ColorInd),find(ColorInd==color));
        ind = [r,u,v];
        RASCoor = RASmat*[ind,ones(size(ind,1),1)]';
        RASCoor = RASCoor(1:3,:)';
        hi_subCoor = [hi_subCoor;RASCoor];
        hi_subROIid = [hi_subROIid;ones(size(ind,1),1)*subroi];
        if strcmp(downsample,'no')
            lo_subCoor = [lo_subCoor;RASCoor];
            lo_subROIid = [lo_subROIid;ones(size(ind,1),1)*subroi];
        elseif strcmp(downsample,'yes')
            sprintf('perform downsample to subcortical regions and the rate is %1f',rate)
            pcCloudIn = pointCloud(RASCoor);
            ptCloudOut = pcdownsample(pcCloudIn,'random',rate); % random downsample
            RASCoor = ptCloudOut.Location;
            lo_subCoor = [lo_subCoor;RASCoor];
            lo_subROIid = [lo_subROIid;ones(size(RASCoor,1),1)*subroi];
        end


    elseif color==8 || color==47 %is cerebellar cortex
        [r,u,v] = ind2sub(size(ColorInd),find(ColorInd==color));
        ind = [r,u,v];
        RASCoor = RASmat*[ind,ones(size(ind,1),1)]';
        RASCoor = RASCoor(1:3,:)';
        hi_subCoor = [hi_subCoor;RASCoor];
        hi_subROIid = [hi_subROIid;ones(size(ind,1),1)*subroi];
        if strcmp(downsample,'no')
            lo_subCoor = [lo_subCoor;RASCoor];
            lo_subROIid = [lo_subROIid;ones(size(ind,1),1)*subroi];
        elseif strcmp(downsample,'yes')
            sprintf('perform downsample to subcortical regions and the rate is %1f',rate)
            pcCloudIn = pointCloud(RASCoor);
            ptCloudOut = pcdownsample(pcCloudIn,'random',rate); % random downsample
            RASCoor = ptCloudOut.Location;
            lo_subCoor = [lo_subCoor;RASCoor];
            lo_subROIid = [lo_subROIid;ones(size(RASCoor,1),1)*subroi];
        end
    end
end

hi_centroidsL=meshcentroid(hi_glpvertex,hi_glpfaces);% centroids in hi-res mesh
hi_centroidsR=meshcentroid(hi_grpvertex,hi_grpfaces);% centroids in hi-res mesh

%% check if downsample and define the final nodes
if strcmp(downsample,'no')
    disp('Not downsampling. Where a downsampled surface is needed downstream, we will just use the high-res surface.')
    lo_glpvertex = hi_glpvertex;
    lo_glpfaces = hi_facesLH(:,1:3);
    lo_faceROIidL = hi_facesLH(:,4);
    lo_centroidsL = hi_centroidsL;% centroids of hi-res mesh will pretend to be low-res.

    lo_grpvertex = hi_grpvertex;
    lo_grpfaces = hi_facesRH(:,1:3);
    lo_faceROIidR = hi_facesRH(:,4);
    lo_centroidsR = hi_centroidsR;% centroids of hi-res mesh will pretend to be low-res.

elseif strcmp(downsample,'yes')
    if(strcmp(presetDownsampledSurface,'0'))
        sprintf('perform downsample to cortical regions and the rate is %1f',rate)
        % downsample mesh
        [lo_glpvertex,lo_glpfaces]=meshresample(hi_glpvertex,hi_glpfaces,rate);
        [lo_grpvertex,lo_grpfaces]=meshresample(hi_grpvertex,hi_grpfaces,rate);
        [lo_glpvertex,lo_glpfaces]=meshcheckrepair(lo_glpvertex,lo_glpfaces,opt);
        [lo_grpvertex,lo_grpfaces]=meshcheckrepair(lo_grpvertex,lo_grpfaces,opt);
        % get centroids
        lo_centroidsL=meshcentroid(lo_glpvertex,lo_glpfaces);% centroids in lo-res mesh
        lo_centroidsR=meshcentroid(lo_grpvertex,lo_grpfaces);% centroids in lo-res mesh
        [lo_faceROIidL] = loopFacesProjectFromHiToLoRes(lo_centroidsL, hi_centroidsL, hi_facesLH);
        [lo_faceROIidR] = loopFacesProjectFromHiToLoRes(lo_centroidsR, hi_centroidsR, hi_facesRH);

        % Store surface labels as new gifti
        %{
            TODO: To create label files, we must attach anatomical labels
            to nodes (not faces).
        for k=length([filesname; subfilenames'])
            faceIndices = find(faceROIidL == k);
            lines = strings(2+length(faceIndices),5);
            lines(1,1)='#!ascii label , from subject 100610 vox2ras=TkReg';
            lines(2,1)='#No. Label Name: R   G   B   A';
            lines(3:2+length(faceIndices),1) = faceIndices;
            lines(3:2+length(faceIndices),2:5) = [rand(length(faceIndices),3), zeros(length(faceIndices),1)];
        end
        %}

    elseif(strcmp(presetDownsampledSurface,'1'))
        disp("Getting preset downsampled surface: "+presetDownsampledSurface);
        [lo_glpfaces, lo_grpfaces, lo_glpvertex, lo_grpvertex, filenames, subfilenames, lo_ROIfacevert] = loadMesh(presetDownsampledSurface_L,presetDownsampledSurface_R,pathToFile,subjectId,type);
        %[lo_glpvertex,lo_glpfaces]=meshcheckrepair(lo_glpvertex,lo_glpfaces,opt);
        %[lo_grpvertex,lo_grpfaces]=meshcheckrepair(lo_grpvertex,lo_grpfaces,opt);
        
        highestLhLabelId = find(contains(filenames,'lh.'), 1, 'last' );
        lowestLhLabelId = find(contains(filenames,'lh.'), 1, 'first' );
        highestRhLabelId = find(contains(filenames,'rh.'), 1, 'last' );
        lowestRhLabelId = find(contains(filenames,'rh.'), 1, 'first' );
        
        lo_facesLH = loopROIAndAssignLabels(lowestLhLabelId,highestLhLabelId, lo_glpfaces, lo_ROIfacevert);
        lo_faceROIidL = lo_facesLH(:,4);
        
        lo_facesRH = loopROIAndAssignLabels(lowestRhLabelId, highestRhLabelId, lo_grpfaces, lo_ROIfacevert);
        lo_faceROIidR = lo_facesRH(:,4);
        
        lo_centroidsL=meshcentroid(lo_glpvertex,lo_glpfaces); %centroids in lo-res mesh
        lo_centroidsR=meshcentroid(lo_grpvertex,lo_grpfaces); %centroids in lo-res mesh
    else
        disp("presetDownsampledSurface_L and/or presetDownsampledSurface_R incorrectly set. Does it exist? Is presetDownsampledSurface set to true?")
        return;
    end

    % Store surface as new gifti
    new_surf_L = gifti;
    new_surf_L.mat = eye(4);
    new_surf_L.vertices = lo_glpvertex;
    new_surf_L.faces = lo_glpfaces;
    save(new_surf_L,[presetDownsampledSurface_L,'.automated.surf.gii']);
    new_surf_R = gifti;
    new_surf_R.mat = eye(4);
    new_surf_R.vertices = lo_grpvertex;
    new_surf_R.faces = lo_grpfaces;
    save(new_surf_R,[presetDownsampledSurface_R,'.automated.surf.gii']);


else
    disp('wrong description of downsample, please type ''yes'' or ''no''.')
end

%% Sort the faces according to region number
% LH
lo_faceROIidL(:,2)=[1:length(lo_faceROIidL)]'; % Add node index as 2nd column.
lo_faceROIidLsorted=sortrows(lo_faceROIidL,1); % Per row, column1= label ID; column2= node ID
%lo_glpfaces=lo_glpfaces(lo_faceROIidLsorted(:,2),:); % Reorder lo_glpfaces so that faces are in asc. order of label ID.
%lo_faceROIidL=lo_faceROIidLsorted(:,1); % Reorder lo_lo_faceROIidL so that label IDs are in asc. order.
clear lo_faceROIidLsorted
% LH
lo_faceROIidR(:,2)=[1:length(lo_faceROIidR)]';
lo_faceROIidRsorted=sortrows(lo_faceROIidR,1);
%lo_grpfaces=lo_grpfaces(lo_faceROIidRsorted(:,2),:);
%lo_faceROIidR=lo_faceROIidRsorted(:,1);
clear lo_faceROIidRsorted



% --
% NESTED FUNCTIONS
% --

    function [facesROI] = loopROIAndAssignLabels(ROI_startIndex, ROI_endIndex, faces, ROIfacevert)
        facesROI={};
        parfor roi=ROI_startIndex:ROI_endIndex
            x=sum(ismember(faces,ROIfacevert(roi).faces(:,1)+1),2);
            ROIfacevert(roi).ffaces=find(x>1); %by Xue
            nbffaces=length(ROIfacevert(roi).ffaces);
            facesROI{roi} = [faces(ROIfacevert(roi).ffaces,:), ones(nbffaces,1)*roi];
        end
        facesROI=cat(1,facesROI{:});
    end
    function [lo_faces_scalar] = loopFacesProjectFromHiToLoRes(lo_face_centroids, hi_face_centroids, hi_faces_scalar)
        %% Loop through each face on downsampled mesh to find closest face on original mesh. Returns a vector of correspoding label IDs.
        nLoFaces = size(lo_face_centroids,1);
        lo_faces_scalar=zeros(nLoFaces,1);
        missingAnatomLabel=0;
        parfor k=1:nLoFaces
            % Print progress.
            if mod(k/1000,1)==0
                disp(num2str(nLoFaces\k))
            end

            currentface=lo_face_centroids(k,:); %current face's centroid coordinates
            %Euclidean distances (vector double) between current face and all mesh centroids
            ds=((currentface(:,1)-hi_face_centroids(:,1)).^2 + (currentface(:,2)-hi_face_centroids(:,2)).^2 + (currentface(:,3)-hi_face_centroids(:,3)).^2 );

            % ID of the mesh centroid that is closest to current face's
            % centroid.
            [~,closestCentroid_id]=min(ds);

            % Replace ID (as above) with the label ID of that centroid.
            try
                lo_faces_scalar(k,1)=hi_faces_scalar(closestCentroid_id,4);
            catch
                missingAnatomLabel =missingAnatomLabel +1;
                lo_faces_scalar(k,1)=NaN;
            end
        end
        if(missingAnatomLabel>0)
            disp(missingAnatomLabel+" faces with an unknown/missing scalar value encountered. It is possibly subcortical, but set as unknown.");
        end
    end


end