function [faceROIidL,faceROIidR,filenames,subfilenames,glpfaces,grpfaces,glpvertex,grpvertex,nfl,nfr,nvl,nvr,subCoor,subROIid]=loadLabels(pathToFile,type,downsample,rate)
%% load label info
display('step2: load surface node coordinates and their denoted label')

clear ROIfacevert
filenames={'lh.bankssts.label';'lh.caudalanteriorcingulate.label';'lh.caudalmiddlefrontal.label';'lh.cuneus.label';'lh.entorhinal.label';'lh.frontalpole.label';'lh.fusiform.label';'lh.inferiorparietal.label';'lh.inferiortemporal.label';'lh.insula.label';'lh.isthmuscingulate.label';'lh.lateraloccipital.label';'lh.lateralorbitofrontal.label';'lh.lingual.label';'lh.medialorbitofrontal.label';'lh.middletemporal.label';'lh.paracentral.label';'lh.parahippocampal.label';'lh.parsopercularis.label';'lh.parsorbitalis.label';'lh.parstriangularis.label';'lh.pericalcarine.label';'lh.postcentral.label';'lh.posteriorcingulate.label';'lh.precentral.label';'lh.precuneus.label';'lh.rostralanteriorcingulate.label';'lh.rostralmiddlefrontal.label';'lh.superiorfrontal.label';'lh.superiorparietal.label';'lh.superiortemporal.label';'lh.supramarginal.label';'lh.temporalpole.label';'lh.transversetemporal.label';'rh.bankssts.label';'rh.caudalanteriorcingulate.label';'rh.caudalmiddlefrontal.label';'rh.cuneus.label';'rh.entorhinal.label';'rh.frontalpole.label';'rh.fusiform.label';'rh.inferiorparietal.label';'rh.inferiortemporal.label';'rh.insula.label';'rh.isthmuscingulate.label';'rh.lateraloccipital.label';'rh.lateralorbitofrontal.label';'rh.lingual.label';'rh.medialorbitofrontal.label';'rh.middletemporal.label';'rh.paracentral.label';'rh.parahippocampal.label';'rh.parsopercularis.label';'rh.parsorbitalis.label';'rh.parstriangularis.label';'rh.pericalcarine.label';'rh.postcentral.label';'rh.posteriorcingulate.label';'rh.precentral.label';'rh.precuneus.label';'rh.rostralanteriorcingulate.label';'rh.rostralmiddlefrontal.label';'rh.superiorfrontal.label';'rh.superiorparietal.label';'rh.superiortemporal.label';'rh.supramarginal.label';'rh.temporalpole.label';'rh.transversetemporal.label'};
subfilenames={'lh.thalamus','lh.caudate','lh.putamen','lh.pallidum','lh.amygdala','lh.hippocampus','lh.accumbens','lh.cerebellum','rh.thalamus','rh.caudate','rh.putamen','rh.pallidum','rh.amygdala','rh.hippocampus','rh.accumbens','rh.cerebellum','Brain-stem'};
%filenames([10,44])=[];
nbROI=length(filenames);
nbInROI=zeros(nbROI,1);

ft_defaults
atlas=ft_read_mri([pathToFile,'/../aparc+aseg.nii']); % load aparc+aseg.nii to get subcortical coordinates


if type==1
    for i=1:nbROI
        ROIfacevert(i,1).id=filenames(i);
        ROIfacevert(i,1).faces=importfile([pathToFile,'/ROI/label_type1/',filenames{i}]);    
    end
    % load hi-res surface - pial.surf.gii
    display('load lh(rh).pial.surf.gii as surface')
    
    giftilh=gifti([pathToFile,'/surf/lh.pial.surf.gii']);
    glpfaces      = giftilh.faces;
    glpvertex     = giftilh.vertices;
    giftirh=gifti([pathToFile,'/surf/rh.pial.surf.gii']);
    grpfaces      = giftirh.faces;
    grpvertex     = giftirh.vertices;
    clear giftilh giftirh 
    
    RASmat = atlas.hdr.vox2ras; % vox2RAS: from voxel slices to scanner RAS coordinates (that is lh/rh.pial.surf.gii)
elseif type==2
    for i=1:nbROI
        ROIfacevert(i,1).id=filenames(i);
        ROIfacevert(i,1).faces=importfile([pathToFile,'/ROI/label_type2/',filenames{i}]);    
    end
    % load hi-res surface - pial
    display('load lh(rh).pial as surface')
    
    l=SurfStatReadSurf([pathToFile,'/surf/lh.pial']);
    r=SurfStatReadSurf([pathToFile,'/surf/rh.pial']);
    glpfaces = l.tri;
    glpvertex = l.coord';
    grpfaces = r.tri;
    grpvertex = r.coord';
    clear l r
    
    RASmat = atlas.hdr.tkrvox2ras; % from voxel slices to tk surface RAS coordinates (that is lh/rh.pial).
end


%% assign labels to LH hi-res
facesLH=[];
for roi=1:nbROI/2
    x=sum(ismember(glpfaces,ROIfacevert(roi).faces(:,1)+1),2);  
%     ROIfacevert(roi).ffaces=find(x>0); %by Peter
    ROIfacevert(roi).ffaces=find(x>1); %by Xue
    nbffaces=length(ROIfacevert(roi).ffaces);
    facesLH=[facesLH;glpfaces(ROIfacevert(roi).ffaces,:),ones(nbffaces,1)*roi];
    
end
%% assign labels to RH hi-res
facesRH=[];
for roi=(nbROI/2)+1:nbROI
    x=sum(ismember(grpfaces,ROIfacevert(roi).faces(:,1)+1),2);  
%     ROIfacevert(roi).ffaces=find(x>0);% by Peter
    ROIfacevert(roi).ffaces=find(x>1);% by Xue
    nbffaces=length(ROIfacevert(roi).ffaces);
    facesRH=[facesRH;grpfaces(ROIfacevert(roi).ffaces,:),ones(nbffaces,1)*roi-(nbROI/2)];
    
end

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
    for k=1:numnfl
        if mod(k/1000,1)==0
            disp(num2str(numnfl\k))
        end
        currentface=lo_centroidsL(k,:);% euclid dist b
        dsl=((currentface(:,1)-hi_centroidsL(:,1)).^2 + (currentface(:,2)-hi_centroidsL(:,2)).^2 + (currentface(:,3)-hi_centroidsL(:,3)).^2 );
        [~,faceROIidL(k,1)]=min(dsl);
        faceROIidL(k,1)=facesLH(faceROIidL(k,1),4);
    end
    % RH
    numnfr=size(nfr,1);
    faceROIidR=zeros(size(nfr,1),1);
    for k=1:numnfr
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
faceROIidL(:,2)=[1:length(faceROIidL)]';
faceROIidLsorted=sortrows(faceROIidL,1);
nfl=nfl(faceROIidLsorted(:,2),:);
faceROIidL=faceROIidLsorted(:,1);
clear faceROIidLsorted 
% LH
faceROIidR(:,2)=[1:length(faceROIidR)]';
faceROIidRsorted=sortrows(faceROIidR,1);
nfr=nfr(faceROIidRsorted(:,2),:);
faceROIidR=faceROIidRsorted(:,1);
clear faceROIidRsorted 
end