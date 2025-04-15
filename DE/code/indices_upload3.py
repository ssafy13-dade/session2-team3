# !pip install finance-datareader sqlalchemy psycopg2-binary python-dotenv
import pandas as pd
import FinanceDataReader as fdr
from sqlalchemy import create_engine
from dotenv import load_dotenv
from datetime import datetime
import os

# -------------------- 환경 설정 --------------------
load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DB_URL)

# 오늘 날짜
today = datetime.today().strftime('%Y-%m-%d')

# -------------------- 한국 경제 지수 처리 --------------------
ks11 = fdr.DataReader('KS11').reset_index()
ks200 = fdr.DataReader('KS200').reset_index()
kq11 = fdr.DataReader('KQ11').reset_index()

ks11['IndexType'] = 'KOSPI'
ks200['IndexType'] = 'KOSPI200'
kq11['IndexType'] = 'KOSDAQ'

kr_merged = pd.concat([ks11, ks200, kq11], axis=0, ignore_index=True)

kr_merged = kr_merged.rename(columns={
    'Date': 'date',
    'Open': 'open',
    'High': 'high',
    'Low': 'low',
    'Close': 'close',
    'Volume': 'volume',
    'Change': 'change',
    'UpDown': 'updown',
    'Comp': 'comp',
    'Amount': 'amount',
    'MarCap': 'marcap',
    'IndexType': 'market'
})

kr_merged = kr_merged[['date', 'open', 'high', 'low', 'close', 'volume',
                       'change', 'updown', 'comp', 'amount', 'marcap', 'market']]

kr_merged.to_csv('./data/korea_indices_merged.csv', index=False, encoding='utf-8-sig')
kr_merged.to_sql('kr_indices', engine, if_exists='append', index=False)
print("✅ 한국 지수 저장 완료")

# -------------------- 미국 경제 지수 처리 --------------------
# 지수 및 기간 설정
symbols = {
    'DJI': 'DJI',
    'IXIC': 'IXIC',
    'S&P500': 'S&P500'
}
start_date = '2001-06-11'
end_date = datetime.today().strftime('%Y-%m-%d')

def load_and_prepare(symbol, index_name):
    df = fdr.DataReader(symbol).loc[start_date:end_date]
    df.index.name = 'date'  # ✅ 인덱스 이름 지정 (컬럼으로 바꾸기 전 준비)
    df = df.reset_index()   # ✅ 인덱스를 컬럼으로 이동
    df['market'] = index_name
    return df

# 주요 3대 지수 수집
us_dfs = [load_and_prepare(symbol, name) for name, symbol in symbols.items()]
us_merged = pd.concat(us_dfs, axis=0, ignore_index=True)

# 기준 날짜 추출
valid_dates = us_merged['date'].unique()

# ✅ VIX 수집
vix = fdr.DataReader('VIX').loc[start_date:end_date]
vix.index.name = 'date'  # ✅ 인덱스에 이름 부여
vix = vix.reset_index()  # ✅ 인덱스를 date 컬럼으로 바꿈
vix = vix[vix['date'].isin(valid_dates)]  # ✅ 날짜 기준 필터링
vix['market'] = 'VIX'

# 병합
us_merged = pd.concat([us_merged, vix], axis=0, ignore_index=True)

# 컬럼 정리
us_merged = us_merged.rename(columns={
    'Open': 'open', 'High': 'high', 'Low': 'low',
    'Close': 'close', 'Volume': 'volume', 'Adj Close': 'adj_close'
})

us_merged = us_merged[['date', 'open', 'high', 'low', 'close', 'volume', 'adj_close', 'market']]

# 저장
us_merged.to_csv('./data/us_indices_merged.csv', index=False, encoding='utf-8-sig')
us_merged.to_sql('us_indices', engine, if_exists='append', index=False)

print("✅ 미국 지수 저장 완료!")
