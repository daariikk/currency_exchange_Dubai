from telebot import types
from datetime import datetime, timedelta
def currency_reply(cnt: int = 4, ch_cur: str = None):
    markup_currency = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(text='Рубль')
    btn2 = types.KeyboardButton(text='Доллар')
    btn3 = types.KeyboardButton(text='Дирхам')
    btn4 = types.KeyboardButton(text='Teaher')
    if cnt == 4:
        markup_currency.row(btn1, btn2)
        markup_currency.row(btn3, btn4)
    else:
        if ch_cur != 'Рубль':
            markup_currency.row(btn2, btn3, btn4)
        elif ch_cur != 'Доллар':
            markup_currency.row(btn1, btn3, btn4)
        elif ch_cur != 'Дирхам':
            markup_currency.row(btn1, btn2, btn4)
        else:
            markup_currency.row(btn1, btn2, btn3)


    return markup_currency

def create_date_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
    today = datetime.now().date()
    row1_buttons = []
    row2_buttons = []
    for i in range(7):
        date = today + timedelta(days=i)
        if i < 4:
            row1_buttons.append(types.KeyboardButton(text=date.strftime('%d.%m')))
        else:
            row2_buttons.append(types.KeyboardButton(text=date.strftime('%d.%m')))
    keyboard.add(*row1_buttons)
    keyboard.add(*row2_buttons)
    return keyboard


def create_time_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
    for hour in range(11, 22):
        keyboard.add(types.KeyboardButton(text=str(hour) + ":00"))
    return keyboard