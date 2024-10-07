from pathlib import Path
from typing import List
import modules.globals as g

def deleteFilesByExtensions(directory: Path, extensions: List[str], recursive: bool = False, depth: int = 0):
    """
    Delete files in the specified directory that match any of the given extensions.
    
    Parameters:
    - directory: The directory where the files are located.
    - extensions: A list of extensions to delete (e.g., ['*.nii.gz', '*.txt']).
    - recursive: If True, will search subdirectories up to the specified depth.
    - depth: The maximum depth to search in subdirectories (0 = no recursion, 1 = direct subfolders, etc.).
    """
    
    # Loop through each extension
    for ext in extensions:
        # Choose the correct method based on recursion flag
        if recursive:
            # Using rglob for recursive search and filtering by depth
            for file_path in directory.rglob(ext):
                # Only proceed if the file is within the specified depth
                relative_depth = len(file_path.relative_to(directory).parts) - 1
                if depth == -1 or relative_depth <= depth:
                    if file_path.exists():
                        file_path.unlink()  # Delete the file
                        g.logger.info(f"Deleted: {file_path}")
                    else:
                        g.logger.info(f"File does not exist: {file_path}")
        else:
            # Non-recursive search with glob
            for file_path in directory.glob(ext):
                if file_path.exists():
                    file_path.unlink()  # Delete the file
                    g.logger.info(f"Deleted: {file_path}")
                else:
                    g.logger.info(f"File does not exist: {file_path}")