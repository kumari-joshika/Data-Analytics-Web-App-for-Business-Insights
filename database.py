import sqlite3
import pandas as pd

def get_connection():
    conn = sqlite3.connect("analytics.db", check_same_thread=False)
    return conn

def save_dataframe_to_db(df, table_name="uploaded_data"):
    conn = get_connection()
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()

def run_query(query):
    conn = get_connection()
    result = pd.read_sql(query, conn)
    conn.close()
    return result
