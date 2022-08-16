function untitled(pathToParticipants, subject)
load('D:\Dissertation\Participants\sub-01\edgeList.mat');
[Coor_MNI305,Coor_MNI152] = getMNIFromRasCoords([pathToParticipants '/' subject],[lpcentroids;rpcentroids;subCoor],2);
    filename=[pathToParticipants '/' subject '/MNIcoor.mat'];
    save(filename,'Coor_MNI305','Coor_MNI152','-v7.3');
    %clear lpcentroids,rpcentroids,subCoor;

end