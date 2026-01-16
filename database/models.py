import sqlite3
from datetime import date

DB_FILE = "trader_graduation.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_scores (
            date TEXT PRIMARY KEY,
            risk_discipline REAL,
            edge_consistency REAL,
            execution_discipline REAL,
            stability REAL,
            psychology REAL
        )
    ''')
    conn.commit()
    conn.close()

def save_daily_scores(scores):
    today = date.today().isoformat()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO daily_scores
        (date, risk_discipline, edge_consistency, execution_discipline, stability, psychology)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (today, scores['risk_discipline'], scores['edge_consistency'],
          scores['execution_discipline'], scores['stability'], scores['psychology']))
    conn.commit()
    conn.close()