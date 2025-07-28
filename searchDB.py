import sqlite3
from database.utils import table_names

# def search(message, search_type):
#     if search_type == "🔑 Поиск по коду":
#         return searchByCode(message)
#     else:
#         return searchByArt(message, search_type)

def searchByCode(message):
    conn = None
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

def searchByArt(message, category):
    conn = None
    try:
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        
        cursor.execute(f"""
            SELECT * FROM "{category}" 
            WHERE "Артикул" LIKE ? 
            ORDER BY "Артикул"
            LIMIT 10
        """, (f'%{message}%',))
        
        # Получаем результаты и названия колонок
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description] if cursor.description else []
        
        # Преобразуем в список словарей
        products = []
        for row in results:
            product_dict = dict(zip(columns, row))
            products.append(product_dict)
        
        return products
    
    except sqlite3.OperationalError as e:
        print(f"Ошибка поиска в категории {category}: {e}")
        return []
    finally:
        if conn:
            conn.close()