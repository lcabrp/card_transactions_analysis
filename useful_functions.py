# useful_functions.py

from pathlib import Path


def get_files_in_directory_pathlib(directory_path, file_mask='*.csv', recursive=False) -> list:
    """
    Get all files (.csv by default) in a directory.
    
    Args:
        directory_path: Path to the directory
        file_mask: File pattern to match(default: '*.csv')
        recursive: If True, process subdirectories recursively
        
    Returns:
        list: List of file paths
    """   
    
    pattern = '**/' + file_mask if recursive else file_mask
    file_list = [str(path) for path in Path(directory_path).rglob(pattern)]
    
    if not file_list:
        print(f"No files found in {directory_path} matching pattern '{file_mask}'")
    
    return file_list

if __name__ == "__main__":

    # Example usage of get_files_in_directory
    # This is just for demonstration purposes and can be removed or modified as needed.
    files = get_files_in_directory('data', file_mask='*.csv', recursive=False) # or recursive=True
    
    for f in files:
        print(f)