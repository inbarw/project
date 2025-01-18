from pathlib import Path
import allure
import pytest

from part_1.config.config import CONFIG
from part_1.src.utils.aws_utils import download_parquet
from part_1.src.utils.db_utils import fetch_table_schema, compare_schemas
from part_1.src.utils.file_utils import get_csv_file_paths

@pytest.mark.run(order=3)
@allure.title("Test Schema Consistency Between DB and S3 Parquet Files")
def test_schema_consistency(db_connection, s3_client):
    bucket_name = CONFIG["aws"]["bucket_name"]

    directory_path = Path(__file__).resolve().parent / 'tests_data'
    for csv_path in get_csv_file_paths(directory_path):
        table_name = csv_path.stem
        parquet_key = f"output/{table_name}.parquet"

        with allure.step(f"Fetching schema from DB for table '{table_name}'"):
            db_schema = fetch_table_schema(db_connection, table_name)

        with allure.step(f"Downloading Parquet data from S3 for table '{table_name}'"):
            parquet_data = download_parquet(s3_client, bucket_name, parquet_key)

        parquet_schema = {col: str(dtype) for col, dtype in parquet_data.dtypes.items()}

        with allure.step(f"Comparing DB schema with Parquet schema for table '{table_name}'"):
            assert compare_schemas(db_schema, parquet_schema), "Schema mismatch between DB and Parquet"