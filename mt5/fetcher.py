import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta

def fetch_trading_data(login, password, server):
    if not mt5.initialize():
        print("MT5 initialize failed - using fallback")
        return pd.DataFrame()

    if not mt5.login(login, password=password, server=server):
        print(f"MT5 login failed: {mt5.last_error()} - using fallback")
        mt5.shutdown()
        return pd.DataFrame()

    # Get deals from last 90 days
    from_date = datetime.now() - timedelta(days=90)
    to_date = datetime.now()
    deals = mt5.history_deals_get(from_date, to_date)

    mt5.shutdown()

    if deals is None or len(deals) == 0:
        print("No deals found - using fallback")
        return pd.DataFrame()

    df = pd.DataFrame(list(deals))
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.rename(columns={'profit': 'pnl', 'time': 'entry_time'}, inplace=True)
    return df