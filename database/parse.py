from bs4 import BeautifulSoup as bs
from insertData import insertData
import os

def parse_price(price_element):
    """Парсит цену из элемента, учитывая разделители тысяч"""
    try:
        price_text = price_element.text.replace('₽', '').replace('\xa0', ' ').strip()
        clean_price = float(price_text.replace(' ', ''))
        return clean_price
    except (AttributeError, ValueError):
        return 3.3

def parsePage(links, driver, db_file):
    for link in links:
        driver.get(link)
        html = driver.page_source
        soup = bs(html, 'html.parser')
        specs = {}

        try:
            name = soup.find(class_="alert alert-primary size-biger mb-2")
            specs['Название'] = name.text.strip() if name else "Не указано"
        except Exception as e:
            print(f"Ошибка при парсинге названия: {e}")
            specs['Название'] = "Ошибка парсинга"

        price_element = soup.find(class_="size-bigest ccolor")
        if not price_element:
            price_elements = soup.find_all(class_="size-bigest text-danger")
            price_element = price_elements[0] if price_elements else None

        try:
            img = driver.find_element("xpath", "//div[@class='view']/picture/img")
            if img:
                img = img.get_attribute("src")
            else:
                img = None
                print("00000000000")
            specs['Картинка'] = img
        except Exception as e:
            print(f"Ошибка при парсинге изображения: {e}")
            specs['Картинка'] = None

        specs['Ссылка'] = link
        specs['Цена'] = parse_price(price_element) if price_element else 0

        if 'Название' in specs and 'Категория' in specs and 'Бренд' in specs:
            articul = specs['Название'].replace(specs['Категория'], '').strip().replace(specs['Бренд'], '').strip()
            specs['Артикул'] = articul
        
        spec_containers = soup.find_all(class_="col-md-4 col-12 mb-3")
        if not spec_containers:
            print("Контейнер с характеристиками не найден!")
        else:
            spec_container = spec_containers[0]
            for spec_container in spec_containers:
                for row in spec_container.find_all('div', class_='col-12 py-2 border-bottom'):
                    try:
                        name_span = row.find_next()
                        if not name_span:
                            continue
                        
                        name = name_span.text.strip(': ')
                        
                        value_span = row.find('span', class_='ccolor ml-3')
                        if not value_span:
                            continue
                        
                        if value_span.find('a'):
                            value = value_span.find('a').text.strip()
                        elif value_span.find('picture'):
                            value = value_span.get_text(strip=True)
                        else:
                            value = value_span.get_text(strip=True)
                        if name == 'Метраж':
                            clean_value = value.replace(' м2', '').strip()
                            specs[name] = clean_value
                            continue
                        specs[name] = value
                    
                    except Exception as e:
                        print(f"Ошибка при парсинге строки: {e}")
                        continue
                

        required_fields = ['Страна производства', 'Вид дерева', 'Тип рисунка', 
                        'Размер доски', 'В упаковке', 'Способ укладки', 'Износостойкость']
        for field in required_fields:
            if field not in specs:
                specs[field] = "Не указано"
            
        print("Характеристики товара:", specs)
        insertData(specs, db_file, specs['Категория'])
    
    txt_filename = f"{specs['Категория']}_links.txt"
    if not os.path.exists(txt_filename):
        with open(txt_filename, 'w', encoding='utf-8') as f:
            for idx, link in enumerate(links, 1):
                f.write(f"{idx}. {link}\n")
        print(f"Создан файл {txt_filename} с {len(links)} ссылками")
    else:
        print(f"Файл {txt_filename} уже существует")
