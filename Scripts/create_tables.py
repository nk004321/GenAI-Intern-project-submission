import sqlite3
import pandas as pd
import os

# Paths
data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
db_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'ecommerce.db')

# Read CSVs
ad_sales = pd.read_csv(os.path.join(data_dir, 'ad_sales.csv'))
total_sales = pd.read_csv(os.path.join(data_dir, 'total_sales.csv'))
eligibility = pd.read_csv(os.path.join(data_dir, 'eligibility.csv'))

# Connect to SQLite
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Load DataFrames into SQLite
ad_sales.to_sql('ad_sales', conn, if_exists='replace', index=False)
total_sales.to_sql('total_sales', conn, if_exists='replace', index=False)
eligibility.to_sql('eligibility', conn, if_exists='replace', index=False)

# Confirm tables
tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
print("Tables created:", tables)

conn.close()
