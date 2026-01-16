from flask import Flask, render_template
import datetime

app = Flask(__name__)

def get_trading_data():
    # Safe mock with ALL needed keys
    return {
        'gain_percent': 2560.02,
        'net_pnl': 179.87,
        'trade_count': 216,
        'win_rate': 33.3,
        'profit_factor': 1.08,
        'expectancy': 0.2,
        'avg_win_loss_ratio': 1.8,
        'max_drawdown': 18.04,
        'risk_per_trade': 0.8,
        'sl_compliance': 100.0,
        'overtrading_score': 5,
        'revenge_trades': 0,
        'actual_max_trades_per_day': 4,
        'total_trades': 350,
        'trading_days': 70,
        'equity_cliff': 8.0,
        'losing_streak_recovery': 3,
        'martingale_escalation': False,
        'current_equity': 2236.87,
        'current_balance': 2167.87,
        'highest_balance': 2167.87,
        'deposits': 1804.00,
        'withdrawals': 0.00,
        'commissions': 0.00,
        'swaps': -14.72,
        'period_returns_daily': 0.00,
        'period_returns_weekly': 0.00,
        'period_returns_monthly': -2560.02,
    }

targets = {
    'max_drawdown': 20,
    'risk_per_trade': 1,
    'sl_compliance': 100,
    'profit_factor': 1.3,
    'expectancy': 0,
    'avg_win_loss_ratio': 1.5,
    'overtrading_threshold': 10,
    'revenge_trades': 0,
    'max_trades_per_day': 5,
    'total_trades': 300,
    'trading_days': 60,
    'cliff_threshold': 10,
    'recovery_threshold': 5,
    'martingale_escalation': False,
}

def calculate_scores(data, targets):
    scores = {}
    dd_score = 100 if data['max_drawdown'] <= targets['max_drawdown'] else 100 * (targets['max_drawdown'] / data['max_drawdown'])
    risk_score = 100 if data['risk_per_trade'] <= targets['risk_per_trade'] else 100 * (targets['risk_per_trade'] / data['risk_per_trade'])
    sl_score = data['sl_compliance']
    scores['risk_discipline'] = round((dd_score + risk_score + sl_score) / 3, 1)

    pf_score = 100 if data['profit_factor'] >= targets['profit_factor'] else 100 * (data['profit_factor'] / targets['profit_factor'])
    exp_score = 100 if data['expectancy'] > targets['expectancy'] else 0
    ratio_score = 100 if data['avg_win_loss_ratio'] >= targets['avg_win_loss_ratio'] else 100 * (data['avg_win_loss_ratio'] / targets['avg_win_loss_ratio'])
    scores['edge_consistency'] = round((pf_score + exp_score + ratio_score) / 3, 1)

    ot_score = 100 if data['overtrading_score'] <= targets['overtrading_threshold'] else 100 * (targets['overtrading_threshold'] / data['overtrading_score'])
    revenge_score = 100 if data['revenge_trades'] == targets['revenge_trades'] else 0
    mtd_score = 100 if data['actual_max_trades_per_day'] <= targets['max_trades_per_day'] else 100 * (targets['max_trades_per_day'] / data['actual_max_trades_per_day'])
    scores['execution_discipline'] = round((ot_score + revenge_score + mtd_score) / 3, 1)

    trades_score = 100 if data['total_trades'] >= targets['total_trades'] else 100 * (data['total_trades'] / targets['total_trades'])
    days_score = 100 if data['trading_days'] >= targets['trading_days'] else 100 * (data['trading_days'] / targets['trading_days'])
    cliff_score = 100 if data['equity_cliff'] <= targets['cliff_threshold'] else 100 * (targets['cliff_threshold'] / data['equity_cliff'])
    scores['stability'] = round((trades_score + days_score + cliff_score) / 3, 1)

    recovery_score = 100 if data['losing_streak_recovery'] < targets['recovery_threshold'] else 100 * ((targets['recovery_threshold'] - 1) / data['losing_streak_recovery'])
    martingale_score = 100 if not data['martingale_escalation'] else 0
    scores['psychology'] = round((recovery_score + martingale_score) / 2, 1)

    return scores

def is_graduated(scores):
    return all(score >= 100 for score in scores.values())

@app.route('/')
def dashboard():
    data = get_trading_data()
    scores = calculate_scores(data, targets)
    graduated = is_graduated(scores)
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    equity_curve = [2000, 2100, 2050, 2200, 2300, 2236.87]
    profit_curve = [0, 50, -20, 100, 150, 293.59]
    return render_template('dashboard.html', data=data, scores=scores, targets=targets, graduated=graduated, current_time=current_time, equity_curve=equity_curve, profit_curve=profit_curve)

if __name__ == '__main__':
    app.run(debug=True)