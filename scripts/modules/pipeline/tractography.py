from pathlib import Path
import modules.globals as g
from modules.hcp_data_manager.downloader import getFile
from ..file_directory.file_directory import createDirectories
from modules.subprocess_caller.call import *
from shutil import copy2
from scipy.io.matlab import loadmat
from numpy import typing as npt
import numpy as np
import ants
import pandas as pd
import nibabel as nib


def runDsiStudio(subjectId: str) -> bool:
    return (
        generateSrcFile(subjectId)
        and reconstructImage(subjectId)
        and trackFibres(subjectId)
        and registerFibresToMNI152(subjectId)
        # and registerDsiStudioTemplateToSubject(subjectId) # No longer used
    )


def generateSrcFile(subjectId: str) -> bool:
    import config

    if config.DSI_STUDIO_USE_RECONST:
        sourceFile = getFile(
            localPath=config.SUBJECT_DIR
            / "T1w"
            / config.DIFFUSION_FOLDER
            / "data.nii.gz"
        )
        bval = getFile(
            localPath=config.SUBJECT_DIR / "T1w" / config.DIFFUSION_FOLDER / "bvals"
        )
        bvec = getFile(
            localPath=config.SUBJECT_DIR / "T1w" / config.DIFFUSION_FOLDER / "bvecs"
        )

        # The destination file need not exist locally already, but its folders must.
        destinationFolder = config.SUBJECT_DIR / "T1w" / config.DIFFUSION_FOLDER
        createDirectories(
            directoryPaths=[destinationFolder],
            createParents=True,
            throwErrorIfExists=False,
        )

        destinationFile: str = str(destinationFolder / "data.src.gz")
        g.logger.info("Running DSI Studio: generate Src file.")

        return call(
            cmdLabel="DSI Studio",
            cmd=[
                config.DSI_STUDIO.__str__(),
                "--action=src",
                f"--source={sourceFile}",
                f"--bval={bval}",
                f"--bvec={bvec}",
                f"--output={destinationFile}",
            ],
        )
    else:
        return True
        # If we use BedpostX data, we do not need to generate a .src file.


def reconstructImage(subjectId: str) -> bool:
    import config

    # The destination file need not exist locally already, but its folders must.
    destinationFolder = config.SUBJECT_DIR / "T1w" / config.DIFFUSION_FOLDER
    createDirectories(
        directoryPaths=[destinationFolder], createParents=True, throwErrorIfExists=False
    )

    if config.DSI_STUDIO_USE_RECONST:
        sourceFile = Path(
            config.SUBJECT_DIR / "T1w" / config.DIFFUSION_FOLDER / "data.src.gz"
        ).resolve(strict=True)
        threadCount = config.CPU_THREADS  # Default: CPU number.
        method = config.DSI_STUDIO_RECONSTRUCTION_METHOD
        maskFile = getFile(
            localPath=config.SUBJECT_DIR
            / "T1w"
            / config.DIFFUSION_FOLDER
            / "nodif_brain_mask.nii.gz"
        )

        if config.NORMALISE_TO_MNI152:
            destinationFile: str = str(
                destinationFolder / ("automated_" + "data.src.gz.gqi.1.25.fib.gz")
            )

            # TODO: Convert the filename to parameter.
            # refFile = getFile(localPath=config.SUBJECT_DIR / "MNINonLinear" / "T1w_restore_brain.nii.gz" )
            # refFile = getFile(localPath=config.SUBJECT_DIR / "T1w" / "T1w_acpc_dc_restore_brain.nii.gz" )
            refFile = getFile(
                localPath=config.SUBJECT_DIR
                / "T1w"
                / "T1w_acpc_dc_restore_brain.nii.gz"
            )
            copiedRefFile = (
                config.SUBJECT_DIR
                / "T1w"
                / ("automated_" + "T1w_acpc_dc_restore_brain.nii.gz")
            )

            refFile = copy2(refFile, copiedRefFile)
        else:
            refFile = "NOT-SET"  # TODO
            # TODO: Does this need to change if not mni?
            destinationFile: str = str(
                destinationFolder / "data.src.gz.gqi.1.25.fib.gz"
            )

        # processedFile: str = str(destinationFolder / 'data_proc.nii.gz')
        g.logger.info("Running DSI Studio: reconstructing image (.fib.gz).")
        return call(
            cmdLabel="DSIStudio",
            cmd=[
                config.DSI_STUDIO,
                "--action=rec",
                f"--source={sourceFile}",
                f"--align_acpc=0",
                f"--align_to={refFile}",
                f"--motion_correction=1",
                f"--template=0",
                # f'--save_nii={processedFile}',
                f"--method={method}",
                f"--mask={maskFile}",
                f"--thread_count={threadCount}",
                f"--output={destinationFile}",
                f"--param0=1.25",
                f"--record_odf=1",
                f"--dti_no_high_b=1",
                f"--check_btable=1",
                f"--other_output=all",
            ],
        )
    else:
        # Ensure Bedpost files exist.
        subjectDir = config.SUBJECT_DIR / "T1w"
        filesToExist = [
            (subjectDir / "Diffusion.bedpostX" / "mean_f1samples.nii.gz"),
            (subjectDir / "Diffusion.bedpostX" / "mean_f2samples.nii.gz"),
            (subjectDir / "Diffusion.bedpostX" / "mean_f3samples.nii.gz"),
            (subjectDir / "Diffusion.bedpostX" / "mean_ph1samples.nii.gz"),
            (subjectDir / "Diffusion.bedpostX" / "mean_ph2samples.nii.gz"),
            (subjectDir / "Diffusion.bedpostX" / "mean_ph3samples.nii.gz"),
            (subjectDir / "Diffusion.bedpostX" / "mean_th1samples.nii.gz"),
            (subjectDir / "Diffusion.bedpostX" / "mean_th2samples.nii.gz"),
            (subjectDir / "Diffusion.bedpostX" / "mean_th3samples.nii.gz"),
        ]
        _ = [getFile(localPath=fileToExist) for fileToExist in filesToExist]

        return call(
            cmdLabel="MATLAB",
            cmd=[
                config.MATLAB,
                f'-batch "bedpostXtoDsiStudio {config.matLabDriveAndPathToSubjects} {subjectId}"',
            ],
            cwd=config.matlabScriptsFolder,
        )


