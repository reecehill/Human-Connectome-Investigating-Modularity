"""
This type stub file was generated by pyright.
"""

from ..base import File, InputMultiPath, OutputMultiPath, TraitedSpec, traits
from .base import FSCommand, FSTraitedSpec

"""The freesurfer module provides basic functions for interfacing with
   freesurfer tools.
"""
__docformat__ = ...
class MRISPreprocInputSpec(FSTraitedSpec):
    out_file = ...
    target = ...
    hemi = ...
    surf_measure = ...
    surf_area = ...
    subjects = ...
    fsgd_file = ...
    subject_file = ...
    surf_measure_file = InputMultiPath(File(exists=True), argstr="--is %s...", xor=("surf_measure", "surf_measure_file", "surf_area"), desc="file alternative to surfmeas, still requires list of subjects")
    source_format = ...
    surf_dir = ...
    vol_measure_file = InputMultiPath(traits.Tuple(File(exists=True), File(exists=True)), argstr="--iv %s %s...", desc="list of volume measure and reg file tuples")
    proj_frac = ...
    fwhm = ...
    num_iters = ...
    fwhm_source = ...
    num_iters_source = ...
    smooth_cortex_only = ...


class MRISPreprocOutputSpec(TraitedSpec):
    out_file = ...


class MRISPreproc(FSCommand):
    """Use FreeSurfer mris_preproc to prepare a group of contrasts for
    a second level analysis

    Examples
    --------
    >>> preproc = MRISPreproc()
    >>> preproc.inputs.target = 'fsaverage'
    >>> preproc.inputs.hemi = 'lh'
    >>> preproc.inputs.vol_measure_file = [('cont1.nii', 'register.dat'), \
                                           ('cont1a.nii', 'register.dat')]
    >>> preproc.inputs.out_file = 'concatenated_file.mgz'
    >>> preproc.cmdline
    'mris_preproc --hemi lh --out concatenated_file.mgz --target fsaverage --iv cont1.nii register.dat --iv cont1a.nii register.dat'

    """
    _cmd = ...
    input_spec = MRISPreprocInputSpec
    output_spec = MRISPreprocOutputSpec


class MRISPreprocReconAllInputSpec(MRISPreprocInputSpec):
    surf_measure_file = ...
    surfreg_files = InputMultiPath(File(exists=True), argstr="--surfreg %s", requires=["lh_surfreg_target", "rh_surfreg_target"], desc="lh and rh input surface registration files")
    lh_surfreg_target = ...
    rh_surfreg_target = ...
    subject_id = ...
    copy_inputs = ...


class MRISPreprocReconAll(MRISPreproc):
    """Extends MRISPreproc to allow it to be used in a recon-all workflow

    Examples
    --------
    >>> preproc = MRISPreprocReconAll()
    >>> preproc.inputs.target = 'fsaverage'
    >>> preproc.inputs.hemi = 'lh'
    >>> preproc.inputs.vol_measure_file = [('cont1.nii', 'register.dat'), \
                                           ('cont1a.nii', 'register.dat')]
    >>> preproc.inputs.out_file = 'concatenated_file.mgz'
    >>> preproc.cmdline
    'mris_preproc --hemi lh --out concatenated_file.mgz --s subject_id --target fsaverage --iv cont1.nii register.dat --iv cont1a.nii register.dat'

    """
    input_spec = MRISPreprocReconAllInputSpec
    def run(self, **inputs): # -> InterfaceResult:
        ...
    


class GLMFitInputSpec(FSTraitedSpec):
    glm_dir = ...
    in_file = ...
    _design_xor = ...
    fsgd = ...
    design = ...
    contrast = InputMultiPath(File(exists=True), argstr="--C %s...", desc="contrast file")
    one_sample = ...
    no_contrast_ok = ...
    per_voxel_reg = InputMultiPath(File(exists=True), argstr="--pvr %s...", desc="per-voxel regressors")
    self_reg = ...
    weighted_ls = ...
    fixed_fx_var = ...
    fixed_fx_dof = ...
    fixed_fx_dof_file = ...
    weight_file = ...
    weight_inv = ...
    weight_sqrt = ...
    fwhm = ...
    var_fwhm = ...
    no_mask_smooth = ...
    no_est_fwhm = ...
    mask_file = ...
    label_file = ...
    cortex = ...
    invert_mask = ...
    prune = ...
    no_prune = ...
    prune_thresh = ...
    compute_log_y = ...
    save_estimate = ...
    save_residual = ...
    save_res_corr_mtx = ...
    surf = ...
    subject_id = ...
    hemi = ...
    surf_geo = ...
    simulation = ...
    sim_sign = ...
    uniform = ...
    pca = ...
    calc_AR1 = ...
    save_cond = ...
    vox_dump = ...
    seed = ...
    synth = ...
    resynth_test = ...
    profile = ...
    mrtm1 = ...
    mrtm2 = ...
    logan = ...
    force_perm = ...
    diag = ...
    diag_cluster = ...
    debug = ...
    check_opts = ...
    allow_repeated_subjects = ...
    allow_ill_cond = ...
    sim_done_file = ...
    _ext_xor = ...
    nii = ...
    nii_gz = ...


