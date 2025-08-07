
# useful_functions.py
from pathlib import Path
import pandas as pd
import glob
import sqlite3
import numpy as np
from typing import Union, List, Dict, Any
import gc
import sys

def get_files_dir(directory_path: str, file_mask: str = '*.csv') -> list:
    """
    Get all files matching the pattern in a directory.

    Args:
        directory_path: Path to the directory containing files
        file_mask: File pattern to match (default: '*.csv')

    Returns:
        list: List of file paths matching the pattern
    """
    # Ensure directory path ends with separator
    if not directory_path.endswith(('/', '\\')):
        directory_path += '/'
    
    # Check if directory exists
    if not Path(directory_path).exists():
        raise ValueError(f"Directory not found: {directory_path}")
    
    # Build the search pattern and get files
    pattern = directory_path + file_mask
    files = glob.glob(pattern)

    return files

def get_safe_int_type(series: pd.Series) -> str:
    """Determine the smallest safe integer type for a series"""

    if type(series) != pd.Series:
        raise TypeError("Expected a pandas Series")

    min_val = series.min()
    max_val = series.max()

    # Check ranges for different integer types
    if min_val >= 0:  # Unsigned types
        if max_val <= 255:
            return 'uint8'
        elif max_val <= 65535:
            return 'uint16'
        elif max_val <= 4294967295:
            return 'uint32'
        else:
            return 'uint64'
    else:  # Signed types
        if min_val >= -128 and max_val <= 127:
            return 'int8'
        elif min_val >= -32768 and max_val <= 32767:
            return 'int16'
        elif min_val >= -2147483648 and max_val <= 2147483647:
            return 'int32'
        else:
            return 'int64'

