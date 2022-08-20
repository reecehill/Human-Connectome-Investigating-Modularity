### TEMPLATE
<#
$jobName = "stepX-sub-${subjectId}"
$pso = New-Object psobject -property @{subjectId = $subjectId; driveAndPathToParticipants = $global:driveAndPathToParticipants; jobName = $jobName };
$job = Start-Job -Name ${jobName} -ArgumentList $global:driveAndPathToParticipants, $subjectId, $PSScriptRoot -ScriptBlock {
  param($global:driveAndPathToParticipants, $subjectId, $scriptLocation)
  Set-Location "$scriptLocation";
  # ACTION
};
Register-ObjectEvent -InputObject $job -EventName StateChanged -Action {
  Write-Host ("Job #" + $Event.MessageData.jobName + " complete.");
  Unregister-Event $EventSubscriber.SourceIdentifier;
  Remove-Job $EventSubscriber.SourceIdentifier;
  Remove-Job -Id $EventSubscriber.SourceObject.Id;
} -MessageData $pso | Out-Null;
Receive-Job -Job $job -Wait;
#>

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
$global:drive = 'C:\'
# Paths must begin from after the drive number. i.e., (C:\Users\... becomes \Users\...)
$global:pathToFreeSurferLicence = "Users/Reece/Documents/Dissertation/freesurfer/license.txt"
$global:pathToParticipants = "Users/Reece/Documents/Dissertation/Main/Participants"
$global:driveAndPathToParticipants = $($global:drive + $global:pathToParticipants)
$global:pathToDsiStudio = $global:drive + 'Users\Reece\Documents\Dissertation\dsi_studio_win'
$global:pathToSpmPackage = $global:drive + 'Program Files\MATLAB\R2021b\spm12'
#$global:numberOfTracts = 10000
$global:numberOfTracts = 10000000
$global:type = 2
$global:downsample = 'yes'
$global:rate = 0.1

<# 
**OVERVIEW OF SCRIPT**
As a brief overview, this script processes data in three parts. When prompted, you can instruct the script to begin from any one of these sections.
 ---1) Unprocessed: begin with raw, fMRI, DWI and MRI (T1 and T2) scans. Uses Freesurfer for surface extraction from T1/T2 data, and DSIStudio for streamline/tract detection.
 ---2) Structural: begin from pial surface files (aparc+aseg.nii) and DSIStudio tracts (1m0.trk) file. Matlab is used to convert tracts into same space, to assign anatomical labels to the surface files, and to compute a global connectivity matrix from the tracts.
 ---3) Functional: begin from the raw fMRI scan, and use SPM (Matlab) to perform 1st-level analysis and produce a binary volume of activated clusters.
 ---4) Overlay: take the output of (2) and (3) and independently sort their modules. The output is then the ROI surface with the modules assigned. Parts of the surface with modules from the two sections are also highlighted.    
 ---5) Statistics: take the output of (4), and calculate percentage overlap (measured in millimetres) for each fMRI condition (left hand, right hand etc.)
***
#>


# "motor" : https://openfmri.org/s3-browser/?prefix=ds000244
# "hcp": https://humanconnectome.org/study/hcp-young-adult
$global:dataSetToUse = Read-host 'As of 15/07/22, only the Motor dataset works. Which dataset do you wish to use? ([M]otor/[H]cp)'
$global:startAFresh = Read-host 'Delete all participant information and start afresh? (Y/N)'
$global:dataToUse = Read-host 'Which type of data do you wish to handle? [A]ll; [U]nprocessed data; [Str]uctural data; [F]unctional data; [O]verlay; [Sta]tistics. '