class GLMFitOutputSpec(TraitedSpec):
    glm_dir = ...
    beta_file = ...
    error_file = ...
    error_var_file = ...
    error_stddev_file = ...
    estimate_file = ...
    mask_file = ...
    fwhm_file = ...
    dof_file = ...
    gamma_file = OutputMultiPath(desc="map of contrast of regression coefficients")
    gamma_var_file = OutputMultiPath(desc="map of regression contrast variance")
    sig_file = OutputMultiPath(desc="map of F-test significance (in -log10p)")
    ftest_file = OutputMultiPath(desc="map of test statistic values")
    spatial_eigenvectors = ...
    frame_eigenvectors = ...
    singular_values = ...
    svd_stats_file = ...
    k2p_file = ...
    bp_file = ...


class GLMFit(FSCommand):
    """Use FreeSurfer's mri_glmfit to specify and estimate a general linear model.

    Examples
    --------
    >>> glmfit = GLMFit()
    >>> glmfit.inputs.in_file = 'functional.nii'
    >>> glmfit.inputs.one_sample = True
    >>> glmfit.cmdline == 'mri_glmfit --glmdir %s --y functional.nii --osgm'%os.getcwd()
    True

    """
    _cmd = ...
    input_spec = GLMFitInputSpec
    output_spec = GLMFitOutputSpec


class OneSampleTTest(GLMFit):
    def __init__(self, **kwargs) -> None:
        ...
    


class BinarizeInputSpec(FSTraitedSpec):
    in_file = ...
    min = ...
    max = ...
    rmin = ...
    rmax = ...
    match = ...
    wm = ...
    ventricles = ...
    wm_ven_csf = ...
    binary_file = ...
    out_type = ...
    count_file = ...
    bin_val = ...
    bin_val_not = ...
    invert = ...
    frame_no = ...
    merge_file = ...
    mask_file = ...
    mask_thresh = ...
    abs = ...
    bin_col_num = ...
    zero_edges = ...
    zero_slice_edge = ...
    dilate = ...
    erode = ...
    erode2d = ...


class BinarizeOutputSpec(TraitedSpec):
    binary_file = ...
    count_file = ...


class Binarize(FSCommand):
    """Use FreeSurfer mri_binarize to threshold an input volume

    Examples
    --------
    >>> binvol = Binarize(in_file='structural.nii', min=10, binary_file='foo_out.nii')
    >>> binvol.cmdline
    'mri_binarize --o foo_out.nii --i structural.nii --min 10.000000'

    """
    _cmd = ...
    input_spec = BinarizeInputSpec
    output_spec = BinarizeOutputSpec


class ConcatenateInputSpec(FSTraitedSpec):
    in_files = InputMultiPath(File(exists=True), desc="Individual volumes to be concatenated", argstr="--i %s...", mandatory=True)
    concatenated_file = ...
    sign = ...
    stats = ...
    paired_stats = ...
    gmean = ...
    mean_div_n = ...
    multiply_by = ...
    add_val = ...
    multiply_matrix_file = ...
    combine = ...
    keep_dtype = ...
    max_bonfcor = ...
    max_index = ...
    mask_file = ...
    vote = ...
    sort = ...


class ConcatenateOutputSpec(TraitedSpec):
    concatenated_file = ...


