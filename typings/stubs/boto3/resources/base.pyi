"""
This type stub file was generated by pyright.
"""

logger = ...
class ResourceMeta:
    """
    An object containing metadata about a resource.
    """
    def __init__(self, service_name, identifiers=..., client=..., data=..., resource_model=...) -> None:
        ...
    
    def __repr__(self): # -> str:
        ...
    
    def __eq__(self, other) -> bool:
        ...
    
    def copy(self): # -> ResourceMeta:
        """
        Create a copy of this metadata object.
        """
        ...
    


class ServiceResource:
    """
    A base class for resources.

    :type client: botocore.client
    :param client: A low-level Botocore client instance
    """
    meta = ...
    def __init__(self, *args, **kwargs) -> None:
        ...
    
    def __repr__(self): # -> str:
        ...
    
    def __eq__(self, other) -> bool:
        ...
    
    def __hash__(self) -> int:
        ...
    

