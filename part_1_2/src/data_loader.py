import os

import pandas as pd
from pathlib import Path
from part_1_2.src.utils.db_utils import get_db_connection

class DataLoader:
    def __init__(self, db_connection=None):
        self.conn = db_connection or get_db_connection()

    def load_csv_to_postgres(self, csv_file_path):
        table_name = Path(csv_file_path).stem  # This removes the .csv extension

        # Open the CSV file and import data into the table
        with open(csv_file_path, 'r') as file:
            next(file)  # Skip the header row
            cur = self.conn.cursor()
            cur.copy_from(file, table_name, sep=',')  # Adjust separator if needed
            self.conn.commit()
            cur.close()

        print(f"Data from '{csv_file_path}' imported into '{table_name}'.")

    def get_table_row_count(self, table_name):
        cur = self.conn.cursor()
        cur.execute(f"SELECT COUNT(*) FROM {table_name}")
        return cur.fetchone()[0]

    def close(self):
        self.conn.close()