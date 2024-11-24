from pathlib import Path
from typing import Callable, TypedDict, List, Optional, Any
import subprocess


class SaverType(TypedDict):
    user: str
    host: str
    uploadRunCount: int
    uploadName: str
    userHost: str
    pathToKey: str
    sshCmd: List[str]
    connection: subprocess.Popen[Any]
    rsyncCmd: Optional[List[str]]
    compress: Callable[[List[Path]], str]