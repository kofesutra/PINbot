import logging
import asyncio
from datetime import datetime
from multiprocessing import Process

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, Text
from aiogram.types import BotCommand
from pyrogram import Client, idle
from pyrogram.handlers import MessageHandler

from Utils.Bot import bot, get_logging
from Defs_Admin.Defs_Mass_Mailing import run_message_mass, get_text_for_mass, check_letter_for_mass
from Defs_Admin.Defs_Send_message_to_user import run_message_to_user, get_user_id_for_letter, get_text_for_letter, \
    check_letter_to_user
from Defs_Admin.Defs_admin import run_db_export, run_ping_bot, run_logs_export
from Defs.Get_Support import get_support
from Utils.Process_Employee import get_employee, check_employee, confirm_remove_employee, remove_employee
from Utils.Process_Payment import start_payment, check_payment
from Utils.Process_Cabinet import get_cabinet, cabinet_buttons
from Utils.Process_Worker import stop_registration
from Defs.Registration import greeting, get_channel, set_channel, check_admins
from Utils.Watcher import get_new_channel_post
from Defs.Defs import set_picture, get_picture, get_text, set_button, get_button_text, \
    get_button_link, check_post, set_text, is_post_ok, get_corrections, on_start, get_getting_post, receive_post, \
    publishing, confirm_date, select_getting_post_0, get_status, status_buttons, get_month, get_day, \
    get_hour, get_minutes, get_check
from Utils.State_Machine import States, StatesAdmin
from Config.config import ADMIN_ID, USERBOTSESSIONNAME, USERBOTAPI, BOTUSERNAME


async def start_pyro():
    get_logging()

    user_bot = Client(name=USERBOTSESSIONNAME, api_id=USERBOTAPI)
    user_bot.add_handler(MessageHandler(get_new_channel_post))

    try:
        await user_bot.start()
        await idle()
        await user_bot.stop()
    except Exception as ex:
        logging.error(f"[Pyrogram start ERROR] - {ex}", exc_info=True)


async def start_bot(bot: Bot):
    await bot.send_message(chat_id=ADMIN_ID, text='Бот запущен')
    date_time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f'{BOTUSERNAME} запущен {date_time_now}')


async def stop_bot(bot: Bot):
    await bot.send_message(chat_id=ADMIN_ID, text='Бот остановлен')
    date_time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f'{BOTUSERNAME} остановлен {date_time_now}')


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Старт"),
    ]
    await bot.set_my_commands(commands)


