def calculate_performance_metrics(deals_df):
    if deals_df.empty:
        return {
            'profit_factor': 0.0,
            'expectancy': 0.0,
            'avg_win_loss_ratio': 0.0,
            'win_rate': 0.0,
            'net_pnl': 0.0,
            'gain_percent': 0.0
        }

    wins = deals_df[deals_df['pnl'] > 0]
    losses = deals_df[deals_df['pnl'] < 0]

    pos = wins['pnl'].sum()
    neg = abs(losses['pnl'].sum())
    profit_factor = pos / neg if neg > 0 else 999.0

    expectancy = deals_df['pnl'].mean()
    avg_win = wins['pnl'].mean() if not wins.empty else 0
    avg_loss = abs(losses['pnl'].mean()) if not losses.empty else 1
    ratio = avg_win / avg_loss if avg_loss != 0 else 0
    win_rate = len(wins) / len(deals_df) * 100 if len(deals_df) > 0 else 0

    return {
        'profit_factor': profit_factor,
        'expectancy': expectancy,
        'avg_win_loss_ratio': ratio,
        'win_rate': win_rate,
        'net_pnl': deals_df['pnl'].sum(),
        'gain_percent': 0.0  # improve with starting balance later
    }