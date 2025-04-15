from strategy.macd_cross import generate_macd_cross_signals
from strategy.macd import generate_macd_signals

def calculate_all_signals(df):
    result = df[['symbol', 'date']].copy()

    result['macd_cross'] = df.groupby('symbol', group_keys=False).apply(generate_macd_cross_signals).reset_index(drop=True)
    result['macd'] = df.groupby('symbol', group_keys=False).apply(generate_macd_signals).reset_index(drop= True)

    return result