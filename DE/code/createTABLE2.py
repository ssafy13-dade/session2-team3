import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

# 연결 정보 (.env에서 가져오기)
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
name = os.getenv("DB_NAME")

conn = psycopg2.connect(
    dbname=name,  # PostgreSQL 새로 생성한 stockdb
    user=user,
    password=password,
    host=host,
    port=port,
)

cur = conn.cursor()

# US 종목 테이블
create_us_stocks_info_table = '''
CREATE TABLE IF NOT EXISTS us_stocks_info (
    symbol      VARCHAR(20) PRIMARY KEY,
    name        TEXT        NOT NULL,
    sector      TEXT,
    industry    TEXT,
    market      VARCHAR(10) NOT NULL
);
'''

# US 주가 테이블
create_us_stocks_prices_table = '''
CREATE TABLE IF NOT EXISTS us_stocks_prices (
    symbol      VARCHAR(20) NOT NULL,
    date        DATE        NOT NULL,
    open        DOUBLE PRECISION,
    high        DOUBLE PRECISION,
    low         DOUBLE PRECISION,
    close       DOUBLE PRECISION,
    volume      DOUBLE PRECISION,
    adj_close   DOUBLE PRECISION,
    PRIMARY KEY (symbol, date),
    FOREIGN KEY (symbol) REFERENCES us_stocks_info(symbol)
);
'''

# KOR 종목 테이블
create_kr_stocks_info_table = '''
CREATE TABLE IF NOT EXISTS kr_stocks_info (
    code          VARCHAR(20)     PRIMARY KEY,
    isu_cd        VARCHAR(20),
    name          TEXT            NOT NULL,
    dept          VARCHAR(20),
    close         INTEGER,
    change_code   SMALLINT,
    changes       INTEGER,
    change_ratio  NUMERIC(6,2),
    open          INTEGER,
    high          INTEGER,
    low           INTEGER,
    volume        BIGINT,
    amount        BIGINT,
    marcap        NUMERIC(20,0),
    stocks        BIGINT,
    market_id     VARCHAR(10)     NOT NULL,
    market        VARCHAR(10)     NOT NULL
);
'''

# KOR 주가 테이블
create_kr_stocks_prices_table = '''
CREATE TABLE IF NOT EXISTS kr_stocks_prices (
    code       VARCHAR(20),
    date       DATE         NOT NULL,
    open       DOUBLE PRECISION,
    high       DOUBLE PRECISION,
    low        DOUBLE PRECISION,
    close      DOUBLE PRECISION,
    volume     DOUBLE PRECISION,
    change     DOUBLE PRECISION,
    PRIMARY KEY (code, date),
    FOREIGN KEY (code) REFERENCES kr_stocks_info(code)
);
'''

# 한국 경제 지수 테이블
create_kr_indices_table = '''
CREATE TABLE IF NOT EXISTS kr_indices (
    date        TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    open        DOUBLE PRECISION,
    high        DOUBLE PRECISION,
    low         DOUBLE PRECISION,
    close       DOUBLE PRECISION,
    volume      BIGINT,
    change      DOUBLE PRECISION,
    updown      BIGINT,
    comp        DOUBLE PRECISION,
    amount      BIGINT,
    marcap      BIGINT,
    market      TEXT NOT NULL
);
'''
# 미국 경제 지수 테이블
create_us_indices_table = '''
CREATE TABLE IF NOT EXISTS us_indices (
    date        TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    open        DOUBLE PRECISION,
    high        DOUBLE PRECISION,
    low         DOUBLE PRECISION,
    close       DOUBLE PRECISION,
    volume      DOUBLE PRECISION,
    adj_close   DOUBLE PRECISION,
    market      TEXT NOT NULL
);
'''
# 테이블 실행
cur.execute(create_us_stocks_info_table)
cur.execute(create_us_stocks_prices_table)
cur.execute(create_kr_stocks_info_table)
cur.execute(create_kr_stocks_prices_table)
cur.execute(create_kr_indices_table)
cur.execute(create_us_indices_table)

conn.commit()
cur.close()
conn.close()
print("✅ 6개 테이블 생성 완료!")