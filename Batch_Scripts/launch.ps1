# Paths must begin from after the drive number. i.e., (C:\Users\... becomes \Users\...)
$pathToFreeSurferLicence = "Users/Reece/Documents/Dissertation/freesurfer/license.txt"
$pathToParticipants = "Users/Reece/Documents/Dissertation/Main/Participants"

# The drive letter that contains all files. In format like - C:\
$drive = 'C:/'
$startAfresh = Read-host 'Delete all participant information and start afresh? (Y/N)'
$dataToUse = Read-host 'Begin with Freesurfer and unprocessed data [u], or retrieve preprocessed data and skip Freesurfer [p]?'
$subjectList = Get-Content -Path $($drive + $pathToParticipants+'\file_list_HCP_all_subset.txt')

if("Y" -eq $startAfresh) {
  Rename-Item $($drive + $pathToParticipants) $($drive + $pathToParticipants + '-old') -Force
  New-Item -Path $($drive + $pathToParticipants) -ItemType Directory
  Copy-Item $($drive + $pathToParticipants + '-old/file_list_HCP_all_subset.txt') $($drive + $pathToParticipants + '/file_list_HCP_all_subset.txt')
  Copy-Item $($drive + $pathToParticipants + '-old/.gitignore') $($drive + $pathToParticipants + '/.gitignore')
  Remove-Item $($drive + $pathToParticipants + '-old') -Recurse
  Write-Host "The participant folder has been cleared. Please rerun the command and answer 'No'".
  exit;
}
elseif("N" -eq $startAfresh) {
    # Loop through subjectIds
  foreach ($subjectId in $subjectList){

    if("u" -eq $dataToUse) {
      # Set the local directory as the subject's root. We only check it contains the _T1.nii.gz file.
      $rawFileDirectory = $($drive + $pathToParticipants + '\' + $subjectId + '\T1\')
      $rawFileName = $($subjectId) + '_T1.nii.gz'
      $rawFilePath = $($rawFileDirectory+$rawFileName)
      # Set the host's filepath as that of _T1.nii.gz file. Note that we change the folder hierarchy.
      $hostPath = "s3://hcp-openaccess/HCP_1200/$subjectId/unprocessed/3T/T1w_MPR1/"+$subjectId+"_3T_T1w_MPR1.nii.gz"
      $recursive = ''
    }
    elseif ("p" -eq $dataToUse) {
      # Set the directory in question as the subject's bert folder (the output of Freesurfer). We only check for aparc+aseg.mgz
      $rawFileDirectory = $($drive + $pathToParticipants + '\' + $subjectId + '\T1\bert\')
      $rawFileName = 'mri/aparc+aseg.mgz'
      $rawFilePath = $($rawFileDirectory+$rawFileName)
      # Set the host's filepath as that of the subject's bert folder. Note that we change the folder hierarchy.
      $hostPath = "s3://hcp-openaccess/HCP_1200/$subjectId/T1w/$subjectId/"
      $recursive = '--recursive'
    }
    else {
      Write-Host "Please ensure you enter either u or p.".
      exit;
    }

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

  # Launch WSL (Ubuntu 18 environment first)
  wsl -d "Ubuntu-18.04" -u reece /mnt/c/Users/Reece/Documents/Dissertation/Main/Batch_Scripts/freesurfer_batch.sh $("/mnt/c/"+$pathToFreeSurferLicence) $("/mnt/c/"+$pathToParticipants) "$dataToUse";
}
else {
  Write-Host "Ensure you enter either Y or N."
}
