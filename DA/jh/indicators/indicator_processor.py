from indicators.moving_average import add_ma_for_all
from indicators.rsi import add_rsi_for_all
from indicators.macd import add_macd_for_all
from indicators.bollinger import add_bollinger_for_all
from indicators.stochastic import add_stochastic_for_all
from indicators.atr import add_atr_for_all
from indicators.adx import add_adx_for_all
from indicators.parabolic_sar import add_parabolic_sar_for_all

def calculate_all_indicators(df):
    result_df = df[['symbol', 'date', 'close', 'adj_close']].copy()

    result_df['ma20'] = add_ma_for_all(df, window=20)
    result_df['ma60'] = add_ma_for_all(df, window=60)
    result_df['rsi14'] = add_rsi_for_all(df, window=14)

    macd_result = add_macd_for_all(df)
    result_df = result_df.merge(macd_result, on=['symbol', 'date'], how='left')

    bb_result = add_bollinger_for_all(df)
    result_df = result_df.merge(bb_result, on=['symbol', 'date'], how='left')

    stoch_result = add_stochastic_for_all(df)
    result_df = result_df.merge(stoch_result, on=['symbol', 'date'], how='left')

    result_df['atr'] = add_atr_for_all(df)

    adx_result = add_adx_for_all(df)
    result_df = result_df.merge(adx_result, on=['symbol', 'date'], how='left')

    result_df['psar'] = add_parabolic_sar_for_all(df)

    return result_df