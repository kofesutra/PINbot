import datetime
import logging
from aiogram import Bot
from Config.config import BOT_TOKEN, LOGSTATE, LOGNAME

bot = Bot(token=BOT_TOKEN)


def get_logging():
    if LOGSTATE == 'INFO':
        return logging.basicConfig(level=logging.INFO,  # WARNING
                        # filename=LOGNAME,
                        format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
                        datefmt='%H:%M:%S',)
    elif LOGSTATE == 'WARNING':
        return logging.basicConfig(level=logging.WARNING,  # WARNING
                        filename=LOGNAME,
                        format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
                        datefmt='%H:%M:%S',)


def get_future_date(date_time, days_plus):
    end_date = (date_time + datetime.timedelta(days=days_plus)).strftime("%Y-%m-%d 23:59:59")  # Получаем будущую дату
    print(f'Конец: {end_date}')
    return end_date
