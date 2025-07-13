import sqlite3
import psycopg

# Connect to SQLite DB
sqlite_conn = sqlite3.connect('Diary_updated.db')
sqlite_cursor = sqlite_conn.cursor()

# Connect to PostgreSQL DB
pg_conn = psycopg.connect(
    dbname="DiaryDB",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)
pg_cursor = pg_conn.cursor()

# Get all table names from SQLite
sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [row[0] for row in sqlite_cursor.fetchall()]

for table in tables:
    print(f"🔄 Migrating table: {table}")

    # Get columns
    sqlite_cursor.execute(f"PRAGMA table_info({table})")
    columns_info = sqlite_cursor.fetchall()
    column_names = [col[1] for col in columns_info]

    # Prepare and execute SELECT
    sqlite_cursor.execute(f"SELECT {', '.join(column_names)} FROM {table}")
    rows = sqlite_cursor.fetchall()

    # Prepare INSERT
    placeholders = ', '.join(['%s'] * len(column_names))
    insert_stmt = f"INSERT INTO {table} ({', '.join(column_names)}) VALUES ({placeholders})"

    # Execute INSERT for each row
    for row in rows:
        pg_cursor.execute(insert_stmt, row)

    print(f"✅ {len(rows)} rows copied from {table}")

pg_conn.commit()
sqlite_conn.close()
pg_conn.close()

print("🎉 All tables migrated from Diary_updated.db to PostgreSQL.")
