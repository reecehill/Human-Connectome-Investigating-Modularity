Set-Location $pathToDsiStudio
Write-host "Commencing dsiBatch.ps1..."
Write-host "driveAndPathToParticipants: $driveAndPathToParticipants"
Write-host "subjectId: $subjectId"

if (!(Test-Path $driveAndPathToParticipants/$subjectId/T1w/Diffusion/logs -PathType Container)) {
    New-Item -ItemType Directory -Force -Path $driveAndPathToParticipants/$subjectId/T1w/Diffusion/logs
}

Write-host "Generating .src file for diffusion data of subject: $subjectId..."
Start-Process $pathToDsiStudio/dsi_studio.exe -ArgumentList "--action=src --source=$driveAndPathToParticipants/$subjectId/T1w/Diffusion/data.nii.gz --bval=$driveAndPathToParticipants/$subjectId/T1w/Diffusion/bvals --bvec=$driveAndPathToParticipants/$subjectId/T1w/Diffusion/bvecs --output=$driveAndPathToParticipants/$subjectId/T1w/Diffusion/data.src.gz" -wait -UseNewEnvironment -RedirectStandardOutput "$driveAndPathToParticipants/$subjectId/T1w/Diffusion/logs/dsi-src-output.log" -RedirectStandardError "$driveAndPathToParticipants/$subjectId/T1w/Diffusion/logs/dsi-src-error.log"

Write-host "Reconstructing image (.fib.gz) for diffusion data of subject: $subjectId..."
# Removed --csf_calibration=1 as it is no longer an option in DSI Studio (It may be included by default: https://groups.google.com/g/dsi-studio/c/dzJYDTdlDQo/m/NJGvdKXSBwAJ)
# Removed --output_rdi=0 --output_dif=0"  as no longer an option in DSI Studio (Have been moved to other_output: https://dsi-studio.labsolver.org/doc/cli_t2.html)
Start-Process $pathToDsiStudio/dsi_studio.exe -ArgumentList "--action=rec  --thread_count=4 --source=$driveAndPathToParticipants/$subjectId/T1w/Diffusion/data.src.gz --output=$driveAndPathToParticipants/$subjectId/T1w/Diffusion/data.src.gz.gqi.1.25.fib.gz --method=4 --param0=1.25 --scheme_balance=1 --check_btable=1" -wait -UseNewEnvironment -RedirectStandardOutput "$driveAndPathToParticipants/$subjectId/T1w/Diffusion/logs/dsi-rec-output.log" -RedirectStandardError "$driveAndPathToParticipants/$subjectId/T1w/Diffusion/logs/dsi-rec-error.log"


Write-host "Tracking fibres (1/10) for diffusion data of subject: $subjectId..."
Start-Process $pathToDsiStudio/dsi_studio.exe -ArgumentList "--action=trk --source=$driveAndPathToParticipants/$subjectId/T1w/Diffusion/data.src.gz.gqi.1.25.fib.gz --fiber_count=10000 --initial_dir=0 --thread_count=4 --fa_threshold=0.02908 --step_size=0.625 --turning_angle=60 --smoothing=0 --min_length=10 --max_length=300 --method=0 --ref=$driveAndPathToParticipants/$subjectId/T1w/bert/mri/aparc+aseg.nii --output=$driveAndPathToParticipants/$subjectId/T1w/Diffusion/1m0.trk" -wait -UseNewEnvironment -RedirectStandardOutput "$driveAndPathToParticipants/$subjectId/T1w/Diffusion/logs/dsi-trk-0-output.log" -RedirectStandardError "$driveAndPathToParticipants/$subjectId/T1w/Diffusion/logs/dsi-trk-0-error.log"

exit