class Concatenate(FSCommand):
    """Use Freesurfer mri_concat to combine several input volumes
    into one output volume.  Can concatenate by frames, or compute
    a variety of statistics on the input volumes.

    Examples
    --------
    Combine two input volumes into one volume with two frames

    >>> concat = Concatenate()
    >>> concat.inputs.in_files = ['cont1.nii', 'cont2.nii']
    >>> concat.inputs.concatenated_file = 'bar.nii'
    >>> concat.cmdline
    'mri_concat --o bar.nii --i cont1.nii --i cont2.nii'

    """
    _cmd = ...
    input_spec = ConcatenateInputSpec
    output_spec = ConcatenateOutputSpec


class SegStatsInputSpec(FSTraitedSpec):
    _xor_inputs = ...
    segmentation_file = ...
    annot = ...
    surf_label = ...
    summary_file = ...
    partial_volume_file = ...
    in_file = ...
    frame = ...
    multiply = ...
    calc_snr = ...
    calc_power = ...
    _ctab_inputs = ...
    color_table_file = ...
    default_color_table = ...
    gca_color_table = ...
    segment_id = ...
    exclude_id = ...
    exclude_ctx_gm_wm = ...
    wm_vol_from_surf = ...
    cortex_vol_from_surf = ...
    non_empty_only = ...
    empty = ...
    mask_file = ...
    mask_thresh = ...
    mask_sign = ...
    mask_frame = ...
    mask_invert = ...
    mask_erode = ...
    brain_vol = ...
    brainmask_file = ...
    etiv = ...
    etiv_only = ...
    avgwf_txt_file = ...
    avgwf_file = ...
    sf_avg_file = ...
    vox = ...
    supratent = ...
    subcort_gm = ...
    total_gray = ...
    euler = ...
    in_intensity = ...
    intensity_units = ...


class SegStatsOutputSpec(TraitedSpec):
    summary_file = ...
    avgwf_txt_file = ...
    avgwf_file = ...
    sf_avg_file = ...


class SegStats(FSCommand):
    """Use FreeSurfer mri_segstats for ROI analysis

    Examples
    --------
    >>> import nipype.interfaces.freesurfer as fs
    >>> ss = fs.SegStats()
    >>> ss.inputs.annot = ('PWS04', 'lh', 'aparc')
    >>> ss.inputs.in_file = 'functional.nii'
    >>> ss.inputs.subjects_dir = '.'
    >>> ss.inputs.avgwf_txt_file = 'avgwf.txt'
    >>> ss.inputs.summary_file = 'summary.stats'
    >>> ss.cmdline
    'mri_segstats --annot PWS04 lh aparc --avgwf ./avgwf.txt --i functional.nii --sum ./summary.stats'

    """
    _cmd = ...
    input_spec = SegStatsInputSpec
    output_spec = SegStatsOutputSpec


class SegStatsReconAllInputSpec(SegStatsInputSpec):
    subject_id = ...
    ribbon = ...
    presurf_seg = ...
    transform = ...
    lh_orig_nofix = ...
    rh_orig_nofix = ...
    lh_white = ...
    rh_white = ...
    lh_pial = ...
    rh_pial = ...
    aseg = ...
    copy_inputs = ...


