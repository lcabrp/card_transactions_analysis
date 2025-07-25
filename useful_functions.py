# useful_functions.py
from pathlib import Path
import pandas as pd

def get_safe_int_type(series: pd.Series) -> str:
    """Determine the smallest safe integer type for a series"""
    min_val = series.min()
    max_val = series.max()
    
    if min_val >= 0:  # Unsigned types
        if max_val <= 255:  # 2^8 - 1
            return 'uint8'
        elif max_val <= 65535: # 2^16 - 1
            return 'uint16'
        elif max_val <= 4294967295: # 2^32 - 1
            return 'uint32'
        else:
            return 'uint64'
    else:  # Signed types needed
        if min_val >= -128 and max_val <= 127: # 2^7 - 1
            return 'int8'
        elif min_val >= -32768 and max_val <= 32767: # 2^15 - 1
            return 'int16'
        elif min_val >= -2147483648 and max_val <= 2147483647: # 2^31 - 1
            return 'int32'
        else:
            return 'int64'

def show_df_info(df: pd.DataFrame) -> None:
    """
    Display information about a DataFrame including the top few rows, column names, shape, and data types.
    """
    print("\nFirst few rows of the DataFrame:")
    print(df.head(5))
    print("\nDataFrame columns:")
    print(list(df.columns))  # Print column names
    print(f"\nDataFrame shape: {df.shape}")  # Print shape
    print("\nDataFrame info:")
    print(df.info(memory_usage='deep'))  # Print info with deep memory usage

def optimize_df_types(df: pd.DataFrame, df_types: dict) -> pd.DataFrame:
    """
    Optimize memory usage of DataFrame based on provided types
    The expected dictionary should have data types as keys, and a list of the columns that need to be converted to that type.
    Example:
    {
        'category': ['col1', 'col2'],
        'string': ['col3'],
        'uint16': ['col4', 'col5'],
        'float32': ['col6', 'col7']
    }
    """
    # Check if df_types is provided
    if df_types is None:
        return df  # Return the original DataFrame if no types are provided

    # Create a copy of the DataFrame to avoid modifying the original
    df_optimized = df.copy()
    
    # Apply the specified data types
    for dtype, columns in df_types.items():
        for col in columns:
            if col in df_optimized.columns:  # Safety check
                df_optimized[col] = df_optimized[col].astype(dtype)
            else:
                print(f"Warning: Column '{col}' not found in DataFrame")
    
    return df_optimized


def get_files_in_directory(directory_path, file_mask='*.csv', recursive=False) -> list:
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

    print("Useful functions loaded successfully")
