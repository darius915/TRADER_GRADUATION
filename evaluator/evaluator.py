def calculate_scores(metrics, targets):
    scores = {}
    # RISK DISCIPLINE
    dd_score = 100 if metrics['max_drawdown'] <= targets['max_drawdown'] else 100 * (targets['max_drawdown'] / metrics['max_drawdown'])
    risk_score = 100 if metrics['risk_per_trade'] <= targets['risk_per_trade'] else 100 * (targets['risk_per_trade'] / metrics['risk_per_trade'])
    sl_score = metrics['sl_compliance']
    scores['risk_discipline'] = round((dd_score + risk_score + sl_score) / 3, 1)

    # EDGE CONSISTENCY
    pf_score = 100 if metrics['profit_factor'] >= targets['profit_factor'] else 100 * (metrics['profit_factor'] / targets['profit_factor'])
    exp_score = 100 if metrics['expectancy'] > targets['expectancy'] else 0
    ratio_score = 100 if metrics['avg_win_loss_ratio'] >= targets['avg_win_loss_ratio'] else 100 * (metrics['avg_win_loss_ratio'] / targets['avg_win_loss_ratio'])
    scores['edge_consistency'] = round((pf_score + exp_score + ratio_score) / 3, 1)

    # EXECUTION DISCIPLINE
    ot_score = 100 if metrics['overtrading_score'] <= targets['overtrading_threshold'] else 100 * (targets['overtrading_threshold'] / metrics['overtrading_score'])
    revenge_score = 100 if metrics['revenge_trades'] == 0 else 0
    mtd_score = 100 if metrics['actual_max_trades_per_day'] <= targets['max_trades_per_day'] else 100 * (targets['max_trades_per_day'] / metrics['actual_max_trades_per_day'])
    scores['execution_discipline'] = round((ot_score + revenge_score + mtd_score) / 3, 1)

    # STABILITY
    trades_score = 100 if metrics['total_trades'] >= targets['total_trades'] else 100 * (metrics['total_trades'] / targets['total_trades'])
    days_score = 100 if metrics['trading_days'] >= targets['trading_days'] else 100 * (metrics['trading_days'] / targets['trading_days'])
    cliff_score = 100 if metrics['equity_cliff'] <= targets['cliff_threshold'] else 100 * (targets['cliff_threshold'] / metrics['equity_cliff'])
    scores['stability'] = round((trades_score + days_score + cliff_score) / 3, 1)

    # PSYCHOLOGY
    recovery_score = 100 if metrics['losing_streak_recovery'] < targets['recovery_threshold'] else 100 * ((targets['recovery_threshold'] - 1) / metrics['losing_streak_recovery'])
    martingale_score = 100 if not metrics['martingale_escalation'] else 0
    scores['psychology'] = round((recovery_score + martingale_score) / 2, 1)

    return scores

def is_graduated(scores):
    return all(score >= 100 for score in scores.values())