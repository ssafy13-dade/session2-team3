from dotenv import load_dotenv
import os
import pandas as pd
import FinanceDataReader as fdr
from sqlalchemy import create_engine
from tqdm import tqdm
from datetime import datetime

# -------------------- DB 설정 --------------------
load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DB_URL)

# -------------------- US 함수 --------------------
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
        'Date': 'date', 'Open': 'open', 'High': 'high', 'Low': 'low',
        'Close': 'close', 'Volume': 'volume', 'Adj Close': 'adj_close'
    })[['symbol', 'date', 'open', 'high', 'low', 'close', 'volume', 'adj_close']]
    return df.dropna(subset=['symbol', 'date'])

def load_us_prices(df):
    with engine.connect() as conn:
        existing = pd.read_sql("SELECT symbol, date FROM us_stocks_prices", conn)

    merged = df.merge(existing, on=['symbol', 'date'], how='left', indicator=True)
    new_data = merged[merged['_merge'] == 'left_only'].drop(columns=['_merge'])

    if not new_data.empty:
        new_data.to_sql('us_stocks_prices', engine, if_exists='append', index=False, chunksize=1000)
        print(f"🆕 US 주가 {len(new_data)}건 저장 완료")
    else:
        print("⚠️ 저장할 US 주가 데이터가 없습니다 (모두 중복)")

    df.to_csv('us_stocks_prices.csv', encoding='utf-8', index=False)

# -------------------- KOR 함수 --------------------
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
    df.to_sql('kr_stocks_info', engine, if_exists='append', index=False, chunksize=1000)
    df.to_csv('kr_stocks_info.csv', encoding='utf-8', index=False)

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
    with engine.connect() as conn:
        existing = pd.read_sql("SELECT code, date FROM kr_stocks_prices", conn)

    merged = df.merge(existing, on=['code', 'date'], how='left', indicator=True)
    new_data = merged[merged['_merge'] == 'left_only'].drop(columns=['_merge'])

    if not new_data.empty:
        new_data.to_sql('kr_stocks_prices', engine, if_exists='append', index=False, chunksize=1000)
        print(f"🆕 KOR 주가 {len(new_data)}건 저장 완료")
    else:
        print("⚠️ 저장할 KOR 주가 데이터가 없습니다 (모두 중복)")

    df.to_csv('kr_stocks_prices.csv', encoding='utf-8', index=False)

# -------------------- 실행 제어 --------------------
def run_etl_partial():
    print("🔍 [3/8] US 주가 데이터 수집 중...")
    us_info = pd.read_csv('us_stocks_info.csv')
    us_prices = transform_us_prices(extract_us_prices(us_info['symbol'].tolist()))
    print(f"✅ US 주가 {len(us_prices)}건 수집 완료")

    print("💾 [4/8] US 주가 정보 저장 중...")
    load_us_prices(us_prices)
    print("📁 us_stocks_prices.csv 저장 완료")

    print("🔍 [5/8] KOR 종목 정보 추출 중...")
    kr_info = transform_kr_info(extract_kr_info())
    print(f"✅ KOR 종목 {len(kr_info)}개 추출 완료")

    print("💾 [6/8] KOR 종목 정보 저장 중...")
    load_kr_info(kr_info)
    print("📁 kr_stocks_info.csv 저장 완료")

    print("🔍 [7/8] KOR 주가 데이터 수집 중...")
    kr_prices = transform_kr_prices(extract_kr_prices(kr_info['code'].tolist()))
    print(f"✅ KOR 주가 {len(kr_prices)}건 수집 완료")

    print("💾 [8/8] KOR 주가 정보 저장 중...")
    load_kr_prices(kr_prices)
    print("📁 kr_stocks_prices.csv 저장 완료")

    print("🎉 모든 ETL 작업이 완료되었습니다!")

# -------------------- 메인 --------------------
if __name__ == '__main__':
    run_etl_partial()
