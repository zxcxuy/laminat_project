import sqlite3
from databaseCheck import add_missing_columns

def insertData(data, db_file, table_name):
    add_missing_columns(db_file, data, table_name)
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        columns = [f'"{key}"' for key in data.keys()]
        values = list(data.values())

        placeholders = ", ".join(['?'] * len(columns))
        columns_str = ', '.join(columns)

        cursor.execute(f"""
        INSERT OR REPLACE INTO "{table_name}" ({columns_str})
        VALUES ({placeholders})
        """, values)
        
        conn.commit()
        print(f"Данные успешно сохранены в таблицу {table_name}")
    except sqlite3.Error as e:
        print(f"Ошибка при добавлении продукта: {e}")
    finally:
        if conn:
            conn.close()