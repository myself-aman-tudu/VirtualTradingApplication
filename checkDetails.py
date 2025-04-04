import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), "assets", "clientData.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def print_table_data(table_name):
    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        
        if not rows:
            print(f"\nTable '{table_name}' is empty.")
            return
        
        column_names = [desc[0] for desc in cursor.description]
        
        print(f"\n=== Data in '{table_name}' Table ===")
        print(" | ".join(column_names))
        print("-" * 50)
        
        for row in rows:
            print(" | ".join(map(str, row)))
    
    except sqlite3.Error as e:
        print(f"Error reading table '{table_name}':", e)

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [table[0] for table in cursor.fetchall()]

for table in tables:
    print_table_data(table)

conn.close()
