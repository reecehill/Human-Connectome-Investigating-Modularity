"""
This type stub file was generated by pyright.
"""

from .specs import BaseInterfaceInputSpec, CommandLineInputSpec, MpiCommandLineInputSpec, StdOutCommandLineInputSpec

"""
Nipype interfaces core
......................

Defines the ``Interface`` API and the body of the
most basic interfaces.
The I/O specifications corresponding to these base
interfaces are found in the ``specs`` module.

"""
iflogger = ...
VALID_TERMINAL_OUTPUT = ...
__docformat__ = ...
class Interface:
    """This is an abstract definition for Interface objects.

    It provides no functionality.  It defines the necessary attributes
    and methods all Interface objects should have.

    """
    input_spec = ...
    output_spec = ...
    _can_resume = ...
    _always_run = ...
    @property
    def can_resume(self): # -> bool:
        """Defines if the interface can reuse partial results after interruption.
        Only applies to interfaces being run within a workflow context."""
        ...
    
    @property
    def always_run(self): # -> bool:
        """Should the interface be always run even if the inputs were not changed?
        Only applies to interfaces being run within a workflow context."""
        ...
    
    @property
    def version(self):
        """interfaces should implement a version property"""
        ...
    
    @classmethod
    def help(cls, returnhelp=...): # -> LiteralString | None:
        """Prints class help"""
        ...
    
    def __init__(self) -> None:
        """Subclasses must implement __init__"""
        ...
    
    def run(self):
        """Execute the command."""
        ...
    
    def aggregate_outputs(self, runtime=..., needed_outputs=...):
        """Called to populate outputs"""
        ...
    


class BaseInterface(Interface):
    """Implement common interface functionality.

    * Initializes inputs/outputs from input_spec/output_spec
    * Provides help based on input_spec and output_spec
    * Checks for mandatory inputs before running an interface
    * Runs an interface and returns results
    * Determines which inputs should be copied or linked to cwd

    This class does not implement aggregate_outputs, input_spec or
    output_spec. These should be defined by derived classes.

    This class cannot be instantiated.

    Attributes
    ----------
    input_spec: :obj:`nipype.interfaces.base.specs.TraitedSpec`
        points to the traited class for the inputs
    output_spec: :obj:`nipype.interfaces.base.specs.TraitedSpec`
        points to the traited class for the outputs
    _redirect_x: bool
        should be set to ``True`` when the interface requires
        connecting to a ``$DISPLAY`` (default is ``False``).
    resource_monitor: bool
        If ``False``, prevents resource-monitoring this interface
        If ``True`` monitoring will be enabled IFF the general
        Nipype config is set on (``resource_monitor = true``).

    """
    input_spec = BaseInterfaceInputSpec
    _version = ...
    _additional_metadata = ...
    _redirect_x = ...
    _references = ...
    resource_monitor = ...
    _etelemetry_version_data = ...
    def __init__(self, from_file=..., resource_monitor=..., ignore_exception=..., **inputs) -> None:
        ...
    
    def run(self, cwd=..., ignore_exception=..., **inputs): # -> InterfaceResult:
        """Execute this interface.

        This interface will not raise an exception if runtime.returncode is
        non-zero.

        Parameters
        ----------
        cwd : specify a folder where the interface should be run
        inputs : allows the interface settings to be updated

        Returns
        -------
        results :  :obj:`nipype.interfaces.base.support.InterfaceResult`
            A copy of the instance that was executed, provenance information and,
            if successful, results

        """
        ...
    
    def aggregate_outputs(self, runtime=..., needed_outputs=...): # -> None:
        """Collate expected outputs and apply output traits validation."""
        ...
    
    @property
    def version(self): # -> None:
        ...
    
    def load_inputs_from_json(self, json_file, overwrite=...): # -> None:
        """
        A convenient way to load pre-set inputs from a JSON file.
        """
        ...
    
    def save_inputs_to_json(self, json_file): # -> None:
        """
        A convenient way to save current inputs to a JSON file.
        """
        ...
    


class SimpleInterface(BaseInterface):
    """An interface pattern that allows outputs to be set in a dictionary
    called ``_results`` that is automatically interpreted by
    ``_list_outputs()`` to find the outputs.

    When implementing ``_run_interface``, set outputs with::

        self._results[out_name] = out_value

    This can be a way to upgrade a ``Function`` interface to do type checking.

    Examples
    --------
    >>> from nipype.interfaces.base import (
    ...     SimpleInterface, BaseInterfaceInputSpec, TraitedSpec)

    >>> def double(x):
    ...    return 2 * x
    ...
    >>> class DoubleInputSpec(BaseInterfaceInputSpec):
    ...     x = traits.Float(mandatory=True)
    ...
    >>> class DoubleOutputSpec(TraitedSpec):
    ...     doubled = traits.Float()
    ...
    >>> class Double(SimpleInterface):
    ...     input_spec = DoubleInputSpec
    ...     output_spec = DoubleOutputSpec
    ...
    ...     def _run_interface(self, runtime):
    ...          self._results['doubled'] = double(self.inputs.x)
    ...          return runtime

    >>> dbl = Double()
    >>> dbl.inputs.x = 2
    >>> dbl.run().outputs.doubled
    4.0

    """
    def __init__(self, from_file=..., resource_monitor=..., **inputs) -> None:
        ...
    


