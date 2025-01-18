import pandas as pd
import psycopg2
from part_1.config.config import CONFIG

def get_db_connection():
    return psycopg2.connect(
        host=CONFIG['database']['host'],
        database=CONFIG['database']['dbname'],
        user=CONFIG['database']['user'],
        password=CONFIG['database']['password']
    )

def fetch_table_schema(connection, table_name):
    query = f"""
    SELECT column_name, data_type
    FROM information_schema.columns
    WHERE table_name = '{table_name}';
    """
    with connection.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

def fetch_table_data(connection, table_name):
    query = f"SELECT * FROM {table_name}"
    return pd.read_sql_query(query, connection)


def normalize_schema(db_schema, parquet_schema):
    """
    Normalize the data types in both schemas for comparison.
    PostgreSQL types are mapped to Parquet types for compatibility.
    """
    normalized_db_schema = {}

    # Map PostgreSQL types to corresponding Parquet types (int64 for integer and string for character varying)
    type_mapping = {
        'integer': 'int64',
        'character varying': 'object'
    }

    for db_col, db_type in db_schema:
        normalized_db_schema[db_col] = type_mapping.get(db_type, db_type)

    # Now compare the normalized schemas
    return normalized_db_schema

def compare_schemas(db_schema, parquet_schema):
    normalized_db_schema = normalize_schema(db_schema, parquet_schema)

    for db_col, db_type in normalized_db_schema.items():
        if db_col not in parquet_schema or parquet_schema[db_col] != db_type:
            return False
    return True

def fetch_column_names(db_connection, table_name):
    """
    Fetch column names for the given table.
    """
    query = f"""
        SELECT column_name FROM information_schema.columns
        WHERE table_name = '{table_name}';
    """
    with db_connection.cursor() as cur:
        cur.execute(query)
        columns = [row[0] for row in cur.fetchall()]
    return columns

def insert_data(db_connection, table_name, column_names, values):
    """
    Insert data into the table.
    """
    columns = ", ".join(column_names)
    placeholders = ", ".join(["%s"] * len(values))
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    with db_connection.cursor() as cur:
        cur.execute(query, values)
    db_connection.commit()

def update_data(db_connection, table_name, column_name, new_value, condition):
    """
    Update data in the table.
    """
    query = f"UPDATE {table_name} SET {column_name} = %s WHERE {condition}"
    with db_connection.cursor() as cur:
        cur.execute(query, (new_value,))
    db_connection.commit()

def delete_data(db_connection, table_name, condition):
    """
    Delete data from the table.
    """
    query = f"DELETE FROM {table_name} WHERE {condition}"
    with db_connection.cursor() as cur:
        cur.execute(query)
    db_connection.commit()

def validate_data(db_data, parquet_data):
    """
    Validates that two dataframes (db_data and parquet_data) are equal.
    Raises an AssertionError if they are not.
    """
    try:
        pd.testing.assert_frame_equal(db_data, parquet_data, check_dtype=False)
        print("Validation successful: Dataframes are equal.")
    except AssertionError as e:
        raise AssertionError(f"Data validation failed: {e}")

def generate_sample_values(column_names_and_types):
    sample_data = []
    for column_name, column_type in column_names_and_types:
        if "integer" in column_type:
            sample_data.append(1)  # Integer sample value
        elif "character" in column_type or "text" in column_type:
            sample_data.append("sample_text")  # String sample value
        else:
            sample_data.append(None)  # Handle other types as needed
    return sample_data