from pathlib import Path
from typing import List
import config
import modules.globals as g
from shutil import rmtree

def deleteFilesByExtensions(directories: List[Path], extensions: List[str], recursive: bool = False, depth: int = 0):
    """
    Delete files in the specified directories that match any of the given extensions.
    
    Parameters:
    - directories: A list of directories where the files are located.
    - extensions: A list of extensions to delete (e.g., ['*.nii.gz', '*.txt']).
    - recursive: If True, will search subdirectories up to the specified depth.
    - depth: The maximum depth to search in subdirectories (-1 = no depth limit, 0 = no recursion, 1 = direct subfolders, etc.).
    """
    if(len(config.ALL_SUBJECTS)<5):
        g.logger.info("Skipped deleting files as small sample size.")
        return 
    # Loop through each directory
    for directory in directories:
        # Ensure the directory exists
        if not directory.exists() or not directory.is_dir():
            g.logger.warning(f"Directory does not exist or is not a directory: {directory}")
            continue

        # Loop through each extension
        for ext in extensions:
            # Choose the correct method based on recursion flag
            if recursive:
                # Using rglob for recursive search and filtering by depth
                for file_path in directory.rglob(ext):
                    # Only proceed if the file is within the specified depth
                    relative_depth = len(file_path.relative_to(directory).parts) - 1
                    if depth == -1 or relative_depth <= depth:
                        if file_path.is_file():
                            file_path.unlink()  # Delete the file
                            g.logger.info(f"Deleted: {file_path}")
                        elif file_path.is_dir():
                            rmtree(str(file_path.resolve()))
                            g.logger.info(f"Deleted: {file_path}")
                        else:
                            g.logger.info(f"File/folder does not exist: {file_path}")
            else:
                # Non-recursive search with glob
                for file_path in directory.glob(ext):
                    if file_path.is_file():
                        file_path.unlink()  # Delete the file
                        g.logger.info(f"Deleted: {file_path}")
                    elif file_path.is_dir():
                        rmtree(str(file_path.resolve()))
                        g.logger.info(f"Deleted: {file_path}")
                    else:
                        g.logger.info(f"File/folder does not exist: {file_path}")