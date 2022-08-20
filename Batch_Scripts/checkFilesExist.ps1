$global:drive = 'C:\'
# Paths must begin from after the drive number. i.e., (C:\Users\... becomes \Users\...)
$global:pathToFreeSurferLicence = "Users/Reece/Documents/Dissertation/freesurfer/license.txt"
$global:pathToParticipants = "Users/Reece/Documents/Dissertation/Main/Participants"

$subjectList = Get-Content -Path $($global:driveAndPathToParticipants + '\file_list_HCP_all_subset.txt')
$filesToCheck = Get-Content $PSScriptRoot/filesToCheck.csv


foreach ($subjectId in $subjectList) {
  foreach ($filename in $filesToCheck) {
    Write-host $filename
    Get-ChildItem -Path 'C:/Users/Reece/Documents/Dissertation/Main/Participants/sub-' + $subjectId + '/' -Filter car.png -Recurse -ErrorAction SilentlyContinue -Force
    Write-host "next..."

    #-ErrorAction SilentlyContinue 
  }
}