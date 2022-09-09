function step1() {
  ######
  # GET DATA (START, STEP 1)
  ######
  Write-Host "STEP 1 of 9: RETRIEVAL OF MISSING DATA" -ForegroundColor Green -BackgroundColor Black
  foreach ($subjectId in $subjectList) {
    Write-Host "Processing Subject $subjectId" -ForegroundColor Green -BackgroundColor Black
    $jobName = "step1-sub-${subjectId}"
    $pso = New-Object psobject -property @{subjectId = $subjectId; driveAndPathToParticipants = $driveAndPathToParticipants; jobName = $jobName };
    $job = Start-Job -Name ${jobName} -ArgumentList $driveAndPathToParticipants, $subjectId, $dataSetToUse, $PSScriptRoot -ScriptBlock {
      param($driveAndPathToParticipants, $subjectId, $dataSetToUse, $scriptLocation)
      Set-Location "$scriptLocation";
      if ("M" -eq $dataSetToUse) {
        Write-Host "Skipping checking for existence and/or downloading of Motor dataset..."
      }
      elseif ("H" -eq $dataSetToUse) {
        if ("U" -eq $dataToUse) {
          # Get only the T1 raw data, to be processed later.
          getHcpData $subjectId "unprocessed";
          getHcpData $subjectId "diffusion";
        }
        elseif ("S" -eq $dataToUse) {
          # Get the T1 raw data and the structural data from the HCP Freesurfer pipeline.
          getHcpData $subjectId "structural";
          getHcpData $subjectId "diffusion";
        }
        else {
          Write-Host "Please ensure you enter either U (for unprocessed data) or S (for structural data)." -ForegroundColor Red -BackgroundColor Black
          exit;
        }
      }
      else {
        Write-Host "Please ensure you enter either M (for Motor dataset) or H (for HumanConnectomeProject dataset - unsupported)." -ForegroundColor Red -BackgroundColor Black
        exit;
      }
    };
    Register-ObjectEvent -InputObject $job -EventName StateChanged -Action {
      Write-Host ("Job #" + $Event.MessageData.jobName + " complete.");
      Unregister-Event $EventSubscriber.SourceIdentifier;
      Remove-Job $EventSubscriber.SourceIdentifier;
      Remove-Job -Id $EventSubscriber.SourceObject.Id;
    } -MessageData $pso | Out-Null;
    Receive-Job -Job $job -Wait;
  } 
  ######
  # (END)
  ######
}


# ---------------------------------------

function step2() {
  ######
  # LAUNCH WSL AND FREESURFER (START, STEP 2-3)
  ######
  # Launch WSL (Ubuntu 18 environment)
  # We did loop through subjects inside Linux, but this led to unexpected behaviour where only the last subject was processed. For consistency, we loop through all here.
  Write-Host "STEP 2 of 9: FreeSurfer" -ForegroundColor Green -BackgroundColor Black
  foreach ($subjectId in $subjectList) {
    Write-Host "Processing Subject $subjectId" -ForegroundColor Green -BackgroundColor Black
    $jobName = "step2-sub-${subjectId}"
    $pso = New-Object psobject -property @{subjectId = $subjectId; driveAndPathToParticipants = $driveAndPathToParticipants; jobName = $jobName };
    $job = Start-Job -Name ${jobName} -ArgumentList $pathToFreeSurferLicence, $driveAndPathToParticipants, $subjectId, $pathToParticipants, $dataToUse, $PSScriptRoot -ScriptBlock {
      param($pathToFreeSurferLicence, $driveAndPathToParticipants, $subjectId, $pathToParticipants, $dataToUse, $scriptLocation)
      Set-Location "$scriptLocation";
      Write-Host "$driveAndPathToParticipants";


      if (Test-Path "$driveAndPathToParticipants/sub-$subjectId/data/bert") {
        Write-Host "Freesurfer output already exists..."
        Remove-Item "$driveAndPathToParticipants/sub-$subjectId/data/bert" -Force -Recurse -Confirm
      }
      wsl -d "Ubuntu-18.04" -u reece /mnt/c/Users/Reece/Documents/Dissertation/Main/Batch_Scripts/freesurferBatch.sh $("/mnt/c/" + $pathToFreeSurferLicence) $("/mnt/c/" + $pathToParticipants) "sub-$subjectId" "$dataToUse" 
    };
    Register-ObjectEvent -InputObject $job -EventName StateChanged -Action {
      Write-Host ("Job #" + $Event.MessageData.jobName + " complete.");
      # It is possible that freesurfer does not produce necessary symlinks. So once it's done, delete existing pial files/symlinks, and renew.
      #Remove-Item "$driveAndPathToParticipants\sub-$subjectId\data\bert\surf\lh.pial" -Force
      #Remove-Item "$driveAndPathToParticipants\sub-$subjectId\data\bert\surf\rh.pial" -Force
      cmd.exe /c mklink $event.MessageData.driveAndPathToParticipants+"\sub-"+$Event.MessageData.subjectId+"\data\bert\surf\lh.pial.windowsSymlink" $event.MessageData.driveAndPathToParticipants+"\sub-$subjectId\data\bert\surf\lh.pial.T2"
      cmd.exe /c mklink $event.MessageData.driveAndPathToParticipants+"\sub-"+$Event.MessageData.subjectId+"\data\bert\surf\rh.pial.windowsSymlink" $event.MessageData.driveAndPathToParticipants+"\sub-$subjectId\data\bert\surf\rh.pial.T2"
      Unregister-Event $EventSubscriber.SourceIdentifier;
      Remove-Job $EventSubscriber.SourceIdentifier;
      Remove-Job -Id $EventSubscriber.SourceObject.Id;
    } -MessageData $pso | Out-Null;
    Receive-Job -Job $job -Wait;
  }
  ######
  # (END)
  ######
}


