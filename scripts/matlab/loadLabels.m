function [faceROIidL,faceROIidR,hi_faceROIidL, hi_faceROIidR, filenames,subfilenames,glpfaces,grpfaces,glpvertex,grpvertex,nfl,nfr,nvl,nvr,subCoor,subROIid,hi_subCoor,hi_subROIid,lo_centroidsL,lo_centroidsR,hi_centroidsL,hi_centroidsR]=loadLabels(pathToFile,subjectId,type,downsample,rate)
    function [facesROI] = loopROIAndAssignLabels(ROI_startIndex, ROI_endIndex, faces)
        facesROI={};
        parfor roi=ROI_startIndex:ROI_endIndex
            x=sum(ismember(faces,ROIfacevert(roi).faces(:,1)+1),2);
            ROIfacevert(roi).ffaces=find(x>1); %by Xue
            nbffaces=length(ROIfacevert(roi).ffaces);
            facesROI{roi} = [faces(ROIfacevert(roi).ffaces,:), ones(nbffaces,1)*roi];
        end
        facesROI=cat(1,facesROI{:});
    end
addpath(genpath('toolboxes/SurfStat'));
addpath('toolboxes/FieldTrip');
ft_defaults;
ft_hastoolbox('spm12',1);
ft_hastoolbox('iso2mesh',1);
%% load label info
disp('step2: load surface node coordinates and their denoted label')

clear ROIfacevert

atlas=ft_read_mri([pathToFile,'/MNINonLinear/aparc+aseg.nii']);% load aparc+aseg.nii to get subcortical coordinates
[glpfaces, grpfaces, glpvertex, grpvertex, filenames, subfilenames, ROIfacevert, nbROI] = load164kMesh(pathToFile,subjectId,type);
if type==1
    RASmat = atlas.hdr.vox2ras; % vox2RAS: from voxel slices to scanner RAS coordinates (that is lh/rh.pial.surf.gii)
elseif type==2
    RASmat = atlas.hdr.tkrvox2ras; % from voxel slices to tk surface RAS coordinates (that is lh/rh.pial).
end


%% assign labels to LH hi-res
facesLH = loopROIAndAssignLabels(1,nbROI/2, glpfaces);
hi_faceROIidL = facesLH(:,4);


%% assign labels to RH hi-res
facesRH = loopROIAndAssignLabels((nbROI/2)+1, nbROI, glpfaces);
hi_faceROIidR = facesRH(:,4);

%% get subcortical coordinates and then map to pial space
hi_subROIid = []; hi_subCoor = []; subROIid = []; subCoor = [];
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
            subCoor = [subCoor;RASCoor];
            subROIid = [subROIid;ones(size(ind,1),1)*subroi];
        elseif strcmp(downsample,'yes')
            sprintf('perform downsample to subcortical regions and the rate is %1f',rate)
            pcCloudIn = pointCloud(RASCoor);
            ptCloudOut = pcdownsample(pcCloudIn,'random',rate); % random downsample
            RASCoor = ptCloudOut.Location;
            subCoor = [subCoor;RASCoor];
            subROIid = [subROIid;ones(size(RASCoor,1),1)*subroi];
        end

    
    elseif color==8 || color==47 %is cerebellar cortex
        [r,u,v] = ind2sub(size(ColorInd),find(ColorInd==color));
        ind = [r,u,v];
        RASCoor = RASmat*[ind,ones(size(ind,1),1)]';
        RASCoor = RASCoor(1:3,:)';
        hi_subCoor = [hi_subCoor;RASCoor];
        hi_subROIid = [hi_subROIid;ones(size(ind,1),1)*subroi];
        if strcmp(downsample,'no')
            subCoor = [subCoor;RASCoor];
            subROIid = [subROIid;ones(size(ind,1),1)*subroi];
        elseif strcmp(downsample,'yes')
            sprintf('perform downsample to subcortical regions and the rate is %1f',rate)
            pcCloudIn = pointCloud(RASCoor);
            ptCloudOut = pcdownsample(pcCloudIn,'random',rate); % random downsample
            RASCoor = ptCloudOut.Location;
            subCoor = [subCoor;RASCoor];
            subROIid = [subROIid;ones(size(RASCoor,1),1)*subroi];
        end
    end
end

hi_centroidsL=meshcentroid(glpvertex,glpfaces);% centroids in hi-res mesh
hi_centroidsR=meshcentroid(grpvertex,grpfaces);% centroids in hi-res mesh

