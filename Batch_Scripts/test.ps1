$drive = 'C:\';
$pathToParticipants = "Users/Reece/Documents/Dissertation/Main/Participants"
$driveAndPathToParticipants = $($drive + $pathToParticipants)
$subjectList = Get-Content -Path $($driveAndPathToParticipants + '\file_list_HCP_all_subset.txt')

foreach ($subjectId in $subjectList) {
  $jobName = "HelloJob-${subjectId}";
  $pso = New-Object psobject -property @{test="ok"; test1="ok1"};
  $job = Start-Job -Name ${jobName} -ArgumentList $driveAndPathToParticipants -ScriptBlock {
    param($driveAndPathToParticipants);
    Write-Host "${driveAndPathToParticipants}";
    Sleep 3;
    Write-Host "ok";
  };
  Register-ObjectEvent -InputObject $job -EventName StateChanged -Action {
    Write-Host ("Job #"+$Event.MessageData.test1+" () complete.");
    Unregister-Event $EventSubscriber.SourceIdentifier;
    Remove-Job $EventSubscriber.SourceIdentifier;
    Remove-Job -Id $EventSubscriber.SourceObject.Id;
  } -MessageData $pso | Out-Null;
  Receive-Job -Job $job -Wait;
  #Wait-Job $job;
}

