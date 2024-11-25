import shutil
from pathlib import Path
from typing import Union

from modules.file_directory.file_directory import createDirectories
import modules.globals as g


def copy_file(
    source_path: Union[str, Path], destination_path: Union[str, Path]
) -> None:
    """
    Copies a file from the source path to the destination path.

    Parameters:
    - source_path (str or Path): The full path to the source file.
    - destination_path (str or Path): The full path to the destination, including the new file name if desired.

    Returns:
    - None
    """
    try:
        # Ensure the source file exists
        if not Path(source_path).is_file():
            raise FileNotFoundError(f"Source file not found: {source_path}")

        # Ensure the destination directory exists
        createDirectories(
            directoryPaths=[Path(destination_path).parent],
            createParents=True,
            throwErrorIfExists=False,
        )

        # Copy the file
        shutil.copy(source_path, destination_path)
        g.logger.info(
            f"File copied successfully from '{source_path}' to '{destination_path}'."
        )
    except Exception as e:
        g.logger.error("Error copying file: {e}")
        raise
