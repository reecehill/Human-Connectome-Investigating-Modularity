"""
This type stub file was generated by pyright.
"""

from .struct import GM_MNI152_FILE_PATH, MNI152_FILE_PATH, WM_MNI152_FILE_PATH, fetch_icbm152_2009, fetch_icbm152_brain_gm_mask, fetch_oasis_vbm, fetch_surf_fsaverage, load_mni152_brain_mask, load_mni152_gm_mask, load_mni152_gm_template, load_mni152_template, load_mni152_wm_mask, load_mni152_wm_template
from .func import fetch_abide_pcp, fetch_adhd, fetch_bids_langloc_dataset, fetch_development_fmri, fetch_ds000030_urls, fetch_fiac_first_level, fetch_haxby, fetch_language_localizer_demo_dataset, fetch_localizer_button_task, fetch_localizer_calculation_task, fetch_localizer_contrasts, fetch_localizer_first_level, fetch_megatrawls_netmats, fetch_mixed_gambles, fetch_miyawaki2008, fetch_openneuro_dataset, fetch_openneuro_dataset_index, fetch_spm_auditory, fetch_spm_multimodal_fmri, fetch_surf_nki_enhanced, patch_openneuro_dataset, select_from_index
from .atlas import fetch_atlas_aal, fetch_atlas_allen_2011, fetch_atlas_basc_multiscale_2015, fetch_atlas_craddock_2012, fetch_atlas_destrieux_2009, fetch_atlas_difumo, fetch_atlas_harvard_oxford, fetch_atlas_juelich, fetch_atlas_msdl, fetch_atlas_pauli_2017, fetch_atlas_schaefer_2018, fetch_atlas_smith_2009, fetch_atlas_surf_destrieux, fetch_atlas_talairach, fetch_atlas_yeo_2011, fetch_coords_dosenbach_2010, fetch_coords_power_2011, fetch_coords_seitzman_2018
from .utils import get_data_dirs
from .neurovault import fetch_neurovault, fetch_neurovault_auditory_computation_task, fetch_neurovault_ids, fetch_neurovault_motor_task

"""
Helper functions to download NeuroImaging datasets
"""
__all__ = ['MNI152_FILE_PATH', 'GM_MNI152_FILE_PATH', 'WM_MNI152_FILE_PATH', 'fetch_icbm152_2009', 'load_mni152_template', 'load_mni152_gm_template', 'load_mni152_wm_template', 'fetch_oasis_vbm', 'fetch_haxby', 'fetch_adhd', 'fetch_miyawaki2008', 'fetch_localizer_contrasts', 'fetch_localizer_button_task', 'fetch_abide_pcp', 'fetch_localizer_calculation_task', 'fetch_atlas_craddock_2012', 'fetch_atlas_destrieux_2009', 'fetch_atlas_juelich', 'fetch_atlas_harvard_oxford', 'fetch_atlas_msdl', 'fetch_atlas_schaefer_2018', 'fetch_coords_power_2011', 'fetch_coords_seitzman_2018', 'fetch_atlas_smith_2009', 'fetch_atlas_allen_2011', 'fetch_atlas_yeo_2011', 'fetch_mixed_gambles', 'fetch_atlas_aal', 'fetch_atlas_difumo', 'fetch_megatrawls_netmats', 'fetch_surf_nki_enhanced', 'fetch_development_fmri', 'fetch_surf_fsaverage', 'fetch_atlas_basc_multiscale_2015', 'fetch_coords_dosenbach_2010', 'fetch_neurovault', 'fetch_neurovault_ids', 'fetch_neurovault_motor_task', 'fetch_neurovault_auditory_computation_task', 'load_mni152_brain_mask', 'load_mni152_gm_mask', 'load_mni152_wm_mask', 'fetch_icbm152_brain_gm_mask', 'fetch_atlas_surf_destrieux', 'fetch_atlas_talairach', 'get_data_dirs', 'fetch_language_localizer_demo_dataset', 'fetch_bids_langloc_dataset', 'fetch_openneuro_dataset_index', 'select_from_index', 'patch_openneuro_dataset', 'fetch_openneuro_dataset', 'fetch_localizer_first_level', 'fetch_spm_auditory', 'fetch_spm_multimodal_fmri', 'fetch_fiac_first_level']