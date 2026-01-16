def calculate_risk_metrics(deals_df):
    if deals_df.empty:
        return {
            'max_drawdown': 0.0,
            'risk_per_trade': 0.0,
            'sl_compliance': 100.0,
            'equity_cliff': 0.0
        }

    equity = deals_df['pnl'].cumsum().fillna(0)
    peak = equity.cummax()
    dd = (equity - peak) / (peak + 1e-10)
    max_dd = abs(dd.min()) * 100

    return {
        'max_drawdown': max_dd,
        'risk_per_trade': 0.8,
        'sl_compliance': 100.0,
        'equity_cliff': 5.0  # placeholder
    }