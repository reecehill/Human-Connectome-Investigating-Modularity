"""
This type stub file was generated by pyright.
"""

from ..utils import auto_repr

"""Interface information about credentials

Provides minimalistic interface to deal (query, request, store) with most common
types of credentials.  To be used by Authenticators
"""
__dev_doc__ = ...
lgr = ...
@auto_repr
class Credential:
    """Base class for different types of credentials
    """
    _FIELDS = ...
    _KNOWN_ATTRS = ...
    def __init__(self, name, url=..., keyring=...) -> None:
        """
        Parameters
        ----------
        name : str
            Name of the credential, as it would be identified by in the centralized
            storage of credentials
        url : str, optional
            URL string to point users to where to seek obtaining the credentials
        keyring : a keyring
            An object providing (g|s)et_password.  If None, keyring module is used
            as is
        """
        ...
    
    @property
    def is_known(self): # -> bool:
        """Return True if values for all fields of the credential are known"""
        ...
    
    def enter_new(self, instructions=..., **kwargs): # -> None:
        """Enter new values for the credential fields

        Parameters
        ----------
        instructions : str, optional
          If given, the auto-generated instructions based on a login-URL are
          replaced by the given string
        **kwargs
          Any given key value pairs with non-None values are used to set the
          field `key` to the given value, without asking for user input
        """
        ...
    
    def __call__(self): # -> dict[Unknown, Unknown]:
        """Obtain credentials from a keyring and if any is not known -- ask"""
        ...
    
    def set(self, **kwargs): # -> None:
        """Set field(s) of the credential"""
        ...
    
    def get(self, f, default=...): # -> str | None:
        """Get a field of the credential"""
        ...
    
    def delete(self): # -> None:
        """Deletes credential values from the keyring"""
        ...
    


class UserPassword(Credential):
    """Simple type of a credential which consists of user/password pair"""
    _FIELDS = ...
    is_expired = ...


class Token(Credential):
    """Simple type of a credential which provides a single token"""
    _FIELDS = ...
    is_expired = ...


class AWS_S3(Credential):
    """Credential for AWS S3 service"""
    _FIELDS = ...
    @property
    def is_expired(self): # -> bool:
        ...
    


@auto_repr
class CompositeCredential(Credential):
    """Credential which represent a sequence of Credentials where front one is exposed to user
    """
    _CREDENTIAL_CLASSES = ...
    _CREDENTIAL_ADAPTERS = ...
    def enter_new(self): # -> None:
        ...
    
    def __call__(self):
        """Obtain credentials from a keyring and if any is not known -- ask"""
        ...
    


class NDA_S3(CompositeCredential):
    """Credential to access NDA AWS

    So for NDA we need a credential which is a composite credential.
    User provides UserPassword and then some adapter generates AWS_S3
    out of it
    """
    _CREDENTIAL_CLASSES = ...
    _CREDENTIAL_ADAPTERS = ...


class LORIS_Token(CompositeCredential):
    _CREDENTIAL_CLASSES = ...
    _CREDENTIAL_ADAPTERS = ...
    def __init__(self, name, url=..., keyring=...) -> None:
        ...
    


CREDENTIAL_TYPES = ...