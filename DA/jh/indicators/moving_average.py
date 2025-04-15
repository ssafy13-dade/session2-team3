import pandas as pd

def add_moving_average(df: pd.DataFrame, window: int) -> pd.Series:
    result = df['adj_close'].rolling(window=window, min_periods=window).mean()

    return result

def add_ma_for_all(df: pd.DataFrame, window: int) -> pd.Series:
    def compute_ma(group):
        sorted_group = group.sort_values('date')
    
        return add_moving_average(sorted_group, window)
    
    ma_series = df.groupby('symbol', group_keys=False).apply(compute_ma)
    
    return ma_series.reset_index(drop=True)