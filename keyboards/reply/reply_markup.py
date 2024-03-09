from telebot import types
from datetime import datetime, timedelta
def currency_reply(cnt: int = 4, ch_cur: str = None):
    """
    Функция currency_reply реализована для создания кнопок выбора валюты

    :param cnt:  количество кнопок, которое необходимо вывести
    :param ch_cur: название валюты, которое уже выбрано
    :return: reply-клавиатура
    """
    markup_currency = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(text='Рубль')
    btn2 = types.KeyboardButton(text='Доллар')
    btn3 = types.KeyboardButton(text='Дирхам')
    btn4 = types.KeyboardButton(text='Teaher')
    if cnt == 4:
        markup_currency.row(btn1, btn2)
        markup_currency.row(btn3, btn4)
    else:
        if ch_cur == 'Рубль':
            markup_currency.row(btn2, btn3, btn4)
        elif ch_cur == 'Доллар':
            markup_currency.row(btn1, btn3, btn4)
        elif ch_cur == 'Дирхам':
            markup_currency.row(btn1, btn2, btn4)
        else:
            markup_currency.row(btn1, btn2, btn3)


    return markup_currency

def create_date_keyboard():
    """
    Функция create_date_keyboard реализована для создания клавиатуры с датами на ближайщую неделю

    :return: reply-клавиатура с датами
    """
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
    """
    Функция create_time_keyboard реализована для создания клавиатуры с временем

    :return: reply-клавиатура с временем
    """
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    row1 = []
    row2 = []
    row3 = []
    for hour in range(11, 21):
        if hour < 14:
            row1.append(types.KeyboardButton(text=str(hour) + ":00"))
        elif hour < 18:
            row2.append(types.KeyboardButton(text=str(hour) + ":00"))
        else:
            row3.append(types.KeyboardButton(text=str(hour) + ":00"))

    keyboard.add(*row1)
    keyboard.add(*row2)
    keyboard.add(*row3)
    return keyboard


def create_confirmation():
    """
    Функция create_confirmation реализована для вывода клавиатуры подтверждения

    :return: reply-клавиатура с выбором
    """
    keyboard = types.ReplyKeyboardMarkup( resize_keyboard=True)
    btn1 = types.KeyboardButton(text='Да✔️')
    btn2 = types.KeyboardButton(text='Нет❌')
    keyboard.row(btn1, btn2)
    return keyboard


def confirmation():
    """
    Функция confirmation реализована для вывода reply-кнопки с целью последующего вывода с информацией о бронируемой сделки

    :return: reply-клавиатура
    """
    keyboard = types.ReplyKeyboardMarkup( resize_keyboard=True)
    btn1 = types.KeyboardButton(text='Информация о брони')
    keyboard.row(btn1)
    return keyboard
