"""
This type stub file was generated by pyright.
"""

from ..base import BaseInterface, BaseInterfaceInputSpec, DynamicTraitedSpec, InputMultiPath, OutputMultiPath, SimpleInterface, TraitedSpec, traits
from ..io import IOBase

"""
    # changing to temporary directories
    >>> tmp = getfixture('tmpdir')
    >>> old = tmp.chdir()
"""
class IdentityInterface(IOBase):
    """Basic interface class generates identity mappings

    Examples
    --------

    >>> from nipype.interfaces.utility import IdentityInterface
    >>> ii = IdentityInterface(fields=['a', 'b'], mandatory_inputs=False)
    >>> ii.inputs.a
    <undefined>

    >>> ii.inputs.a = 'foo'
    >>> out = ii._outputs()
    >>> out.a
    <undefined>

    >>> out = ii.run()
    >>> out.outputs.a
    'foo'

    >>> ii2 = IdentityInterface(fields=['a', 'b'], mandatory_inputs=True)
    >>> ii2.inputs.a = 'foo'
    >>> out = ii2.run() # doctest: +SKIP
    ValueError: IdentityInterface requires a value for input 'b' because it was listed in 'fields' Interface IdentityInterface failed to run.
    """
    input_spec = DynamicTraitedSpec
    output_spec = DynamicTraitedSpec
    def __init__(self, fields=..., mandatory_inputs=..., **inputs) -> None:
        ...
    


class MergeInputSpec(DynamicTraitedSpec, BaseInterfaceInputSpec):
    axis = ...
    no_flatten = ...
    ravel_inputs = ...


class MergeOutputSpec(TraitedSpec):
    out = ...


class Merge(IOBase):
    """Basic interface class to merge inputs into a single list

    ``Merge(1)`` will merge a list of lists

    Examples
    --------

    >>> from nipype.interfaces.utility import Merge
    >>> mi = Merge(3)
    >>> mi.inputs.in1 = 1
    >>> mi.inputs.in2 = [2, 5]
    >>> mi.inputs.in3 = 3
    >>> out = mi.run()
    >>> out.outputs.out
    [1, 2, 5, 3]

    >>> merge = Merge(1)
    >>> merge.inputs.in1 = [1, [2, 5], 3]
    >>> out = merge.run()
    >>> out.outputs.out
    [1, [2, 5], 3]

    >>> merge = Merge(1)
    >>> merge.inputs.in1 = [1, [2, 5], 3]
    >>> merge.inputs.ravel_inputs = True
    >>> out = merge.run()
    >>> out.outputs.out
    [1, 2, 5, 3]

    >>> merge = Merge(1)
    >>> merge.inputs.in1 = [1, [2, 5], 3]
    >>> merge.inputs.no_flatten = True
    >>> out = merge.run()
    >>> out.outputs.out
    [[1, [2, 5], 3]]
    """
    input_spec = MergeInputSpec
    output_spec = MergeOutputSpec
    def __init__(self, numinputs=..., **inputs) -> None:
        ...
    


class RenameInputSpec(DynamicTraitedSpec):
    in_file = ...
    keep_ext = ...
    format_string = ...
    parse_string = ...
    use_fullpath = ...


class RenameOutputSpec(TraitedSpec):
    out_file = ...


class Rename(SimpleInterface, IOBase):
    """Change the name of a file based on a mapped format string.

    To use additional inputs that will be defined at run-time, the class
    constructor must be called with the format template, and the fields
    identified will become inputs to the interface.

    Additionally, you may set the parse_string input, which will be run
    over the input filename with a regular expressions search, and will
    fill in additional input fields from matched groups. Fields set with
    inputs have precedence over fields filled in with the regexp match.

    Examples
    --------

    >>> from nipype.interfaces.utility import Rename
    >>> rename1 = Rename()
    >>> rename1.inputs.in_file = os.path.join(datadir, "zstat1.nii.gz") # datadir is a directory with exemplary files, defined in conftest.py
    >>> rename1.inputs.format_string = "Faces-Scenes.nii.gz"
    >>> res = rename1.run()          # doctest: +SKIP
    >>> res.outputs.out_file         # doctest: +SKIP
    'Faces-Scenes.nii.gz"            # doctest: +SKIP

    >>> rename2 = Rename(format_string="%(subject_id)s_func_run%(run)02d")
    >>> rename2.inputs.in_file = os.path.join(datadir, "functional.nii")
    >>> rename2.inputs.keep_ext = True
    >>> rename2.inputs.subject_id = "subj_201"
    >>> rename2.inputs.run = 2
    >>> res = rename2.run()          # doctest: +SKIP
    >>> res.outputs.out_file         # doctest: +SKIP
    'subj_201_func_run02.nii'        # doctest: +SKIP

    >>> rename3 = Rename(format_string="%(subject_id)s_%(seq)s_run%(run)02d.nii")
    >>> rename3.inputs.in_file = os.path.join(datadir, "func_epi_1_1.nii")
    >>> rename3.inputs.parse_string = r"func_(?P<seq>\w*)_.*"
    >>> rename3.inputs.subject_id = "subj_201"
    >>> rename3.inputs.run = 2
    >>> res = rename3.run()          # doctest: +SKIP
    >>> res.outputs.out_file         # doctest: +SKIP
    'subj_201_epi_run02.nii'         # doctest: +SKIP

    """
    input_spec = RenameInputSpec
    output_spec = RenameOutputSpec
    def __init__(self, format_string=..., **inputs) -> None:
        ...
    


class SplitInputSpec(BaseInterfaceInputSpec):
    inlist = ...
    splits = ...
    squeeze = ...


class Split(IOBase):
    """Basic interface class to split lists into multiple outputs

    Examples
    --------

    >>> from nipype.interfaces.utility import Split
    >>> sp = Split()
    >>> _ = sp.inputs.trait_set(inlist=[1, 2, 3], splits=[2, 1])
    >>> out = sp.run()
    >>> out.outputs.out1
    [1, 2]

    """
    input_spec = SplitInputSpec
    output_spec = DynamicTraitedSpec


class SelectInputSpec(BaseInterfaceInputSpec):
    inlist = InputMultiPath(traits.Any, mandatory=True, desc="list of values to choose from")
    index = InputMultiPath(traits.Int, mandatory=True, desc="0-based indices of values to choose")


class SelectOutputSpec(TraitedSpec):
    out = OutputMultiPath(traits.Any, desc="list of selected values")


class Select(IOBase):
    """Basic interface class to select specific elements from a list

    Examples
    --------

    >>> from nipype.interfaces.utility import Select
    >>> sl = Select()
    >>> _ = sl.inputs.trait_set(inlist=[1, 2, 3, 4, 5], index=[3])
    >>> out = sl.run()
    >>> out.outputs.out
    4

    >>> _ = sl.inputs.trait_set(inlist=[1, 2, 3, 4, 5], index=[3, 4])
    >>> out = sl.run()
    >>> out.outputs.out
    [4, 5]

    """
    input_spec = SelectInputSpec
    output_spec = SelectOutputSpec


class AssertEqualInputSpec(BaseInterfaceInputSpec):
    volume1 = ...
    volume2 = ...


class AssertEqual(BaseInterface):
    input_spec = AssertEqualInputSpec

