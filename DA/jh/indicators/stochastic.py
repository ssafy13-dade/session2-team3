import pandas as pd

def add_stochastic(df: pd.DataFrame, k_window: int=14, d_window: int=3) -> pd.DataFrame:
    low_min = df['low'].rolling(window=k_window, min_periods=k_window).min()
    high_max = df['high'].rolling(window=k_window, min_periods=k_window).max()

    percent_k = 100 * (df['close'] - low_min) / (high_max - low_min)
    percent_d = percent_k.rolling(window=d_window, min_periods=d_window).mean()

    result = pd.DataFrame({
        'stoch_k': percent_k,
        'stoch_d': percent_d
    }, index=df.index)

    return result

def add_stochastic_for_all(df: pd.DataFrame, k_window: int=14, d_window: int=3) -> pd.DataFrame:
    def compute_stochastic(group):
        sorted_group = group.sort_values('date')
        stoch_df = add_stochastic(sorted_group, k_window, d_window)

        result = pd.concat([
            sorted_group[['symbol', 'date']].reset_index(drop=True),
            stoch_df.reset_index(drop=True)
        ], axis=1)

        return result
    
    result = df.groupby('symbol').apply(compute_stochastic)

    return result.reset_index(drop=True)