%% check if downsample and define the final nodes
if strcmp(downsample,'no')
    disp('Not downsampling. Where a downsampled surface is needed downstream, we will just use the high-res surface.')
    nvl = glpvertex;
    nfl = facesLH(:,1:3);
    faceROIidL = facesLH(:,4);
    lo_centroidsL = hi_centroidsL;% centroids of hi-res mesh will pretend to be low-res.

    nvr = grpvertex;
    nfr = facesRH(:,1:3);
    faceROIidR = facesRH(:,4);
    lo_centroidsR = hi_centroidsR;% centroids of hi-res mesh will pretend to be low-res.

elseif strcmp(downsample,'yes')
    sprintf('perform downsample to cortical regions and the rate is %1f',rate)
    % downsample mesh
    [nvl,nfl]=meshresample(glpvertex,glpfaces,rate);
    [nvr,nfr]=meshresample(grpvertex,grpfaces,rate);
    % get centroids
    lo_centroidsL=meshcentroid(nvl,nfl);% centroids in lo-res mesh
    lo_centroidsR=meshcentroid(nvr,nfr);% centroids in lo-res mesh

    % match downsampled mesh to original hi-res labelled mesh using nearest centroid
    % LH
    numnfl=size(nfl,1);
    faceROIidL=zeros(size(nfl,1),1);
    missingAnatomLabel=0;
    %% Loop through each face on downsampled mesh to find closest face on original mesh. Returns a vector of correspoding label IDs.
    parfor k=1:numnfl
        % Print progress.
        if mod(k/1000,1)==0
            disp(num2str(numnfl\k))
        end

        currentface=lo_centroidsL(k,:); %current face's centroid coordinates
        %Euclidean distances (vector double) between current face and all mesh centroids
        dsl=((currentface(:,1)-hi_centroidsL(:,1)).^2 + (currentface(:,2)-hi_centroidsL(:,2)).^2 + (currentface(:,3)-hi_centroidsL(:,3)).^2 );

        % ID of the mesh centroid that is closest to current face's
        % centroid.
        [~,closestCentroid_id]=min(dsl);

        % Replace ID (as above) with the label ID of that centroid.
        try
            faceROIidL(k,1)=facesLH(closestCentroid_id,4);
        catch
            missingAnatomLabel =missingAnatomLabel +1;
            faceROIidL(k,1)=NaN;
        end
    end

    % RH
    numnfr=size(nfr,1);
    faceROIidR=zeros(size(nfr,1),1);
    parfor k=1:numnfr
        if mod(k/1000,1)==0
            disp(num2str(numnfr\k))
        end
        currentface=lo_centroidsR(k,:);
        dsr=((currentface(:,1)-hi_centroidsR(:,1)).^2 + (currentface(:,2)-hi_centroidsR(:,2)).^2 + (currentface(:,3)-hi_centroidsR(:,3)).^2 );
        [~,closestCentroid_id]=min(dsr);
        try
            faceROIidR(k,1)=facesRH(closestCentroid_id,4);
        catch
            missingAnatomLabel =missingAnatomLabel +1;
            faceROIidR(k,1)=NaN;
        end
    end
    clear dsl k currentface numnfl dsr k currentface numnfr
else
    disp('wrong description of downsample, please type ''yes'' or ''no''.')
end

if(missingAnatomLabel>0)
    disp(missingAnatomLabel+" faces with an unknown/missing anatomical label encountered. It is possibly subcortical, so skipped.");
end

%% Sort the faces according to region number
% LH
faceROIidL(:,2)=[1:length(faceROIidL)]'; % Add node index as 2nd column.
faceROIidLsorted=sortrows(faceROIidL,1); % Per row, column1= label ID; column2= node ID
nfl=nfl(faceROIidLsorted(:,2),:); % Reorder nfl so that faces are in asc. order of label ID.
faceROIidL=faceROIidLsorted(:,1); % Reorder faceROIidL so that label IDs are in asc. order.
clear faceROIidLsorted
% LH
faceROIidR(:,2)=[1:length(faceROIidR)]';
faceROIidRsorted=sortrows(faceROIidR,1);
nfr=nfr(faceROIidRsorted(:,2),:);
faceROIidR=faceROIidRsorted(:,1);
clear faceROIidRsorted
end