from dotenv import load_dotenv
import os
import psycopg2
import pandas as pd
import FinanceDataReader as fdr
from sqlalchemy import create_engine
from tqdm import tqdm
from datetime import datetime

# -------------------- DB 설정 및 테이블 생성 --------------------
load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

# # psycopg2 연결
# conn = psycopg2.connect(
#     dbname=DB_NAME,
#     user=DB_USER,
#     password=DB_PASSWORD,
#     host=DB_HOST,
#     port=DB_PORT
# )

# cur = conn.cursor()

# # US 종목 테이블
# create_us_stocks_info_table = '''
# CREATE TABLE IF NOT EXISTS us_stocks_info (
#     symbol      VARCHAR(20) PRIMARY KEY,
#     name        TEXT        NOT NULL,
#     sector      TEXT,
#     industry    TEXT,
#     market      VARCHAR(10) NOT NULL
# );
# '''

# # US 주가 테이블
# create_us_stocks_prices_table = '''
# CREATE TABLE IF NOT EXISTS us_stocks_prices (
#     symbol      VARCHAR(20) NOT NULL,
#     date        DATE        NOT NULL,
#     open        DOUBLE PRECISION,
#     high        DOUBLE PRECISION,
#     low         DOUBLE PRECISION,
#     close       DOUBLE PRECISION,
#     volume      DOUBLE PRECISION,
#     adj_close   DOUBLE PRECISION,
#     PRIMARY KEY (symbol, date),
#     FOREIGN KEY (symbol) REFERENCES us_stocks_info(symbol)
# );
# '''

# # KOR 종목 테이블
# create_kr_stocks_info_table = '''
# CREATE TABLE IF NOT EXISTS kr_stocks_info (
#     code          VARCHAR(20)     PRIMARY KEY,
#     isu_cd        VARCHAR(20),
#     name          TEXT            NOT NULL,
#     dept          VARCHAR(20),
#     close         INTEGER,
#     change_code   SMALLINT,
#     changes       INTEGER,
#     change_ratio  NUMERIC(6,2),
#     open          INTEGER,
#     high          INTEGER,
#     low           INTEGER,
#     volume        BIGINT,
#     amount        BIGINT,
#     marcap        NUMERIC(20,0),
#     stocks        BIGINT,
#     market_id     VARCHAR(10)     NOT NULL,
#     market        VARCHAR(10)     NOT NULL
# );
# '''

# # KOR 주가 테이블
# create_kr_stocks_prices = '''
# CREATE TABLE IF NOT EXISTS kr_stocks_prices (
#     code       VARCHAR(20),
#     date       DATE         NOT NULL,
#     open       DOUBLE PRECISION,
#     high       DOUBLE PRECISION,
#     low        DOUBLE PRECISION,
#     close      DOUBLE PRECISION,
#     volume     DOUBLE PRECISION,
#     change     DOUBLE PRECISION,
#     PRIMARY KEY (code, date),
#     FOREIGN KEY (code) REFERENCES kr_stocks_info(code)
# );
# '''

# # 테이블 생성
# cur.execute(create_us_stocks_info_table)
# cur.execute(create_us_stocks_prices_table)
# cur.execute(create_kr_stocks_info_table)
# cur.execute(create_kr_stocks_prices)

# conn.commit()
# cur.close()
# conn.close()

# -------------------- ETL 함수 정의 --------------------
DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# US 종목 정보
def extract_us_info():
    sp500 = fdr.StockListing('S&P500')
    nasdaq = fdr.StockListing('NASDAQ')
    nyse = fdr.StockListing('NYSE')
    sp500['Market'] = 'S&P500'
    nasdaq['Market'] = 'nasdaq'
    nyse['Market'] = 'nyse'
    return pd.concat([sp500, nasdaq, nyse], ignore_index=True)

def transform_us_info(df):
    df = df.rename(columns={
        'Symbol': 'symbol',
        'Name': 'name',
        'Sector': 'sector',
        'Industry': 'industry',
        'Market': 'market'
    })[['symbol', 'name', 'sector', 'industry', 'market']]
    return df.dropna(subset=['symbol', 'name']).drop_duplicates(subset='symbol')

def load_us_info(df):
    engine = create_engine(DB_URL)
    df.to_sql('us_stocks_info', engine, if_exists='append', index=False)
    df.to_csv('us_stocks_info.csv', encoding='utf-8', index=False)

# US 주가 정보
def extract_us_prices(symbols, end=None):
    if end is None:
        end = datetime.today().strftime('%Y-%m-%d')
    all_data = []
    for symbol in tqdm(symbols, desc="US 주가 수집"):
        try:
            df = fdr.DataReader(symbol, end=end).reset_index()
            df['symbol'] = symbol
            all_data.append(df)
        except Exception as e:
            print(f"{symbol} 실패: {e}")
    return pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame()

