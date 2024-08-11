from collections import deque

from pyrogram import Client
from pyrogram.types import Message
from Config.config import ARCHIVE
from DB.DB_utils import request_to_db_multi
from Utils.Autopost import autopost

messages_list = deque()  # Создаём очередь
is_processing_allow = True  # Флажок доступности обработки


# Юзербот обладает минимальной функциональностью чтобы быстро загружать в очередь
async def get_new_channel_post(client: Client, message: Message):
    message_id = message.id
    channel_id = message.chat.id
    channel_type = message.chat.type

    # Если тип канала - канал (а не чат или робот) и он не Архив
    if str(channel_type) == 'ChatType.CHANNEL' and channel_id != ARCHIVE:
        if message_id in messages_list:  # Перепроверка чтобы не подгружать дубликаты
            return

        mes_and_channel = [channel_id, message_id]  # Получаем ID канала и сообщения
        messages_list.append(mes_and_channel)  # Добавляем в очередь
        await processing_messages()  # Вызываем обработчик


# Обработчик выполняет процедуру для каждого элемента очереди
async def processing_messages():
    global is_processing_allow
    if is_processing_allow == True and len(messages_list) != 0:  # Если доступен и очередь не пустая
        is_processing_allow = False  # Отключаем вызов обработчика снаружи на время работы

        while len(messages_list) != 0:  # Выполняется пока очередь не опустеет (она увеличивается динамически)
            channel_id_here = messages_list[0][0]
            message_id_here = messages_list[0][1]

            # Запрос в базу
            list_of_request = "id, bot_last_post, watch_on, user_channel_allowed, user_bot_allowed, post_id_archive, user_id, button_text, button_link, b"
            sss = list(request_to_db_multi(list_of_request, 'user_channel', channel_id_here)[0])
            id_here = sss[0]
            bot_last_post = sss[1]
            watch_on = sss[2]
            is_bot_allowed = sss[3]
            is_userbot_allowed = sss[4]

            # Если запись в базе есть и наблюдение включено и бот с юзерботом имеют доступ к каналу
            # и последний пост бота раньше, чем последнее сообщение в канале
            if id_here is not None and watch_on == 'on' and is_bot_allowed == 'yes' and is_userbot_allowed == 'yes' and bot_last_post < message_id_here:

                await autopost(channel_id_here, message_id_here, bot_last_post)
                del messages_list[0]
            else:
                del messages_list[0]

        is_processing_allow = True  # Если очередь опустела переключаем флажок доступности
