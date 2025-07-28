import telebot
from telebot import types
from searchDB import search

token = "6175392804:AAE_F9DiCwJwxydTY9V6qdU1spRAelfJS6E"
bot = telebot.TeleBot(token)

# Состояния бота
USER_STATES = {}

@bot.message_handler(commands=['start'])
def start(message):
    USER_STATES[message.chat.id] = None
    bot.send_message(
        message.chat.id,
        "👋 Привет! Как ищем?",
        reply_markup=main_buttons()
    )

@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    chat_id = message.chat.id
    
    if message.text in ["🔍 Поиск по артикулу", "🔑 Поиск по коду"]:
        USER_STATES[chat_id] = message.text
        prompt = "Введите артикул (буквы и цифры):" if message.text == "🔍 Поиск по артикулу" else "Введите код (только цифры):"
        bot.send_message(chat_id, prompt, reply_markup=types.ReplyKeyboardRemove())
    
    elif chat_id in USER_STATES and USER_STATES[chat_id]:
        search_type = USER_STATES[chat_id]
        search_query = message.text
        
        product_data = search(search_query, search_type)
        formatted_message, image_url = formatter(product_data)
        
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
        
        USER_STATES[chat_id] = None
    
    else:
        bot.send_message(
            chat_id,
            "Пожалуйста, выберите тип поиска:",
            reply_markup=main_buttons()
        )

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

bot.infinity_polling()
