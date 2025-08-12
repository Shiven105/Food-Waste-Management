
import sqlite3
import pandas as pd
from io import BytesIO
import base64

DB_PATH = "/mnt/data/food_waste.db"

def run_query(q):
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query(q, conn)
    finally:
        conn.close()
    return df

def run_modify(q, params=()):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(q, params)
    conn.commit()
    conn.close()

def get_table(name, limit=1000):
    return run_query(f"SELECT * FROM {name} LIMIT {limit}")

def to_csv_download_link(df, filename="data.csv"):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download CSV</a>'
    return href
