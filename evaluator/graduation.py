def evaluate(metrics):
    checks = {
        "max_drawdown": metrics["max_dd"] <= 20,
        "profit_factor": metrics["pf"] >= 1.3,
        "expectancy": metrics["expectancy"] > 0,
        "trade_count": metrics["trades"] >= 300
    }

    graduated = all(checks.values())
    return graduated, checks
