"""
This type stub file was generated by pyright.
"""

from multiprocessing.process import BaseProcess

class LokyProcess(BaseProcess):
    _start_method = ...
    def __init__(self, group=..., target=..., name=..., args=..., kwargs=..., daemon=..., init_main_module=..., env=...) -> None:
        ...
    


class LokyInitMainProcess(LokyProcess):
    _start_method = ...
    def __init__(self, group=..., target=..., name=..., args=..., kwargs=..., daemon=...) -> None:
        ...
    


class AuthenticationKey(bytes):
    def __reduce__(self): # -> tuple[Type[AuthenticationKey], tuple[bytes]]:
        ...
    

