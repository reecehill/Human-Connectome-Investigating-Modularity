function bedpostXtoDsiStudio(pathToParticipants, subject)
% Courtesy of: https://sites.google.com/a/labsolver.org/dsi-studio/Manual/data-exchange-between-dsi-studio-and-mrtrix
% You may need to download a nifti file loader to run this function.
% http://www.mathworks.com/matlabcentral/fileexchange/8797-tools-for-nifti-and-analyze-image
% This example shows converting a maximum of 3 fiber populations.
% For populations more than 3, you may need to modify the codes.theta1 = niftiread('mean_th1samples.nii.gz');
arguments
    pathToParticipants char
    subject char
end

disp("pathToParticipants: ");
disp(pathToParticipants);
fprintf('Subject: %', subject);
disp(subject);

N = 3;
flip=1;
for i = 1:N
    thetaFieldname = sprintf('theta%i', i);
    s.(thetaFieldname ) = niftiinfo([pathToParticipants subject '/T1w/Diffusion.bedpostX/mean_th' int2str(i) 'samples.nii.gz']);
    s.(thetaFieldname ).img = niftiread([pathToParticipants subject '/T1w/Diffusion.bedpostX/mean_th' int2str(i) 'samples.nii.gz']);

    phiFieldName = sprintf('phi%i', i);
    s.(phiFieldName) = niftiinfo([pathToParticipants subject '/T1w/Diffusion.bedpostX/mean_ph' int2str(i) 'samples.nii.gz']);
    s.(phiFieldName).img = niftiread([pathToParticipants subject '/T1w/Diffusion.bedpostX/mean_ph' int2str(i) 'samples.nii.gz']);

    fFieldName = sprintf('f%i', i);
    s.(fFieldName) = niftiinfo([pathToParticipants subject '/T1w/Diffusion.bedpostX/mean_f' int2str(i) 'samples.nii.gz']);
    s.(fFieldName).img = niftiread([pathToParticipants subject '/T1w/Diffusion.bedpostX/mean_f' int2str(i) 'samples.nii.gz']);
end

fib.dimension = size(s.f1.img);
fib.voxel_size = s.f1.PixelDimensions;

for i = 1:N
    fFieldName = sprintf('fa%i', i-1);
    fib.(fFieldName) = double(reshape(s.(sprintf('f%i', i)).img,1,[]));
    fib.(sprintf('dir%i', i-1))(1,:,:,:) = sin(s.(sprintf('theta%i', i)).img).*cos(s.(sprintf('phi%i', i)).img);
    fib.(sprintf('dir%i', i-1))(2,:,:,:) = sin(s.(sprintf('theta%i', i)).img).*sin(s.(sprintf('phi%i', i)).img);
    fib.(sprintf('dir%i', i-1))(3,:,:,:) = cos(s.(sprintf('theta%i', i)).img);
    fib.(sprintf('dir%i', i-1)) = double(reshape(fib.(sprintf('dir%i', i-1)),3,[]));
end

% flip xy: you may need to make sure that this orientation is correct
if(flip==1)
    for i = 1:N
        fib.(sprintf('fa%i', i-1)) = reshape(fib.(sprintf('fa%i', i-1)),fib.dimension);
        
        % Reverse x and y.
        %fib.(sprintf('fa%i', i-1)) = fib.(sprintf('fa%i', i-1))(fib.dimension(1):-1:1,fib.dimension(2):-1:1,:);
        
        % reverse just y.
        fib.(sprintf('fa%i', i-1)) = fib.(sprintf('fa%i', i-1))(:,fib.dimension(2):-1:1,:);

        fib.(sprintf('fa%i', i-1)) = reshape(fib.(sprintf('fa%i', i-1)),1,[]);
    end
    
    for i = 1:N
        fib.(sprintf('dir%i', i-1)) = reshape(fib.(sprintf('dir%i', i-1)),[3 fib.dimension]);
        
        % reverse x and y.
        %fib.(sprintf('dir%i', i-1)) = fib.(sprintf('dir%i', i-1))(:,fib.dimension(1):-1:1,fib.dimension(2):-1:1,:);
        
        %reversse just y.
        fib.(sprintf('dir%i', i-1)) = fib.(sprintf('dir%i', i-1))(:,:,fib.dimension(2):-1:1,:);
        
        fib.(sprintf('dir%i', i-1))(3,:,:,:) = -fib.(sprintf('dir%i', i-1))(3,:,:,:);
        fib.(sprintf('dir%i', i-1)) = reshape(fib.(sprintf('dir%i', i-1)),3,[]);
    end
end
save([pathToParticipants subject '/T1w/Diffusion/automated.fib'], '-struct','fib','-v4');
end
