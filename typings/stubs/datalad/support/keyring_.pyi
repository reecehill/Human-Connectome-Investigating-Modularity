"""
This type stub file was generated by pyright.
"""

"""Adapters and decorators for keyrings
"""
class Keyring:
    """Adapter to keyring module

    It also delays import of keyring which takes 300ms I guess due to all plugins etc
    """
    def __init__(self) -> None:
        ...
    
    def get(self, name, field): # -> str | None:
        ...
    
    def set(self, name, field, value): # -> None:
        ...
    
    def delete(self, name, field=...): # -> None:
        ...
    


class MemoryKeyring:
    """A simple keyring which just stores provided info in memory

    Primarily for testing
    """
    def __init__(self) -> None:
        ...
    
    def get(self, name, field): # -> None:
        """Get password from the specified service.
        """
        ...
    
    def set(self, name, field, value): # -> None:
        """Set password for the user in the specified service.
        """
        ...
    
    def delete(self, name, field=...): # -> None:
        """Delete password from the specified service.
        """
        ...
    


keyring = ...