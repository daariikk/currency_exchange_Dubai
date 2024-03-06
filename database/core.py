import sqlite3

def create_database():
    """
        Функция, которая создаёт таблицу для хранения истории действий пользователей
        Поля таблицы:
        id - первичный ключ, создаётся по умолчанию
        user_name - имя пользователя
        command - название команды
        """
    conn = sqlite3.connect('CurrencyChangerDubaiBot.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS commands (id int auto increment primary key, user_name varchar(50), command varchar(200))')

    conn.commit()
    cur.close()
    conn.close()

def insert_command(name: str, command:str):
    """Функция, которая добавляет запись в таблицу"""
    conn = sqlite3.connect('CurrencyChangerDubaiBot.sql')
    cur = conn.cursor()

    cur.execute("INSERT INTO commands (user_name, command) VALUES (?, ?)", (name, command))



    conn.commit()
    cur.close()
    conn.close()

def check_database() -> str:
    """Функция, которая выводит последние 10 запросов"""
    conn = sqlite3.connect('nailmakerbar.sql')
    cur = conn.cursor()

    cur.execute("SELECT * FROM commands")
    history_commands = cur.fetchall()

    cur.close()
    conn.close()

    HISTORY = 'Имя пользователя | Команда\n'

    if len(history_commands) > 10:
        for item in history_commands[len(history_commands) - 10:]:
            HISTORY += f'{item[1]}{"  " * (16-len(item[1]))} | {item[2]}\n'
    else:
        for item in history_commands:
            HISTORY += f'{item[1]}{"  " * (16-len(item[1]))} | {item[2]}\n'

    return HISTORY