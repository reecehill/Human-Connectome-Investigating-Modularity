"""
This type stub file was generated by pyright.
"""

from .base import FSCommand, FSCommandOpenMP, FSScriptCommand, FSScriptOutputSpec, FSTraitedSpec, FSTraitedSpecOpenMP
from ..base import TraitedSpec

"""Provides interfaces to various longitudinal commands provided by freesurfer
"""
__docformat__ = ...
iflogger = ...
class MPRtoMNI305InputSpec(FSTraitedSpec):
    reference_dir = ...
    target = ...
    in_file = ...


class MPRtoMNI305OutputSpec(FSScriptOutputSpec):
    out_file = ...


class MPRtoMNI305(FSScriptCommand):
    """
    For complete details, see FreeSurfer documentation

    Examples
    --------
    >>> from nipype.interfaces.freesurfer import MPRtoMNI305, Info
    >>> mprtomni305 = MPRtoMNI305()
    >>> mprtomni305.inputs.target = 'structural.nii'
    >>> mprtomni305.inputs.reference_dir = '.' # doctest: +SKIP
    >>> mprtomni305.cmdline # doctest: +SKIP
    'mpr2mni305 output'
    >>> mprtomni305.inputs.out_file = 'struct_out' # doctest: +SKIP
    >>> mprtomni305.cmdline # doctest: +SKIP
    'mpr2mni305 struct_out' # doctest: +SKIP
    >>> mprtomni305.inputs.environ['REFDIR'] == os.path.join(Info.home(), 'average') # doctest: +SKIP
    True
    >>> mprtomni305.inputs.environ['MPR2MNI305_TARGET'] # doctest: +SKIP
    'structural'
    >>> mprtomni305.run() # doctest: +SKIP

    """
    _cmd = ...
    input_spec = MPRtoMNI305InputSpec
    output_spec = MPRtoMNI305OutputSpec
    def __init__(self, **inputs) -> None:
        ...
    


class RegisterAVItoTalairachInputSpec(FSTraitedSpec):
    in_file = ...
    target = ...
    vox2vox = ...
    out_file = ...


class RegisterAVItoTalairachOutputSpec(FSScriptOutputSpec):
    out_file = ...


class RegisterAVItoTalairach(FSScriptCommand):
    """
    converts the vox2vox from talairach_avi to a talairach.xfm file

    This is a script that converts the vox2vox from talairach_avi to a
    talairach.xfm file. It is meant to replace the following cmd line:

    tkregister2_cmdl \
        --mov $InVol \
        --targ $FREESURFER_HOME/average/mni305.cor.mgz \
        --xfmout ${XFM} \
        --vox2vox talsrcimg_to_${target}_t4_vox2vox.txt \
        --noedit \
        --reg talsrcimg.reg.tmp.dat
    set targ = $FREESURFER_HOME/average/mni305.cor.mgz
    set subject = mgh-02407836-v2
    set InVol = $SUBJECTS_DIR/$subject/mri/orig.mgz
    set vox2vox = $SUBJECTS_DIR/$subject/mri/transforms/talsrcimg_to_711-2C_as_mni_average_305_t4_vox2vox.txt

    Examples
    ========

    >>> from nipype.interfaces.freesurfer import RegisterAVItoTalairach
    >>> register = RegisterAVItoTalairach()
    >>> register.inputs.in_file = 'structural.mgz'                         # doctest: +SKIP
    >>> register.inputs.target = 'mni305.cor.mgz'                          # doctest: +SKIP
    >>> register.inputs.vox2vox = 'talsrcimg_to_structural_t4_vox2vox.txt' # doctest: +SKIP
    >>> register.cmdline                                                   # doctest: +SKIP
    'avi2talxfm structural.mgz mni305.cor.mgz talsrcimg_to_structural_t4_vox2vox.txt talairach.auto.xfm'

    >>> register.run() # doctest: +SKIP
    """
    _cmd = ...
    input_spec = RegisterAVItoTalairachInputSpec
    output_spec = RegisterAVItoTalairachOutputSpec


class EMRegisterInputSpec(FSTraitedSpecOpenMP):
    in_file = ...
    template = ...
    out_file = ...
    skull = ...
    mask = ...
    nbrspacing = ...
    transform = ...


class EMRegisterOutputSpec(TraitedSpec):
    out_file = ...


class EMRegister(FSCommandOpenMP):
    """This program creates a transform in lta format

    Examples
    ========
    >>> from nipype.interfaces.freesurfer import EMRegister
    >>> register = EMRegister()
    >>> register.inputs.in_file = 'norm.mgz'
    >>> register.inputs.template = 'aseg.mgz'
    >>> register.inputs.out_file = 'norm_transform.lta'
    >>> register.inputs.skull = True
    >>> register.inputs.nbrspacing = 9
    >>> register.cmdline
    'mri_em_register -uns 9 -skull norm.mgz aseg.mgz norm_transform.lta'
    """
    _cmd = ...
    input_spec = EMRegisterInputSpec
    output_spec = EMRegisterOutputSpec


