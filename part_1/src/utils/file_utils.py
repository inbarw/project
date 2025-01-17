from pathlib import Path
import os

def get_csv_file_paths(directory_path):
    """
    Get a list of all CSV file paths in the given directory.

    :param directory_path: Path to the directory containing CSV files.
    :return: Generator yielding paths to CSV files.
    :raises ValueError: If the given directory path is not valid.
    """
    directory_path = Path(directory_path)
    if not directory_path.is_dir():
        raise ValueError(f"{directory_path} is not a valid directory.")

    for filename in os.listdir(directory_path):
        if filename.endswith('.csv'):  # Ensure the file is a CSV
            yield directory_path / filename