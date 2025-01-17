import psycopg2
from part_1.config.config import CONFIG

def get_db_connection():
    return psycopg2.connect(
        host=CONFIG['database']['host'],
        database=CONFIG['database']['dbname'],
        user=CONFIG['database']['user'],
        password=CONFIG['database']['password']
    )