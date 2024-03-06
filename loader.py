import telebot
from telebot.storage import StateMemoryStorage
from config_data import config


storage = StateMemoryStorage()
print(storage)
bot = telebot.TeleBot(token=config.BOT_TOKEN, state_storage=storage)

