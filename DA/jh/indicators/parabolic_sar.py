import pandas as pd
from ta.trend import PSARIndicator

def add_parabolic_sar(df: pd.DataFrame) -> pd.Series:
    indicator = PSARIndicator(
        high = df['high'],
        low = df['low'],
        close = df['close'],
        step = 0.02,
        max_step = 0.2
    )

    return indicator.psar()

def add_parabolic_sar_for_all(df: pd.DataFrame) -> pd.Series:
    def compute_psar(group):
        sorted_group = group.sort_values('date').reset_index(drop=True)

        result = add_parabolic_sar(sorted_group).copy()
        result.iloc[:3] = pd.NA

        return result.reset_index(drop=True)
    
    result_list = []

    for _, group in df.groupby('symbol'):
        result_list.append(compute_psar(group))

    psar_series = pd.concat(result_list, ignore_index=True)

    return psar_series.reset_index(drop=True)