# import sqlite3

# old_db = 'Diary.db'
# new_db = 'Diary_updated.db'

# # Connect to old and new DBs
# conn_old = sqlite3.connect(old_db)
# cursor_old = conn_old.cursor()

# conn_new = sqlite3.connect(new_db)
# cursor_new = conn_new.cursor()

# # Get all table names from old DB
# cursor_old.execute("SELECT name FROM sqlite_master WHERE type='table'")
# tables = [row[0] for row in cursor_old.fetchall()]

# for table in tables:
    # print(f"🔄 Processing table: {table}")

    # # Get columns and types from old table
    # cursor_old.execute(f"PRAGMA table_info({table})")
    # columns_info = cursor_old.fetchall()  # (cid, name, type, notnull, dflt_value, pk)

    # column_defs = []
    # columns_without_id = []

    # for col in columns_info:
        # name, col_type = col[1], col[2]
        # columns_without_id.append(name)
        # column_defs.append(f"{name} {col_type}")

    # # Add ID column as primary key
    # # create_stmt = f"CREATE TABLE {table} (id INTEGER PRIMARY KEY AUTOINCREMENT, {', '.join(column_defs)})"
    # # cursor_new.execute(create_stmt)
    
    # # Add ID column as primary key at the end
    # column_defs.append("id INTEGER PRIMARY KEY AUTOINCREMENT")
    # create_stmt = f"CREATE TABLE {table} ({', '.join(column_defs)})"
    # cursor_new.execute(create_stmt)

    # # Copy data from old to new, inserting NULL for auto-ID
    # cursor_old.execute(f"SELECT {', '.join(columns_without_id)} FROM {table}")
    # rows = cursor_old.fetchall()

    # placeholders = ", ".join("?" for _ in columns_without_id)
    # insert_stmt = f"INSERT INTO {table} ({', '.join(columns_without_id)}) VALUES ({placeholders})"
    # cursor_new.executemany(insert_stmt, rows)

    # print(f"✅ {len(rows)} rows copied from {table}")

# conn_new.commit()
# conn_old.close()
# conn_new.close()

# print("🎉 All tables copied to Diary_updated.db with ID columns.")


import sqlite3

old_db = 'Diary.db'
new_db = 'Diary_updated.db'

# Connect to old and new DBs
conn_old = sqlite3.connect(old_db)
cursor_old = conn_old.cursor()

conn_new = sqlite3.connect(new_db)
cursor_new = conn_new.cursor()

# Step 1: Inspect column types from the first valid table to build schema
cursor_old.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [row[0] for row in cursor_old.fetchall()]

schema_found = False
for table in tables:
    cursor_old.execute(f"PRAGMA table_info({table})")
    columns_info = cursor_old.fetchall()
    column_names = [col[1] for col in columns_info]

    if set(['Strtime', 'Title', 'Tasktime', 'TaskDetails', 'Detailtime', 'Endtime']).issubset(column_names):
        column_types = {col[1]: col[2] for col in columns_info if col[1] in ['Strtime', 'Title', 'Tasktime', 'TaskDetails', 'Detailtime', 'Endtime']}
        schema_found = True
        break

if not schema_found:
    raise Exception("❌ No compatible tables found to infer schema.")

# Step 2: Create a temporary table without ID using actual types
cursor_new.execute("DROP TABLE IF EXISTS temp_diary")
temp_table_fields = ",\n        ".join([f"{col} {col_type}" for col, col_type in column_types.items()])
cursor_new.execute(f"""
    CREATE TABLE temp_diary (
        {temp_table_fields},
        goal TEXT
    )
""")

# Step 3: Merge all compatible tables into temp_diary

total_inserted = 0
for table in tables:
    print(f"🔄 Processing table: {table}")

    cursor_old.execute(f"PRAGMA table_info({table})")
    columns_info = cursor_old.fetchall()
    column_names = [col[1] for col in columns_info]
    print(f"📋 Columns in '{table}': {column_names}")

    if not set(column_types.keys()).issubset(column_names):
        print(f"⚠️ Skipping table '{table}' due to incompatible structure.")
        continue

    cursor_old.execute(f"SELECT {', '.join(column_types.keys())} FROM {table}")
    rows = cursor_old.fetchall()

    for row in rows:
        row_with_goal = row + (table,)
        cursor_new.execute(f"""
            INSERT INTO temp_diary ({', '.join(column_types.keys())}, goal)
            VALUES ({', '.join(['?' for _ in column_types])}, ?)
        """, row_with_goal)

    print(f"✅ {len(rows)} rows copied from '{table}'")
    total_inserted += len(rows)

conn_new.commit()

# Step 4: Create sorted unified table
cursor_new.execute("DROP TABLE IF EXISTS unified_diary")
cursor_new.execute(f"""
    CREATE TABLE unified_diary AS
    SELECT 
        NULL AS id,
        {', '.join(column_types.keys())},
        goal
    FROM temp_diary
    ORDER BY strtime
""")

# Step 5: Recreate the unified_diary table with proper ID autoincrement and original types
cursor_new.execute("DROP TABLE IF EXISTS final_diary")
cursor_new.execute(f"""
    CREATE TABLE final_diary (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        {', '.join([f'{col} {col_type}' for col, col_type in column_types.items()])},
        goal TEXT
    )
""")

cursor_new.execute(f"""
    INSERT INTO final_diary ({', '.join(column_types.keys())}, goal)
    SELECT {', '.join(column_types.keys())}, goal FROM unified_diary
""")

# Step 6: Drop all intermediate tables
cursor_new.execute("DROP TABLE IF EXISTS temp_diary")
cursor_new.execute("DROP TABLE IF EXISTS unified_diary")

conn_new.commit()
conn_old.close()
conn_new.close()

print(f"🎉 {total_inserted} rows merged, sorted by 'strtime', with types preserved and inserted into final_diary with ID column. All temporary tables removed.")
