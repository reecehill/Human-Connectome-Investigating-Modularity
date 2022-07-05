# Paths must begin from after the drive number. i.e., (C:\Users\... becomes \Users\...)
$pathToFreeSurferLicence = "Users/Reece/Documents/Dissertation/freesurfer/license.txt"
$pathToParticipants = "Users/Reece/Documents/Dissertation/Main/Participants"

# The drive letter that contains all files. In format like - C:\
$drive = 'C:/'

$startAfresh = Read-host 'Delete all participant information and start afresh? (Yes/No)'

$subjectList = Get-Content -Path $($drive + $pathToParticipants+'\file_list_HCP_all_subset.txt')

if("Yes" -eq $startAfresh) {
  Rename-Item $($drive + $pathToParticipants) $($drive + $pathToParticipants + '-old')
  New-Item -Path $($drive + $pathToParticipants) -ItemType Directory
  Copy-Item $($drive + $pathToParticipants + '-old/file_list_HCP_all_subset.txt') $($drive + $pathToParticipants + '/file_list_HCP_all_subset.txt')
  Copy-Item $($drive + $pathToParticipants + '-old/.gitignore') $($drive + $pathToParticipants + '/.gitignore')
  Remove-Item $($drive + $pathToParticipants + '-old') -Recurse
  Write-Host "The participant folder has been cleared. Please rerun the command and answer 'No'".
  exit;
}

# Loop through subjectIds
foreach ($subjectId in $subjectList){
  # Check that the raw data for this subject exists.
  $rawFileDirectory = $($drive + $pathToParticipants + '\' + $subjectId + '\unprocessed\3T\T1w_MPR1\')
  $rawFileName = $($subjectId) + '_3T_T1w_MPR1.nii.gz'
  $rawFilePath = $($rawFileDirectory+$rawFileName)
  if (-not(Test-Path -Path $rawFilePath -PathType Leaf)) {
    Write-Host "The file [$rawFilePath] does not exist."
     try {
         $null = New-Item $rawFileDirectory -itemType Directory -Force -ErrorAction Stop
         Write-Host "The directory [$rawFileDirectory] has been created."
         $hostPath = "s3://hcp-openaccess/HCP_1200/$subjectId/unprocessed/3T/T1w_MPR1/"+$subjectId+"_3T_T1w_MPR1.nii.gz"
         & "C:\Program Files\Amazon\AWSCLIV2\aws.exe" "s3" "cp" "$hostPath" "$rawFileDirectory"
         Write-Host "The file [$($rawFileDirectory+$rawFileName)] has now been created."

        }
     catch {
         throw $_.Exception.Message
     }
 }
}

# Launch WSL (Ubuntu 18 environment first)
wsl -d "Ubuntu-18.04" -u reece /mnt/c/Users/Reece/Documents/Dissertation/Main/Batch_Scripts/freesurfer_batch.sh $("/mnt/c/"+$pathToFreeSurferLicence) $("/mnt/c/"+$pathToParticipants);