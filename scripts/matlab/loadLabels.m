function [faceROIidL,faceROIidR,filenames,subfilenames,glpfaces,grpfaces,glpvertex,grpvertex,nfl,nfr,nvl,nvr,subCoor,subROIid]=loadLabels(pathToFile,subjectId,type,downsample,rate)
addpath(genpath('toolboxes/SurfStat'));
addpath('toolboxes/FieldTrip');
ft_defaults;
ft_hastoolbox('spm12',1);
addpath('toolboxes/Iso2Mesh/iso2mesh');
%% load label info
display('step2: load surface node coordinates and their denoted label')

clear ROIfacevert
filenames={'lh.L_bankssts.label';'lh.L_caudalanteriorcingulate.label';'lh.L_caudalmiddlefrontal.label';'lh.L_cuneus.label';'lh.L_entorhinal.label';'lh.L_frontalpole.label';'lh.L_fusiform.label';'lh.L_inferiorparietal.label';'lh.L_inferiortemporal.label';'lh.L_insula.label';'lh.L_isthmuscingulate.label';'lh.L_lateraloccipital.label';'lh.L_lateralorbitofrontal.label';'lh.L_lingual.label';'lh.L_medialorbitofrontal.label';'lh.L_middletemporal.label';'lh.L_paracentral.label';'lh.L_parahippocampal.label';'lh.L_parsopercularis.label';'lh.L_parsorbitalis.label';'lh.L_parstriangularis.label';'lh.L_pericalcarine.label';'lh.L_postcentral.label';'lh.L_posteriorcingulate.label';'lh.L_precentral.label';'lh.L_precuneus.label';'lh.L_rostralanteriorcingulate.label';'lh.L_rostralmiddlefrontal.label';'lh.L_superiorfrontal.label';'lh.L_superiorparietal.label';'lh.L_superiortemporal.label';'lh.L_supramarginal.label';'lh.L_temporalpole.label';'lh.L_transversetemporal.label';'rh.R_bankssts.label';'rh.R_caudalanteriorcingulate.label';'rh.R_caudalmiddlefrontal.label';'rh.R_cuneus.label';'rh.R_entorhinal.label';'rh.R_frontalpole.label';'rh.R_fusiform.label';'rh.R_inferiorparietal.label';'rh.R_inferiortemporal.label';'rh.R_insula.label';'rh.R_isthmuscingulate.label';'rh.R_lateraloccipital.label';'rh.R_lateralorbitofrontal.label';'rh.R_lingual.label';'rh.R_medialorbitofrontal.label';'rh.R_middletemporal.label';'rh.R_paracentral.label';'rh.R_parahippocampal.label';'rh.R_parsopercularis.label';'rh.R_parsorbitalis.label';'rh.R_parstriangularis.label';'rh.R_pericalcarine.label';'rh.R_postcentral.label';'rh.R_posteriorcingulate.label';'rh.R_precentral.label';'rh.R_precuneus.label';'rh.R_rostralanteriorcingulate.label';'rh.R_rostralmiddlefrontal.label';'rh.R_superiorfrontal.label';'rh.R_superiorparietal.label';'rh.R_superiortemporal.label';'rh.R_supramarginal.label';'rh.R_temporalpole.label';'rh.R_transversetemporal.label'};
subfilenames={'lh.thalamus','lh.caudate','lh.putamen','lh.pallidum','lh.amygdala','lh.hippocampus','lh.accumbens','lh.cerebellum','rh.thalamus','rh.caudate','rh.putamen','rh.pallidum','rh.amygdala','rh.hippocampus','rh.accumbens','rh.cerebellum','Brain-stem'};
%filenames([10,44])=[];
nbROI=length(filenames);
%nbInROI=zeros(nbROI,1);

%ft_defaults
atlas=ft_read_mri([pathToFile,'/MNINonLinear/aparc+aseg.nii']);% load aparc+aseg.nii to get subcortical coordinates

if type==1
    for i=1:nbROI
        ROIfacevert(i,1).id=filenames(i);
        ROIfacevert(i,1).faces=importfile([pathToFile,'/T1w/',subjectId,'/label/label_type1/',filenames{i}]);    
    end
    % load hi-res surface - pial.surf.gii
    display('load lh(rh).pial.surf.gii as surface')
    
    giftilh=gifti([pathToFile,'/MNINonLinear/',subjectId,'/surf/lh.pial.surf.gii']);
    glpfaces      = giftilh.faces;
    glpvertex     = giftilh.vertices;
    giftirh=gifti([pathToFile,'/MNINonLinear/',subjectId,'/surf/rh.pial.surf.gii']);
    grpfaces      = giftirh.faces;
    grpvertex     = giftirh.vertices;
    clear giftilh giftirh 
    
    RASmat = atlas.hdr.vox2ras; % vox2RAS: from voxel slices to scanner RAS coordinates (that is lh/rh.pial.surf.gii)
