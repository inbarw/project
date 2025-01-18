import os
from dotenv import load_dotenv

load_dotenv()

CONFIG = {
    'database': {
        'host': os.getenv('DB_HOST'),
        'dbname': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD')
    },
    'aws': {
        'access_key': os.getenv('AWS_ACCESS_KEY_ID'),
        'secret_key': os.getenv('AWS_SECRET_ACCESS_KEY'),
        'bucket_name': os.getenv('S3_BUCKET_NAME')
    }
}