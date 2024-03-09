from telebot.types import Message
from telebot import types
from loader import bot
from keyboards.inline.inline_markup import start_inline
from keyboards.reply.reply_markup import currency_reply, create_date_keyboard, create_time_keyboard, create_confirmation, confirmation
from .support_functions import check_date_format, check_time_format, exchange_calculator



@bot.message_handler(commands=["start"])
def bot_start(message: Message):
    """
    Шаг 1
    Функция bot_start иницирует запуск бота, отправляет привественной сообщение

    :param message: команда /start
    :return: inline-кнопка для запуска основного функционала
    """

    WELCOME_MESSAGE = """
    Приветствуем вас!

    Я ваш персональный помощник в обмене валюты. С радостью помогу вам забронировать необходимую сумму сделки и согласовать удобное время встречи для обмена валюты. Просто укажите желаемую сумму и время, и я сделаю все возможное, чтобы обеспечить вам быстрый и удобный обмен.
    """
    bot.reply_to(message, WELCOME_MESSAGE, reply_markup=start_inline())


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    """
    Шаг 2
    Функция callback_message создаёт пустой словарь со всеми необходимыми атрибутами для будущей заявки на бронирование сделки,
                             запрашивает у пользователя информацию об обмениваемой валюте

    :param callback:
    :return: сообщение пользователю с выбором валюты в виде reply-кнопок
    """
    user_id = callback.from_user.id
    if callback.data == 'booking':
        info  = {
            "name" : callback.from_user.first_name,
            "changeable_currency" : None,
            "currency_received" : None,
            "amount" : None,
            "date" : None,
            "time" : None
        }

        bot.send_message(user_id, "Выберите валюту, которую вы хотите обменять:", reply_markup=currency_reply(4))

        bot.register_next_step_handler(callback.message, get_first_currency, info)


def get_first_currency(message: Message, info_dict):
    """
    Шаг 3
    Функция get_first_currency обрабатывает ввод обмениваемой валюты
                                Если ввод успешный: запрашивает у пользователя информацию о валюте, которую он желает получить
                                Если ввод неуспешный: рекурсивно вызывает себя вновь

    :param message: инфомарция об обмениваемой валюте - название валюты
    :param info_dict: словарь со всей текущений инфомарцией по сделке
    :return: сообщение пользователю в виде reply-кнопок для получения информации о валюте, которую он желает получить
    """
    get_changeable_currency = message.text

    if not (get_changeable_currency in ['Рубль', 'Доллар', 'Дирхам', 'Teaher']):
        bot.send_message(message.chat.id, "Выберите валюту, которую вы хотите обменять:", reply_markup=currency_reply(4))

        bot.register_next_step_handler(message, get_first_currency, info_dict)

    else:
        info_dict['changeable_currency'] = get_changeable_currency
        bot.send_message(message.chat.id, "Выберите валюту, на которую вы хотите обменять:", reply_markup=currency_reply(3, get_changeable_currency))

        bot.register_next_step_handler(message, get_second_currency, info_dict)


def get_second_currency(message: Message, info_dict):
    """
    Шаг 4
    Функция get_second_currency обрабатывает ввод валюты, которую пользователь желает получить
                                Если ввод успешный: запрашивает у пользователя информацию о сумме сделки
                                Если ввод неуспешный: рекурсивно вызывает себя вновь
    :param message: инфомарция о желаемой валюте - название валюты
    :param info_dict: словарь со всей текущений инфомарцией по сделке
    :return: сообщение пользователю с запросом суммы сделки
    """
    get_received_currency = message.text

    if not (get_received_currency in ['Рубль', 'Доллар', 'Дирхам', 'Teaher']):
        bot.send_message(message.chat.id, "Выберите валюту, на которую вы хотите обменять:", reply_markup=currency_reply(3, info_dict['changeable_currency']))

        bot.register_next_step_handler(message, get_second_currency, info_dict)

    else:
        info_dict['currency_received'] = get_received_currency
        bot.send_message(message.chat.id,
                         "Отлично, валюты выбраны! На какую сумму Вы желаете произвести обмен:  \n\n\n(Введите целое число без лишних символов и пробелов. Сумма обмена не должна превышать 1 000 000)",
                         reply_markup=types.ReplyKeyboardRemove()
                         )

        bot.register_next_step_handler(message, get_amount_exchange, info_dict)