# ---------------------------------------


function step3() {
  ######
  # LAUNCH DSI (START, STEP 4)
  ######
  Write-Host "STEP 3 of 9: DSIStudio" -ForegroundColor Green -BackgroundColor Black
  foreach ($subjectId in $subjectList) {
    Write-Host "Processing Subject $subjectId" -ForegroundColor Green -BackgroundColor Black
    $jobName = "step4-sub-" + $subjectId;
    $pso = New-Object psobject -property @{subjectId = $subjectId; driveAndPathToParticipants = $driveAndPathToParticipants; jobName = $jobName };
    $job = Start-Job -Name ${jobName}  -ScriptBlock {
      param($driveAndPathToParticipants, $subjectId, $pathToDsiStudio, $numberOfTracts, $scriptLocation);
      Set-Location $scriptLocation;
      & $($scriptLocation + '\dsiBatch.ps1') $driveAndPathToParticipants $subjectId $pathToDsiStudio $numberOfTracts | Out-Null;
    } -ArgumentList $driveAndPathToParticipants, $subjectId, $pathToDsiStudio, $numberOfTracts, $PSScriptRoot;
  
    Register-ObjectEvent -InputObject $job -EventName StateChanged -Action {
      Write-Host ("Job #" + $Event.MessageData.jobName + " complete.");
      Unregister-Event $EventSubscriber.SourceIdentifier;
      Remove-Job $EventSubscriber.SourceIdentifier;
      Remove-Job -Id $EventSubscriber.SourceObject.Id;
    } -MessageData $pso ;
    Receive-Job -Job $job -Wait;
  }
  ######
  # (END)
  ######
}


# ---------------------------------------


