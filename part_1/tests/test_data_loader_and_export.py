import allure
import pytest

from part_1.config.config import CONFIG
from part_1.src.data_loader import DataLoader
from pathlib import Path
from part_1.src.s3_client import S3Client
from part_1.src.table_creation import TableCreator
from part_1.src.utils.file_utils import get_csv_file_paths

@pytest.mark.run(order=1)
@allure.title("Test Data Loading, Transformation, and Export to S3")
def test_data_loading_and_export(db_connection, s3_client):
    db_connection = db_connection
    loader = DataLoader(db_connection)
    table = TableCreator(db_connection)
    s3 = S3Client(s3_client, CONFIG["aws"]["bucket_name"])
    table_list = []

    with allure.step("Iterating through the CSV files in the 'tests_data' directory"):
        directory_path = Path(__file__).resolve().parent / 'tests_data'
        for csv_path in get_csv_file_paths(directory_path):
            table_name = csv_path.stem
            with allure.step(f"Creating table and loading data from {csv_path}"):
                table.create_table_from_csv(csv_path)
                table.clear_table(csv_path) # Clear table in case it's not empty
                loader.load_csv_to_postgres(csv_path)

            table_list.append(table)

            with allure.step(f"Verifying row count for table '{table_name}'"):
                assert loader.get_table_row_count(table_name) > 0, "No records were loaded"

            with allure.step(f"Uploading '{table_name}' to S3 as Parquet"):
                s3_object_key = s3.upload_parquet(table_name, db_connection)

            with allure.step(f"Verifying S3 upload for object '{s3_object_key}'"):
                assert s3.validate_upload(s3_object_key), f"S3 object '{s3_object_key}' was not uploaded"