def get_amount_exchange(message: Message, info_dict):
    """
    Шаг 5
    Функция get_amount_exchange обрабатывает ввод суммы сделки
                                Если ввод успешный: предлагает пользователю выбрать дату встречи
                                Если ввод неуспешный: рекурсивно вызывает себя вновь

    :param message: сумма сделки
    :param info_dict: словарь со всей текущений инфомарцией по сделке
    :return: сообщение пользователю в виде reply-кнопок с датами встречи
    """

    amount_exchange = message.text

    if not (amount_exchange.isdigit() and 0 <= int(amount_exchange) <= 1000000):
        bot.send_message(message.chat.id,
                         "Некорректный ввод! На какую сумму Вы желаете произвести обмен: \n\n\n(Введите целое число без лишних символов и пробелов. Сумма обмена не должна превышать 1 000 000)",
                         reply_markup=types.ReplyKeyboardRemove()
                         )

        bot.register_next_step_handler(message, get_amount_exchange, info_dict)

    else:
        info_dict['amount'] = amount_exchange
        bot.send_message(message.chat.id,
                         "Дело осталось за малым! Выберите день встречи:",
                         reply_markup=create_date_keyboard())

        bot.register_next_step_handler(message, get_date, info_dict)


def get_date(message: Message, info_dict):
    """
    Шаг 6
    Функция get_date обрабатывает введенную пользователем дату
                                Если ввод успешный: предлагает пользователю выбрать время встречи
                                Если ввод неуспешный: рекурсивно вызывает себя вновь

    :param message: дата встречи - строка
    :param info_dict: словарь со всей текущений инфомарцией по сделке
    :return: сообщение пользователю в виде reply-кнопок с временем встречи
    """
    get_date_of_meetings = message.text

    if not check_date_format(get_date_of_meetings):
        bot.send_message(message.chat.id, "Некорректная дата! Попробуйте ещё раз...  \n\n\nВыберите день встречи:", reply_markup=create_date_keyboard())

        bot.register_next_step_handler(message, get_date, info_dict)

    else:
        info_dict['date'] = get_date_of_meetings
        bot.send_message(message.chat.id, "Для оптимизации работы нашего агенства выберите удобное для Вас время", reply_markup=create_time_keyboard())

        bot.register_next_step_handler(message, get_time, info_dict)


def get_time(message: Message, info_dict):
    """
    Шаг 7
    Функция get_time обрабатывает введенное пользователем время встречи
                                Если ввод успешный: предлагает пользователю вывести информацию о бронировании
                                Если ввод неуспешный: рекурсивно вызывает себя вновь

    :param message: время встречи - строка
    :param info_dict: словарь со всей текущений инфомарцией по сделке
    :return: сообщение пользователю в виде reply-кнопки
    """
    try:
        get_time_of_meetings = message.text
        if not check_time_format(get_time_of_meetings):
            bot.send_message(message.chat.id, "Некорректный ввод времени! Попробуйте ещё раз...  \n\n\nВыберите удобное для Вас время встречи:",
                             reply_markup=create_time_keyboard())
            bot.register_next_step_handler(message, get_time, info_dict)
        else:
            info_dict['time'] = get_time_of_meetings
            bot.send_message(message.chat.id,
                             "Успешно!",
                             reply_markup=confirmation())
            bot.register_next_step_handler(message, booking_confirmation, info_dict=info_dict)
            print(info_dict)
    except Exception as e:
        print(f"Error occurred in get_time: {e}")


def booking_confirmation(message: Message, info_dict):
    """
    Шаг 8
    Функция booking_confirmation выводит всю информацию по сделке, включая рассчёт итоговой суммы,
                                 запрашивает подтверждение сделки

    :param message: сообщение пользваотеля "Информация о сделке"
    :param info_dict: словарь со всей текущений инфомарцией по сделке
    :return: сообщение пользователю в виде reply-кнопкок для подтверждения
    """
    try:
        print(info_dict)
        total_amount = exchange_calculator(
                                           info_dict["changeable_currency"],
                                           info_dict["currency_received"],
                                           int(info_dict["amount"])
        )
        message_confirmation = (
            f"{info_dict['changeable_currency']} ({info_dict['amount']}) ⮂ {info_dict['currency_received']} ({total_amount})\n"
            f"Дата встречи назначена на {info_dict['date']} в {info_dict['time']}\n\n\n"
            f"Вы подтверждаете бронирование?")
        bot.send_message(message.chat.id,
                         message_confirmation,
                         reply_markup=create_confirmation())
        bot.register_next_step_handler(message, checking)
    except Exception as e:
        print(f"Error occurred in booking_confirmation: {e}")


def checking(message: Message):
    """
    Шаг 9
    Функция checking проверяет подтверждение сделки
                                    Если пользователь подтверждает: вывод сообщения об успешной брони
                                    Если пользователь не подтверждает: Отмена бронирования и вывож inline-кнопки для новой заявки на сделку

    :param message: сообщение пользователя с согласием или несогласием сделки
    :return: сообщение об успешном или неуспешном бронировании
    """
    verification_of_confirmation = message.text

    if 'Да' in verification_of_confirmation:
        bot.send_message(message.chat.id,
                         "Бронирование подтверждено✔️! До встречи!",
                         reply_markup=types.ReplyKeyboardRemove()
                         )
    else:

        bot.send_message(message.chat.id,
                         "Бронирование отменено❌!",
                         reply_markup=start_inline()
                         )






