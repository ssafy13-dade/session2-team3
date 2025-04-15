import pandas as pd

def add_rsi(df: pd.DataFrame, window: int=14) -> pd.Series:
    delta = df['adj_close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=window, min_periods=window).mean()
    avg_loss = loss.rolling(window=window, min_periods=window).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi

def add_rsi_for_all(df: pd.DataFrame, window: int=14) -> pd.Series:
    def compute_rsi(group):
        sorted_group = group.sort_values('date')

        return add_rsi(sorted_group, window)
    
    rsi_series = df.groupby('symbol', group_keys=False).apply(compute_rsi)
    
    return rsi_series.reset_index(drop=True)