function getHcpData($subjectId, $dataToFetch) {
  if ($dataToFetch -eq "unprocessed") {
    $localDirectoryToCheck = $($global:driveAndPathToParticipants + '\' + $subjectId + '\T1w\')
    $localFileToCheck = 'T1.nii.gz'
    $localPathForInsert = $($localDirectoryToCheck + '/' + $localFileToCheck)
    # Set the host's filepath as that of _T1.nii.gz file. Note that we change the folder hierarchy.
    $remotePath = "s3://hcp-openaccess/HCP_1200/$subjectId/unprocessed/3T/T1w_MPR1/" + $subjectId + "_3T_T1w_MPR1.nii.gz"
    $recursive = ''
  }
  elseif ($dataToFetch -eq "structural") {
    # Set the directory in question as the subject's bert folder (the output of Freesurfer). We only check for aparc+aseg.mgz
    $localDirectoryToCheck = $($global:driveAndPathToParticipants + '\' + $subjectId + '\T1w\bert\')
    $localPathForInsert = $localDirectoryToCheck
    $localFileToCheck = 'mri/aparc+aseg.mgz'
    # Set the host's filepath as that of the subject's bert folder. Note that we change the folder hierarchy.
    $remotePath = "s3://hcp-openaccess/HCP_1200/$subjectId/T1w/$subjectId/"
    $recursive = '--recursive';
  }
  elseif ($dataToFetch -eq "diffusion") {
    # Set the directory in question as the subject's Diffusion data folder (for use in DSIStudio). We only check for data.nii.gz.
    $localDirectoryToCheck = $($global:driveAndPathToParticipants + '\' + $subjectId + '\T1w\Diffusion\')
    $localPathForInsert = $localDirectoryToCheck
    $localFileToCheck = 'data.nii.gz'
    # Set the host's filepath as that of the subject's Diffusion data folder (structural).
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
    Get-ChildItem -Path $($global:driveAndPathToParticipants + '/sub-' + $subjectId + '/') -Include $('sub-' + $subjectId + "*" + $filename) -Recurse -ErrorAction SilentlyContinue -Force
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

if ("Y" -eq $global:startAFresh) {
  # Remove # if folder cannot be deleted due to permissions issue.
  # Get-ChildItem -Recurse -Path $global:driveAndPathToParticipants | Set-ItemProperty -Name IsReadOnly -Value $false
  try {
    Rename-Item -Path $global:driveAndPathToParticipants -NewName $($global:driveAndPathToParticipants + '-old') -ErrorAction Stop
  }
  catch {
    Write-Host "There is a permissions issue with the Participants folder. Please manually delete the sub-folders within the Participants folder." -ForegroundColor Red -BackgroundColor Black
    exit;
  }
  New-Item -Path $global:driveAndPathToParticipants -ItemType Directory
  Copy-Item $($global:driveAndPathToParticipants + '-old/file_list_HCP_all_subset.txt') $($global:driveAndPathToParticipants + '/file_list_HCP_all_subset.txt')
  Copy-Item $($global:driveAndPathToParticipants + '-old/.gitignore') $($global:driveAndPathToParticipants + '/.gitignore')
  Remove-Item $($global:driveAndPathToParticipants + '-old') -Recurse
  Write-Host "The participant folder has been cleared. Please rerun the command and answer 'No'" -ForegroundColor Red -BackgroundColor Black
  exit;
}
elseif ("N" -eq $global:startAFresh) {
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

$global:subjectList = Get-Content -Path $($global:driveAndPathToParticipants + '\file_list_HCP_all_subset.txt')

. "${PSScriptRoot}/launch_functions.ps1";

if ($global:dataToUse -eq "A") {
  step1;
  step2;
  step3;
  step4;
  step5;
  step6;
  step7;
  step8;
}
elseif ($global:dataToUse -eq "U") {
  step1;
  step2;
}
elseif ($global:dataToUse -eq "Str") {
  step3;
  step4;
}
elseif ($global:dataToUse -eq "F") {
  #step5;
  #step6;
  step7;
}
elseif ($global:dataToUse -eq "O") {
  step8;
}
elseif ($global:dataToUse -eq "Sta") {
  Write-Host "This hasn't been coded yet!";
}
else {
  Write-Host "Error: Please type either A, U, Str, F, O or Sta.";
}