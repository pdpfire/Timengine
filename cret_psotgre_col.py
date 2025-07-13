import sqlite3

# Map SQLite types to PostgreSQL types
TYPE_MAP = {
    "INTEGER": "INTEGER",
    "TEXT": "VARCHAR",
    "REAL": "FLOAT",
    "NUMERIC": "NUMERIC",
    "BLOB": "BYTEA",
    "TIMESTAMP": "TIMESTAMP",
    "DATE": "DATE",
    "DATETIME": "TIMESTAMP"
}

sqlite_conn = sqlite3.connect('Diary_updated.db')
sqlite_cursor = sqlite_conn.cursor()

# Get all tables
sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [row[0] for row in sqlite_cursor.fetchall()]

for table in tables:
    print(f"\n-- Generating PostgreSQL CREATE TABLE for '{table}'")

    sqlite_cursor.execute(f"PRAGMA table_info({table})")
    columns = sqlite_cursor.fetchall()  # (cid, name, type, notnull, dflt_value, pk)

    pg_columns = []
    for col in columns:
        name = col[1]
        col_type = col[2].upper()
        notnull = "NOT NULL" if col[3] else ""

        # Convert type to PostgreSQL equivalent
        pg_type = TYPE_MAP.get(col_type.split('(')[0], "TEXT")

        if name == "id":
            pg_columns.insert(0, f"{name} SERIAL PRIMARY KEY")
        else:
            pg_columns.append(f"{name} {pg_type} {notnull}")

    # Build CREATE TABLE statement
    create_stmt = f"CREATE TABLE {table} (\n    " + ",\n    ".join(pg_columns) + "\n);"
    print(create_stmt)

sqlite_conn.close()
