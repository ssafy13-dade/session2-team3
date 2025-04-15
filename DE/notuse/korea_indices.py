# ! pip install finance-datareader
import FinanceDataReader as fdr
import pandas as pd


#.env 파일 불러오기
load_dotenv()


# 1. 지수별 데이터 수집
ks11 = fdr.DataReader('KS11')
ks200 = fdr.DataReader('KS200')
kq11 = fdr.DataReader('KQ11')

# 2. 인덱스를 컬럼으로 변환
ks11 = ks11.reset_index()
ks200 = ks200.reset_index()
kq11 = kq11.reset_index()

# 3. IndexType 컬럼 추가 (지수 구분용)
ks11['IndexType'] = 'KS11'
ks200['IndexType'] = 'KS200'
kq11['IndexType'] = 'KQ11'

# 4. 세 개를 세로 방향으로 concat
merged = pd.concat([ks11, ks200, kq11], axis=0, ignore_index=True)

# 5. 결과 확인
print(merged['IndexType'].value_counts())
print(merged.head())


# 6. csv파일로 저장
merged.to_csv('./data/korea_indices_merged.csv', index=False, encoding='utf-8-sig')