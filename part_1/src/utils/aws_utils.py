import boto3
import pandas as pd

from part_1.config.config import CONFIG

def get_s3_client():
    return boto3.client(
        "s3",
        aws_access_key_id=CONFIG["aws"]["access_key"],
        aws_secret_access_key=CONFIG["aws"]["secret_key"],
        region_name="us-east-1"
    )

def download_parquet(s3_client, bucket_name, object_key):
    s3_client.download_file(bucket_name, object_key, "/tmp/temp.parquet")
    return pd.read_parquet("/tmp/temp.parquet")