import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_avg_return_per_symbol(df: pd.DataFrame, strategy_name: str):
    mean_returns = df.groupby('symbol')['return'].mean().sort_values()

    plt.figure(figsize=(10, 6))
    sns.barplot(x=mean_returns.index, y=mean_returns.values * 100, hue=mean_returns.index, palette='Blues_d')
    plt.xticks(rotation=45)
    plt.title(f'Average Return per Symbol - {strategy_name}')
    plt.ylabel('Avg Return (%)')
    plt.tight_layout()

    plt.savefig(f'./output/average_return_{strategy_name}.png', bbox_inches='tight')
    plt.close()

def plot_cumulative_return(df: pd.DataFrame, symbol: str, strategy_name: str):
    df = df[df['symbol'] == symbol].sort_values('exit_date')
    df['cumulative_return'] = (1 + df['return']).cumprod()
    years = df['exit_date'].dt.year
    year_start_dates = df.groupby(years)['exit_date'].first().values

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df['exit_date'], df['cumulative_return'], label=strategy_name)
    ax.set_xticks(year_start_dates)
    ax.set_xticklabels([pd.Timestamp(d).year for d in year_start_dates])
    ax.set_title(f'Cumulative Return - {strategy_name} - {symbol}')
    ax.set_xlabel('Year')
    ax.set_ylabel('Cumulative Return')
    plt.tight_layout()
    
    plt.savefig(f'./output/cumulative_return_{symbol}', bbox_inches='tight')
    plt.close()

def plot_return_distribution(df: pd.DataFrame, symbol: str, strategy_name: str):
    df = df[df['symbol'] == symbol]

    plt.figure(figsize=(8, 5))
    plt.hist(df['return'], bins=30, color='skyblue', edgecolor='black')
    plt.title(f'Return Distribution - {strategy_name} - {symbol}')
    plt.xlabel('Return')
    plt.ylabel('Frequency')
    plt.tight_layout()
    
    plt.savefig(f'./output/return_distribution_{symbol}', bbox_inches='tight')
    plt.close()

def plot_win_ratio(df: pd.DataFrame, symbol: str, strategy_name: str):
    df = df[df['symbol'] == symbol]

    win_ratio = (df['return'] > 0).mean()
    loss_ratio = 1 - win_ratio

    plt.bar(['Win', 'Loss'], [win_ratio, loss_ratio], color=['green', 'red'])
    plt.title(f'Win vs Loss Ratio - {strategy_name} - {symbol}')
    plt.ylim(0, 1)
    plt.ylabel('Ratio')
    plt.tight_layout()
    
    plt.savefig(f'./output/win_ratio_{symbol}', bbox_inches='tight')
    plt.close()