class SegStatsReconAll(SegStats):
    """
    This class inherits SegStats and modifies it for use in a recon-all workflow.
    This implementation mandates implicit inputs that SegStats.
    To ensure backwards compatibility of SegStats, this class was created.

    Examples
    --------
    >>> from nipype.interfaces.freesurfer import SegStatsReconAll
    >>> segstatsreconall = SegStatsReconAll()
    >>> segstatsreconall.inputs.annot = ('PWS04', 'lh', 'aparc')
    >>> segstatsreconall.inputs.avgwf_txt_file = 'avgwf.txt'
    >>> segstatsreconall.inputs.summary_file = 'summary.stats'
    >>> segstatsreconall.inputs.subject_id = '10335'
    >>> segstatsreconall.inputs.ribbon = 'wm.mgz'
    >>> segstatsreconall.inputs.transform = 'trans.mat'
    >>> segstatsreconall.inputs.presurf_seg = 'wm.mgz'
    >>> segstatsreconall.inputs.lh_orig_nofix = 'lh.pial'
    >>> segstatsreconall.inputs.rh_orig_nofix = 'lh.pial'
    >>> segstatsreconall.inputs.lh_pial = 'lh.pial'
    >>> segstatsreconall.inputs.rh_pial = 'lh.pial'
    >>> segstatsreconall.inputs.lh_white = 'lh.pial'
    >>> segstatsreconall.inputs.rh_white = 'lh.pial'
    >>> segstatsreconall.inputs.empty = True
    >>> segstatsreconall.inputs.brain_vol = 'brain-vol-from-seg'
    >>> segstatsreconall.inputs.exclude_ctx_gm_wm = True
    >>> segstatsreconall.inputs.supratent = True
    >>> segstatsreconall.inputs.subcort_gm = True
    >>> segstatsreconall.inputs.etiv = True
    >>> segstatsreconall.inputs.wm_vol_from_surf = True
    >>> segstatsreconall.inputs.cortex_vol_from_surf = True
    >>> segstatsreconall.inputs.total_gray = True
    >>> segstatsreconall.inputs.euler = True
    >>> segstatsreconall.inputs.exclude_id = 0
    >>> segstatsreconall.cmdline
    'mri_segstats --annot PWS04 lh aparc --avgwf ./avgwf.txt --brain-vol-from-seg --surf-ctx-vol --empty --etiv --euler --excl-ctxgmwm --excludeid 0 --subcortgray --subject 10335 --supratent --totalgray --surf-wm-vol --sum ./summary.stats'

    """
    input_spec = SegStatsReconAllInputSpec
    output_spec = SegStatsOutputSpec
    def run(self, **inputs): # -> InterfaceResult:
        ...
    


class Label2VolInputSpec(FSTraitedSpec):
    label_file = InputMultiPath(File(exists=True), argstr="--label %s...", xor=("label_file", "annot_file", "seg_file", "aparc_aseg"), copyfile=False, mandatory=True, desc="list of label files")
    annot_file = ...
    seg_file = ...
    aparc_aseg = ...
    template_file = ...
    reg_file = ...
    reg_header = ...
    identity = ...
    invert_mtx = ...
    fill_thresh = ...
    label_voxel_volume = ...
    proj = ...
    subject_id = ...
    hemi = ...
    surface = ...
    vol_label_file = ...
    label_hit_file = ...
    map_label_stat = ...
    native_vox2ras = ...


class Label2VolOutputSpec(TraitedSpec):
    vol_label_file = ...


class Label2Vol(FSCommand):
    """Make a binary volume from a Freesurfer label

    Examples
    --------
    >>> binvol = Label2Vol(label_file='cortex.label', template_file='structural.nii', reg_file='register.dat', fill_thresh=0.5, vol_label_file='foo_out.nii')
    >>> binvol.cmdline
    'mri_label2vol --fillthresh 0.5 --label cortex.label --reg register.dat --temp structural.nii --o foo_out.nii'

    """
    _cmd = ...
    input_spec = Label2VolInputSpec
    output_spec = Label2VolOutputSpec


class MS_LDAInputSpec(FSTraitedSpec):
    lda_labels = ...
    weight_file = ...
    vol_synth_file = ...
    label_file = ...
    mask_file = ...
    shift = ...
    conform = ...
    use_weights = ...
    images = InputMultiPath(File(exists=True), argstr="%s", mandatory=True, copyfile=False, desc="list of input FLASH images", position=-1)


class MS_LDAOutputSpec(TraitedSpec):
    weight_file = ...
    vol_synth_file = ...


class MS_LDA(FSCommand):
    """Perform LDA reduction on the intensity space of an arbitrary # of FLASH images

    Examples
    --------
    >>> grey_label = 2
    >>> white_label = 3
    >>> zero_value = 1
    >>> optimalWeights = MS_LDA(lda_labels=[grey_label, white_label], \
                                label_file='label.mgz', weight_file='weights.txt', \
                                shift=zero_value, vol_synth_file='synth_out.mgz', \
                                conform=True, use_weights=True, \
                                images=['FLASH1.mgz', 'FLASH2.mgz', 'FLASH3.mgz'])
    >>> optimalWeights.cmdline
    'mri_ms_LDA -conform -label label.mgz -lda 2 3 -shift 1 -W -synth synth_out.mgz -weight weights.txt FLASH1.mgz FLASH2.mgz FLASH3.mgz'

    """
    _cmd = ...
    input_spec = MS_LDAInputSpec
    output_spec = MS_LDAOutputSpec


