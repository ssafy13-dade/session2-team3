import psycopg2
import os
from dotenv import load_dotenv


load_dotenv()

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

# 기본 DB(postgres)에 접속해서 새 DB 생성
try:
    # 1. 기본 DB에 접속
    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        dbname="postgres",  # 반드시 기존 DB로 먼저 접속
        user=db_user,
        password=db_password
    )
    conn.autocommit = True  # CREATE DATABASE 실행 위해 필요
    cur = conn.cursor()

    # 2. stockdb 생성 시도
    cur.execute("CREATE DATABASE stockdb;")
    print("✅ stockdb 데이터베이스 생성 완료!")

    # 3. 마무리
    cur.close()
    conn.close()

except Exception as e:
    print("❌ 오류 발생:", e)
