import pandas as pd

def run_backtest(result_df: pd.DataFrame, signal_df: pd.DataFrame, signal_col: str) -> pd.DataFrame:
    result = []

    for symbol in signal_df['symbol'].unique():
        symbol_signals = signal_df[signal_df['symbol'] == symbol].sort_values('date').reset_index(drop=True)
        symbol_prices = result_df[result_df['symbol'] == symbol].sort_values('date').reset_index(drop=True)

        holding = False
        entry_price = None
        entry_date = None

        for _, row in symbol_signals.iterrows():
            signal = row[signal_col]
            date = row['date']

            price_row = symbol_prices[symbol_prices['date'] == date]
            if price_row.empty:
                continue

            price = price_row['close'].values[0]

            if signal == 1 and not holding:
                holding = True
                entry_price = price
                entry_date = date
            elif signal == -1 and holding:
                holding = False
                exit_price = price
                exit_date = date
                rtn = (exit_price / entry_price) - 1
            
                result.append({
                    'symbol': symbol,
                    'entry_date': entry_date,
                    'exit_date': exit_date,
                    'entry_price': entry_price,
                    'exit_price': exit_price,
                    'return': rtn
                })
    
    return pd.DataFrame(result)