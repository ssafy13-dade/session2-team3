# import psycopg2
# import pandas as pd
# from sqlalchemy import create_engine


# # PostgreSQL 연결
# conn = psycopg2.connect(
#     dbname='stockdb_mocv',
#     user='myuser',
#     password='vTsxYAIzQkWzDu7Mc4cdadE27LpIXZqh',
#     host='dpg-cvqc7pbe5dus73f6s2og-a.oregon-postgres.render.com',
#     port=5432
# )

# # 테이블 목록 조회 (public 스키마 기준)
# query = """
# SELECT table_name
# FROM information_schema.tables
# WHERE table_schema = 'public'
#   AND table_type = 'BASE TABLE';
# """

# tables_df = pd.read_sql(query, conn)
# conn.close()

# # 테이블 목록 출력
# print("✅ 현재 PostgreSQL에 저장된 테이블 목록:")
# print(tables_df)


# # PostgreSQL 접속 정보
# user = "myuser"
# password = "vTsxYAIzQkWzDu7Mc4cdadE27LpIXZqh"
# host = "dpg-cvqc7pbe5dus73f6s2og-a.oregon-postgres.render.com"         # 또는 RDS 주소 등
# port = "5432"              # 기본 포트
# database = "stockdb_mocv"

# # SQLAlchemy 엔진 생성
# engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}")

# # 쿼리 실행
# query = "SELECT * FROM kr_stocks_prices"
# query1 = "SELECT * FROM kr_indices"
# df = pd.read_sql(query, engine)
# df1 = pd.read_sql(query1, engine)

# print(df.head())
# print(df1.head())

# df.to_csv("ko_stock_prices.csv", index=False)
# df1.to_csv("ko_indexes.csv", index=False)

