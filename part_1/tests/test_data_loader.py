from part_1.config.config import CONFIG
from part_1.src.data_loader import DataLoader
from pathlib import Path

from part_1.src.s3_client import S3Client
from part_1.src.table_creation import TableCreator
from part_1.src.utils.file_utils import get_csv_file_paths

def test_data_loading_and_export(db_connection, s3_client):
    db_connection = db_connection
    s3_client = s3_client
    loader = DataLoader(db_connection)
    table = TableCreator(db_connection)
    s3 = S3Client(s3_client, CONFIG["aws"]["bucket_name"])
    table_list = []
    directory_path = Path(__file__).resolve().parent / 'tests_data'
    for csv_path in get_csv_file_paths(directory_path):
        table_name = csv_path.stem
        table.create_table_from_csv(csv_path)
        loader.load_csv_to_postgres(csv_path)

        table_list.append(table)
        assert loader.get_table_row_count(table_name) > 0, "No records were loaded"

        s3_object_key = s3.upload_parquet(table_name, db_connection)
        assert s3.validate_upload(s3_object_key), f"S3 object '{s3_object_key}' was not uploaded"
