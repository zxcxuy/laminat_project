import sqlite3

def init_database(db_file, table_name):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS "{table_name}" (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        "Ссылка" TEXT UNIQUE,
        "Название" TEXT,
        "Цена" REAL
    )
    """)
    conn.commit()
    conn.close()

def add_missing_columns(db_file, data, table_name):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute(f'PRAGMA table_info("{table_name}")')
    existing_columns = [column[1] for column in cursor.fetchall()]
    
    for column_name in data.keys():
        safe_column_name = f'"{column_name}"'
        
        if column_name not in existing_columns:
            value = data[column_name]
            col_type = "TEXT"
            
            if isinstance(value, (int, float)):
                col_type = "REAL" if isinstance(value, float) else "INTEGER"
            
            try:
                cursor.execute(f'ALTER TABLE "{table_name}" ADD COLUMN {safe_column_name} {col_type}')
                print(f"✅ Добавлен столбец: {safe_column_name} ({col_type})")
            except sqlite3.OperationalError as e:
                print(f"❌ Ошибка при добавлении {safe_column_name}: {e}")
    
    conn.commit()
    conn.close()