def show_df_info(df: pd.DataFrame) -> None:
    """
    Display information about a DataFrame including the top few rows, column names, shape, and data types.
    """
    if type(df) != pd.DataFrame:
        raise TypeError("Expected a pandas DataFrame")
    
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

    Example: {'type': ['col1', 'col2'] }
    """
    if df_types is None:
        return df

    df_optimized = df.copy()
    df_columns = df_optimized.columns

    for dtype, columns in df_types.items():
        for col in columns:
            if col in df_columns:
                df_optimized[col] = df_optimized[col].astype(dtype)
            else:
                print(f"Warning: Column '{col}' not found in DataFrame")
    
    return df_optimized

def get_missing_values(df: pd.DataFrame) -> pd.Series:
    """Get the number of missing values in each column of a DataFrame"""
    if type(df) != pd.DataFrame:
        raise TypeError("Expected a pandas DataFrame")
    return df.isnull().sum()

def check_primary_key_candidates(df: pd.DataFrame, columns: list) -> dict:
    """
    Check if specified columns can serve as primary keys (unique, non-null).

    Args:
        df: DataFrame to check
        columns: List of column names to evaluate as primary key candidates

    Returns:
        dict: Results for each column with uniqueness and null information
    """
    # Input validation
    if type(df) != pd.DataFrame:
        raise TypeError("Expected a pandas DataFrame")
    if type(columns) != list:
        raise TypeError("Expected a list of column names")
    if not all(isinstance(col, str) for col in columns):
        raise TypeError("Column names must be strings")
    
    results = {}
    df_columns = df.columns
    # Check each column
    for col in columns:
        if col not in df_columns:
            results[col] = {
                'status': 'COLUMN_NOT_FOUND',
                'unique_count': 0,
                'total_count': 0,
                'null_count': 0,
                'duplicate_count': 0,
                'sample_duplicates': {}
            }
            continue

        total_count = len(df)
        unique_count = df[col].nunique()
        null_count = df[col].isnull().sum()
        duplicate_count = total_count - unique_count

        # Determine if it can be a primary key
        if null_count > 0:
            status = 'HAS_NULLS'
        elif duplicate_count > 0:
            status = 'HAS_DUPLICATES'
        else:
            status = 'VALID_PRIMARY_KEY'

        # Get sample duplicates if there are any (and not too many)
        # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.duplicated.html#pandas.Series.duplicated
        sample_duplicates = {}
        if status == 'HAS_DUPLICATES' and duplicate_count <= 10:
            duplicates = df[df[col].duplicated(keep=False)][col].value_counts().head(5) # Get the top 5 duplicates
            sample_duplicates = duplicates.to_dict()

        results[col] = {
            'status': status,
            'unique_count': unique_count,
            'total_count': total_count,
            'null_count': null_count,
            'duplicate_count': duplicate_count,
            'sample_duplicates': sample_duplicates
        }

    return results

def display_primary_key_analysis(pk_results: dict) -> None:
    """
    Display detailed primary key analysis results.

    Args:
        pk_results: Results from check_primary_key_candidates function
    """
    for col, result in pk_results.items():
        if result['status'] == 'COLUMN_NOT_FOUND':
            print(f"\nPrimary Key Analysis for '{col}':")
            print(f"  Column not found in DataFrame")
            continue

        print(f"\nPrimary Key Analysis for '{col}':")
        print(f"  Total rows: {result['total_count']:,}")
        print(f"  Unique values: {result['unique_count']:,}")
        print(f"  Null values: {result['null_count']:,}")
        print(f"  Duplicate values: {result['duplicate_count']:,}")
        print(f"  Status: {result['status']}")

        # Show sample duplicates if available
        if result['sample_duplicates']:
            print(f"  Sample duplicates:")
            for value, count in result['sample_duplicates'].items():
                print(f"    '{value}': appears {count} times")

def process_and_merge_files(file_list: list, optimization_types: dict, delimiter: str = '|') -> pd.DataFrame:
    """
    Process multiple CSV files by optimizing data types and merging them.
    
    Args:
        file_list: List of file paths to process
        optimization_types: Dictionary with data types and columns to optimize
        delimiter: CSV delimiter (default: '|')
    
    Returns:
        pd.DataFrame: Merged and optimized DataFrame
    """
    optimized_chunks = []
    total_rows = 0
    
    for i, file_path in enumerate(file_list):
        print(f"Processing file {i+1}/{len(file_list)}: {file_path}")
        
        # Load and optimize
        chunk_df = pd.read_csv(file_path, delimiter=delimiter)
        chunk_df = optimize_df_types(chunk_df, optimization_types)
        
        optimized_chunks.append(chunk_df)
        total_rows += len(chunk_df)
        
        if i % 10 == 0:  # Progress update every 10 files
            print(f"Processed {total_rows:,} rows so far...")
    
    # Merge all chunks
    print("Merging all optimized files...")
    merged_df = pd.concat(optimized_chunks, ignore_index=True)
    
    # Cleanup to free up memory
    del optimized_chunks
    import gc
    gc.collect()
    
    return merged_df     

def create_fraud_detection_db(customers_df: pd.DataFrame, transactions_df: pd.DataFrame) -> None:
    """
    Create fraud detection database with proper primary keys and foreign keys.

    Args:
        customers_df: Customer DataFrame
        transactions_df: Transaction DataFrame
    """
    conn = sqlite3.connect('fraud_detection.db')
    cursor = conn.cursor()

    try:
        cursor.execute('PRAGMA foreign_keys = OFF')
        cursor.execute('DROP TABLE IF EXISTS transactions')
        cursor.execute('DROP TABLE IF EXISTS customers')
        cursor.execute('''
            CREATE TABLE customers (
                ssn TEXT PRIMARY KEY,
                cc_num TEXT,
                first TEXT,
                last TEXT,
                gender TEXT,
                street TEXT,
                city TEXT,
                state TEXT,
                zip TEXT,
                lat REAL,
                long REAL,
                city_pop INTEGER,
                job TEXT,
                dob TEXT,
                acct_num TEXT,
                pop_group TEXT,
                location TEXT
            )
        ''')


        cursor.execute('''
            CREATE TABLE transactions (
                trans_num TEXT PRIMARY KEY,
                ssn TEXT,
                trans_date TEXT,
                trans_time TEXT,
                unix_time INTEGER,
                category TEXT,
                amt REAL,
                is_fraud INTEGER,
                merchant TEXT,
                merch_lat REAL,
                merch_long REAL,
                FOREIGN KEY (ssn) REFERENCES customers (ssn)
            )
        ''')

        customers_df.to_sql('customers', conn, if_exists='append', index=False)
        transactions_df.to_sql('transactions', conn, if_exists='append', index=False)
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_transactions_ssn ON transactions(ssn)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_transactions_unix_time ON transactions(unix_time)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_transactions_is_fraud ON transactions(is_fraud)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_transactions_category ON transactions(category)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_customers_state ON customers(state)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_customers_pop_group ON customers(pop_group)')

        cursor.execute('PRAGMA foreign_keys = ON')

        conn.commit()
        print("Database created successfully with proper primary keys, foreign keys, and indexes")

    except Exception as e:
        print(f"Error creating database: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()


def calculate_distance(lat1: Union[float, pd.Series, np.ndarray],
                      lon1: Union[float, pd.Series, np.ndarray],
                      lat2: Union[float, pd.Series, np.ndarray],
                      lon2: Union[float, pd.Series, np.ndarray]) -> Union[float, np.ndarray]:
    """
    Calculate the great circle distance between two points on Earth using the Haversine formula.

    Args:
        lat1: Latitude of first point(s) in decimal degrees (float, Series, or array)
        lon1: Longitude of first point(s) in decimal degrees (float, Series, or array)
        lat2: Latitude of second point(s) in decimal degrees (float, Series, or array)
        lon2: Longitude of second point(s) in decimal degrees (float, Series, or array)

    Returns:
        Distance between the points in kilometers (float if inputs are scalars, array if inputs are Series/arrays)

    Example:
        >>> distance = calculate_distance(40.7128, -74.0060, 34.0522, -118.2437)
        >>> print(f"Distance: {distance:.2f} km")
        Distance: 3944.42 km
    """

    # Convert to numpy arrays to handle both Series and individual values
    lat1, lon1, lat2, lon2 = map(np.asarray, [lat1, lon1, lat2, lon2])
    
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))

    # Earth's radius in kilometers
    earth_radius_km = 6371

    return c * earth_radius_km

if __name__ == "__main__":

    print("Useful functions loaded successfully")
