import pandas as pd

def add_bollinger(df: pd.DataFrame, window: int=20, std: float=2.0) -> pd.DataFrame:
    ma = df['adj_close'].rolling(window=window, min_periods=window).mean()
    std_dev = df['adj_close'].rolling(window=window, min_periods=window).std()

    upper_band = ma + (std * std_dev)
    lower_band = ma - (std * std_dev)

    result = pd.DataFrame({
        'bb_mid': ma,
        'bb_upper': upper_band,
        'bb_lower': lower_band
    }, index=df.index)

    return result

def add_bollinger_for_all(df: pd.DataFrame, window: int=20, std: float=2.0) -> pd.DataFrame:
    def compute_bollinger(group):
        sorted_group = group.sort_values('date')
        bb_df = add_bollinger(sorted_group, window, std)
        
        result = pd.concat([
            sorted_group[['symbol', 'date']].reset_index(drop=True),
            bb_df.reset_index(drop=True)
        ], axis=1)

        return result
    
    result = df.groupby('symbol').apply(compute_bollinger)
    
    return result.reset_index(drop=True)