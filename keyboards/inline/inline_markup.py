from telebot import types

def start_inline():
    markup_start = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text='Забронировать сумму сделки', callback_data='booking')
    markup_start.add(button)

    return markup_start

