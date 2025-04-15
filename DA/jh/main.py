import sys
import argparse

from db.connector import create_connection
from fetch.data_loader import load_table, load_csv
from indicators.indicator_processor import calculate_all_indicators
from strategy.signal_processor import calculate_all_signals
from backtest.backtest_runner import run_backtest
from visualize import performance

def main():
    # ArgumentParser
    parser = argparse.ArgumentParser()
    parser.add_argument('--action', choices=['create', 'update', 'visualize'], required=True,
                        help='작업 선택: "create", "update", "visualize"')
    parser.add_argument('--strategy', choices=['macd_cross'],
                        help='시각화 대상 전략 선택')
    args = parser.parse_args()

    # 최초 실행 시 기술 지표, 백테스트 결과 dataframe 생성
    if args.action == 'create':
        # DB 연결
        connection = create_connection()
        if connection is None:
            sys.exit()

        # 전체 data load
        stock_info_df = load_table(connection, 'us_stocks_info')
        # stock_prices_df = load_table(connection, 'us_stocks_prices')

        # 테스트용 dataframe
        # stock_info_df = stock_info_df[:10]
        # stock_prices_df = stock_prices_df[(stock_prices_df['symbol'].isin(stock_info_df['symbol'])) & (stock_prices_df['date'].dt.year >= 2010)]
        # stock_prices_df.to_csv('./data/temp/temp_prices.csv', index=False, encoding='utf-8')

        stock_prices_df = load_csv('./data/temp/temp_prices.csv')

        # 기술지표 dataframe
        indicators_df = calculate_all_indicators(stock_prices_df)
        indicators_df.to_csv('./data/temp/temp_indicators.csv', index=False, encoding='utf-8')

        indicators_df = load_csv('./data/temp/temp_indicators.csv')

        # 매수매도 시그널 dataframe
        signal_df = calculate_all_signals(indicators_df)
        signal_df.to_csv('./data/temp/temp_strategy_signals.csv', index=False, encoding='utf-8')

        signal_df = load_csv('./data/temp/temp_strategy_signals.csv')

        # 백테스트 dataframe
        macd_cross = run_backtest(indicators_df, signal_df, 'macd_cross')
        macd_cross.to_csv('./data/temp/temp_macd_cross_backtest.csv', index=False, encoding='utf-8')
        macd_cross = load_csv('./data/temp/temp_macd_cross_backtest.csv')

        # DB 연결 종료
        connection.close()

    elif args.action == 'update':
        # DB 연결
        connection = create_connection()
        if connection is None:
            sys.exit()
        
        # DB 연결 종료
        connection.close()

    elif args.action == 'visualize':
        if args.strategy is None:
            parser.error('visualize를 사용할 때는 --strategy 인자가 필수입니다.')
        
        strategy = args.strategy

        df = load_csv(f'./data/temp/temp_{strategy}_backtest.csv')
        symbols = df['symbol'].unique()

        performance.plot_avg_return_per_symbol(df, strategy)

        for symbol in symbols:
            performance.plot_cumulative_return(df, symbol, strategy)

        for symbol in symbols:
            performance.plot_return_distribution(df, symbol, strategy)

        for symbol in symbols:
            performance.plot_win_ratio(df, symbol, strategy)    

if __name__ == '__main__':
    main()