function step4() {
  ######
  # LAUNCH WSL AND MATLAB (START, STEP 5)
  ######
  Write-Host "STEP 4 of 9: MATLAB" -ForegroundColor Green -BackgroundColor Black
  foreach ($subjectId in $subjectList) {
    Write-Host "Processing Subject $subjectId" -ForegroundColor Green -BackgroundColor Black;
    $jobName = "step5-sub-${subjectId}"
    $pso = New-Object psobject -property @{subjectId = $subjectId; driveAndPathToParticipants = $driveAndPathToParticipants; jobName = $jobName };
    $job = Start-Job -Name ${jobName} -ArgumentList $driveAndPathToParticipants, $subjectId, $type, $downsample, $rate, $PSScriptRoot -ScriptBlock {
      param($driveAndPathToParticipants, $subjectId, $type, $downsample, $rate, $scriptLocation)
      Set-Location "$scriptLocation/../";
      & matlab -batch "batch_process $driveAndPathToParticipants/ sub-$subjectId $type $downsample $rate"
    };
    Register-ObjectEvent -InputObject $job -EventName StateChanged -Action {
      Write-Host ("Job #" + $Event.MessageData.jobName + " complete.");
      Write-Host ("Checking if all files were successfully created...");
      # Ensure files were successfully made.
      if (-not(Test-Path -Path $Event.MessageData.driveAndPathToParticipants + "/sub-" + $Event.MessageData.subjectId "/edgeList.mat" -PathType Leaf) -or
        -not(Test-Path -Path $Event.MessageData.driveAndPathToParticipants + "/sub-" + $Event.MessageData.subjectId + "/labelSRF.mat" -PathType Leaf) -or
        -not(Test-Path -Path $Event.MessageData.driveAndPathToParticipants + "/sub-" + $Event.MessageData.subjectId + "/matrices.mat" -PathType Leaf) -or
        -not(Test-Path -Path $Event.MessageData.driveAndPathToParticipants + "/sub-" + $Event.MessageData.subjectId + "/MNIcoor.mat" -PathType Leaf) -or
        -not(Test-Path -Path $Event.MessageData.driveAndPathToParticipants + "/sub-" + $Event.MessageData.subjectId + "/trsfmTrk.mat" -PathType Leaf)
      ) {
        Write-Host "Error during structural analysis: Subject sub-" + $Event.MessageData.subjectId + " is missing some output. Check the console log above for errors. You can delete all data and try again." -ForegroundColor Red -BackgroundColor Black
        exit;
      }
      else {
        Write-Host "---------------------------------------" -ForegroundColor Green -BackgroundColor Black
        Write-Host "Success for subject " + $Event.MessageData.subjectId + "! All output files from structural data were created successfully. You may wish to check the console above for any errors, though." -ForegroundColor Green -BackgroundColor Black
        Write-Host "---------------------------------------" -ForegroundColor Green -BackgroundColor Black
        Write-Host "_______________________________________" -ForegroundColor Green -BackgroundColor Black
        Write-Host "---------------------------------------" -ForegroundColor Green -BackgroundColor Black
        Write-Host "Now commencing analysis of functional MRI data..." -ForegroundColor Green -BackgroundColor Black
        Write-Host "---------------------------------------" -ForegroundColor Green -BackgroundColor Black
      }
      Unregister-Event $EventSubscriber.SourceIdentifier;
      Remove-Job $EventSubscriber.SourceIdentifier;
      Remove-Job -Id $EventSubscriber.SourceObject.Id;
    } -MessageData $pso | Out-Null;
    Receive-Job -Job $job -Wait;
  }
  ######
  # (END)
  ######
}


# ---------------------------------------


function step5() {
  ######
  # LAUNCH WSL AND MATLAB (START, STEP 6)
  ######
  # So the matlab function can be found, set to current location of this .ps1 file.
  Write-Host "STEP 5 of 9: MATLAB (2)" -ForegroundColor Green -BackgroundColor Black;
  foreach ($subjectId in $subjectList) {
    Write-Host "Processing Subject $subjectId" -ForegroundColor Green -BackgroundColor Black
    $jobName = "step6-sub-${subjectId}"
    $pso = New-Object psobject -property @{subjectId = $subjectId; driveAndPathToParticipants = $driveAndPathToParticipants; jobName = $jobName };
    # Ensure timing files are all created, if not, create them.
    if (
      -not(Test-Path -Path "$driveAndPathToParticipants/sub-$subjectId/data/func/timing_files/left_hand.txt" -PathType Leaf) -or
      -not(Test-Path -Path "$driveAndPathToParticipants/sub-$subjectId/data/func/timing_files/right_hand.txt" -PathType Leaf) -or
      -not(Test-Path -Path "$driveAndPathToParticipants/sub-$subjectId/data/func/timing_files/left_foot.txt" -PathType Leaf) -or
      -not(Test-Path -Path "$driveAndPathToParticipants/sub-$subjectId/data/func/timing_files/right_foot.txt" -PathType Leaf) -or
      -not(Test-Path -Path "$driveAndPathToParticipants/sub-$subjectId/data/func/timing_files/tongue.txt" -PathType Leaf)
    ) {
      $job = Start-Job -Name ${jobName} -ArgumentList $driveAndPathToParticipants, $subjectId, $PSScriptRoot -ScriptBlock {
        param($driveAndPathToParticipants, $subjectId, $scriptLocation)
        Set-Location "$scriptLocation";
        Write-Host "Creating timing files for subject: sub-$subjectId" -ForegroundColor Green -BackgroundColor Black;
        & matlab -batch "try, createTimingFiles $driveAndPathToParticipants sub-$subjectId; end;";
      }
    }
    else {
      $job = Start-Job -Name ${jobName} -ArgumentList $driveAndPathToParticipants, $subjectId, $PSScriptRoot -ScriptBlock {
        param($driveAndPathToParticipants, $subjectId, $scriptLocation)
        Set-Location "$scriptLocation/../";
        Write-Host "No need to create timing files for subject: sub-$subjectId" -ForegroundColor Green -BackgroundColor Black;
      };
    }
    Register-ObjectEvent -InputObject $job -EventName StateChanged -Action {
      Write-Host ("Job #" + $Event.MessageData.jobName + " complete.");
      Unregister-Event $EventSubscriber.SourceIdentifier;
      Remove-Job $EventSubscriber.SourceIdentifier;
      Remove-Job -Id $EventSubscriber.SourceObject.Id;
    } -MessageData $pso | Out-Null;
    Receive-Job -Job $job -Wait;
  };

  ######
  # (END)
  ######
}


