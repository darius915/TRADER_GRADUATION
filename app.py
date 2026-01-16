from flask import Flask, render_template

app = Flask(__name__)   # 👈 THIS LINE MUST EXIST BEFORE @app.route

@app.route("/")
def dashboard():
    metrics = {
        "skills": {
            "Discipline": 70,
            "Risk Management": 85,
            "Patience": 60
        },
        "equity": 1200,
        "drawdown": 12
    }

    return render_template("dashboard.html", metrics=metrics)


@app.route("/")
def dashboard():
    trades_raw = fetch_trades("2025-01-01", "2026-01-16")
    trades = prepare_trades(trades_raw)

    if trades.empty:
        return render_template(
            "dashboard.html",
            metrics={"skills": {}},
            graduated=False,
            message="No trade data available yet."
        )

    # =========================
    # RAW METRICS
    # =========================
    equity_curve = trades["net_profit"].cumsum().tolist()

    max_dd = round(max_drawdown(equity_curve), 2)
    pf = round(profit_factor(trades.rename(columns={"net_profit": "profit"})), 2)
    exp = round(expectancy(trades.rename(columns={"net_profit": "profit"})), 2)
    trade_count = len(trades)

    # =========================
    # SKILL SCORES (0–100)
    # =========================
    risk_score = min(100, max(0, 100 - (max_dd * 2)))
    edge_score = min(100, max(0, (pf - 1) * 50))
    execution_score = min(100, max(0, 100 - (trade_count / 5)))
    psychology_score = min(100, max(0, 100 - (abs(exp) * 10)))

    skills = {
        "Risk Discipline": round(risk_score),
        "Edge Quality": round(edge_score),
        "Execution Discipline": round(execution_score),
        "Psychological Stability": round(psychology_score)
    }

    # =========================
    # GRADUATION LOGIC
    # =========================
    graduated = (
        skills["Risk Discipline"] >= 75 and
        skills["Edge Quality"] >= 70 and
        skills["Execution Discipline"] >= 70 and
        skills["Psychological Stability"] >= 65
    )

    metrics = {
        "skills": skills,
        "raw": {
            "max_drawdown": max_dd,
            "profit_factor": pf,
            "expectancy": exp,
            "trade_count": trade_count
        }
    }

    return render_template(
        "dashboard.html",
        metrics=metrics,
        graduated=graduated,
        message=None
    )