def trackFibres(subjectId: str) -> bool:
    import config

    if config.NORMALISE_TO_MNI152:
        sourceFile = Path(
            config.SUBJECT_DIR
            / "T1w"
            / config.DIFFUSION_FOLDER
            / (
                ("automated_" + "data.src.gz.gqi.1.25.fib.gz")
                if config.DSI_STUDIO_USE_RECONST
                else "automated.fib"
            )
        ).resolve(strict=True)

        # The destination file need not exist locally already, but its folders must.
        destinationFolder = config.SUBJECT_DIR / "T1w" / config.DIFFUSION_FOLDER

        createDirectories(
            directoryPaths=[destinationFolder, destinationFolder / "dsistudio"],
            createParents=True,
            throwErrorIfExists=False,
        )

        refFile = getFile(localPath=config.SUBJECT_DIR / "T1w" / "aparc+aseg.nii.gz")
        copiedRefFile = (
            config.SUBJECT_DIR / "T1w" / ("automated_reg_" + "aparc+aseg.nii.gz")
        )
        copy2(refFile, copiedRefFile)
        refFile = copiedRefFile

        # Needed when using bedpostX reconstructed images. As --other_slices
        t1wFile = getFile(
            localPath=config.SUBJECT_DIR / "T1w" / "T1w_acpc_dc_restore_brain.nii.gz"
        )
        copiedT1wFile = (
            config.SUBJECT_DIR
            / "T1w"
            / ("automated_reg_" + "T1w_acpc_dc_restore_brain.nii.gz")
        )
        copy2(t1wFile, copiedT1wFile)
        t1wFile = copiedT1wFile

    else:
        t1wFile = "NOT-SET-TODO"  # TODO
        sourceFile = Path(
            config.SUBJECT_DIR
            / "T1w"
            / config.DIFFUSION_FOLDER
            / (
                "data.src.gz.gqi.1.25.fib.gz"
                if config.DSI_STUDIO_USE_RECONST
                else "automated.fib"
            )
        ).resolve(strict=True)

        # The destination file need not exist locally already, but its folders must.
        destinationFolder = config.SUBJECT_DIR / "T1w" / config.DIFFUSION_FOLDER
        createDirectories(
            directoryPaths=[destinationFolder, destinationFolder / "dsistudio"],
            createParents=True,
            throwErrorIfExists=False,
        )

        refFile = getFile(
            localPath=config.SUBJECT_DIR / "T1w" / "T1w_restore_brain.nii.gz"
        )

    if config.DSI_STUDIO_USE_ROI:
        createRoiFiles(subjectId)

    iterationSuccess: "list[bool]" = []
    for currentIteration in range(0, config.DSI_STUDIO_ITERATION_COUNT, 1):
        destinationFile: str = str(
            destinationFolder / ("1m" + str(currentIteration) + ".trk")
        )
        # destinationFile_template: str = str(destinationFolder / ('template_'+'1m'+str(currentIteration)+'.trk') )

        cmd = [
            config.DSI_STUDIO,
            "--action=trk",
            f"--source={sourceFile}",
            f"--random_seed={str(config.DSI_STUDIO_RANDOM_SEED)}",  # Set seed for reproducability
            f"--thread_count={config.CPU_THREADS}",
            # f'--output={destinationFolder / "dsistudio"}',
            f"--fiber_count={config.DSI_STUDIO_FIBRE_COUNT}",
            f"--seed_count={config.DSI_STUDIO_SEED_COUNT}",
            f"--method={config.DSI_STUDIO_TRACKING_METHOD}",
            f"--fa_threshold={config.DSI_STUDIO_FA_THRESH}",
            f"--step_size={config.DSI_STUDIO_STEP_SIZE}",
            f"--turning_angle={config.DSI_STUDIO_TURNING_ANGLE}",
            f"--smoothing={config.DSI_STUDIO_SMOOTHING}",
            f"--min_length={config.DSI_STUDIO_MIN_LENGTH}",
            f"--max_length={config.DSI_STUDIO_MAX_LENGTH}",
            # f'--ref={refFileMni152}',
            # f'--template_track={destinationFile_template}',
            f"--check_ending={config.DSI_STUDIO_CHECK_ENDING}",
            f"--ref={refFile}",
        ]

        if config.DSI_STUDIO_USE_RECONST == False:
            cmd = cmd + [f"--other_slices={Path(t1wFile).resolve(True)}"]

        # Limit tracks to only those that pass through the precentral gyri.
        lhTractFile: str = destinationFile.replace("/1m", "/" + "L_" + "1m")
        lhEndPointsFile: str = lhTractFile.replace(".trk", ".mat")
        rhTractFile: str = destinationFile.replace("/1m", "/" + "R_" + "1m")
        rhEndPointsFile: str = rhTractFile.replace(".trk", ".mat")

        # Run command on left hemisphere.
        lhCmd = cmd.copy()
        lhCmd = lhCmd + [
            f"--tip_iteration=16",
            f"--output={lhTractFile}",
            f"--end_point={lhEndPointsFile}",
        ]

        # Run command on right hemisphere.
        rhCmd = cmd.copy()
        rhCmd = rhCmd + [
            f"--tip_iteration=16",
            f"--output={rhTractFile}",
            f"--end_point={rhEndPointsFile}",
        ]
        del cmd
        
        if config.DSI_STUDIO_USE_ROI:
            if config.NORMALISE_TO_MNI152:
                lhRoiFilePath_dti: Path = Path(
                    str(
                        config.SUBJECT_DIR
                        / "T1w"
                        / config.IMAGES["T1w"]["STANDARD_RES"]["MASKS"]["LEFT"]
                    ).replace(".nii.gz", ".dti_space.nii.gz")
                ).resolve(strict=True)
                lhCmd = lhCmd + [
                    # f'--lim={roiFile.resolve(strict=True)},dilation',
                    f"--seed={lhRoiFilePath_dti}",
                    # f'--end2={roiFile.resolve(strict=True)},dilation',
                    f"--nend={lhRoiFilePath_dti},negate",
                ]
                rhRoiFilePath_dti: Path = Path(
                    str(
                        config.SUBJECT_DIR
                        / "T1w"
                        / config.IMAGES["T1w"]["STANDARD_RES"]["MASKS"]["RIGHT"]
                    ).replace(".nii.gz", ".dti_space.nii.gz")
                ).resolve(strict=True)
                rhCmd = rhCmd + [
                    # f'--lim={roiFile.resolve(strict=True)},dilation',
                    f"--seed={rhRoiFilePath_dti}",
                    # f'--end2={roiFile.resolve(strict=True)},dilation',
                    f"--nend={rhRoiFilePath_dti},negate",
                ]
            else:
                g.logger.error("ROI files are not yet supported for non-MNI152 normalisation.")
        else:
            g.logger.info("ROI files are not used.")

        iterationSuccess.append(call(cmdLabel="DSIStudio", cmd=lhCmd))
        iterationSuccess.append(call(cmdLabel="DSIStudio", cmd=rhCmd))
        iterationSuccess.append(
            mergeTracts(sourceFile, lhTractFile, rhTractFile, destinationFile)
        )

        # ----------------------------------------------------------------
        # Export tracts as an image too
        # ----------------------------------------------------------------
        iterationSuccess.append(
            call(
                cmdLabel="DSIStudio",
                cmd=[
                    config.DSI_STUDIO,
                    "--action=ana",
                    f"--source={str(sourceFile)}",
                    f"--tract={str(destinationFile)}",
                    f"--other_slices={str(refFile)}",
                    f"--output={destinationFile.replace('.trk', '.nii.gz')}",
                ],
            )
        )
        iterationSuccess.append(
            call(
                cmdLabel="FSL: fslcpgeom",
                cmd=[
                    "fslcpgeom",
                    f"{str(refFile)}",
                    f"{destinationFile.replace('.trk', '.nii.gz')}",
                    "-d",
                ],
            )
        )
        iterationSuccess.append(
            call(
                cmdLabel="Freesurfer: mri_convert",
                cmd=[
                    "mri_convert",
                    "--in_orientation",
                    "LPS",
                    "--out_orientation",
                    "LAS",
                    "-rt",
                    "nearest",  # Nearest neighbour resampling
                    f"{destinationFile.replace('.trk', '.nii.gz')}",
                    f"{destinationFile.replace('.trk', '_negy.nii.gz')}",
                ],
            )
        )

    g.logger.info("Running DSI Studio: tracking fibres.")
    return all(iterationSuccess)


