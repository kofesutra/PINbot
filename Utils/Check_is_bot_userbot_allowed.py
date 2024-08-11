import asyncio
import logging

from aiogram import Bot
from pyrogram import Client

from Config.config import BOTID, USERBOTID, BOTUSERNAME, ADMIN_ID, USERBOTUSERNAME, LOGNAME, USERBOTSESSIONNAME, \
    USERBOTAPI, USERBOTSESSIONNAMECOPY, BOT_TOKEN
from DB.DB_utils import update_values_db, get_max_id_two, request_to_db_single_two
from Utils.Bot import get_logging


async def is_bot_and_userbot_allowed(channel_here):
    get_logging()

    bot = Bot(token=BOT_TOKEN)
    is_bot = ''
    is_userbot = ''
    try:
        is_bot_allowed = await bot.get_chat_member(channel_here, BOTID)
        status = is_bot_allowed.status

        if status == 'administrator':
            list_values_of_DB = f"user_channel_allowed='yes'"
            condition = get_max_id_two('user_channel', channel_here)
            update_values_db(list_values_of_DB, condition)
            is_bot = 'ok'
        else:
            zzz = request_to_db_single_two('user_id', 'user_channel', channel_here)
            await bot.send_message(zzz, f'🔘 Внимание, дорогой пользователь! Добавь {BOTUSERNAME} в администраторы канала, иначе я не смогу работать!')
            list_values_of_DB = f"user_channel_allowed='no'"
            condition = get_max_id_two('user_channel', channel_here)
            update_values_db(list_values_of_DB, condition)
            is_bot = 'not_ok'
            await bot.send_message(ADMIN_ID, f'АХТУНГ! У нас проблемы с ботом {BOTUSERNAME} в канале {channel_here}.\n'
                                             f'{BOTUSERNAME} не является администратором')

    except Exception as ex:
        logging.error(f"[Проверка доступа бота к каналу - ошибка] - {ex}", exc_info=True)
        await bot.send_message(ADMIN_ID, f'АХТУНГ! У нас проблемы с ботом {BOTUSERNAME} в канале {channel_here}.\n'
                                         f'[Проверка доступа бота к каналу - ошибка] - {ex}')

    try:
        is_userbot_allowed = await bot.get_chat_member(channel_here, USERBOTID)
        status_userbot = is_userbot_allowed.status

        if status_userbot == 'member' or status_userbot == 'administrator':
            list_values_of_DB = f"user_bot_allowed='yes'"
            condition = get_max_id_two('user_channel', channel_here)
            update_values_db(list_values_of_DB, condition)
            is_userbot = 'ok'
        else:
            if is_bot == 'ok':
                if status_userbot == 'left':
                    ChatInviteLink = await bot.create_chat_invite_link(channel_here)
                    await bot.send_message(USERBOTID, ChatInviteLink.invite_link)
                    await asyncio.sleep(5)

                    user_bot_here = Client(name=USERBOTSESSIONNAMECOPY, api_id=USERBOTAPI)
                    try:
                        if await user_bot_here.start():
                            await user_bot_here.join_chat(ChatInviteLink.invite_link)
                        await user_bot_here.stop()
                        await asyncio.sleep(5)
                    except Exception as ex:
                        logging.error(f"[Автодобавление юзербота - ошибка] - {ex}", exc_info=True)
                        await bot.send_message(ADMIN_ID,
                                               f'АХТУНГ! У нас проблемы с ботом {USERBOTUSERNAME} в канале {channel_here}.\n'
                                               f'[Автодобавление юзербота - ошибка] - {ex}')

                    is_userbot_allowed = await bot.get_chat_member(channel_here, USERBOTID)
                    status = is_userbot_allowed.status

                    if status == 'member' or status == 'administrator':
                        list_values_of_DB = f"user_bot_allowed='yes'"
                        condition = get_max_id_two('user_channel', channel_here)
                        update_values_db(list_values_of_DB, condition)
                        is_userbot = 'ok'
                    else:
                        list_values_of_DB = f"user_bot_allowed='no'"
                        condition = get_max_id_two('user_channel', channel_here)
                        update_values_db(list_values_of_DB, condition)
                        is_userbot = 'not_ok'
                        zzz = request_to_db_single_two('user_id', 'user_channel', channel_here)
                        await bot.send_message(zzz, f'🔘 Внимание, дорогой пользователь! Добавь {USERBOTUSERNAME} в подписчики канала, иначе я не смогу работать!')
                        await bot.send_message(ADMIN_ID, f'АХТУНГ! У нас проблемы с юзерботом {USERBOTUSERNAME} в канале {channel_here}.\n'
                                                         f'{USERBOTUSERNAME} не добавляется в подписчики автоматически')

                elif status_userbot == 'kicked':
                    zzz = request_to_db_single_two('user_id', 'user_channel', channel_here)
                    await bot.send_message(zzz,
                                           f'🔘 Внимание, дорогой пользователь! Разблокируй и добавь {USERBOTUSERNAME} в подписчики канала, иначе я не смогу работать!')
                    await bot.send_message(ADMIN_ID, f'АХТУНГ! У нас проблемы с юзерботом {USERBOTUSERNAME} в канале {channel_here}.\n'
                                                     f'{USERBOTUSERNAME} блокирован в канале и не добавляется в подписчики автоматически')
                else:
                    zzz = request_to_db_single_two('user_id', 'user_channel', channel_here)
                    await bot.send_message(zzz,
                                           f'🔘 Дорогой пользователь! Разблокируй и добавь {USERBOTUSERNAME} в подписчики канала, иначе я не смогу работать!')
                    await bot.send_message(ADMIN_ID, f'АХТУНГ! У нас проблемы с юзерботом {USERBOTUSERNAME} в канале {channel_here}.\n'
                                                     f'По неизвестной ошибке {USERBOTUSERNAME} не добавляется в подписчики автоматически')

    except Exception as ex:
        logging.error(f"[Проверка доступа юзербота к каналу - ошибка] - {ex}", exc_info=True)
        await bot.send_message(ADMIN_ID,
                               f'АХТУНГ! У нас проблемы с юзерботом {USERBOTUSERNAME} в канале {channel_here}.\n'
                               f'[Проверка доступа юзербота к каналу - ошибка] - {ex}')

    if is_bot == 'ok' and is_userbot == 'ok':
        return True
    else:
        return False
