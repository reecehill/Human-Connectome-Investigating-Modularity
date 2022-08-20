$global:drive = 'C:\';
$global:pathToParticipants = "Users/Reece/Documents/Dissertation/Main/Participants"
$global:driveAndPathToParticipants = $($global:drive + $global:pathToParticipants)
$subjectList = Get-Content -Path $($global:driveAndPathToParticipants + '\file_list_HCP_all_subset.txt')

foreach ($subjectId in $subjectList) {
  $jobName = "HelloJob-${subjectId}";
  $pso = New-Object psobject -property @{test="ok"; test1="ok1"};
  $job = Start-Job -Name ${jobName} -ArgumentList $global:driveAndPathToParticipants -ScriptBlock {
    param($global:driveAndPathToParticipants);
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