elseif type==2
    for i=1:nbROI
        ROIfacevert(i,1).id=filenames(i);
        ROIfacevert(i,1).faces=importfile([pathToFile,'/MNINonLinear/',subjectId,'/label/label_type2/',filenames{i}]);    
    end
    % load hi-res surface - pial
    display('load lh(rh).pial as surface')
    
    l=SurfStatReadSurf([pathToFile,'/MNINonLinear/',subjectId,'/surf/lh.pial']);
    r=SurfStatReadSurf([pathToFile,'/MNINonLinear/',subjectId,'/surf/rh.pial']);
    glpfaces = l.tri; %118,580x3 int32 (each row is the ID of the 3 nodes of the face)
    glpvertex = l.coord'; %59292x3 double (each row are the coordinates of a node; row id = node ID)
    grpfaces = r.tri; %118,580x3 int32 (each row is the ID of the 3 nodes of the face)
    grpvertex = r.coord'; %59292x3 double (each row are the coordinates of a node; row id = node ID)
    clear l r
    
    RASmat = atlas.hdr.tkrvox2ras; % from voxel slices to tk surface RAS coordinates (that is lh/rh.pial).
end


%% assign labels to LH hi-res
facesLH={};
parfor roi=1:nbROI/2
    x=sum(ismember(glpfaces,ROIfacevert(roi).faces(:,1)+1),2);  
%     ROIfacevert(roi).ffaces=find(x>0); %by Peter
    ROIfacevert(roi).ffaces=find(x>1); %by Xue
    nbffaces=length(ROIfacevert(roi).ffaces);
    %facesLH(roi,1)=glpfaces(ROIfacevert(roi).ffaces,:);
    facesLH{roi} = [glpfaces(ROIfacevert(roi).ffaces,:), ones(nbffaces,1)*roi];
end
facesLH = cat(1,facesLH{:});
%% assign labels to RH hi-res
facesRH={};
parfor roi=(nbROI/2)+1:nbROI
    x=sum(ismember(grpfaces,ROIfacevert(roi).faces(:,1)+1),2);  
%     ROIfacevert(roi).ffaces=find(x>0);% by Peter
    ROIfacevert(roi).ffaces=find(x>1);% by Xue
    nbffaces=length(ROIfacevert(roi).ffaces);
    facesRH{roi}=[grpfaces(ROIfacevert(roi).ffaces,:),ones(nbffaces,1)*(roi-(nbROI/2))];
end
facesRH = cat(1,facesRH{:});


%% get subcortical coordinates and then map to pial space
subROIid = []; subCoor = [];
subColor = [10,11,12,13,18,17,26,7,8,49,50,51,52,54,53,58,46,47,16]; % freesurfer color index correspond to subfilenames, note: 7 and 8 are left cerebellum-white-matter
% and left cerebellum-cortex, two together are denoted as lh.cerebellum;
% likely, 46 and 47 together are denoted as rh.cerebellum; 16 is Brain-stem
ColorInd = atlas.anatomy;
subroi = 0;
for i = 1:length(subColor)
    color = subColor(i);
    if color~=8 && color~=47 
      subroi = subroi +1;
      [r,u,v] = ind2sub(size(ColorInd),find(ColorInd==color));
      ind = [r,u,v];
      RASCoor = RASmat*[ind,ones(size(ind,1),1)]';
      RASCoor = RASCoor(1:3,:)';
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
      
    elseif color==8 || color==47
      [r,u,v] = ind2sub(size(ColorInd),find(ColorInd==color));
      ind = [r,u,v];
      RASCoor = RASmat*[ind,ones(size(ind,1),1)]';
      RASCoor = RASCoor(1:3,:)';
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

%% check if downsample and define the final nodes
if strcmp(downsample,'no')
    display('do not perform downsample')
    nvl = glpvertex;
    nfl = facesLH(:,1:3);
    faceROIidL = facesLH(:,4);
    
    nvr = grpvertex;
    nfr = facesRH(:,1:3);
    faceROIidR = facesRH(:,4);
elseif strcmp(downsample,'yes')
    sprintf('perform downsample to cortical regions and the rate is %1f',rate)
    % downsample mesh
    [nvl,nfl]=meshresample(glpvertex,glpfaces,rate);
    [nvr,nfr]=meshresample(grpvertex,grpfaces,rate);
    % get centroids
    lo_centroidsL=meshcentroid(nvl,nfl);% centroids in lo-res mesh
    hi_centroidsL=meshcentroid(glpvertex,facesLH(:,1:3));% centroids in hi-res mesh
    lo_centroidsR=meshcentroid(nvr,nfr);% centroids in lo-res mesh
    hi_centroidsR=meshcentroid(grpvertex,facesRH(:,1:3));% centroids in hi-res mesh
    % match downsampled mesh to original hi-res labelled mesh using nearest centroid
    % LH
    numnfl=size(nfl,1);
    faceROIidL=zeros(size(nfl,1),1);

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
        [~,faceROIidL(k,1)]=min(dsl);

        % Replace ID (as above) with the label ID of that centroid.
        faceROIidL(k,1)=facesLH(faceROIidL(k,1),4);
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
        [~,faceROIidR(k,1)]=min(dsr);
        faceROIidR(k,1)=facesRH(faceROIidR(k,1),4);
    end
    clear dsl k currentface numnfl hi_centroidsL lo_centroidsL dsr k currentface numnfr hi_centroidsR lo_centroidsR
else
    display('wrong description of downsample, please type ''yes'' or ''no''.')
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