class Label2LabelInputSpec(FSTraitedSpec):
    hemisphere = ...
    subject_id = ...
    sphere_reg = ...
    white = ...
    source_sphere_reg = ...
    source_white = ...
    source_label = ...
    source_subject = ...
    out_file = ...
    registration_method = ...
    copy_inputs = ...


class Label2LabelOutputSpec(TraitedSpec):
    out_file = ...


class Label2Label(FSCommand):
    """
    Converts a label in one subject's space to a label
    in another subject's space using either talairach or spherical
    as an intermediate registration space.

    If a source mask is used, then the input label must have been
    created from a surface (ie, the vertex numbers are valid). The
    format can be anything supported by mri_convert or curv or paint.
    Vertices in the source label that do not meet threshold in the
    mask will be removed from the label.

    Examples
    --------
    >>> from nipype.interfaces.freesurfer import Label2Label
    >>> l2l = Label2Label()
    >>> l2l.inputs.hemisphere = 'lh'
    >>> l2l.inputs.subject_id = '10335'
    >>> l2l.inputs.sphere_reg = 'lh.pial'
    >>> l2l.inputs.white = 'lh.pial'
    >>> l2l.inputs.source_subject = 'fsaverage'
    >>> l2l.inputs.source_label = 'lh-pial.stl'
    >>> l2l.inputs.source_white = 'lh.pial'
    >>> l2l.inputs.source_sphere_reg = 'lh.pial'
    >>> l2l.cmdline
    'mri_label2label --hemi lh --trglabel lh-pial_converted.stl --regmethod surface --srclabel lh-pial.stl --srcsubject fsaverage --trgsubject 10335'
    """
    _cmd = ...
    input_spec = Label2LabelInputSpec
    output_spec = Label2LabelOutputSpec
    def run(self, **inputs): # -> InterfaceResult:
        ...
    


class Label2AnnotInputSpec(FSTraitedSpec):
    hemisphere = ...
    subject_id = ...
    in_labels = ...
    out_annot = ...
    orig = ...
    keep_max = ...
    verbose_off = ...
    color_table = ...
    copy_inputs = ...


class Label2AnnotOutputSpec(TraitedSpec):
    out_file = ...


class Label2Annot(FSCommand):
    """
    Converts a set of surface labels to an annotation file

    Examples
    --------
    >>> from nipype.interfaces.freesurfer import Label2Annot
    >>> l2a = Label2Annot()
    >>> l2a.inputs.hemisphere = 'lh'
    >>> l2a.inputs.subject_id = '10335'
    >>> l2a.inputs.in_labels = ['lh.aparc.label']
    >>> l2a.inputs.orig = 'lh.pial'
    >>> l2a.inputs.out_annot = 'test'
    >>> l2a.cmdline
    'mris_label2annot --hemi lh --l lh.aparc.label --a test --s 10335'
    """
    _cmd = ...
    input_spec = Label2AnnotInputSpec
    output_spec = Label2AnnotOutputSpec
    def run(self, **inputs): # -> InterfaceResult:
        ...
    


class SphericalAverageInputSpec(FSTraitedSpec):
    out_file = ...
    in_average = ...
    in_surf = ...
    hemisphere = ...
    fname = ...
    which = ...
    subject_id = ...
    erode = ...
    in_orig = ...
    threshold = ...


class SphericalAverageOutputSpec(TraitedSpec):
    out_file = ...


class SphericalAverage(FSCommand):
    """
    This program will add a template into an average surface.

    Examples
    --------
    >>> from nipype.interfaces.freesurfer import SphericalAverage
    >>> sphericalavg = SphericalAverage()
    >>> sphericalavg.inputs.out_file = 'test.out'
    >>> sphericalavg.inputs.in_average = '.'
    >>> sphericalavg.inputs.in_surf = 'lh.pial'
    >>> sphericalavg.inputs.hemisphere = 'lh'
    >>> sphericalavg.inputs.fname = 'lh.entorhinal'
    >>> sphericalavg.inputs.which = 'label'
    >>> sphericalavg.inputs.subject_id = '10335'
    >>> sphericalavg.inputs.erode = 2
    >>> sphericalavg.inputs.threshold = 5
    >>> sphericalavg.cmdline
    'mris_spherical_average -erode 2 -o 10335 -t 5.0 label lh.entorhinal lh pial . test.out'

    """
    _cmd = ...
    input_spec = SphericalAverageInputSpec
    output_spec = SphericalAverageOutputSpec

