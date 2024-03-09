from  re import match


def check_date_format(input_string):
    """
    Функция check_date_format проверяет дату на корректный ввод с помощью регулярного выражения

    :param input_string: Строка с датой, введённая пользователем
    :return: Булевое значение - результат проверки
    """
    pattern = r'^\d{1,2}\.\d{1,2}$'
    if match(pattern, input_string):
        return True
    else:
        return False

def check_time_format(input_string):
    """
    Функция check_time_format проверяет время на корректный ввод с помощью регулярного выражения

    :param input_string: Строка с временем, введённая пользователем
    :return: Булевое значение - результат проверки
    """
    pattern = r'^1[1-9]:[0-5][0-9]$|^[2][0]:[0-5][0-9]$'
    if match(pattern, input_string):
        return True
    else:
        return False


def exchange_calculator(currency_1: str, currency_2: str, amount: int) -> float:
    """
    Функция exchange_calculator выполняет расчет обмена валют по текущему курсу.

    :param currency_1: Валюта, которую клиент планирует обменять.
    :param currency_2: Валюта, которую клиент планирует получить.
    :param amount: Сумма обмена в курсе обмениваемой валюты.
    :return: Сумма валюты, которую клиент планирует получить.
    """

    if currency_1 == 'Рубль':
        if currency_2 == 'Доллар':
            total_sum = amount * 0.011019
        elif currency_2 == 'Дирхам':
            total_sum = amount * 0.040469
        else:
            total_sum = amount * 0.349201

    elif currency_1 == 'Доллар':
        if currency_2 == 'Рубль':
            total_sum = amount * 90.75
        elif currency_2 == 'Дирхам':
            total_sum = amount * 3.37
        else:
            total_sum = amount * 31.69

    elif currency_1 == 'Дирхам':
        if currency_2 == 'Рубль':
            total_sum = amount * 24.71
        elif currency_2 == 'Доллар':
            total_sum = amount * 0.272294
        else:
            total_sum = amount * 8.63

    else:
        if currency_2 == 'Рубль':
            total_sum = amount * 2.86
        elif currency_2 == 'Доллар':
            total_sum = amount * 0.031556
        else:
            total_sum = amount * 115889

    return round(total_sum, 2)
