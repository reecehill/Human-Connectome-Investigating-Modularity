Write-host "Commencing dsiBatch.ps1..."
$global:driveAndPathToParticipants = $args[0];
$subjectId = $args[1];
$global:pathToDsiStudio = $args[2];
$global:numberOfTracts = $args[3];
Set-Location $global:pathToDsiStudio
Write-host "driveAndPathToParticipants: $global:driveAndPathToParticipants"
Write-host "subjectId: $subjectId"

if (!(Test-Path $global:driveAndPathToParticipants/sub-$subjectId/logs -PathType Container)) {
    New-Item -ItemType Directory -Force -Path $global:driveAndPathToParticipants/sub-$subjectId/logs
}

if (!(Test-Path $global:driveAndPathToParticipants/sub-$subjectId/dsi-data -PathType Container)) {
    New-Item -ItemType Directory -Force -Path $global:driveAndPathToParticipants/sub-$subjectId/dsi-data
}
Invoke-Expression "$global:pathToDsiStudio/dsi_studio.exe --action=rec  --thread_count=10 --source=$global:driveAndPathToParticipants/sub-$subjectId/dsi-data/data.src.gz --output=$global:driveAndPathToParticipants/sub-$subjectId/dsi-data/data.src.gz.gqi.1.25.fib.gz --method=4 --param0=1.25 --scheme_balance=1 --check_btable=1"

Write-host "Generating .src file for diffusion data of subject: $subjectId..."

Start-Process $global:pathToDsiStudio/dsi_studio.exe -ArgumentList "--action=src --source=$global:driveAndPathToParticipants/sub-$subjectId/data/dwi/dwi.nii.gz --bval=$global:driveAndPathToParticipants/sub-$subjectId/data/dwi/bvals --bvec=$global:driveAndPathToParticipants/sub-$subjectId/data/dwi/bvecs --output=$global:driveAndPathToParticipants/sub-$subjectId/dsi-data/data.src.gz" -wait -UseNewEnvironment -RedirectStandardOutput "$global:driveAndPathToParticipants/sub-$subjectId/logs/src-output.log" -RedirectStandardError "$global:driveAndPathToParticipants/sub-$subjectId/logs/dsi-src-error.log"

Write-host "Reconstructing image (.fib.gz) for diffusion data of subject: $subjectId..."
# Removed --csf_calibration=1 as it is no longer an option in DSI Studio (It may be included by default: https://groups.google.com/g/dsi-studio/c/dzJYDTdlDQo/m/NJGvdKXSBwAJ)
# Removed --output_rdi=0 --output_dif=0"  as no longer an option in DSI Studio (Have been moved to other_output: https://dsi-studio.labsolver.org/doc/cli_t2.html)
Start-Process $global:pathToDsiStudio/dsi_studio.exe -ArgumentList "--action=rec  --thread_count=10 --source=$global:driveAndPathToParticipants/sub-$subjectId/dsi-data/data.src.gz --output=$global:driveAndPathToParticipants/sub-$subjectId/dsi-data/data.src.gz.gqi.1.25.fib.gz --method=4 --param0=1.25 --scheme_balance=1 --check_btable=1" -wait -UseNewEnvironment -RedirectStandardOutput "$global:driveAndPathToParticipants/sub-$subjectId/logs/dsi-rec-output.log" -RedirectStandardError "$global:driveAndPathToParticipants/sub-$subjectId/logs/dsi-rec-error.log"


Write-host "Tracking fibres for diffusion data of subject: $subjectId..."
Start-Process $global:pathToDsiStudio/dsi_studio.exe -ArgumentList "--action=trk --source=$global:driveAndPathToParticipants/sub-$subjectId/dsi-data/data.src.gz.gqi.1.25.fib.gz --fiber_count=$global:numberOfTracts --initial_dir=0 --thread_count=10 --fa_threshold=0.02908 --step_size=0.625 --turning_angle=60 --smoothing=0 --min_length=10 --max_length=300 --method=0 --ref=$global:driveAndPathToParticipants/sub-$subjectId/data/bert/mri/aparc+aseg.nii --output=$global:driveAndPathToParticipants/sub-$subjectId/dsi-data/1m0.trk" -wait -UseNewEnvironment -RedirectStandardOutput "$global:driveAndPathToParticipants/sub-$subjectId/logs/dsi-trk-0-output.log" -RedirectStandardError "$global:driveAndPathToParticipants/sub-$subjectId/logs/dsi-trk-0-error.log"