def convertFnirtTransformIntoITK(subjectId: str) -> bool:
    import config

    fnirtTransformationFile = (
        config.SUBJECT_DIR / "MNINonLinear" / "xfms" / "standard2acpc_dc.nii.gz"
    )
    srcFile = config.SUBJECT_DIR / "MNINonLinear" / "T1w_restore.nii.gz"

    remoteFilesToExist = [fnirtTransformationFile, srcFile]
    _ = [getFile(localPath=fileToExist) for fileToExist in remoteFilesToExist]
    cmd = [
        config.WB_COMMAND,
        "-convert-warpfield",
        "-from-fnirt",
        # "-from-world",
        str(fnirtTransformationFile),
        str(srcFile),
        "-to-itk",
        str(fnirtTransformationFile).replace(".nii.gz", "_ants.nii.gz"),
    ]
    return call(cmdLabel="wb_command", cmd=cmd)


def registerFibresToMNI152(subjectId: str) -> bool:
    import config

    # Generate transformation file in ANTS format.
    convertFnirtTransformIntoITK(subjectId)

    nonlinearTransformationFile = (
        config.SUBJECT_DIR / "MNINonLinear" / "xfms" / "standard2acpc_dc_ants.nii.gz"
    )
    remoteFilesToExist = [nonlinearTransformationFile]
    _ = [getFile(localPath=fileToExist) for fileToExist in remoteFilesToExist]
    if config.NORMALISE_TO_MNI152:
        destinationFolder = config.SUBJECT_DIR / "T1w" / config.DIFFUSION_FOLDER
    else:
        raise Exception("Logic needed if MNI152 normalisation is disabled.")

    for currentIteration in range(0, config.DSI_STUDIO_ITERATION_COUNT, 1):
        # ----------------------------------------------------------------
        # Ensure files exist
        # ----------------------------------------------------------------
        # We use the diffusion mask just because its a small file and we need header only.
        diffusionMask = (
            config.SUBJECT_DIR / "T1w" / "Diffusion" / "nodif_brain_mask.nii.gz"
        )
        refFile = config.SUBJECT_DIR / "T1w" / "aparc+aseg.nii.gz"

        remoteFilesToExist = [refFile, diffusionMask]
        localFilesToExist = []
        destinationFile: str = str(
            destinationFolder / ("1m" + str(currentIteration) + ".trk")
        )
        lhTractFile: str = destinationFile.replace("/1m", "/" + "L_" + "1m")
        lhEndPointsFile: str = lhTractFile.replace(".trk", ".mat")
        localFilesToExist.append(Path(lhEndPointsFile))
        rhTractFile: str = destinationFile.replace("/1m", "/" + "R_" + "1m")
        rhEndPointsFile: str = rhTractFile.replace(".trk", ".mat")
        localFilesToExist.append(Path(rhEndPointsFile))

        _ = [getFile(localPath=fileToExist) for fileToExist in remoteFilesToExist]
        _ = [
            getFile(localPath=fileToExist, localOnly=True)
            for fileToExist in localFilesToExist
        ]

        # ----------------------------------------------------------------
        # Transform the coordinates and save as .csv
        # ----------------------------------------------------------------
        lhEndPointsFileMat: npt.NDArray = loadmat(lhEndPointsFile)["end_points"].T
        rhEndPointsFileMat: npt.NDArray = loadmat(rhEndPointsFile)["end_points"].T

        # Load NIfTI files
        anatomical_info = nib.load(f"{refFile}").header  # type:ignore
        diffusion_info = nib.load(f"{diffusionMask}").header  # type:ignore

        # Get pixel dimensions (voxel sizes)
        anatomical_voxel_size: float = anatomical_info.get_zooms()[:3]  # type:ignore
        diffusion_voxel_size: float = diffusion_info.get_zooms()[:3]  # type:ignore

        # Compute the sampling ratio
        sampling_ratio = np.array(anatomical_voxel_size) / np.array(
            diffusion_voxel_size
        )

        y_dim: int = anatomical_info.get_data_shape()[1]  # type:ignore
        # Create the T_to_dif matrix
        T_to_dif = np.array(
            [
                [sampling_ratio[0], 0.0, 0.0, 0.0],
                [0.0, -sampling_ratio[1], 0.0, y_dim * sampling_ratio[1]],
                [0.0, 0.0, sampling_ratio[2], 0.0],
                [0.0, 0.0, 0.0, 1.0],
            ]
        )
        T_RAS_to_LPS = np.array(
            [
                [-1, 0.0, 0.0, 0],
                [0.0, -1, 0.0, 0],
                [0.0, 0.0, 1, 0.0],
                [0.0, 0.0, 0.0, 1.0],
            ]
        )

        # Add column of ones to coordinates.
        lhEndPointsFileMat_ones = np.hstack(
            [lhEndPointsFileMat, np.ones((lhEndPointsFileMat.shape[0], 1))]
        ).T
        rhEndPointsFileMat_ones = np.hstack(
            [rhEndPointsFileMat, np.ones((rhEndPointsFileMat.shape[0], 1))]
        ).T

        # Transform the coordinates
        lhEndPointsFileMat_in_t1 = (
            np.linalg.inv(T_to_dif).dot(lhEndPointsFileMat_ones).T
        )
        rhEndPointsFileMat_in_t1 = (
            np.linalg.inv(T_to_dif).dot(rhEndPointsFileMat_ones).T
        )

        np.savetxt(
            f"{lhEndPointsFile.replace('.mat', '_int1w.csv')}",
            lhEndPointsFileMat_in_t1,
            delimiter=",",
            header="x,y,z,t",
            comments="",
            fmt="%.6f",
        )
        np.savetxt(
            f"{rhEndPointsFile.replace('.mat', '_int1w.csv')}",
            rhEndPointsFileMat_in_t1,
            delimiter=",",
            header="x,y,z,t",
            comments="",
            fmt="%.6f",
        )
        np.savetxt(
            f"{destinationFile.replace('.trk', '.csv')}",
            np.vstack((lhEndPointsFileMat_in_t1, rhEndPointsFileMat_in_t1)),
            delimiter=",",
            header="x,y,z,t",
            comments="",
            fmt="%.6f",
        )

        # lhEndPointsFileMat_in_t1 stores the coordinates in CRS (RAS) format. We need to convert these to real world coordinates (*sform) and then to LPS for ANTS.
        sform: npt.NDArray = anatomical_info.get_sform()  # type:ignore
        lhEndPointsFileMat_in_t1_xyz = sform.dot(lhEndPointsFileMat_in_t1.T)
        rhEndPointsFileMat_in_t1_xyz = sform.dot(rhEndPointsFileMat_in_t1.T)

        # Now convert to LPS.
        lhEndPointsFileMat_in_t1_xyz_lps = T_RAS_to_LPS.dot(
            lhEndPointsFileMat_in_t1_xyz
        )
        rhEndPointsFileMat_in_t1_xyz_lps = T_RAS_to_LPS.dot(
            rhEndPointsFileMat_in_t1_xyz
        )

        lhEndPointsFileMat_MNI152_xyz_warped: npt.NDArray = (
            ants.apply_transforms_to_points(  # type:ignore
                3,
                pd.DataFrame(
                    lhEndPointsFileMat_in_t1_xyz_lps.T,
                    columns=["x", "y", "z", "t"],
                ),
                [str(nonlinearTransformationFile.resolve(strict=True))],
                verbose=True,
            )
        ).to_numpy()
        rhEndPointsFileMat_MNI152_xyz_warped: npt.NDArray = (
            ants.apply_transforms_to_points(  # type:ignore
                3,
                pd.DataFrame(
                    rhEndPointsFileMat_in_t1_xyz_lps.T,
                    columns=["x", "y", "z", "t"],
                ),
                [str(nonlinearTransformationFile.resolve(strict=True))],
                verbose=True,
            )
        ).to_numpy()

        # Now revert back to RAS
        lhEndPointsFileMat_MNI152_xyz_ras_warped = (
            np.linalg.inv(T_RAS_to_LPS).dot(lhEndPointsFileMat_MNI152_xyz_warped.T).T
        )
        rhEndPointsFileMat_MNI152_xyz_ras_warped = (
            np.linalg.inv(T_RAS_to_LPS).dot(rhEndPointsFileMat_MNI152_xyz_warped.T).T
        )

        # Now revert back to CRS
        lhEndPointsFileMat_MNI152_ijk_ras_warped = (
            np.linalg.inv(sform).dot(lhEndPointsFileMat_MNI152_xyz_ras_warped.T).T
        )
        rhEndPointsFileMat_MNI152_ijk_ras_warped = (
            np.linalg.inv(sform).dot(rhEndPointsFileMat_MNI152_xyz_ras_warped.T).T
        )

        lhEndPointsFileMat_MNI152_warped = lhEndPointsFileMat_MNI152_ijk_ras_warped
        rhEndPointsFileMat_MNI152_warped = rhEndPointsFileMat_MNI152_ijk_ras_warped

        np.savetxt(
            f"{lhEndPointsFile.replace('.mat', '_int1w_mni.csv')}",
            lhEndPointsFileMat_MNI152_warped,
            delimiter=",",
            header="x,y,z,t",
            comments="",
            fmt="%.6f",
        )
        np.savetxt(
            f"{rhEndPointsFile.replace('.mat', '_int1w_mni.csv')}",
            rhEndPointsFileMat_MNI152_warped,
            delimiter=",",
            header="x,y,z,t",
            comments="",
            fmt="%.6f",
        )
        np.savetxt(
            f"{destinationFile.replace('.trk', '_int1w_mni.csv')}",
            np.vstack(
                (lhEndPointsFileMat_MNI152_warped, rhEndPointsFileMat_MNI152_warped)
            ),
            delimiter=",",
            header="x,y,z,t",
            comments="",
            fmt="%.6f",
        )

    return True


