import pandas as pd

class S3Client:
    def __init__(self, s3_client, bucket_name):
        self.s3_client = s3_client
        self.bucket_name = bucket_name

    def upload_parquet(self, table_name, db_connection):
        """
        Converts table data to Parquet format and uploads it to S3.
        """
        query = f"SELECT * FROM {table_name}"
        dataframe = pd.read_sql_query(query, db_connection)
        parquet_file_path = f"{table_name}.parquet"
        dataframe.to_parquet(parquet_file_path)
        self.s3_client.upload_file(parquet_file_path, self.bucket_name, f"output/{parquet_file_path}")

        # Returning the key that will be used in the validation
        return f"output/{parquet_file_path}"

    def validate_upload(self, s3_object_key):
        """
        Validates that the Parquet file was uploaded to S3.
        """
        response = self.s3_client.list_objects_v2(Bucket=self.bucket_name, Prefix=s3_object_key)
        s3_objects = response.get('Contents', [])
        is_uploaded = any(obj['Key'] == s3_object_key for obj in s3_objects)
        return is_uploaded


