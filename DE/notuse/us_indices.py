# ! pip install finance-datareader
import FinanceDataReader as fdr
import pandas as pd

# 1. 지수 리스트와 이름 정의
symbols = {
    'DJI': 'DJI',
    'IXIC': 'IXIC',
    'S&P500': 'S&P500'
}

# 2. 기간 정의
start_date = '2001-06-11'
end_date = '2025-04-07'

# 3. 수집 및 전처리 함수 정의
def load_and_prepare(symbol, index_name):
    df = fdr.DataReader(symbol)
    df = df.loc[start_date:end_date]        # 날짜 슬라이싱
    df.index.name = 'Date'  # 인덱스 이름 지정
    df = df.reset_index()                   # 인덱스 → Date 컬럼
    df['IndexType'] = index_name           # 지수 타입 컬럼 추가

    return df

# 4. 모든 지수 데이터 수집 및 병합
dfs = [load_and_prepare(symbol, name) for name, symbol in symbols.items()]
merged_indices = pd.concat(dfs, axis=0, ignore_index=True)

# 결과 확인
print(merged_indices.head())
print(merged_indices['IndexType'].value_counts())
print(merged_indices.shape)

# 5. merged_indices에 사용된 날짜만 추출
valid_dates = merged_indices['Date'].unique()

# 6. VIX 데이터 따로 불러오고 필터링
vix = fdr.DataReader('VIX')
vix.index.name = 'Date'
vix = vix.loc[start_date:end_date]
vix = vix.reset_index()
vix = vix[vix['Date'].isin(valid_dates)]  # 날짜 필터링
vix['IndexType'] = 'VIX'

# 7. VIX까지 병합
merged_indices = pd.concat([merged_indices, vix], axis=0, ignore_index=True)

# 8. 확인
print(merged_indices['IndexType'].value_counts())
print(merged_indices['Date'].nunique())

# 9.csv 파일 저장
merged_indices.to_csv('./data/us_indices_merged.csv', index=False, encoding='utf-8-sig')