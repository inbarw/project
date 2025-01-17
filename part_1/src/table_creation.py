import csv
import os
from typing import List, Tuple
from pathlib import Path
from part_1.src.utils.db_utils import get_db_connection


class TableCreator:
    def __init__(self, db_connection=None):
        self.conn = db_connection or get_db_connection()

    @staticmethod
    def is_float(value: str) -> bool:
        try:
            float(value)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_date(value: str) -> bool:
        try:
            from datetime import datetime
            datetime.strptime(value, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    # Function to automatically determine column data types from the CSV file
    def infer_column_types(self, csv_file_path: str) -> List[Tuple[str, str]]:
        column_types = []
        with open(csv_file_path, 'r') as file:
            reader = csv.reader(file)
            headers = next(reader)  # Read header row to get column names

            # Try to infer the type of each column based on the first data row
            for row in reader:
                for i, value in enumerate(row):
                    if value.isdigit():
                        col_type = "INT"
                    elif self.is_float(value):
                        col_type = "FLOAT"
                    elif self.is_date(value):
                        col_type = "DATE"
                    else:
                        col_type = "VARCHAR(255)"

                    # If it's the first row, initialize column types
                    if len(column_types) < len(headers):
                        column_types.append((headers[i], col_type))
                    else:
                        # Check if the inferred type is consistent across rows
                        if column_types[i][1] != col_type:
                            column_types[i] = (
                            headers[i], "VARCHAR(255)")  # Fallback to VARCHAR if types are inconsistent

        return column_types

    # Function to create the table dynamically based on the CSV
    def create_table_from_csv(self, csv_file_path):
        # Infer the column types from the CSV
        column_types = self.infer_column_types(csv_file_path)
        table_name = Path(csv_file_path).stem

        # Construct the CREATE TABLE SQL statement
        create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ("
        for col_name, col_type in column_types:
            create_table_sql += f"{col_name} {col_type}, "

        # Remove the trailing comma and space, then close the parentheses
        create_table_sql = create_table_sql.rstrip(", ") + ");"

        # Create the table
        cur = self.conn.cursor()
        cur.execute(create_table_sql)
        self.conn.commit()
        cur.close()

        print(f"Table '{table_name}' created successfully.")

    def clear_table(self, table_name):
        with self.conn.cursor() as cur:
            cur.execute(f"DELETE FROM {table_name}")  # Clear the table after each test
            self.conn.commit()
            print(f"Table '{table_name}' cleared")