from telebot.types import Message
from telebot import types
from loader import bot
from keyboards.inline.inline_markup import start_inline
from keyboards.reply.reply_markup import currency_reply, create_date_keyboard, create_time_keyboard

from database.core import insert_command



@bot.message_handler(commands=["start"])
def bot_start(message: Message):
    insert_command(message.from_user.first_name, command='/start')
    WELCOME_MESSAGE = """
    Приветствуем вас!

    Я ваш персональный помощник в обмене валюты. С радостью помогу вам забронировать необходимую сумму сделки и согласовать удобное время встречи для обмена валюты. Просто укажите желаемую сумму и время, и я сделаю все возможное, чтобы обеспечить вам быстрый и удобный обмен.
    """
    bot.reply_to(message, WELCOME_MESSAGE, reply_markup=start_inline())

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    user_id = callback.from_user.id
    if callback.data == 'booking':
        info  = {
            "changeable_currency" : None,
            "currency_received" : None,
            "date" : None,
            "time" : None
        }
        insert_command(callback.from_user.first_name, command='Забронировать сумму сделки')
        bot.send_message(user_id, "Выберите валюту, которую вы хотите обменять:", reply_markup=currency_reply(4))

        bot.register_next_step_handler(callback.message, get_first_currency, info)

def get_first_currency(message: Message, info_dict):
    get_changeable_currency = message.text

    print(get_changeable_currency)
    if not (get_changeable_currency in ['Рубль', 'Доллар', 'Дирхам', 'Teaher']):
        bot.send_message(message.chat.id, "Выберите валюту, которую вы хотите обменять:", reply_markup=currency_reply(4))

        bot.register_next_step_handler(message, get_first_currency, info_dict)
        pass #error
    else:
        info_dict['changeable_currency'] = get_changeable_currency
        bot.send_message(message.chat.id, "Выберите валюту, на которую вы хотите обменять:", reply_markup=currency_reply(3, get_changeable_currency))

        bot.register_next_step_handler(message, get_second_currency, info_dict)


def get_second_currency(message: Message, info_dict):
    get_received_currency = message.text
    if not (get_received_currency in ['Рубль', 'Доллар', 'Дирхам', 'Teaher']):
        bot.send_message(message.chat.id, "Выберите валюту, на которую вы хотите обменять:", reply_markup=currency_reply(3, info_dict['changeable_currency']))

        bot.register_next_step_handler(message, get_second_currency, info_dict)
        pass #error
    else:
        info_dict['currency_received'] = get_received_currency
        bot.send_message(message.chat.id, "Отлично, день выбран! Дело осталось за малым! \nВыберите день встречи:", reply_markup=create_date_keyboard())

        bot.register_next_step_handler(message.chat.id, get_time, info_dict)

def get_time(message: Message, info_dict):
    get_received_currency = message.text
    if not (get_received_currency in ['Рубль', 'Доллар', 'Дирхам', 'Teaher']):
        bot.send_message(message.chat.id, "Выберите валюту, на которую вы хотите обменять:", reply_markup=currency_reply(3, info_dict['changeable_currency']))

        bot.register_next_step_handler(message, get_second_currency, info_dict)
        pass #error
    else:
        info_dict['currency_received'] = get_received_currency
        bot.send_message(message.chat.id, "Отлично, день выбран! Дело осталось за малым! \nВыберите день встречи:", reply_markup=create_date_keyboard())

        # bot.register_next_step_handler(message.chat.id, get_second_currency, info_dict)