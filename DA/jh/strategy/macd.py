import pandas as pd

def generate_macd_signals(df: pd.DataFrame) -> pd.Series:
    macd = df['macd']
    signal = df['signal']

    prev_cross = (macd.shift(1) > signal.shift(1))
    curr_cross = (macd > signal)

    buy_signal = (~prev_cross) & (curr_cross)
    sell_signal = (prev_cross) & (~curr_cross)

    signal_series = pd.Series(0, index=df.index)
    signal_series[buy_signal] = 1
    signal_series[sell_signal] = -1

    return signal_series

