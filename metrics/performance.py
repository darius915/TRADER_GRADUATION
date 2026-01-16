def profit_factor(trades):
    wins = trades[trades['profit'] > 0]['profit'].sum()
    losses = abs(trades[trades['profit'] < 0]['profit'].sum())
    return wins / losses if losses != 0 else float('inf')

def expectancy(trades):
    win_rate = len(trades[trades['profit'] > 0]) / len(trades)
    avg_win = trades[trades['profit'] > 0]['profit'].mean()
    avg_loss = abs(trades[trades['profit'] < 0]['profit'].mean())
    return (win_rate * avg_win) - ((1 - win_rate) * avg_loss)