#---------------------------------------


function step6() {
  ######
  Write-Host "STEP 6 of 9: MATLAB (3)" -ForegroundColor Green -BackgroundColor Black
  foreach ($subjectId in $subjectList) {
    Write-Host "Processing Subject $subjectId" -ForegroundColor Green -BackgroundColor Black
    $jobName = "step7-sub-${subjectId}"
    $pso = New-Object psobject -property @{subjectId = $subjectId; driveAndPathToParticipants = $driveAndPathToParticipants; jobName = $jobName };
    $job = Start-Job -Name ${jobName} -ArgumentList $driveAndPathToParticipants, $subjectId, $PSScriptRoot -ScriptBlock {
      param($driveAndPathToParticipants, $subjectId, $scriptLocation)
      Set-Location "$scriptLocation";
      & matlab -batch "RunPreproc_1stLevel_job $driveAndPathToParticipants sub-$subjectId;"
    };
    Register-ObjectEvent -InputObject $job -EventName StateChanged -Action {
      Write-Host ("Job #" + $Event.MessageData.jobName + " complete.");
      Unregister-Event $EventSubscriber.SourceIdentifier;
      Remove-Job $EventSubscriber.SourceIdentifier;
      Remove-Job -Id $EventSubscriber.SourceObject.Id;
    } -MessageData $pso | Out-Null;
    Receive-Job -Job $job -Wait;
  } 

  ######
  # (END)
  ######
}


# ---------------------------------------

function step7() {
  ######
  Write-Host "STEP 7 of 9: FreeSurfer (2)" -ForegroundColor Green -BackgroundColor Black
  foreach ($subjectId in $subjectList) {
    $jobName = "step7-sub-${subjectId}"
    $pso = New-Object psobject -property @{subjectId = $subjectId; driveAndPathToParticipants = $driveAndPathToParticipants; jobName = $jobName };
    $job = Start-Job -Name ${jobName} -ArgumentList $pathToFreeSurferLicence, $driveAndPathToParticipants, $pathToParticipants, $subjectId, $PSScriptRoot -ScriptBlock {
      param($pathToFreeSurferLicence, $driveAndPathToParticipants, $pathToParticipants, $subjectId, $scriptLocation)
      Set-Location "$scriptLocation";
      wsl -d "Ubuntu-18.04" -u reece /mnt/c/Users/Reece/Documents/Dissertation/Main/Batch_Scripts/freesurferGetMatrix.sh $("/mnt/c/" + $pathToFreeSurferLicence) $("/mnt/c/" + $pathToParticipants) "sub-$subjectId";
    };
    Register-ObjectEvent -InputObject $job -EventName StateChanged -Action {
      Write-Host ("Job #" + $Event.MessageData.jobName + " complete.");
      Unregister-Event $EventSubscriber.SourceIdentifier;
      Remove-Job $EventSubscriber.SourceIdentifier;
      Remove-Job -Id $EventSubscriber.SourceObject.Id;
    } -MessageData $pso | Out-Null;
    Receive-Job -Job $job -Wait;
  }
  ######
  # (END)
  ######
}


