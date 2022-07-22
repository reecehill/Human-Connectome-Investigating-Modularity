$drive = 'C:\'
# Paths must begin from after the drive number. i.e., (C:\Users\... becomes \Users\...)
$pathToFreeSurferLicence = "Users/Reece/Documents/Dissertation/freesurfer/license.txt"
$pathToParticipants = "Users/Reece/Documents/Dissertation/Main/Participants"

$subjectList = Get-Content -Path $($driveAndPathToParticipants + '\file_list_HCP_all_subset.txt')
$filesToCheck = Get-Content $PSScriptRoot/filesToCheck.csv


foreach ($subjectId in $subjectList) {
  foreach ($filename in $filesToCheck) {
    Write-host $filename
    Get-ChildItem -Path 'C:/Users/Reece/Documents/Dissertation/Main/Participants/sub-' + $subjectId + '/' -Filter car.png -Recurse -ErrorAction SilentlyContinue -Force
    Write-host "next..."

    #-ErrorAction SilentlyContinue 
  }
}