class RegisterInputSpec(FSTraitedSpec):
    in_surf = ...
    target = ...
    in_sulc = ...
    out_file = ...
    curv = ...
    in_smoothwm = ...


class RegisterOutputSpec(TraitedSpec):
    out_file = ...


class Register(FSCommand):
    """This program registers a surface to an average surface template.

    Examples
    ========
    >>> from nipype.interfaces.freesurfer import Register
    >>> register = Register()
    >>> register.inputs.in_surf = 'lh.pial'
    >>> register.inputs.in_smoothwm = 'lh.pial'
    >>> register.inputs.in_sulc = 'lh.pial'
    >>> register.inputs.target = 'aseg.mgz'
    >>> register.inputs.out_file = 'lh.pial.reg'
    >>> register.inputs.curv = True
    >>> register.cmdline
    'mris_register -curv lh.pial aseg.mgz lh.pial.reg'
    """
    _cmd = ...
    input_spec = RegisterInputSpec
    output_spec = RegisterOutputSpec


class PaintInputSpec(FSTraitedSpec):
    in_surf = ...
    template = ...
    template_param = ...
    averages = ...
    out_file = ...


class PaintOutputSpec(TraitedSpec):
    out_file = ...


class Paint(FSCommand):
    """
    This program is useful for extracting one of the arrays ("a variable")
    from a surface-registration template file. The output is a file
    containing a surface-worth of per-vertex values, saved in "curvature"
    format. Because the template data is sampled to a particular surface
    mesh, this conjures the idea of "painting to a surface".

    Examples
    ========
    >>> from nipype.interfaces.freesurfer import Paint
    >>> paint = Paint()
    >>> paint.inputs.in_surf = 'lh.pial'
    >>> paint.inputs.template = 'aseg.mgz'
    >>> paint.inputs.averages = 5
    >>> paint.inputs.out_file = 'lh.avg_curv'
    >>> paint.cmdline
    'mrisp_paint -a 5 aseg.mgz lh.pial lh.avg_curv'
    """
    _cmd = ...
    input_spec = PaintInputSpec
    output_spec = PaintOutputSpec


class MRICoregInputSpec(FSTraitedSpec):
    source_file = ...
    reference_file = ...
    out_lta_file = ...
    out_reg_file = ...
    out_params_file = ...
    subjects_dir = ...
    subject_id = ...
    dof = ...
    reference_mask = ...
    source_mask = ...
    num_threads = ...
    no_coord_dithering = ...
    no_intensity_dithering = ...
    sep = ...
    initial_translation = ...
    initial_rotation = ...
    initial_scale = ...
    initial_shear = ...
    no_cras0 = ...
    max_iters = ...
    ftol = ...
    linmintol = ...
    saturation_threshold = ...
    conform_reference = ...
    no_brute_force = ...
    brute_force_limit = ...
    brute_force_samples = ...
    no_smooth = ...
    ref_fwhm = ...
    source_oob = ...


class MRICoregOutputSpec(TraitedSpec):
    out_reg_file = ...
    out_lta_file = ...
    out_params_file = ...


class MRICoreg(FSCommand):
    """This program registers one volume to another

    mri_coreg is a C reimplementation of spm_coreg in FreeSurfer

    Examples
    ========
    >>> from nipype.interfaces.freesurfer import MRICoreg
    >>> coreg = MRICoreg()
    >>> coreg.inputs.source_file = 'moving1.nii'
    >>> coreg.inputs.reference_file = 'fixed1.nii'
    >>> coreg.inputs.subjects_dir = '.'
    >>> coreg.cmdline # doctest: +ELLIPSIS
    'mri_coreg --lta .../registration.lta --ref fixed1.nii --mov moving1.nii --sd .'

    If passing a subject ID, the reference mask may be disabled:

    >>> coreg = MRICoreg()
    >>> coreg.inputs.source_file = 'moving1.nii'
    >>> coreg.inputs.subjects_dir = '.'
    >>> coreg.inputs.subject_id = 'fsaverage'
    >>> coreg.inputs.reference_mask = False
    >>> coreg.cmdline # doctest: +ELLIPSIS
    'mri_coreg --s fsaverage --no-ref-mask --lta .../registration.lta --mov moving1.nii --sd .'

    Spatial scales may be specified as a list of one or two separations:

    >>> coreg.inputs.sep = [4]
    >>> coreg.cmdline # doctest: +ELLIPSIS
    'mri_coreg --s fsaverage --no-ref-mask --lta .../registration.lta --sep 4 --mov moving1.nii --sd .'

    >>> coreg.inputs.sep = [4, 5]
    >>> coreg.cmdline # doctest: +ELLIPSIS
    'mri_coreg --s fsaverage --no-ref-mask --lta .../registration.lta --sep 4 --sep 5 --mov moving1.nii --sd .'
    """
    _cmd = ...
    input_spec = MRICoregInputSpec
    output_spec = MRICoregOutputSpec

