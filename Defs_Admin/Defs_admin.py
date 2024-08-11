import logging
import os
from _csv import writer
from datetime import datetime
from aiogram.types import FSInputFile, CallbackQuery
from Config.config import LIST_SUBJECTS, CSV_FILE, LOGNAME
from DB.DB_utils import db_export
from Keyboards.Reply_Admin import r_kb_admin
from Utils.Bot import bot


async def on_start_admin(user):
    await bot.send_message(user, f'Преведт, админ {user}!', reply_markup=r_kb_admin)


async def run_logs_export(call: CallbackQuery):
    admin_here = call.from_user.id

    await bot.send_message(admin_here, 'Экспорт логов бота')

    try:
        await bot.send_document(admin_here, FSInputFile(f"{LOGNAME}"))
    except Exception as ex:
        logging.error(f'Отсутствует файл логов {ex}')
        await bot.send_message(admin_here, f'Отсутствует файл логов')


async def run_db_export(call: CallbackQuery):
    admin_here = call.from_user.id

    await bot.send_message(admin_here, 'Экспорт полной БД')
    zzz = db_export()

    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_time_2 = str(date_time)
    csv_here = CSV_FILE + date_time_2 + '.csv'

    with open(csv_here, mode='a', encoding='utf-8', newline='') as file:
        writer_object = writer(file)
        writer_object.writerow(LIST_SUBJECTS)
        writer_object.writerows(zzz)
        file.close()

    await bot.send_document(admin_here, FSInputFile(f"{csv_here}"))

    os.remove(csv_here)


async def run_ping_bot(call: CallbackQuery):
    admin_here = call.from_user.id
    await bot.send_message(admin_here, 'Я в норме! Я не сплю! )))')