# Запускаем Aiogram - для всего остального
async def start_aio():
    get_logging()

    # bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.message.register(on_start, Command(commands=['start']))
    dp.message.register(on_start, Text(text='Новый пост'))
    dp.message.register(get_support, Text(text='Техподдержка'))
    dp.message.register(get_cabinet, Text(text='Кабинет'))

    # Админ
    dp.message.register(on_start, Command(commands=['start']))
    # dp.message.register(run_ping_bot, Command(commands=['ping']))
    # dp.message.register(resubscribe_userbot, Command(commands=['resubscribe_userbot']))
    # dp.message.register(on_start_admin, Text(text='Начать заново'))
    dp.message.register(run_db_export, Text(text='База'))
    dp.message.register(run_ping_bot, Text(text='Ping'))
    dp.message.register(run_logs_export, Text(text='Логи'))
    dp.message.register(run_message_to_user, Text(text='Письмо'))
    dp.message.register(run_message_mass, Text(text='Рассылка'))
    # dp.message.register(resubscribe_userbot, Text(text='resubscribe'))

    # Для персонального письма юзеру
    dp.message.register(get_user_id_for_letter, StatesAdmin.user_id_for_letter)
    dp.message.register(get_text_for_letter, StatesAdmin.letter_to_user)
    dp.callback_query.register(check_letter_to_user, StatesAdmin.check_letter, Text(text='yes_right'))
    dp.callback_query.register(check_letter_to_user, StatesAdmin.check_letter, Text(text='no_wrong'))
    dp.callback_query.register(check_letter_to_user, StatesAdmin.check_letter, Text(text='cancel'))

    # Для массовой рассылки
    dp.message.register(get_text_for_mass, StatesAdmin.get_text_for_mass)
    dp.callback_query.register(check_letter_for_mass, StatesAdmin.check_letter_for_mass, Text(text='yes_right'))
    dp.callback_query.register(check_letter_for_mass, StatesAdmin.check_letter_for_mass, Text(text='no_wrong'))
    dp.callback_query.register(check_letter_for_mass, StatesAdmin.check_letter_for_mass, Text(text='cancel'))

    # Основные
    dp.callback_query.register(select_getting_post_0, States.select_getting_post_0, Text(text='next'))
    dp.callback_query.register(select_getting_post_0, States.select_getting_post_0, Text(text='registration_ok'))
    dp.callback_query.register(get_getting_post, States.get_getting_post, F.data == 'send_ready')
    dp.callback_query.register(get_getting_post, States.get_getting_post, F.data == 'make_here')
    dp.message.register(receive_post, States.receive_post)
    dp.callback_query.register(set_picture, States.set_picture, F.data == 'yes_picture')
    dp.callback_query.register(set_picture, States.set_picture, F.data == 'no_picture')
    dp.message.register(get_picture, States.get_picture)
    dp.callback_query.register(set_text, States.set_text, F.data == 'yes_text')
    dp.callback_query.register(set_text, States.set_text, F.data == 'no_text')
    dp.message.register(get_text, States.get_text)
    dp.callback_query.register(set_button, States.set_button, F.data == 'yes_button')
    dp.callback_query.register(set_button, States.set_button, F.data == 'no_button')
    dp.message.register(get_button_text, States.set_button_text)
    dp.message.register(get_button_link, States.set_button_link)
    dp.callback_query.register(check_post, States.check, F.data == 'yes_check')
    dp.callback_query.register(is_post_ok, States.ok, F.data == 'yes_post')

    dp.callback_query.register(is_post_ok, States.ok, F.data == 'no_post')
    dp.callback_query.register(get_corrections, States.corrections, F.data == 'change_picture')
    dp.callback_query.register(get_corrections, States.corrections, F.data == 'change_text')
    dp.callback_query.register(get_corrections, States.corrections, F.data == 'change_button')
    dp.callback_query.register(publishing, States.publishing, F.data == 'now')
    dp.callback_query.register(publishing, States.publishing, F.data == 'later')
    dp.callback_query.register(confirm_date, States.confirm_date, F.data == 'right')
    dp.callback_query.register(confirm_date, States.confirm_date, F.data == 'wrong')



    # Регистрация
    dp.message.register(greeting, States.greeting)
    dp.message.register(get_channel, States.get_channel)
    dp.callback_query.register(set_channel, States.set_channel, F.data == 'right')
    dp.callback_query.register(set_channel, States.set_channel, F.data == 'wrong')
    dp.callback_query.register(set_channel, States.set_channel, F.data == 'back')
    dp.callback_query.register(check_admins, States.check_admins, F.data == 'done')
    dp.callback_query.register(check_admins, States.check_admins, F.data == 'how')
    # dp.observers

    dp.message.register(get_status, Text(text='Статус'))

    # Изменить пост-время-отключить
    dp.callback_query.register(status_buttons, States.status_buttons, F.data == 'modify')
    dp.callback_query.register(status_buttons, States.status_buttons, F.data == 'change_time')
    dp.callback_query.register(status_buttons, States.status_buttons, F.data == 'yes_change_time')
    dp.callback_query.register(status_buttons, States.status_buttons, F.data == 'switch_off')
    dp.callback_query.register(status_buttons, States.status_buttons, F.data == 'status_cancel')

    # Отложенный запуск
    dp.callback_query.register(get_month, States.get_month)
    dp.callback_query.register(get_day, States.get_day)
    dp.callback_query.register(get_hour, States.get_hour)
    dp.callback_query.register(get_minutes, States.get_minutes)
    dp.callback_query.register(get_check, States.get_check)

    # Кабинет
    dp.callback_query.register(cabinet_buttons, F.data == 'invitelink')
    dp.callback_query.register(cabinet_buttons, F.data == 'statistics')
    dp.callback_query.register(cabinet_buttons, F.data == 'download_statistics')
    dp.callback_query.register(cabinet_buttons, F.data == 'payment')
    dp.callback_query.register(cabinet_buttons, F.data == 'tarifs')
    dp.callback_query.register(cabinet_buttons, F.data == 'set_employee')
    dp.callback_query.register(cabinet_buttons, F.data == 'remove_employee')
    dp.callback_query.register(cabinet_buttons, F.data == 'howto_employee')

    # Оплата
    dp.callback_query.register(start_payment, States.payment, F.data == 'month_1')
    dp.callback_query.register(start_payment, States.payment, F.data == 'month_3')
    dp.callback_query.register(start_payment, States.payment, F.data == 'month_6')
    dp.callback_query.register(start_payment, States.payment, F.data == 'month_12')
    dp.callback_query.register(check_payment, States.check_payment, F.data == 'check_payment')

    # Работник
    dp.callback_query.register(get_employee, States.get_employee, F.data == 'set_employee')
    dp.callback_query.register(check_employee, States.check_employee, F.data == 'yes')
    dp.callback_query.register(check_employee, States.check_employee, F.data == 'no')

    dp.message.register(get_employee, States.get_employee)

    dp.callback_query.register(remove_employee, States.remove_employee, F.data == 'remove_employee')
    dp.callback_query.register(confirm_remove_employee, States.confirm_remove_employee, F.data == '1')
    dp.callback_query.register(confirm_remove_employee, States.confirm_remove_employee, F.data == '2')
    dp.callback_query.register(confirm_remove_employee, States.confirm_remove_employee, F.data == '3')
    dp.callback_query.register(confirm_remove_employee, States.confirm_remove_employee, F.data == '4')
    dp.callback_query.register(confirm_remove_employee, States.confirm_remove_employee, F.data == '5')

    dp.message.register(stop_registration, States.stop)

    await set_commands(bot)  # Установка команд бота

    try:
        logging.error(f'OK - - - - - - - - - - - - - - - - - - - - OK\n\n'
                      f'[{BOTUSERNAME} started successful]: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', exc_info=True)
        await dp.start_polling(bot)
    except Exception as ex:
        logging.error(f"[Aiogram start ERROR] - {ex}", exc_info=True)
    finally:
        await bot.session.close()


def run_pyro():
    asyncio.run(start_pyro())


def run_aio():
    asyncio.run(start_aio())


if __name__ == '__main__':
    # with contextlib.suppress(KeyboardInterrupt, SystemExit):
    #     asyncio.run(start_aio())

    starting = [run_pyro, run_aio]

    processes = []

    for start in starting:
        process = Process(target=start)
        processes.append(process)
        process.start()

    for process in processes:
        process.join()
