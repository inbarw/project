from pathlib import Path
import allure
import pandas as pd
import pytest
from part_1.config.config import CONFIG
from part_1.src.utils.aws_utils import download_parquet
from part_1.src.utils.db_utils import fetch_table_data
from part_1.src.utils.file_utils import get_csv_file_paths

@pytest.mark.data_validation
@pytest.mark.run(order=2)
@allure.title("Test Data Consistency Between DB and S3")
def test_data_consistency(db_connection, s3_client):
    bucket_name = CONFIG["aws"]["bucket_name"]

    directory_path = Path(__file__).resolve().parent / 'tests_data'
    for csv_path in get_csv_file_paths(directory_path):
        table_name = csv_path.stem
        parquet_key = f"output/{table_name}.parquet"

        with allure.step(f"Fetching data from DB for table '{table_name}'"):
            db_data = fetch_table_data(db_connection, table_name)

        with allure.step(f"Downloading Parquet data from S3 for table '{table_name}'"):
            parquet_data = download_parquet(s3_client, bucket_name, parquet_key)

        with allure.step(f"Verifying consistency between DB and Parquet data for table '{table_name}'"):
            pd.testing.assert_frame_equal(db_data, parquet_data, check_dtype=False)