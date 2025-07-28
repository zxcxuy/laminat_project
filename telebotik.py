import telebot
from telebot import types
from searchDB import *
from database import utils

token = "6175392804:AAE_F9DiCwJwxydTY9V6qdU1spRAelfJS6E"
bot = telebot.TeleBot(token)

# храним тип поиска и выбранную категорию
USER_STATES = {}

@bot.message_handler(commands=['start'])
def start(message):
    USER_STATES[message.chat.id] = {'search_type': None, 'category': None}
    bot.send_message(
        message.chat.id,
        "👋 Привет! Как ищем?",
        reply_markup=main_buttons()
    )

@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    chat_id = message.chat.id
    
    if chat_id not in USER_STATES:
        USER_STATES[chat_id] = {'search_type': None, 'category': None}
    
    if message.text in ["🔍 Поиск по артикулу", "🔑 Поиск по коду"]:
        USER_STATES[chat_id]['search_type'] = message.text
        USER_STATES[chat_id]['category'] = None
        
        if message.text == "🔍 Поиск по артикулу":
            category_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            for category in utils.table_names:
                category_markup.add(types.KeyboardButton(category))
            bot.send_message(
                chat_id,
                "Выберите категорию:",
                reply_markup=category_markup
            )
        else:
            bot.send_message(chat_id, "Введите код (только цифры):", reply_markup=types.ReplyKeyboardRemove())
    
    elif (USER_STATES[chat_id]['search_type'] == "🔍 Поиск по артикулу" and 
          message.text in utils.table_names):
        USER_STATES[chat_id]['category'] = message.text
        bot.send_message(
            chat_id,
            "Введите артикул:",
            reply_markup=types.ReplyKeyboardRemove()
        )
    
    elif (USER_STATES[chat_id]['search_type'] == "🔍 Поиск по артикулу" and 
          USER_STATES[chat_id]['category']):
        products = searchByArt(message.text, USER_STATES[chat_id]['category'])
        if not products:
            bot.send_message(chat_id, "Товары не найдены", reply_markup=main_buttons())
        else:
            for product_data in products:
                formatted_message, image_url = formatter(product_data)
                send_product(chat_id, image_url, formatted_message)
        if len(products) == 10:
            bot.send_message(chat_id, "Выдало 10 запросов, попробуй ввести артикул больше")
        USER_STATES[chat_id] = {'search_type': None, 'category': None}
    
    elif USER_STATES[chat_id]['search_type'] == "🔑 Поиск по коду":
        product_data = searchByCode(message.text)
        if product_data:
            formatted_message, image_url = formatter(product_data)
            send_product(chat_id, image_url, formatted_message)
        else:
            bot.send_message(chat_id, "Товар не найден", reply_markup=main_buttons())
        USER_STATES[chat_id] = {'search_type': None, 'category': None}
    
    else:
        bot.send_message(
            chat_id,
            "Пожалуйста, выберите тип поиска:",
            reply_markup=main_buttons()
        )
        USER_STATES[chat_id] = {'search_type': None, 'category': None}

def main_buttons():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton("🔍 Поиск по артикулу")
    btn2 = types.KeyboardButton("🔑 Поиск по коду")
    markup.add(btn1, btn2)
    return markup

def formatter(data):
    if not data or not isinstance(data, dict):
        return "Товар не найден", None
    
    exclude_fields = {'id', 'Ссылка', 'Картинка', 'Название', 'Категория'}
    
    special_formatting = {
        'Цена': lambda x: f"{float(x):.2f} ₽" if x else None,
        'Метраж': lambda x: f"{x} м²" if x else None
    }
    
    title = f"<a href='{data.get('Ссылка', '')}'>{data.get('Название', 'Без названия')}</a>\n\n"
    
    characteristics = []
    for key, value in data.items():
        if key in exclude_fields or value is None:
            continue
        
        if key in special_formatting:
            value = special_formatting[key](value)
            if value is None:
                continue
        
        characteristics.append(f"<b>{key}:</b> {value}")
    
    message = title + "\n".join(characteristics) + "\n━━━━━━━━━━━━━━━━━"
    
    return message, data.get('Картинка')

def send_product(chat_id, image_url, formatted_message):
    if image_url:
        try:
            bot.send_photo(chat_id, image_url)
        except:
            pass

    bot.send_message(
        chat_id,
        formatted_message if formatted_message else "Товар не найден",
        parse_mode='HTML',
        disable_web_page_preview=True,
        reply_markup=main_buttons()
    )

bot.infinity_polling()