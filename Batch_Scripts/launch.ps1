######
# SET PARAMETERS
######
# The drive letter that contains all files. In format like - C:\
$drive = 'C:/'
# Paths must begin from after the drive number. i.e., (C:\Users\... becomes \Users\...)
$pathToFreeSurferLicence = "Users/Reece/Documents/Dissertation/freesurfer/license.txt"
$pathToParticipants = "Users/Reece/Documents/Dissertation/Main/Participants"
$driveAndPathToParticipants = $($drive+$pathToParticipants)
$pathToDsiStudio = $drive+'Users\Reece\Documents\Dissertation\dsi_studio_win'


$startAfresh = Read-host 'Delete all participant information and start afresh? (Y/N)'
$dataToUse = Read-host 'Begin with Freesurfer and [U]nprocessed data, or retrieve [P]reprocessed data and skip Freesurfer? (U/P)'

function getData($subjectId, $dataToFetch) {
  if($dataToFetch -eq "unprocessed") {
      $rawFileDirectory = $($driveAndPathToParticipants + '\' + $subjectId + '\T1w\')
      $rawFileName = 'T1.nii.gz'
      # Set the host's filepath as that of _T1.nii.gz file. Note that we change the folder hierarchy.
      $hostPath = "s3://hcp-openaccess/HCP_1200/$subjectId/unprocessed/3T/T1w_MPR1/"+$subjectId+"_3T_T1w_MPR1.nii.gz"
      $recursive = ''
  }
  elseif ($dataToFetch -eq "preprocessed") {
      # Set the directory in question as the subject's bert folder (the output of Freesurfer). We only check for aparc+aseg.mgz
      $rawFileDirectory = $($driveAndPathToParticipants + '\' + $subjectId + '\T1w\bert\')
      $rawFileName = 'mri/aparc+aseg.mgz'
      # Set the host's filepath as that of the subject's bert folder. Note that we change the folder hierarchy.
      $hostPath = "s3://hcp-openaccess/HCP_1200/$subjectId/T1w/$subjectId/"
      $recursive = '--recursive';
  }
  elseif ($dataToFetch -eq "diffusion") {
      # Set the directory in question as the subject's Diffusion data folder (for use in DSIStudio). We only check for data.nii.gz.
      $rawFileDirectory = $($driveAndPathToParticipants + '\' + $subjectId + '\T1w\Diffusion\')
      $rawFileName = 'data.nii.gz'
      # Set the host's filepath as that of the subject's Diffusion data folder (preprocessed).
      $hostPath = "s3://hcp-openaccess/HCP_1200/$subjectId/T1w/Diffusion/"
      $recursive = '--recursive';
  }
  else {
    Write-host "Data to fetch was incorrectly set." -ForegroundColor Red -BackgroundColor Black
    exit;
  }
  
  $rawFilePath = $($rawFileDirectory+$rawFileName)
      # Check that the necessary data for this subject exists. If it doesn't, get it from AWS.
  if (-not(Test-Path -Path $rawFilePath -PathType Leaf)) {
    Write-Host "The file [$rawFilePath] does not exist. Creating it now..."
    try {
        $null = New-Item $rawFileDirectory -itemType Directory -Force -ErrorAction Stop;
        & "C:\Program Files\Amazon\AWSCLIV2\aws.exe" "s3" "cp" "$hostPath" "$rawFileDirectory" $recursive;
        Write-Host "The file [$rawFileDirectory] has been created.";
        }
    catch {
        throw $_.Exception.Message
    }
  }
  else {
    Write-Host "The file [$rawFilePath] was found. No need to get from AWS."
  }
}

######
# (END)
######
# ---------------------------------------
######
# CLEAR CURRENT DATA
######

if("Y" -eq $startAfresh) {
  # Remove # if folder cannot be deleted due to permissions issue.
  # Get-ChildItem -Recurse -Path $driveAndPathToParticipants | Set-ItemProperty -Name IsReadOnly -Value $false
  try {
    Rename-Item -Path $driveAndPathToParticipants -NewName $($driveAndPathToParticipants + '-old') -ErrorAction Stop
  }
  catch {
    Write-Host "There is a permissions issue with the Participants folder. Please manually delete the sub-folders within the Participants folder." -ForegroundColor Red -BackgroundColor Black
    exit;
  }
  New-Item -Path $driveAndPathToParticipants -ItemType Directory
  Copy-Item $($driveAndPathToParticipants + '-old/file_list_HCP_all_subset.txt') $($driveAndPathToParticipants + '/file_list_HCP_all_subset.txt')
  Copy-Item $($driveAndPathToParticipants + '-old/.gitignore') $($driveAndPathToParticipants + '/.gitignore')
  Remove-Item $($driveAndPathToParticipants + '-old') -Recurse
  Write-Host "The participant folder has been cleared. Please rerun the command and answer 'No'" -ForegroundColor Red -BackgroundColor Black
  exit;
}
elseif("N" -eq $startAfresh) {
  #continue...
}
else {
  Write-Host "Ensure you enter either Y or N." -ForegroundColor Red -BackgroundColor Black;
  exit;
}
######
# (END)
######
# ---------------------------------------
######
# GET DATA (START, STEP 1)
######

$subjectList = Get-Content -Path $($driveAndPathToParticipants+'\file_list_HCP_all_subset.txt')
Write-Host "STEP 1 of 5: RETRIEVAL OF MISSING DATA" -ForegroundColor Green -BackgroundColor Black
foreach ($subjectId in $subjectList){
    Write-Host "Processing Subject $subjectId" -ForegroundColor Green -BackgroundColor Black
    if("U" -eq $dataToUse) {
      # Get only the T1 raw data, to be processed later.
      getData $subjectId "unprocessed";
      getData $subjectId "diffusion";
    }
    elseif ("P" -eq $dataToUse) {
      # Get the T1 raw data and the preprocessed data from the HCP Freesurfer pipeline.
      getData $subjectId "preprocessed";
      getData $subjectId "diffusion";
    }
    else {
      Write-Host "Please ensure you enter either U (for unprocessed data) or P (for preprocessed data)." -ForegroundColor Red -BackgroundColor Black.
      exit;
    }
}  

######
# (END)
######
# ---------------------------------------
######
# LAUNCH WSL AND FREESURFER (START, STEP 2-3)
######

# Launch WSL (Ubuntu 18 environment)
# No need to loop through subjects here, as it occurs within Linux.
Write-Host "STEP 2-3 of 5: FreeSurfer" -ForegroundColor Green -BackgroundColor Black
wsl -d "Ubuntu-18.04" -u reece /mnt/c/Users/Reece/Documents/Dissertation/Main/Batch_Scripts/freesurferBatch.sh $("/mnt/c/"+$pathToFreeSurferLicence) $("/mnt/c/"+$pathToParticipants) "$dataToUse";
######
# (END)
######
# ---------------------------------------
######
# LAUNCH DSI (START, STEP 4)
######
Write-Host "STEP 4 of 5: DSIStudio" -ForegroundColor Green -BackgroundColor Black
foreach ($subjectId in $subjectList) {
  & $($PSScriptRoot+'\dsiBatch.ps1') -subjectId $subjectId -pathToDsiStudio $pathToDsiStudio
  Write-Host "Processing Subject $subjectId" -ForegroundColor Green -BackgroundColor Black
}
######
# (END)
######
# ---------------------------------------
######
# LAUNCH WSL AND MATLAB (START, STEP 5)
######
$type = 2
$downsample = 'yes'
$rate = 0.1
Set-Location "$driveAndPathToParticipants/../"
Write-Host "STEP 5 of 5: MATLAB" -ForegroundColor Green -BackgroundColor Black
foreach ($subjectId in $subjectList) {
  & matlab -batch "try, batch_process $driveAndPathToParticipants/ $subjectId $type $downsample $rate; end;"
  Write-Host "Processing Subject $subjectId" -ForegroundColor Green -BackgroundColor Black
}
######
# (END)
######
# ---------------------------------------
