from loader import bot
import handlers  # noqa
from utils.set_bot_commands import set_default_commands
from database.core import create_database

if __name__ == "__main__":
    create_database()
    set_default_commands(bot)
    bot.infinity_polling()
