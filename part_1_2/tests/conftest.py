import pytest
import boto3
from part_1_2.src.utils.db_utils import get_db_connection

@pytest.fixture(scope='function')
def db_connection():
    """Fixture for setting up and tearing down database connection."""
    connection = get_db_connection()
    yield connection  # This will provide the connection to the test function
    connection.close()  # Automatically closes the connection after the test
    print("Database connection closed.")

@pytest.fixture(scope='function')
def s3_client():
    """Fixture for setting up and tearing down the S3 client."""
    s3 = boto3.client('s3')  # Initialize the S3 client
    yield s3  # This will provide the S3 client to the test function

