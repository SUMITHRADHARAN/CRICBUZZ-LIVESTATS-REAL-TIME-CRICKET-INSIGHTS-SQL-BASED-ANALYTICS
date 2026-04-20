import pandas as pd
from sqlalchemy import create_engine, text
import urllib.parse
import mysql.connector

# 1. Database Credentials
USER = "root"
PASSWORD = "dm3879@D"
HOST = "localhost"
PORT = "3306"
DATABASE = "cricbuzz_db"

# 2. Fix the @ in password and create engine
safe_password = urllib.parse.quote_plus(PASSWORD)
DB_URL = f"mysql+pymysql://{USER}:{safe_password}@{HOST}:{PORT}/{DATABASE}"
engine = create_engine(DB_URL)

# 3. Define ALL functions required
def get_engine():
    return engine

def init_db():
    try:
        with engine.connect() as conn:
            print("Connected to MySQL!")
    except Exception as e:
        print(f"Connection failed: {e}")

# FIXED: Combined into one function that accepts the arguments sent by crud_operations.py
def get_mysql_schema(host=HOST, user=USER, password=PASSWORD):
    schema = {}
    try:
        conn = mysql.connector.connect(host=host, user=user, password=password)
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SHOW DATABASES")
        for db in cursor.fetchall():
            db_name = db['Database']
            if db_name in ['information_schema', 'mysql', 'performance_schema', 'sys']:
                continue
            
            schema[db_name] = {"tables": {}}
            cursor.execute(f"SHOW TABLES FROM `{db_name}`")
            for table in cursor.fetchall():
                table_name = list(table.values())[0]
                schema[db_name]["tables"][table_name] = {}
        
        cursor.close()
        conn.close()
        return schema
    except Exception as e:
        # Fallback to your original logic if connection fails
        query = f"SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '{DATABASE}'"
        return pd.read_sql(query, engine)

def list_databases():
    return pd.read_sql("SHOW DATABASES", engine)

def list_tables():
    return pd.read_sql("SHOW TABLES", engine)

def get_table_columns(host, user, password, database, table_name):
    # Updated signature to match the call in crud_operations.py
    return pd.read_sql(f"DESCRIBE {database}.{table_name}", engine).to_dict('records')

def fetch_table(host, user, password, database, table_name, limit=200):
    # Updated signature to match the call in crud_operations.py
    sql = f"SELECT * FROM {database}.{table_name} LIMIT {limit}"
    return pd.read_sql(sql, engine), sql

# Set the credentials as default arguments
def run_select(query, host=HOST, user=USER, password=PASSWORD, database=DATABASE):
    return pd.read_sql(query, engine)

# Keep your alias
run_query = run_select


def execute_update(host, user, password, database, table, set_part, where_part):
    sql = f"UPDATE {database}.{table} SET {set_part} WHERE {where_part}"
    with engine.connect() as conn:
        with conn.begin():
            result = conn.execute(text(sql))
            return result.rowcount, sql

def insert_row(host, user, password, database, table, data):
    cols = ", ".join(data.keys())
    placeholders = ", ".join([f"'{v}'" for v in data.values()])
    sql = f"INSERT INTO {database}.{table} ({cols}) VALUES ({placeholders})"
    with engine.connect() as conn:
        with conn.begin():
            result = conn.execute(text(sql))
            return result.rowcount, sql

def delete_rows(host, user, password, database, table, condition):
    sql = f"DELETE FROM {database}.{table} WHERE {condition}"
    with engine.connect() as conn:
        with conn.begin():
            result = conn.execute(text(sql))
            return result.rowcount, sql

# Alias names
run_query = run_select
execute_query = execute_update
