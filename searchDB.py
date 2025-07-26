import sqlite3
from database.utils import table_names

def search(message, search_type):
    if search_type == "🔍 Поиск по артикулу":
        searchByArt(message)
    else:
        return searchByCode(message)

def searchByCode(message):
    try:
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        
        found_products = []
        
        for table_name in table_names:
            try:
                cursor.execute(
                    f'SELECT * FROM "{table_name}" WHERE "Код товара" = ?',
                    (str(message),))
                
                result = cursor.fetchone()
                if result:
                    columns = [desc[0] for desc in cursor.description]
                    found_products.append(dict(zip(columns, result)))
            
            except sqlite3.Error as e:
                print(f"Ошибка поиска в таблице {table_name}: {e}")
                continue
        print(found_products[0]) if found_products else None
        return found_products[0] if found_products else None
    
    except sqlite3.Error as e:
        print(f"Ошибка подключения к базе: {e}")
        return None
    finally:
        if conn:
            conn.close()

def searchByArt(message):
    try:
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()

        cursor.execute()
    except sqlite3.OperationalError as e:
        print(f"Ошибка поиска: {e}")