def registerFibresToT1w(subjectId: str) -> bool:
    import config

    # Flip y dimension (LPS -> LAS)
    # fslswapdim ./HCIM/core/Human-Connectome-Investigating-Modularity/data/subjects/100206/T1w/Diffusion/whole_brain_in_T1w_acpc_dc_restore_brain_headers.tt.nii x -y z ./HCIM/core/Human-Connectome-Investigating-Modularity/data/subjects/100206/T1w/Diffusion/whole_brain_in_T1w_acpc_dc_restore_brain_headers_negy.tt.nii

    # Set sform to match T1w
    # fslorient -setsform $(fslorient -getsform ./HCIM/core/Human-Connectome-Investigating-Modularity/data/subjects/100206/T1w/aparc+aseg.nii.gz) ./HCIM/core/Human-Connectome-Investigating-Modularity/data/subjects/100206/T1w/Diffusion/whole_brain_in_T1w_acpc_dc_restore_brain_headers_negy.tt.nii.gz

    # Get tracts in MNINonLinear space
    # applywarp -r ./HCIM/core/Human-Connectome-Investigating-Modularity/data/subjects/100206/MNINonLinear/T1w.nii.gz -i ./HCIM/core/Human-Connectome-Investigating-Modularity/data/subjects/100206/T1w/Diffusion/whole_brain_in_T1w_acpc_dc_restore_brain_headers_negy.tt.nii.gz -w ./HCIM/core/Human-Connectome-Investigating-Modularity/data/subjects/100206/MNINonLinear/xfms/acpc_dc2standard.nii.gz -o ./HCIM/core/Human-Connectome-Investigating-Modularity/data/subjects/100206/MNINonLinear/trks_warped_from_acpc.nii.gz -vv

    # ? Now how to do this for coordinates?
    # First, convert transform (FNIRT) in ANTS
    # wb_command -convert-warpfield -from-fnirt ./HCIM/core/Human-Connectome-Investigating-Modularity/data/subjects/100206/MNINonLinear/xfms/acpc_dc2standard.nii.gz ./HCIM/core/Human-Connectome-Investigating-Modularity/data/subjects/100206/T1w/T1w_acpc_dc_restore.nii.gz -to-itk ./HCIM/core/Human-Connectome-Investigating-Modularity/data/subjects/100206/MNINonLinear/xfms/acpc_dc2standard_ants.nii.gz

    # Then apply the transformation to the coords
    # antsApplyTransformsToPoints -d 3 -i ./HCIM/core/Human-Connectome-Investigating-Modularity/data/subjects/100206/T1w/Diffusion/L_1m0.csv -o ./HCIM/core/Human-Connectome-Investigating-Modularity/data/subjects/100206/T1w/Diffusion/L_1m0_warped.csv -t ./HCIM/core/Human-Connectome-Investigating-Modularity/data/subjects/100206/MNINonLinear/xfms/acpc_dc2standard_ants.nii.gz -p

    # For proof, you can visualise the same transform on images
    # antsApplyTransforms -d 3 -i ./HCIM/core/Human-Connectome-Investigating-Modularity/data/subjects/100206/T1w/T1w_acpc_dc_restore.nii.gz -r ./HCIM/core/Human-Connectome-Investigating-Modularity/data/subjects/100206/MNINonLinear/T1w_restore.nii.gz -o ./HCIM/core/Human-Connectome-Investigating-Modularity/data/subjects/100206/T1w/test.nii.gz -t ./HCIM/core/Human-Connectome-Investigating-Modularity/data/subjects/100206/MNINonLinear/xfms/acpc_dc2standard_ants.nii.gz
    return True


