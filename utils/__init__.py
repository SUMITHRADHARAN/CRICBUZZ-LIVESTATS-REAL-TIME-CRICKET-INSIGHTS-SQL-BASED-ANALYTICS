# utils/__init__.py
from .db_connection import (
    get_mysql_schema,
    list_databases,
    list_tables,
    get_table_columns,
    fetch_table,
    run_select,
    insert_row,
    delete_rows,
    execute_update,
    get_engine # Added this so main.py can use it
)

def init_db():
    """Verify MySQL connection works."""
    try:
        from .db_connection import get_engine
        with get_engine().connect() as conn:
            print("Connected to MySQL successfully!")
    except Exception as e:
        print(f"Failed to connect to MySQL: {e}")
