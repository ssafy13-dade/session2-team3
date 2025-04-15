import pandas as pd
from sqlalchemy import text

def load_table(connection, table_name: str) -> pd.DataFrame:
    try:
        query = f'SELECT * FROM {table_name}'
        result = connection.execute(text(query))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
        df = str_to_datetime(df)
        return df
    except Exception as e:
        print(f'Error while loadting table {table_name}: {e}')
        return None

def load_csv(file_path, encoding='utf-8') -> pd.DataFrame:
    df = pd.read_csv(file_path, encoding=encoding)
    df = str_to_datetime(df)
    return df

def str_to_datetime(df):
    for col in df.select_dtypes(include=['object']).columns:
            try:
                df[col] = pd.to_datetime(df[col], format='%Y-%m-%d')
            except (ValueError, TypeError):
                continue
    return df