# ---------------------------------------

function step8() {
  ######
  Write-Host "STEP 8 of 10: MATLAB (4)" -ForegroundColor Green -BackgroundColor Black
  foreach ($subjectId in $subjectList) {
    Write-Host "Processing Subject $subjectId" -ForegroundColor Green -BackgroundColor Black
    $jobName = "step8-sub-${subjectId}"
    $pso = New-Object psobject -property @{subjectId = $subjectId; driveAndPathToParticipants = $driveAndPathToParticipants; jobName = $jobName };
    $job = Start-Job -Name ${jobName} -ArgumentList $driveAndPathToParticipants, $subjectId, $PSScriptRoot -ScriptBlock {
      param($driveAndPathToParticipants, $subjectId, $scriptLocation)
      Set-Location "$scriptLocation";
      & matlab -batch "RunPreproc_1stLevel_job_results $driveAndPathToParticipants sub-$subjectId;"
    };
    Register-ObjectEvent -InputObject $job -EventName StateChanged -Action {
      Write-Host ("Job #" + $Event.MessageData.jobName + " complete.");
      Unregister-Event $EventSubscriber.SourceIdentifier;
      Remove-Job $EventSubscriber.SourceIdentifier;
      Remove-Job -Id $EventSubscriber.SourceObject.Id;
    } -MessageData $pso | Out-Null;
    Receive-Job -Job $job -Wait;
  } 

  ######
  # (END)
  ######
}


function step9() {
  ######
  # (START)
  ######
  Write-Host "STEP 9 of 10: Matlab (5)" -ForegroundColor Green -BackgroundColor Black

  foreach ($subjectId in $subjectList) {
    $jobName = "step9-sub-${subjectId}"
    $pso = New-Object psobject -property @{subjectId = $subjectId; driveAndPathToParticipants = $driveAndPathToParticipants; jobName = $jobName };
    $job = Start-Job -Name ${jobName} -ArgumentList $driveAndPathToParticipants, $subjectId, $PSScriptRoot -ScriptBlock {
      param($driveAndPathToParticipants, $subjectId, $scriptLocation)
      Set-Location "$scriptLocation";
      & matlab -batch "mapDwiAndFmriToFaces_batch $driveAndPathToParticipants sub-$subjectId;"
    };
    Register-ObjectEvent -InputObject $job -EventName StateChanged -Action {
      Write-Host ("Job #" + $Event.MessageData.jobName + " complete.");
      Unregister-Event $EventSubscriber.SourceIdentifier;
      Remove-Job $EventSubscriber.SourceIdentifier;
      Remove-Job -Id $EventSubscriber.SourceObject.Id;
    } -MessageData $pso | Out-Null;
    Receive-Job -Job $job -Wait;
  }
  ######
  # (END)
  ######
}

function step10() {
  ######
  # (START)
  ######
  Write-Host "STEP 10 of 10: Matlab" -ForegroundColor Green -BackgroundColor Black

  foreach ($subjectId in $subjectList) {
    $jobName = "step10-sub-${subjectId}"
$pso = New-Object psobject -property @{subjectId = $subjectId; driveAndPathToParticipants = $driveAndPathToParticipants; jobName = $jobName };
$job = Start-Job -Name ${jobName} -ArgumentList $driveAndPathToParticipants, $subjectId, $PSScriptRoot -ScriptBlock {
  param($driveAndPathToParticipants, $subjectId, $scriptLocation)
  Set-Location "$scriptLocation";
  & matlab -batch "runStatistics_batch $driveAndPathToParticipants sub-$subjectId;"
};
Register-ObjectEvent -InputObject $job -EventName StateChanged -Action {
  Write-Host ("Job #" + $Event.MessageData.jobName + " complete.");
  Unregister-Event $EventSubscriber.SourceIdentifier;
  Remove-Job $EventSubscriber.SourceIdentifier;
  Remove-Job -Id $EventSubscriber.SourceObject.Id;
} -MessageData $pso | Out-Null;
Receive-Job -Job $job -Wait;
    }
    
}