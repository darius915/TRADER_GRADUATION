import pandas as pd

def calculate_behavior_metrics(deals_df):
    if deals_df.empty:
        return {
            'overtrading_score': 0,
            'revenge_trades': 0,
            'actual_max_trades_per_day': 0,
            'losing_streak_recovery': 0,
            'martingale_escalation': False,
            'total_trades': 0,
            'trading_days': 0
        }

    # Total trades and days
    total_trades = len(deals_df)
    trading_days = (deals_df['entry_time'].max() - deals_df['entry_time'].min()).days + 1 if total_trades > 0 else 0

    # Losing streak recovery (max consecutive losses)
    streaks = []
    current_streak = 0
    for pnl in deals_df['pnl']:
        if pnl < 0:
            current_streak += 1
        else:
            if current_streak > 0:
                streaks.append(current_streak)
            current_streak = 0
    if current_streak > 0:
        streaks.append(current_streak)
    max_streak = max(streaks) if streaks else 0

    # Martingale escalation (lot > 1.5x after loss)
    martingale = False
    for i in range(1, total_trades):
        if deals_df['pnl'].iloc[i-1] < 0 and deals_df['lot_size'].iloc[i] > deals_df['lot_size'].iloc[i-1] * 1.5:
            martingale = True
            break

    # Revenge trades (quick trade after loss in same direction, <30 min)
    revenge = 0
    for i in range(1, total_trades):
        time_diff = (deals_df['entry_time'].iloc[i] - deals_df['entry_time'].iloc[i-1]).total_seconds() / 60
        if deals_df['pnl'].iloc[i-1] < 0 and time_diff < 30 and deals_df['direction'].iloc[i] == deals_df['direction'].iloc[i-1]:
            revenge += 1

    # Overtrading (max trades/day)
    daily_trades = deals_df.groupby(deals_df['entry_time'].dt.date).size()
    actual_max_trades_per_day = daily_trades.max() if not daily_trades.empty else 0
    overtrading_score = actual_max_trades_per_day  # or (actual_max_trades_per_day - 10) if >10 else 0

    return {
        'overtrading_score': overtrading_score,
        'revenge_trades': revenge,
        'actual_max_trades_per_day': actual_max_trades_per_day,
        'losing_streak_recovery': max_streak,
        'martingale_escalation': martingale,
        'total_trades': total_trades,
        'trading_days': trading_days
    }