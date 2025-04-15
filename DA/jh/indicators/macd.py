import pandas as pd

def add_macd(df: pd.DataFrame, fast: int=12, slow: int=26, signal: int=9) -> pd.DataFrame:
    fast_ema = df['adj_close'].ewm(span=fast, adjust=False).mean()
    slow_ema = df['adj_close'].ewm(span=slow, adjust=False).mean()
    macd = fast_ema - slow_ema
    signal_line = macd.ewm(span=signal, adjust=False).mean()

    macd[:slow - 1] = pd.NA
    signal_line[:slow - 1] = pd.NA

    result = pd.DataFrame({
        'macd': macd,
        'signal': signal_line
    }, index=df.index)
    
    return result

def add_macd_for_all(df: pd.DataFrame, fast: int=12, slow: int=26, signal: int=9) -> pd.DataFrame:
    def compute_macd(group):
        sorted_group = group.sort_values('date')
        macd_df = add_macd(sorted_group, fast, slow, signal)
        
        result = pd.concat([
            sorted_group[['symbol', 'date']].reset_index(drop=True),
            macd_df.reset_index(drop=True)
        ], axis=1)
        
        return result

    result = df.groupby('symbol').apply(compute_macd)
    
    return result.reset_index(drop=True)