def registerDsiStudioTemplateToSubject(subjectId: str) -> bool:
    import config

    # TODO: Is mov correctly set in non-MNI152 settings?
    targ = getFile(
        config.SCRIPTS_DIR
        / "matlab"
        / "toolboxes"
        / "DsiStudio"
        / "atlas"
        / "ICBM152_adult"
        / "ICBM152_adult.T1W.nii.gz",
        localOnly=True,
    )
    mov = getFile(config.SUBJECT_DIR / "MNINonLinear" / "T1w_restore_brain.nii.gz")
    reg = str(
        config.SUBJECT_DIR
        / config.NATIVEORMNI152FOLDER
        / "register_t1w_to_mninonlinear.dat"
    )
    return call(
        cmdLabel="createRegisterDatFile",
        cmd=[
            "tkregister2",
            "--mov",
            mov,
            "--targ",
            targ,
            "--reg",
            reg,
            "--regheader",
            "--noedit",
        ],
    )


def createRoiFiles(subjectId: str) -> bool:
    import config

    brainMaskOfDiffusion: Path = (
        config.SUBJECT_DIR
        / "T1w"
        / "Diffusion"
        / config.IMAGES["DIFFUSION"]["STANDARD_RES"]["NODIF_BRAIN_MASK"]["PATH"]
    )
    lhRoiFilePath: Path = (
        config.SUBJECT_DIR
        / "T1w"
        / config.IMAGES["T1w"]["STANDARD_RES"]["MASKS"]["LEFT"]
    )
    rhRoiFilePath: Path = (
        config.SUBJECT_DIR
        / "T1w"
        / config.IMAGES["T1w"]["STANDARD_RES"]["MASKS"]["RIGHT"]
    )
    inversedLhRoiFilePath: Path = (
        config.SUBJECT_DIR
        / "T1w"
        / config.IMAGES["T1w"]["STANDARD_RES"]["MASKS"]["LEFT_INVERSED"]
    )
    inversedRhRoiFilePath: Path = (
        config.SUBJECT_DIR
        / "T1w"
        / config.IMAGES["T1w"]["STANDARD_RES"]["MASKS"]["RIGHT_INVERSED"]
    )
    labelledFilePath: Path = (
        config.SUBJECT_DIR
        / "T1w"
        / config.IMAGES["T1w"]["STANDARD_RES"]["MASKS"]["ALL_LABELS"]
    )

    _ = [getFile(localPath=fileToExist) for fileToExist in [brainMaskOfDiffusion]]

    lhRoiFilePath_dti: str = str(
        config.SUBJECT_DIR
        / "T1w"
        / config.IMAGES["T1w"]["STANDARD_RES"]["MASKS"]["LEFT"]
    ).replace(".nii.gz", ".dti_space.nii.gz")
    rhRoiFilePath_dti: str = str(
        config.SUBJECT_DIR
        / "T1w"
        / config.IMAGES["T1w"]["STANDARD_RES"]["MASKS"]["RIGHT"]
    ).replace(".nii.gz", ".dti_space.nii.gz")

    lhRoiFileSuccess = all(
        [
            call(
                cmdLabel="Freesurfer",
                cmd=[
                    "mri_binarize",
                    "--i",
                    labelledFilePath.resolve(),
                    "--o",
                    lhRoiFilePath.resolve(),
                    "--match",
                    "1024",
                    "--surf",
                    str(lhRoiFilePath.resolve()).replace(".nii.gz", ".surf.gii"),
                ],
            ),
            call(
                cmdLabel="Freesurfer",
                cmd=[
                    "mri_vol2vol",
                    "--mov",
                    lhRoiFilePath.resolve(),
                    "--targ",
                    brainMaskOfDiffusion.resolve(),
                    "--o",
                    lhRoiFilePath_dti,
                    "--regheader",
                    "--nearest",
                ],
            ),
        ]
    )
    rhRoiFileSuccess = all(
        [
            call(
                cmdLabel="Freesurfer",
                cmd=[
                    "mri_binarize",
                    "--i",
                    labelledFilePath.resolve(),
                    "--o",
                    rhRoiFilePath.resolve(),
                    "--match",
                    "2024",
                    "--surf",
                    str(rhRoiFilePath.resolve()).replace(".nii.gz", ".surf.gii"),
                ],
            ),
            call(
                cmdLabel="Freesurfer",
                cmd=[
                    "mri_vol2vol",
                    "--mov",
                    rhRoiFilePath.resolve(),
                    "--targ",
                    brainMaskOfDiffusion.resolve(),
                    "--o",
                    rhRoiFilePath_dti,
                    "--regheader",
                    "--nearest",
                ],
            ),
        ]
    )

    lhInversedRoiFileSuccess = call(
        cmdLabel="Freesurfer",
        cmd=[
            "mri_binarize",
            "--i",
            Path(lhRoiFilePath_dti).resolve(strict=True),
            "--o",
            inversedLhRoiFilePath.resolve(),
            "--match",
            "1",
            "--inv",
        ],
    )
    rhInversedRoiFileSuccess = call(
        cmdLabel="Freesurfer",
        cmd=[
            "mri_binarize",
            "--i",
            Path(rhRoiFilePath_dti).resolve(strict=True),
            "--o",
            inversedRhRoiFilePath.resolve(),
            "--match",
            "1",
            "--inv",
        ],
    )
    return (
        lhRoiFileSuccess
        and rhRoiFileSuccess
        and lhInversedRoiFileSuccess
        and rhInversedRoiFileSuccess
    )


def mergeTracts(
    sourceFile: Path, lhTractFile: str, rhTractFile: str, destinationFile: str
) -> bool:
    import config

    # dsi_studio --action=ana --source=avg.mean.fib.gz --tract=Tracts1.tt.gz,Tract2.tt.gz --output=Tracts1.txt
    cmd = [
        config.DSI_STUDIO,
        "--action=ana",
        f"--source={sourceFile}",
        f"--tract={lhTractFile},{rhTractFile}",
        f"--output={destinationFile}",
    ]
    return call(cmdLabel="DSIStudio", cmd=cmd)
