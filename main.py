from loader import bot
import handlers  # noqa
from utils.set_bot_commands import set_default_commands
# import pkg_resources


# def create_requirements_txt():
#     # Получаем список всех установленных зависимостей
#     installed_packages = [pkg.key for pkg in pkg_resources.working_set]
#
#     # Создаем файл requirements.txt и записываем зависимости в него
#     with open('requirements.txt', 'w') as req_file:
#         for package in installed_packages:
#             req_file.write(package + '\n')


if __name__ == "__main__":


    # create_requirements_txt()

    set_default_commands(bot)
    bot.infinity_polling()
