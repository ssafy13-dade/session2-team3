import pandas as pd

def add_atr(df: pd.DataFrame, window: int=14) -> pd.Series:
    high = df['high']
    low = df['low']
    close = df['close']

    prev_close = close.shift(1)

    tr = pd.concat([
        (high - low),
        (high - prev_close).abs(),
        (low - prev_close).abs()
    ], axis=1).max(axis=1)

    atr = tr.rolling(window=window, min_periods=window).mean()

    return atr

def add_atr_for_all(df: pd.DataFrame, window: int=14) -> pd.Series:
    def compute_atr(group):
        sorted_group = group.sort_values('date')
        
        return add_atr(sorted_group, window)
    
    atr_series = df.groupby('symbol', group_keys=False).apply(compute_atr)

    return atr_series