class CommandLine(BaseInterface):
    """Implements functionality to interact with command line programs
    class must be instantiated with a command argument

    Parameters
    ----------
    command : str
        define base immutable `command` you wish to run
    args : str, optional
        optional arguments passed to base `command`

    Examples
    --------
    >>> import pprint
    >>> from nipype.interfaces.base import CommandLine
    >>> cli = CommandLine(command='ls', environ={'DISPLAY': ':1'})
    >>> cli.inputs.args = '-al'
    >>> cli.cmdline
    'ls -al'

    >>> # Use get_traitsfree() to check all inputs set
    >>> pprint.pprint(cli.inputs.get_traitsfree())  # doctest:
    {'args': '-al',
     'environ': {'DISPLAY': ':1'}}

    >>> cli.inputs.get_hashval()[0][0]
    ('args', '-al')
    >>> cli.inputs.get_hashval()[1]
    '11c37f97649cd61627f4afe5136af8c0'

    """
    input_spec = CommandLineInputSpec
    _cmd_prefix = ...
    _cmd = ...
    _version = ...
    _terminal_output = ...
    _write_cmdline = ...
    @classmethod
    def set_default_terminal_output(cls, output_type): # -> None:
        """Set the default terminal output for CommandLine Interfaces.

        This method is used to set default terminal output for
        CommandLine Interfaces.  However, setting this will not
        update the output type for any existing instances.  For these,
        assign the <instance>.terminal_output.
        """
        ...
    
    def __init__(self, command=..., terminal_output=..., write_cmdline=..., **inputs) -> None:
        ...
    
    @property
    def cmd(self): # -> Any:
        """sets base command, immutable"""
        ...
    
    @property
    def cmdline(self): # -> LiteralString:
        """`command` plus any arguments (args)
        validates arguments and generates command line"""
        ...
    
    @property
    def terminal_output(self): # -> str:
        ...
    
    @terminal_output.setter
    def terminal_output(self, value): # -> None:
        ...
    
    @property
    def write_cmdline(self): # -> bool:
        ...
    
    @write_cmdline.setter
    def write_cmdline(self, value): # -> None:
        ...
    
    def raise_exception(self, runtime):
        ...
    
    def version_from_command(self, flag=..., cmd=...): # -> bytes | None:
        ...
    


class StdOutCommandLine(CommandLine):
    input_spec = StdOutCommandLineInputSpec


class MpiCommandLine(CommandLine):
    """Implements functionality to interact with command line programs
    that can be run with MPI (i.e. using 'mpiexec').

    Examples
    --------
    >>> from nipype.interfaces.base import MpiCommandLine
    >>> mpi_cli = MpiCommandLine(command='my_mpi_prog')
    >>> mpi_cli.inputs.args = '-v'
    >>> mpi_cli.cmdline
    'my_mpi_prog -v'

    >>> mpi_cli.inputs.use_mpi = True
    >>> mpi_cli.inputs.n_procs = 8
    >>> mpi_cli.cmdline
    'mpiexec -n 8 my_mpi_prog -v'

    """
    input_spec = MpiCommandLineInputSpec
    @property
    def cmdline(self): # -> LiteralString:
        """Adds 'mpiexec' to beginning of command"""
        ...
    


class SEMLikeCommandLine(CommandLine):
    """In SEM derived interface all outputs have corresponding inputs.
    However, some SEM commands create outputs that are not defined in the XML.
    In those cases one has to create a subclass of the autogenerated one and
    overload the _list_outputs method. _outputs_from_inputs should still be
    used but only for the reduced (by excluding those that do not have
    corresponding inputs list of outputs.
    """
    ...


class LibraryBaseInterface(BaseInterface):
    _pkg = ...
    imports = ...
    def __init__(self, check_import=..., *args, **kwargs) -> None:
        ...
    
    @property
    def version(self): # -> None:
        ...
    


class PackageInfo:
    _version = ...
    version_cmd = ...
    version_file = ...
    @classmethod
    def version(klass): # -> None:
        ...
    
    @staticmethod
    def parse_version(raw_info):
        ...
    

