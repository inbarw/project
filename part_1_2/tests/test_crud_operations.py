from pathlib import Path
import allure
import pytest
from part_1_2.config.config import CONFIG
from part_1_2.src.s3_client import S3Client
from part_1_2.src.utils.aws_utils import download_parquet
from part_1_2.src.utils.db_utils import fetch_table_data, insert_data, validate_data, update_data, \
    delete_data, fetch_table_schema, generate_sample_values
from part_1_2.src.utils.file_utils import get_csv_file_paths

@pytest.mark.run(order=4)
@allure.title("Test CRUD Operations: Insert, Read, Update, Delete")
def test_crud_operations(db_connection, s3_client):
    bucket_name = CONFIG["aws"]["bucket_name"]
    s3 = S3Client(s3_client, bucket_name)

    directory_path = Path(__file__).resolve().parent / 'tests_data'
    for csv_path in get_csv_file_paths(directory_path):
        table_name = csv_path.stem
        parquet_key = f"output/{table_name}.parquet"

        # Fetch column names and schema
        db_schema = fetch_table_schema(db_connection, table_name)  # Example: [('col1', 'integer'), ('col2', 'varchar')]
        column_names = [col[0] for col in db_schema]  # Extract column names

        # Create (Insert)
        sample_values = generate_sample_values(db_schema)
        insert_data(db_connection, table_name, column_names, sample_values)

        # Read
        db_data = fetch_table_data(db_connection, table_name)
        s3.upload_parquet(table_name, db_connection) # Regenerate and upload the Parquet file to S3
        parquet_data = download_parquet(s3_client, bucket_name, parquet_key)
        validate_data(db_data, parquet_data)

        # Update
        update_data(db_connection, table_name, 'patient_id', 123, "patient_id = 7168386")

        # Read and Validate Again
        db_data = fetch_table_data(db_connection, table_name)
        s3.upload_parquet(table_name, db_connection)  # Regenerate and upload the Parquet file to S3
        parquet_data = download_parquet(s3_client, bucket_name, parquet_key)
        validate_data(db_data, parquet_data)

        # Delete
        delete_data(db_connection, table_name, "patient_id = 123")

        # Final Validation
        db_data = fetch_table_data(db_connection, table_name)
        s3.upload_parquet(table_name, db_connection)  # Regenerate and upload the Parquet file to S3
        parquet_data = download_parquet(s3_client, bucket_name, parquet_key)
        validate_data(db_data, parquet_data)