def transform_us_prices(df):
    df = df.rename(columns={
        'index': 'date', 'Open': 'open', 'High': 'high', 'Low': 'low',
        'Close': 'close', 'Volume': 'volume', 'Adj Close': 'adj_close'
    })[['symbol', 'date', 'open', 'high', 'low', 'close', 'volume', 'adj_close']]
    return df.dropna(subset=['symbol', 'date'])

def load_us_prices(df):
    engine = create_engine(DB_URL)
    df.to_sql('us_stocks_prices', engine, if_exists='append', index=False, chunksize=1000)
    df.to_csv('us_stocks_prices.csv', encoding='utf-8', index=False)

# KOR 종목 정보
def extract_kr_info():
    return fdr.StockListing('KOSPI')

def transform_kr_info(df):
    df = df.rename(columns={
        'Code': 'code', 'ISU_CD': 'isu_cd', 'Name': 'name', 'Dept': 'dept',
        'Close': 'close', 'ChangeCode': 'change_code', 'Changes': 'changes',
        'ChagesRatio': 'change_ratio', 'Open': 'open', 'High': 'high', 'Low': 'low',
        'Volume': 'volume', 'Amount': 'amount', 'Marcap': 'marcap', 'Stocks': 'stocks',
        'MarketId': 'market_id', 'Market': 'market'
    })[['code', 'isu_cd', 'name', 'dept', 'close', 'change_code', 'changes', 'change_ratio',
        'open', 'high', 'low', 'volume', 'amount', 'marcap', 'stocks', 'market_id', 'market']]
    return df.dropna(subset=['code', 'name']).drop_duplicates(subset='code')

def load_kr_info(df):
    engine = create_engine(DB_URL)
    df.to_sql('kr_stocks_info', engine, if_exists='append', index=False)
    df.to_csv('kr_stocks_info.csv', encoding='utf-8', index=False)

# KOR 주가 정보
def extract_kr_prices(codes, end=None):
    if end is None:
        end = datetime.today().strftime('%Y-%m-%d')
    all_data = []
    for code in tqdm(codes, desc="KR 주가 수집"):
        try:
            df = fdr.DataReader(code, end=end).reset_index()
            df['code'] = code
            all_data.append(df)
        except Exception as e:
            print(f"{code} 실패: {e}")
    return pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame()

def transform_kr_prices(df):
    df = df.rename(columns={
        'Date': 'date', 'Open': 'open', 'High': 'high', 'Low': 'low',
        'Close': 'close', 'Volume': 'volume', 'Change': 'change'
    })[['code', 'date', 'open', 'high', 'low', 'close', 'volume', 'change']]
    return df.dropna(subset=['code', 'date'])

def load_kr_prices(df):
    engine = create_engine(DB_URL)
    df.to_sql('kr_stocks_prices', engine, if_exists='append', index=False, chunksize=1000)
    df.to_csv('kr_stocks_prices.csv', encoding='utf-8', index=False)

# 전체 실행
def run_etl_all():
    print("🔍 [1/8] US 종목 정보 추출 중...")
    us_info = transform_us_info(extract_us_info())
    print(f"✅ US 종목 {len(us_info)}개 추출 완료")

    print("💾 [2/8] US 종목 정보 저장 중...")
    load_us_info(us_info)
    print("📁 us_stocks_info.csv 저장 완료")

    print("🔍 [3/8] US 주가 데이터 수집 중...")
    us_info = pd.read_csv('us_stocks_info.csv')
    us_prices = transform_us_prices(extract_us_prices(us_info['symbol'].tolist()))
    print(f"✅ US 주가 {len(us_prices)}건 수집 완료")

    # 여기까지 진행 후, 한번에 테이블에 삽입되어서 터졌습니다...
    # 이 이후 코드는 stocks_oncinue.py로 진행되었기에 주석처리 합니다.


    # print("💾 [4/8] US 주가 정보 저장 중...")
    # load_us_prices(us_prices)
    # print("📁 us_stocks_prices.csv 저장 완료")

    # print("🔍 [5/8] KOR 종목 정보 추출 중...")
    # kr_info = transform_kr_info(extract_kr_info())
    # print(f"✅ KOR 종목 {len(kr_info)}개 추출 완료")

    # print("💾 [6/8] KOR 종목 정보 저장 중...")
    # load_kr_info(kr_info)
    # print("📁 kr_stocks_info.csv 저장 완료")

    # print("🔍 [7/8] KOR 주가 데이터 수집 중...")
    # kr_prices = transform_kr_prices(extract_kr_prices(kr_info['code'].tolist()))
    # print(f"✅ KOR 주가 {len(kr_prices)}건 수집 완료")

    # print("💾 [8/8] KOR 주가 정보 저장 중...")
    # load_kr_prices(kr_prices)
    # print("📁 kr_stocks_prices.csv 저장 완료")

    # print("🎉 모든 ETL 작업이 완료되었습니다!")

if __name__ == '__main__':
    run_etl_all()
