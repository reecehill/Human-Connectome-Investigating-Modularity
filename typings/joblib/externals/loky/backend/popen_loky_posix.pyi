"""
This type stub file was generated by pyright.
"""

__all__ = ['Popen']
class _DupFd:
    def __init__(self, fd) -> None:
        ...
    
    def detach(self):
        ...
    


class Popen:
    method = ...
    DupFd = _DupFd
    def __init__(self, process_obj) -> None:
        ...
    
    def duplicate_for_child(self, fd):
        ...
    
    def poll(self, flag=...): # -> None:
        ...
    
    def wait(self, timeout=...): # -> None:
        ...
    
    def terminate(self): # -> None:
        ...
    
    @staticmethod
    def thread_is_spawning(): # -> Literal[True]:
        ...
    


if __name__ == '__main__':
    parser = ...
    args = ...
    info = ...
    exitcode = ...
    exitcode = ...