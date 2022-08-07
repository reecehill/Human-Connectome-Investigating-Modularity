### Due to having to make symlinks, this script must be ran as an admin.
If (-NOT (([Security.Principal.WindowsPrincipal] `
        [Security.Principal.WindowsIdentity]::GetCurrent() `
    ).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator))) {
  Write-Host "You do not have Administrator rights to run this script! Please re-run this script as an Administrator!"  -ForegroundColor Red -BackgroundColor Black
  exit;
}


######
# SET PARAMETERS
######
# The drive letter that contains all files. In format like - C:\
$drive = 'C:\'
# Paths must begin from after the drive number. i.e., (C:\Users\... becomes \Users\...)
$pathToFreeSurferLicence = "Users/Reece/Documents/Dissertation/freesurfer/license.txt"
$pathToParticipants = "Users/Reece/Documents/Dissertation/Main/Participants"
$driveAndPathToParticipants = $($drive + $pathToParticipants)
$pathToDsiStudio = $drive + 'Users\Reece\Documents\Dissertation\dsi_studio_win'
$pathToSpmPackage = $drive + 'Program Files\MATLAB\R2021b\spm12'
#$numberOfTracts = 10000
$numberOfTracts = 10000000


# "motor" : https://openfmri.org/s3-browser/?prefix=ds000244
# "hcp": https://humanconnectome.org/study/hcp-young-adult
$dataSetToUse = Read-host 'As of 15/07/22, only the Motor dataset works. Which dataset do you wish to use? ([M]otor/[H]cp)'
$startAfresh = Read-host 'Delete all participant information and start afresh? (Y/N)'
$dataToUse = Read-host 'Begin with Freesurfer and [U]nprocessed data, or retrieve [P]reprocessed data and skip Freesurfer? (U/P)'

