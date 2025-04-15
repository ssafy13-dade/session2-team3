import pandas as pd

def add_adx(df: pd.DataFrame, window: int=14) -> pd.DataFrame:
    high = df['high']
    low = df['low']
    close = df['close']

    prev_high = high.shift(1)
    prev_low = low.shift(1)
    prev_close = close.shift(1)

    plus_dm = (high - prev_high).where((high - prev_high) > (prev_low - low), 0).where((high - prev_high) > 0, 0)
    minus_dm = (prev_low - low).where((prev_low - low) > (high - prev_high), 0).where((prev_low - low) > 0, 0)

    tr = pd.concat([
        (high - low),
        (high - prev_close).abs(),
        (low - prev_close).abs()
    ], axis=1).max(axis=1)

    tr_smooth = tr.rolling(window=window, min_periods=window).sum()
    plus_di = 100 * plus_dm.rolling(window=window, min_periods=window).sum() / tr_smooth
    minus_di = 100 * minus_dm.rolling(window=window, min_periods=window).sum() / tr_smooth

    dx = (abs(plus_di - minus_di) / (plus_di + minus_di)) * 100
    adx = dx.rolling(window=window, min_periods=window).mean()

    result = pd.DataFrame({
        'plus_di': plus_di,
        'minus_di': minus_di,
        'adx': adx
    }, index=df.index)

    return result

def add_adx_for_all(df: pd.DataFrame, window: int=14) -> pd.DataFrame:
    def compute_adx(group):
        sorted_group = group.sort_values('date')
        adx_df = add_adx(sorted_group, window)

        result = pd.concat([
            sorted_group[['symbol', 'date']].reset_index(drop=True),
            adx_df.reset_index(drop=True)
        ], axis=1)
    
        return result
    
    result = df.groupby('symbol').apply(compute_adx)

    return result.reset_index(drop=True)