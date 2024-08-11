import asyncio
import logging
from datetime import datetime

from aiogram.exceptions import TelegramRetryAfter

from Config.config import ARCHIVE
from DB.DB_utils import request_to_db_multi, get_max_id, update_values_db
from Keyboards.Inline_Builder import build_inline
from Utils.Bot import bot


async def autopost(channel_id, message_id, bot_last_post):
    user_channel = str(channel_id)
    list_of_request = "post_id_archive, button_text, button_link, user_id, b"
    sss = list(request_to_db_multi(list_of_request, 'user_channel', user_channel)[0])
    post_id_archive = sss[0]
    button_text = sss[1]
    button_link = sss[2]
    user_id = sss[3]
    is_button = sss[4]
    post_id = 0

    if is_button == 'yes_button':  # Пост с кнопкой
        try:
            await bot.delete_message(channel_id, bot_last_post)
        except TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after)
        except Exception as ex:
            logging.error(f"[Autopost delete] - {ex}", exc_info=True)

        try:
            message_data = await bot.copy_message(user_channel, ARCHIVE, post_id_archive,
                                                   reply_markup=build_inline(button_text, button_link))
            post_id = message_data.message_id  # id поста в канале юзера

        except TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after)
        except Exception as ex:
            logging.error(f"[Autopost send] - {ex}", exc_info=True)

        # post_id = message_data.message_id  # id поста в канале юзера
        date_time_2 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        list_values_of_DB = f"bot_last_post='{post_id}'," \
                            f"channel_last_post='{message_id}'," \
                            f"date_of_use = '{date_time_2}'"
        id_in_base = get_max_id(user_id)
        update_values_db(list_values_of_DB, id_in_base)

    else:  # Пост без кнопки
        try:
            await bot.delete_message(channel_id, bot_last_post)
        except TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after)
        except Exception as ex:
            logging.error(f"[Autopost delete] - {ex}", exc_info=True)

        try:
            message_data = await bot.copy_message(user_channel, ARCHIVE, post_id_archive)
            post_id = message_data.message_id  # id поста в канале юзера

        except TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after)
        except Exception as ex:
            logging.error(f"[Autopost send] - {ex}", exc_info=True)

        # post_id = message_data.message_id  # id поста в канале юзера
        date_time_2 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        list_values_of_DB = f"bot_last_post='{post_id}'," \
                            f"channel_last_post='{message_id}'," \
                            f"date_of_use = '{date_time_2}'"
        id_in_base = get_max_id(user_id)
        update_values_db(list_values_of_DB, id_in_base)


async def first_post(channel_id):
    user_channel = str(channel_id)
    list_of_request = "post_id_archive, button_text, button_link, user_id, b, bot_last_post"
    sss = list(request_to_db_multi(list_of_request, 'user_channel', user_channel)[0])
    post_id_archive = sss[0]
    button_text = sss[1]
    button_link = sss[2]
    user_id = sss[3]
    is_button = sss[4]
    bot_last_post = sss[5]

    if is_button == 'yes_button':

        try:
            if bot_last_post != 0:
                await bot.delete_message(channel_id, bot_last_post)
        except TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after)
        except Exception as ex:
            logging.error(f"[First post delete] - {ex}", exc_info=True)

        message_data = await bot.copy_message(user_channel, ARCHIVE, post_id_archive,
                                                           reply_markup=build_inline(button_text, button_link))

        post_id = message_data.message_id  # id поста в канале юзера
        date_time_2 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        list_values_of_DB = f"bot_last_post='{post_id}'," \
                            f"channel_last_post='{post_id}'," \
                            f"watch_on='on'," \
                            f"scheduler_on='off'," \
                            f"scheduler_time=NULL," \
                            f"date_of_use = '{date_time_2}'"
        id_in_base = get_max_id(user_id)
        update_values_db(list_values_of_DB, id_in_base)
    else:

        try:
            if bot_last_post != 0:
                await bot.delete_message(channel_id, bot_last_post)
        except TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after)
        except Exception as ex:
            logging.error(f"[First post delete] - {ex}", exc_info=True)

        message_data = await bot.copy_message(user_channel, ARCHIVE, post_id_archive)

        post_id = message_data.message_id  # id поста в канале юзера
        post_id_here = post_id
        date_time_2 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        list_values_of_DB = f"bot_last_post='{post_id_here}'," \
                            f"channel_last_post='{post_id}'," \
                            f"watch_on='on'," \
                            f"scheduler_on='off'," \
                            f"scheduler_time=NULL," \
                            f"date_of_use = '{date_time_2}'"
        id_in_base = get_max_id(user_id)
        update_values_db(list_values_of_DB, id_in_base)
