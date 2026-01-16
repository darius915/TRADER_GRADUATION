import pandas as pd
from datetime import datetime

try:
    import MetaTrader5 as mt5
except ImportError:
    mt5 = None


def fetch_trades(from_date, to_date):
    if mt5 is None:
        print("MetaTrader5 not installed")
        return pd.DataFrame()

    if not mt5.initialize():
        print("MT5 init failed:", mt5.last_error())
        return pd.DataFrame()

    deals = mt5.history_deals_get(
        datetime.strptime(from_date, "%Y-%m-%d"),
        datetime.strptime(to_date, "%Y-%m-%d")
    )

    mt5.shutdown()

    if deals is None or len(deals) == 0:
        return pd.DataFrame()

    df = pd.DataFrame(deals)

    # 🔒 NORMALIZE DATA
    required_columns = ['profit', 'commission', 'swap']
    for col in required_columns:
        if col not in df.columns:
            df[col] = 0.0

    # Net profit per deal
    df['net_profit'] = df['profit'] + df['commission'] + df['swap']

    return df
