from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

def create_connection():
    try:
        db_url = f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}'

        engine = create_engine(db_url)
        connection = engine.connect()
        print('PostgreSQL 연결 성공')
        return connection
    except Exception as e:
        print(f'Error while connecting to PostgreSQL: {e}')
        return None