function getHcpData($subjectId, $dataToFetch) {
  if ($dataToFetch -eq "unprocessed") {
    $localDirectoryToCheck = $($driveAndPathToParticipants + '\' + $subjectId + '\T1w\')
    $localFileToCheck = 'T1.nii.gz'
    $localPathForInsert = $($localDirectoryToCheck + '/' + $localFileToCheck)
    # Set the host's filepath as that of _T1.nii.gz file. Note that we change the folder hierarchy.
    $remotePath = "s3://hcp-openaccess/HCP_1200/$subjectId/unprocessed/3T/T1w_MPR1/" + $subjectId + "_3T_T1w_MPR1.nii.gz"
    $recursive = ''
  }
  elseif ($dataToFetch -eq "preprocessed") {
    # Set the directory in question as the subject's bert folder (the output of Freesurfer). We only check for aparc+aseg.mgz
    $localDirectoryToCheck = $($driveAndPathToParticipants + '\' + $subjectId + '\T1w\bert\')
    $localPathForInsert = $localDirectoryToCheck
    $localFileToCheck = 'mri/aparc+aseg.mgz'
    # Set the host's filepath as that of the subject's bert folder. Note that we change the folder hierarchy.
    $remotePath = "s3://hcp-openaccess/HCP_1200/$subjectId/T1w/$subjectId/"
    $recursive = '--recursive';
  }
  elseif ($dataToFetch -eq "diffusion") {
    # Set the directory in question as the subject's Diffusion data folder (for use in DSIStudio). We only check for data.nii.gz.
    $localDirectoryToCheck = $($driveAndPathToParticipants + '\' + $subjectId + '\T1w\Diffusion\')
    $localPathForInsert = $localDirectoryToCheck
    $localFileToCheck = 'data.nii.gz'
    # Set the host's filepath as that of the subject's Diffusion data folder (preprocessed).
    $remotePath = "s3://hcp-openaccess/HCP_1200/$subjectId/T1w/Diffusion/"
    $recursive = '--recursive';
  }
  else {
    Write-host "Data to fetch was incorrectly set." -ForegroundColor Red -BackgroundColor Black
    exit;
  }
  
  $rawFilePath = $($localDirectoryToCheck + $localFileToCheck)
  # Check that the necessary data for this subject exists. If it doesn't, get it from AWS.
  if (-not(Test-Path -Path $rawFilePath -PathType Leaf)) {
    Write-Host "The file [$rawFilePath] does not exist. Creating it now..."
    try {
      $null = New-Item $localDirectoryToCheck -itemType Directory -Force -ErrorAction Stop;
      & "C:\Program Files\Amazon\AWSCLIV2\aws.exe" "s3" "cp" "$remotePath" "$localPathForInsert" "$recursive";
      if ((Test-Path -Path $rawFilePath -PathType Leaf)) {
        Write-Host "The file [$rawFilePath] has been created.";
      }
      else {
        Write-Host "Could not download file [$rawFilePath]. Are you sure that subject ID exists? Please try again." -ForegroundColor Red -BackgroundColor Black
        Write-Host "hostpath=$remotePath" -ForegroundColor Red -BackgroundColor Black
        Write-Host "localDirectoryToCheck=$localDirectoryToCheck" -ForegroundColor Red -BackgroundColor Black
        Write-Host "recursive=$recursive" -ForegroundColor Red -BackgroundColor Black
        exit;
      }
    }
    catch {
      throw $_.Exception.Message;
      exit;
    }
  }
  else {
    Write-Host "The file [$rawFilePath] was found. No need to get from AWS."
  }
}
function getMotorData($subjectId) {
  $filesToCheck = Get-Content filesToCheck.csv
  foreach ($filename in $filesToCheck) {
    Get-ChildItem -Path $($driveAndPathToParticipants + '/sub-' + $subjectId + '/') -Include $('sub-' + $subjectId + "*" + $filename) -Recurse -ErrorAction SilentlyContinue -Force
  }
  Write-Host "We skipped the checks to ensure the subject has the files required. Please manually confirm."
}
######
# (END)
######
# ---------------------------------------
######
# CLEAR CURRENT DATA
######

if ("Y" -eq $startAfresh) {
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
elseif ("N" -eq $startAfresh) {
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

$subjectList = Get-Content -Path $($driveAndPathToParticipants + '\file_list_HCP_all_subset.txt')
Write-Host "STEP 1 of 8: RETRIEVAL OF MISSING DATA" -ForegroundColor Green -BackgroundColor Black
foreach ($subjectId in $subjectList) {
  Write-Host "Processing Subject $subjectId" -ForegroundColor Green -BackgroundColor Black
  if ("M" -eq $dataSetToUse) {
    Write-Host "Skipping checking for existence and/or downloading of Motor dataset..."
  }
  elseif ("H" -eq $dataSetToUse) {
    if ("U" -eq $dataToUse) {
      # Get only the T1 raw data, to be processed later.
      getHcpData $subjectId "unprocessed";
      getHcpData $subjectId "diffusion";
    }
    elseif ("P" -eq $dataToUse) {
      # Get the T1 raw data and the preprocessed data from the HCP Freesurfer pipeline.
      getHcpData $subjectId "preprocessed";
      getHcpData $subjectId "diffusion";
    }
    else {
      Write-Host "Please ensure you enter either U (for unprocessed data) or P (for preprocessed data)." -ForegroundColor Red -BackgroundColor Black
      exit;
    }
  }
  else {
    Write-Host "Please ensure you enter either M (for Motor dataset) or H (for HumanConnectomeProject dataset - unsupported)." -ForegroundColor Red -BackgroundColor Black
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
# We did loop through subjects inside Linux, but this led to unexpected behaviour where only the last subject was processed. For consistency, we loop through all here.
<#
Write-Host "STEP 2-3 of 8: FreeSurfer" -ForegroundColor Green -BackgroundColor Black
foreach ($subjectId in $subjectList) {
  Write-Host "Processing Subject $subjectId" -ForegroundColor Green -BackgroundColor Black

  if (Test-Path "$driveAndPathToParticipants/sub-$subjectId/data/bert") {
    Write-Host "Freesurfer output already exists..."
    Remove-Item "$driveAndPathToParticipants/sub-$subjectId/data/bert" -Force -Recurse -Confirm
  }

  Start-Job -ScriptBlock { 
    param($pathToFreeSurferLicence, $pathToParticipants, $subjectId, $dataToUse)
    wsl -d "Ubuntu-18.04" -u reece /mnt/c/Users/Reece/Documents/Dissertation/Main/Batch_Scripts/freesurferBatch.sh $("/mnt/c/" + $pathToFreeSurferLicence) $("/mnt/c/" + $pathToParticipants) "sub-$subjectId" "$dataToUse" 
  } -Name "fslJob-$subjectId" -ArgumentList $pathToFreeSurferLicence, $pathToParticipants, $subjectId, $dataToUse;
  
  Register-ObjectEvent (Get-Job -Name "fslJob-$subjectId") StateChanged -Action {
  # It is possible that freesurfer does not produce necessary symlinks. So once it's done, delete existing pial files/symlinks, and renew.
    Remove-Item "$driveAndPathToParticipants\sub-$subjectId\data\bert\surf\lh.pial" -Force
    Remove-Item "$driveAndPathToParticipants\sub-$subjectId\data\bert\surf\rh.pial" -Force
    cmd.exe /c mklink "$driveAndPathToParticipants\sub-$subjectId\data\bert\surf\lh.pial" "D:\Dissertation\Participants\sub-$subjectId\data\bert\surf\lh.pial.T1"
    cmd.exe /c mklink "$driveAndPathToParticipants\sub-$subjectId\data\bert\surf\rh.pial" "D:\Dissertation\Participants\sub-$subjectId\data\bert\surf\rh.pial.T1"
  }
}
exit;
#>


######
# (END)
######
# ---------------------------------------
######
# LAUNCH DSI (START, STEP 4)
######
<#
Write-Host "STEP 4 of 8: DSIStudio" -ForegroundColor Green -BackgroundColor Black
foreach ($subjectId in $subjectList) {
  Write-Host "Processing Subject $subjectId" -ForegroundColor Green -BackgroundColor Black
  #& $($PSScriptRoot + '\dsiBatch.ps1') -subjectId $subjectId -pathToDsiStudio $pathToDsiStudio -numberOfTracts $numberOfTracts
}
#>
######
# (END)
######
# ---------------------------------------
######
<#
# LAUNCH WSL AND MATLAB (START, STEP 5)
######
$type = 2
$downsample = 'yes'
$rate = 0.1
Set-Location "$driveAndPathToParticipants/../"
Write-Host "STEP 5 of 8: MATLAB" -ForegroundColor Green -BackgroundColor Black
foreach ($subjectId in $subjectList) {
  Write-Host "Processing Subject $subjectId" -ForegroundColor Green -BackgroundColor Black
  & matlab -batch "try, batch_process $driveAndPathToParticipants/ sub-$subjectId $type $downsample $rate; end;"
}
######
# (END)
######
# ---------------------------------------

$success = $true;
foreach ($subjectId in $subjectList) {
  if (-not(Test-Path -Path "$driveAndPathToParticipants/sub-$subjectId/edgeList.mat" -PathType Leaf) -or
    -not(Test-Path -Path "$driveAndPathToParticipants/sub-$subjectId/labelSRF.mat" -PathType Leaf) -or
    -not(Test-Path -Path "$driveAndPathToParticipants/sub-$subjectId/matrices.mat" -PathType Leaf) -or
    -not(Test-Path -Path "$driveAndPathToParticipants/sub-$subjectId/MNIcoor.mat" -PathType Leaf) -or
    -not(Test-Path -Path "$driveAndPathToParticipants/sub-$subjectId/trsfmTrk.mat" -PathType Leaf)
  ) {
    $success = $false;
    Write-Host "Error during structural analysis: Subject sub-$subjectId is missing some output. Check the console log above for errors. You can delete all data and try again." -ForegroundColor Red -BackgroundColor Black
    exit;
  }
}

if ($success -eq $true) {
  Write-Host "---------------------------------------" -ForegroundColor Green -BackgroundColor Black
  Write-Host "Success! All output files from structural data were created successfully. You may wish to check the console above for any errors, though." -ForegroundColor Green -BackgroundColor Black
  Write-Host "---------------------------------------" -ForegroundColor Green -BackgroundColor Black
  Write-Host "_______________________________________" -ForegroundColor Green -BackgroundColor Black
  Write-Host "---------------------------------------" -ForegroundColor Green -BackgroundColor Black
  Write-Host "Now commencing analysis of functional MRI data..." -ForegroundColor Green -BackgroundColor Black
  Write-Host "---------------------------------------" -ForegroundColor Green -BackgroundColor Black
} 
#>
# ---------------------------------------
######
# LAUNCH WSL AND MATLAB (START, STEP 6)
######
# So the matlab function can be found, set to current location of this .ps1 file.
Set-Location $PSScriptRoot

Write-Host "STEP 6 of 8: MATLAB (2)" -ForegroundColor Green -BackgroundColor Black
foreach ($subjectId in $subjectList) {
  Write-Host "Processing Subject $subjectId" -ForegroundColor Green -BackgroundColor Black
  # Ensure timing files are all created, if not, create them.
  if (
    -not(Test-Path -Path "$driveAndPathToParticipants/sub-$subjectId/data/func/timing_files/left_hand.txt" -PathType Leaf) -or
    -not(Test-Path -Path "$driveAndPathToParticipants/sub-$subjectId/data/func/timing_files/right_hand.txt" -PathType Leaf) -or
    -not(Test-Path -Path "$driveAndPathToParticipants/sub-$subjectId/data/func/timing_files/left_foot.txt" -PathType Leaf) -or
    -not(Test-Path -Path "$driveAndPathToParticipants/sub-$subjectId/data/func/timing_files/right_foot.txt" -PathType Leaf) -or
    -not(Test-Path -Path "$driveAndPathToParticipants/sub-$subjectId/data/func/timing_files/tongue.txt" -PathType Leaf)
  ) {
    
    Write-Host "Creating timing files for subject: sub-$subjectId" -ForegroundColor Green -BackgroundColor Black
    & matlab -batch "try, createTimingFiles $driveAndPathToParticipants sub-$subjectId; end;"
  }
  else {
    Write-Host "No need to create timing files for subject: sub-$subjectId" -ForegroundColor Green -BackgroundColor Black
  }




  Write-Host "STEP 7 of 8: MATLAB (3)" -ForegroundColor Green -BackgroundColor Black
  $step7jobs = foreach ($subjectId in $subjectList) {
    Write-Host "Processing Subject $subjectId" -ForegroundColor Green -BackgroundColor Black
    Start-Job -ScriptBlock { 
      param($driveAndPathToParticipants, $subjectId, $PSScriptRoot)
      Set-Location $PSScriptRoot;
      & matlab -batch "RunPreproc_1stLevel_job $driveAndPathToParticipants sub-$subjectId;"
    } -Name "matlab3-$subjectId" -ArgumentList $driveAndPathToParticipants, $subjectId, $PSScriptRoot;
  } 

  # Wait for Step 7 to complete for all subjects before continuing...
  Receive-Job $step7jobs -Wait -AutoRemoveJob

  Write-Host "STEP 8 of 8: MATLAB (4)" -ForegroundColor Green -BackgroundColor Black
  $step8jobs = foreach ($subjectId in $subjectList) {
    Write-Host "Processing Subject $subjectId" -ForegroundColor Green -BackgroundColor Black
    Start-Job -ScriptBlock { 
      param($driveAndPathToParticipants, $subjectId, $PSScriptRoot)
      Set-Location $PSScriptRoot;
      & matlab -batch "try, convertIntensityToCoordinates $driveAndPathToParticipants sub-$subjectId; end;"
    } -Name "matlab4-$subjectId" -ArgumentList $driveAndPathToParticipants, $subjectId, $PSScriptRoot;
  }

  # Wait for Step 8 to complete for all subjects before continuing...
  Receive-Job $step8jobs -Wait -AutoRemoveJob


}
######
# (END)
######
# ---------------------------------------