from pathlib import Path
from nipype.interfaces.base.core import CommandLine
from nipype.interfaces.base.traits_extension import InputMultiPath
from nipype.interfaces.freesurfer import preprocess


reconall = preprocess.ReconAll()
reconall.inputs.subject_id = 'sub-01'
reconall.inputs.directive = 'all'
reconall.inputs.subjects_dir = Path('/mnt/c/Users/Reece/Documents/Dissertation/Main/data/freesurfer').resolve(strict=True)
reconall.inputs.FLAIR_file = Path('/mnt/c/Users/Reece/Documents/Dissertation/Main/data/ds002685/sub-01/ses-00/anat/sub-01_ses-00_FLAIR.nii').resolve(strict=True)
reconall.inputs.T1_files = Path('/mnt/c/Users/Reece/Documents/Dissertation/Main/data/ds002685/sub-01/ses-00/anat/sub-01_ses-00_T1w.nii').resolve(strict=True)
reconall.run()