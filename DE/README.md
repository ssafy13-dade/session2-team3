# 데이터 적재

## 코드별 설명
1. create_stockDB.py
    - RDS에 생성한 dadeDB 인스턴스에 stockdb라는 데이터베이스 생성 후, 총 6개의 테이블 뼈대 구조 미리 생성
2. createTABLE.PY
    - stockdb 데이터 베이스에 총 6개의 테이블 뼈대 구조 미리 생성
    ## 📄 PostgreSQL 테이블 목록 (stockdb)

    | Schema | Name              | Type  | Owner |
    |--------|-------------------|-------|--------|
    | public | kr_indices        | table | jeunk |
    | public | kr_stocks_info    | table | jeunk |
    | public | kr_stocks_prices  | table | jeunk |
    | public | us_indices        | table | jeunk |
    | public | us_stocks_info    | table | jeunk |
    | public | us_stocks_prices  | table | jeunk |
3. indices_upload.py
    - 경제 지수 테이블 2개 데이터 불러와서 csv파일 생성 및 postgreSQL에 적재
    - 미국 경제 지수 중, VIX(시장 불안도)가 다른 경제 지수에 비해 존재하는 날짜가 많아서 다른 경제 지수들과 같은 날짜들만 가져와서 비교할 수 있도록 가공
4. stocks_upload.py\
    stocks_continue.py
    - 한국 기업, 미국 기업에 관한 4개의 테이블 가공 및 적재
    - 중간에 us_stocks_prices 레코드가 244만개 이상이라 한번에 적재하려니 MemoryError 발생
    - 중간부터 주석 처리 후, stock_continue.py 파일로 이후 테이블 적재

5. batch_insert.py
    - 추후에 필요하다면 배치 처리로 매일 생성되는 데이터 적재 코드 제작 예정.


## ERD
### 한국기업 주요 지수와 미국 기업 주요 지수 테이블 ERD 표
![한국, 미국 기업 주요 정보 ERD](.\stock_db_ERD.png)



![한국, 미국 경제 지수 테이블 표](.\indicesERD.png)