import asyncio
import calendar
import logging
import re
from datetime import datetime

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from pyrogram.errors import FloodWait
from DB.DB_utils import get_max_id, update_values_db, request_to_db_multi, \
    request_to_db_single_two, add_all_to_db, update_values_db_two
from Keyboards.Inline import i_kb_1, i_kb_2, i_kb_3, i_kb_4, i_kb_5, i_kb_6, i_kb_7, i_kb_8, i_kb_9, i_kb_14, i_kb_15
from Keyboards.Inline_Builder import build_inline
from Keyboards.Inline_Date_Time import get_keyboard_year, i_month, get_month_number, get_keyboard_days, \
    get_keyboard_hour, get_keyboard_minutes
from Keyboards.Reply import r_kb_2, r_kb_3
from Utils.Autopost import first_post
from Utils.Bot import bot, get_future_date
from Utils.CallBackQueryAnswer import cbqa
from Utils.Check_is_bot_userbot_allowed import is_bot_and_userbot_allowed
from Defs_Admin.Defs_admin import on_start_admin
from Utils.Process_Deeplinks import process_deeplinks
from Defs.Registration import greeting
from Utils.Sched import run_scheduler, stop_scheduler, stop_scheduler_2
from Utils.State_Machine import States, StatesAdmin
from Config.config import ARCHIVE, NAME_FOR_BASE, LIST_ADMINS, LISTOFUSERSTATUS, LISTOFUSERPAY


async def on_start(message: Message, state: FSMContext, bot: Bot):
    await state.clear()
    user_id_here = message.from_user.id

    # Если вошёл админ, то показываем другой интерфейс
    if user_id_here in LIST_ADMINS:
        await state.set_state(StatesAdmin.admin)
        await on_start_admin(user_id_here)

    else:
        await state.update_data(user_id=user_id_here)
        username_here = message.from_user.username
        await state.update_data(username=username_here)
        first_name_here = message.from_user.first_name
        await state.update_data(first_name=first_name_here)
        last_name_here = message.from_user.last_name
        await state.update_data(last_name=last_name_here)
        await state.update_data(date=message.date)
        await state.update_data(which_bot=NAME_FOR_BASE)
        await state.update_data(worker='none')  # Для фильтрации работника

        # Проверяем есть ли юзер в базе
        if get_max_id(user_id_here) is not None:
            # Узнаём не является ли юзер работником
            list_of_request = "user_status, employee_of"
            sss = list(request_to_db_multi(list_of_request, 'user_id', user_id_here)[0])
            user_status = sss[0]
            employee_of = sss[1]

            # Если работник
            if user_status == 'employee':
                list_of_request = "reg_done, user_channel"
                sss = list(request_to_db_multi(list_of_request, 'user_id', employee_of)[0])
                reg_done = 'yes'
                work_channel = sss[1]  # Получаем id канала, в котором будет вестись работа
                work_user_for_base = employee_of  # И в строку какого юзера (владельца) будем вносить изменения
                await state.update_data(work_user_for_base=work_user_for_base)
                await state.update_data(work_channel=work_channel)
                date_time_2 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                list_values_of_DB = f"date_of_use = '{date_time_2}', user_bot_session = 'allowed'"
                data = await state.get_data()
                update_values_db_two(list_values_of_DB, 'user_id', user_id_here)

            else:  # Юзер не является работником
                list_of_request = "user_channel, reg_done, user_status"
                sss = list(request_to_db_multi(list_of_request, 'user_id', user_id_here)[0])
                user_channel = sss[0]
                reg_done = sss[1]
                user_status = sss[2]

                work_channel = user_channel  # Получаем id канала, в котором будет вестись работа
                work_user_for_base = user_id_here  # И в строку какого юзера (владельца) будем вносить изменения
                await state.update_data(work_user_for_base=work_user_for_base)
                await state.update_data(work_channel=work_channel)

            if reg_done != 'yes':  # Если регистрация не была завершена, то удаляем сведения о канале и начинаем заново
                data = await state.get_data()
                id_in_base = get_max_id(data['user_id'])
                list_values_of_DB = f"user_channel = '-12345', user_bot_session = 'allowed'"
                update_values_db(list_values_of_DB, id_in_base)

                await state.set_state(States.greeting)
                await greeting(message, state, bot)

            else:
                if work_channel != -12345:
                    await state.update_data(user_channel=work_channel)
                    date_time_2 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    if user_status in LISTOFUSERSTATUS:
                        # Проверяем есть ли доступ к каналу у бота и юзербота
                        if await is_bot_and_userbot_allowed(work_channel):
                            list_values_of_DB = f"date_of_use = '{date_time_2}', user_bot_session = 'allowed'"
                            data = await state.get_data()
                            update_values_db_two(list_values_of_DB, 'user_id', user_id_here)

                            await state.set_state(States.select_getting_post)
                            await select_getting_post(message, state, bot)

                    else:
                        await message.answer('🟠 У Вас нет доступа к боту, обратитесь в техподдержку, пожалуйста!\n'
                                             'Причина: закончился пробный или оплаченный период.',
                                             reply_markup=r_kb_2)
                else:
                    await state.set_state(States.greeting)
                    await greeting(message, state, bot)

        else:  # Юзер в базе отсутствует
            # Обработка DeepLinks
            await process_deeplinks(message.text, state, bot)

            data = await state.get_data()
            if data['user_id'] != 88888888:  # Сделано для остановки регистрации stop_registration
                if data['worker'] == 'worker':  # Если регистрация работника
                    await state.set_state(States.select_getting_post)
                    await select_getting_post(message, state, bot)
                else:
                    date_time = datetime.now()
                    date_time_2 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    date_of_end = get_future_date(date_time, 7)
                    list_subjects_of_DB = "user_id, username, first_name, last_name, date_of_start, date_of_use, which_bot, is_payed, come_from, date_of_end, user_status"
                    list_data_of_DB = f"{data['user_id']}, '{data['username']}', '{data['first_name']}', '{data['last_name']}', " \
                                      f"'{date_time_2}', '{date_time_2}', '{data['which_bot']}', 'trial', '{data['come_from']}', '{date_of_end}', 'trial'"
                    add_all_to_db(list_subjects_of_DB, list_data_of_DB)
                    await state.set_state(States.greeting)
                    await greeting(message, state, bot)


async def select_getting_post(message: Message, state: FSMContext, bot: Bot):
    user_id_here = message.from_user.id
    await message.answer("🔘 Давай займёмся твоим постом.", reply_markup=r_kb_2)
    await message.answer("Ты хочешь прислать готовый пост или оформить его здесь поэтапно?", reply_markup=i_kb_7)
    await state.update_data(corrections='no')
    await state.update_data(modify_post='no')
    await state.set_state(States.get_getting_post)
    try:
        data = await state.get_data()
        work_channel = data['work_channel']
        stop_scheduler(user_id_here, work_channel)
    except Exception as ex:
        logging.error(f"[New post deleting scheduler] - {ex}", exc_info=True)


# Только для перехода после регистрации
async def select_getting_post_0(call: CallbackQuery, state: FSMContext, bot: Bot):
    button = call.data
    if button == 'next' or button == 'registration_ok':
        await bot.send_message(call.message.chat.id, "🔘 Давай займёмся твоим постом.", reply_markup=r_kb_2)
        await bot.send_message(call.message.chat.id, "Ты хочешь прислать готовый пост или оформить его здесь поэтапно?",
                               reply_markup=i_kb_7)
        await state.update_data(corrections='no')
        await state.update_data(modify_post='no')
        await state.set_state(States.get_getting_post)


async def get_getting_post(call: CallbackQuery, state: FSMContext, bot: Bot):
    await cbqa(call, bot)
    activ = call.data
    if activ == 'send_ready':
        await bot.send_message(call.message.chat.id, "🔘 Пришли готовый пост\nЯ работаю только с текстом и картинками",
                               reply_markup=r_kb_2)
        await state.set_state(States.receive_post)
    elif activ == 'make_here':
        await state.set_state(States.run_set_post)
        await bot.send_message(call.message.chat.id, "🔘 Давай соберём твой пост", reply_markup=r_kb_2)
        await bot.send_message(call.message.chat.id, "В посте нужна картинка?", reply_markup=i_kb_1)
        await state.set_state(States.set_picture)


async def receive_post(message: Message, state: FSMContext, bot: Bot):
    if message.text or message.photo:
        chat_id = message.chat.id
        picture = message.photo
        post_text = message.text
        caption_text = message.caption
        entities = message.entities
        capt_entities = message.caption_entities

        if post_text is not None:
            await state.update_data(text='yes_text')
            await state.update_data(post_text=post_text)
            if entities is not None:
                await state.update_data(entities=entities)

            else:
                await state.update_data(entities='none')
        elif caption_text is not None:
            await state.update_data(text='yes_text')
            await state.update_data(post_text=caption_text)
            if capt_entities is not None:
                await state.update_data(entities=capt_entities)

            else:
                await state.update_data(entities='none')
        else:
            await state.update_data(text='none')

        if picture is not None:
            await state.update_data(picture='yes_picture')
            picture_id = message.photo[0].file_id
            await state.update_data(picture_id=picture_id)
        else:
            await state.update_data(picture='no_picture')

        await bot.send_message(chat_id, '🔘 Отлично! Я запомнил твой пост.')

        # TODO Запись всех переменных в базу
        data = await state.get_data()
        if picture is not None:
            list_values_of_DB = f"p='{data['picture']}'," \
                                f"t='{data['text']}'," \
                                f"post_text='{data['post_text']}'," \
                                f"picture_id='{data['picture_id']}'"

        else:
            list_values_of_DB = f"p='{data['picture']}'," \
                                f"t='{data['text']}'," \
                                f"post_text='{data['post_text']}'"

        update_values_db_two(list_values_of_DB, 'user_channel', data['work_channel'])

        await message.answer('🔘 Нужна инлайн-кнопка?', reply_markup=i_kb_2)
        await state.set_state(States.set_button)
    else:
        await message.answer(
            '🟠 Я работаю только с текстом и картинками\nбез видео, гиф, аудио  или медиагрупп\nПришли готовый пост',
            reply_markup=i_kb_2)


async def set_picture(call: CallbackQuery, state: FSMContext, bot: Bot):
    await cbqa(call, bot)
    activ = call.data
    if activ == 'yes_picture':
        await state.update_data(picture='yes_picture')
        await bot.send_message(call.message.chat.id, "🔘 Пришли мне картинку без подписи")
        await state.set_state(States.get_picture)

    elif activ == 'no_picture':
        await state.update_data(picture='no_picture')
        await bot.send_message(call.message.chat.id, '🔘 В посте нужен текст?', reply_markup=i_kb_4)
        await state.set_state(States.set_text)


async def get_picture(message: Message, state: FSMContext):
    if message.photo:
        picture_id = message.photo[0].file_id
        await state.update_data(picture_id=picture_id)
        list_values_of_DB = f"picture_id='{picture_id}'"
        data = await state.get_data()
        update_values_db_two(list_values_of_DB, 'user_channel', data['work_channel'])

        data = await state.get_data()
        if data['corrections'] == 'yes':
            await message.answer('🔘 Давай проверим пост', reply_markup=i_kb_3)
            await state.set_state(States.check)
        else:
            await message.answer('🔘 В посте нужен текст?', reply_markup=i_kb_4)
            await state.set_state(States.set_text)
    else:
        await message.answer("🟠 Какая-то ошибка.\nПришли мне картинку без подписи")


async def set_text(call: CallbackQuery, state: FSMContext, bot: Bot):
    await cbqa(call, bot)
    activ = call.data
    if activ == 'yes_text':
        await state.update_data(text='yes_text')
        await bot.send_message(call.message.chat.id, "🔘 Пришли мне текст поста")
        await state.set_state(States.get_text)

    elif activ == 'no_text':
        await state.update_data(text='no_text')
        await bot.send_message(call.message.chat.id, '🔘 Нужна инлайн-кнопка?', reply_markup=i_kb_2)
        await state.set_state(States.set_button)


async def get_text(message: Message, state: FSMContext):
    if message.text:
        post_text = message.text
        entities = message.entities
        await message.answer(f'{post_text}', entities=entities, reply_markup=r_kb_2)
        await state.update_data(post_text=post_text)
        await state.update_data(entities=entities)

        data = await state.get_data()
        if data['corrections'] == 'yes':
            await message.answer('🔘 Давай проверим пост', reply_markup=i_kb_3)
            await state.set_state(States.check)
        else:
            await message.answer('🔘 Нужна инлайн-кнопка?', reply_markup=i_kb_2)
            await state.set_state(States.set_button)

    else:
        await message.answer("🟠 Какая-то ошибка.\nПришли мне текст поста")


async def set_button(call: CallbackQuery, state: FSMContext, bot: Bot):
    await cbqa(call, bot)
    activ = call.data
    if activ == 'yes_button':
        await state.update_data(button='yes_button')
        await bot.send_message(call.message.chat.id, '🔘 Пришли текст на кнопке')
        await state.set_state(States.set_button_text)
    elif activ == 'no_button':
        await state.update_data(button='no_button')
        await state.update_data(button_text='none')
        await state.update_data(button_link='none')
        await bot.send_message(call.message.chat.id, '🔘 Давай проверим пост', reply_markup=i_kb_3)
        await state.set_state(States.check)


async def get_button_text(message: Message, state: FSMContext):
    if message.text:
        button_text = message.text
        await message.answer(f'🔘 Твой текст кнопки:\n\n{button_text}')
        await state.update_data(button_text=button_text)
        await message.answer('🔘 Пришли ссылку кнопки')
        await state.set_state(States.set_button_link)
    else:
        await message.answer("🟠 Какая-то ошибка.\nПришли текст на кнопке")


async def get_button_link(message: Message, state: FSMContext):
    if message.text:
        button_link = message.text
        # Валидация ссылки (простенькая)
        pattern = "^[0-9A-z.]+.[0-9A-z.]+.[a-z]+$"
        validation = re.match(pattern, button_link)
        if validation:
            await message.answer(f'🔘 Ссылка для кнопки:\n\n'
                                 f'{button_link}')
            await state.update_data(button_link=button_link)
            await message.answer('🔘 Давай проверим пост', reply_markup=i_kb_3)
            await state.set_state(States.check)
        else:
            await message.answer("🟠 Какая-то ошибка в ссылке.\nПроверь и пришли ссылку кнопки")
    else:
        await message.answer("🟠 Какая-то ошибка.\nПришли ссылку кнопки")


async def check_post(call: CallbackQuery, state: FSMContext, bot: Bot):
    await cbqa(call, bot)
    activ = call.data
    if activ == 'yes_check':
        picture_id = 'none'
        post_text = 'none'
        button_text = 'none'
        button_link = 'none'

        data = await state.get_data()
        user_id_here = call.from_user.id
        P = data['picture']
        T = data['text']
        B = data['button']

        message_data = ''
        if P == 'yes_picture' and T == 'yes_text' and B == 'yes_button':
            picture_id = data['picture_id']
            post_text = data['post_text']
            button_text = data['button_text']
            button_link = data['button_link']
            try:
                await bot.send_photo(user_id_here, photo=picture_id, caption=post_text,
                                     caption_entities=data['entities'],
                                     reply_markup=build_inline(button_text, button_link))
                message_data = await bot.send_photo(ARCHIVE, photo=picture_id, caption=post_text,
                                                    caption_entities=data['entities'],
                                                    reply_markup=build_inline(button_text, button_link))

                await state.set_state(States.ok)

            except FloodWait as e:
                await asyncio.sleep(e.value)
            except Exception as ex:
                logging.error(f'Check post {ex}', exc_info=True)
                await bot.send_message(call.message.chat.id,
                                       '🟠 Обнаружена ошибка в CHECK_POST модуле\nНачните снова', reply_markup=r_kb_2)
                return

        elif P == 'yes_picture' and T == 'no_text' and B == 'yes_button':
            picture_id = data['picture_id']
            button_text = data['button_text']
            button_link = data['button_link']
            try:
                await bot.send_photo(user_id_here, photo=picture_id,
                                     reply_markup=build_inline(button_text, button_link))
                message_data = await bot.send_photo(ARCHIVE, photo=picture_id,
                                                    reply_markup=build_inline(button_text, button_link))
                await state.set_state(States.ok)
            except FloodWait as e:
                await asyncio.sleep(e.value)
            except Exception as ex:
                logging.error(f'Check post {ex}', exc_info=True)
                await bot.send_message(call.message.chat.id,
                                       '🟠 Обнаружена ошибка в CHECK_POST модуле\nНачните снова', reply_markup=r_kb_2)
                return

        elif P == 'yes_picture' and T == 'yes_text' and B == 'no_button':
            picture_id = data['picture_id']
            post_text = data['post_text']
            try:
                await bot.send_photo(user_id_here, photo=picture_id, caption=post_text,
                                     caption_entities=data['entities'])
                message_data = await bot.send_photo(ARCHIVE, photo=picture_id, caption=post_text,
                                                    caption_entities=data['entities'])
                await state.set_state(States.ok)
            except FloodWait as e:
                await asyncio.sleep(e.value)
            except Exception as ex:
                logging.error(f'Check post {ex}', exc_info=True)
                await bot.send_message(call.message.chat.id,
                                       '🟠 Обнаружена ошибка в CHECK_POST модуле\nНачните снова', reply_markup=r_kb_2)
                return

        elif P == 'yes_picture' and T == 'no_text' and B == 'no_button':
            picture_id = data['picture_id']
            try:
                await bot.send_photo(user_id_here, photo=picture_id)
                message_data = await bot.send_photo(ARCHIVE, photo=picture_id)
                await state.set_state(States.ok)
            except FloodWait as e:
                await asyncio.sleep(e.value)
            except Exception as ex:
                logging.error(f'Check post {ex}', exc_info=True)
                await bot.send_message(call.message.chat.id,
                                       '🟠 Обнаружена ошибка в CHECK_POST модуле\nНачните снова', reply_markup=r_kb_2)
                return

        elif P == 'no_picture' and T == 'yes_text' and B == 'yes_button':
            post_text = data['post_text']
            button_text = data['button_text']
            button_link = data['button_link']
            try:
                await bot.send_message(user_id_here, text=post_text, entities=data['entities'],
                                       reply_markup=build_inline(button_text, button_link),
                                       disable_web_page_preview=True)
                message_data = await bot.send_message(ARCHIVE, text=data['post_text'], entities=data['entities'],
                                                      reply_markup=build_inline(data['button_text'],
                                                                                data['button_link']),
                                                      disable_web_page_preview=True)
                await state.set_state(States.ok)
            except FloodWait as e:
                await asyncio.sleep(e.value)
            except Exception as ex:
                logging.error(f'Check post {ex}', exc_info=True)
                await bot.send_message(call.message.chat.id,
                                       '🟠 Обнаружена ошибка в CHECK_POST модуле\nНачните снова', reply_markup=r_kb_2)
                return

        elif P == 'no_picture' and T == 'yes_text' and B == 'no_button':
            post_text = data['post_text']
            try:
                await bot.send_message(user_id_here, text=post_text, entities=data['entities'],
                                       disable_web_page_preview=True)
                message_data = await bot.send_message(ARCHIVE, text=post_text, entities=data['entities'],
                                                      disable_web_page_preview=True)
                await state.set_state(States.ok)
            except FloodWait as e:
                await asyncio.sleep(e.value)
            except Exception as ex:
                logging.error(f'Check post {ex}', exc_info=True)
                await bot.send_message(call.message.chat.id,
                                       '🟠 Обнаружена ошибка в CHECK_POST модуле\nНачните снова', reply_markup=r_kb_2)
                return

        elif P == 'no_picture' and T == 'no_text' and B == 'yes_button':
            button_text = data['button_text']
            button_link = data['button_link']
            try:
                await bot.send_message(user_id_here, text="⁠",
                                       reply_markup=build_inline(button_text, button_link),
                                       disable_web_page_preview=True)
                message_data = await bot.send_message(ARCHIVE, text="⁠",
                                                      reply_markup=build_inline(button_text, button_link),
                                                      disable_web_page_preview=True)
                await state.set_state(States.ok)
            except FloodWait as e:
                await asyncio.sleep(e.value)
            except Exception as ex:
                logging.error(f'Check post {ex}', exc_info=True)
                await bot.send_message(call.message.chat.id,
                                       '🟠 Обнаружена ошибка в CHECK_POST модуле\nНачните снова', reply_markup=r_kb_2)
                return

        else:
            await bot.send_message(call.message.chat.id,
                                   '🔘 Какая-то тайна!\nНет ни картинки, ни текста, ни кнопки.\n\nДавай заново? Нажми кнопку НОВЫЙ ПОСТ внизу экрана')

        post_id = message_data.message_id  # id поста в архиве
        await state.update_data(post_id_archive=post_id)

        # TODO Запись всех переменных в базу
        data = await state.get_data()
        list_values_of_DB = f"p='{data['picture']}'," \
                            f"t='{data['text']}'," \
                            f"b='{data['button']}'," \
                            f"button_text='{button_text}'," \
                            f"button_link='{button_link}'," \
                            f"picture_id='{picture_id}'," \
                            f"post_text='{post_text}'," \
                            f"post_id_archive='{data['post_id_archive']}'"

        update_values_db_two(list_values_of_DB, 'user_channel', data['work_channel'])

        await bot.send_message(call.message.chat.id, '🔘 Пост выглядит так, как нужно?', reply_markup=i_kb_5)


async def is_post_ok(call: CallbackQuery, state: FSMContext, bot: Bot):
    await cbqa(call, bot)
    activ = call.data
    if activ == 'yes_post':

        data = await state.get_data()
        work_channel = data['work_channel']
        user_id_here = data['user_id']

        list_of_request = "channel_title"
        sss = list(request_to_db_multi(list_of_request, 'user_channel', work_channel)[0])
        channel_title = sss[0]

        list_of_request = "username"
        sss = list(request_to_db_multi(list_of_request, 'user_id', user_id_here)[0])
        username = sss[0]

        await bot.send_message(call.message.chat.id, '🔘 Отлично!')
        await bot.send_message(ARCHIVE,
                               f'Пост канала {channel_title} id={work_channel}\nот юзера {username} id={user_id_here}')

        data = await state.get_data()
        modify_post = data['modify_post']
        if modify_post != 'yes':
            await bot.send_message(call.message.chat.id,
                                   '🔘 Запустить работу сейчас или хочешь запланировать отложенный старт?',
                                   reply_markup=i_kb_8)
            await state.set_state(States.publishing)

        else:
            await bot.send_message(call.message.chat.id, '🔘 Твой пост отредактирован!', reply_markup=r_kb_2)

    elif activ == 'no_post':
        await bot.send_message(call.message.chat.id, '🔘 Что нужно изменить?', reply_markup=i_kb_6)
        data = await state.get_data()
        post_to_remove = data['post_id_archive']
        await bot.delete_message(ARCHIVE, post_to_remove)
        await state.set_state(States.corrections)


async def publishing(call: CallbackQuery, state: FSMContext, bot: Bot):
    await cbqa(call, bot)
    activ = call.data
    user_id_here = call.from_user.id
    if activ == 'now':
        data = await state.get_data()
        await first_post(data['work_channel'])

        await bot.send_message(user_id_here, '🔘 Твой пост опубликован в твоём канале, я буду его перемещать в ТОП!\n\n'
                                             '🔘 Для изменения закреплённого сообщения или проверки его состояния '
                                             'нажми кнопку СТАТУС внизу экрана\n\n'
                                             '🔘 Если нужно закрепить новое сообщение нажми кнопку НОВЫЙ ПОСТ '
                                             '(Внимание: текущий пост перестанет перемещаться '
                                             'и будет заменён на новый в назначенное время)', reply_markup=r_kb_2)
        await state.update_data(corrections='no')
        await state.update_data(mogify_post='no')

    if activ == 'later':
        chat = call.from_user.id
        data = await bot.send_message(chat, "🔘 Выбери год", reply_markup=get_keyboard_year(datetime.now().year))
        mess_tmp = data.message_id
        await state.update_data(mess_tmp=mess_tmp)
        await state.set_state(States.get_month)


async def get_month(call: CallbackQuery, state: FSMContext, bot: Bot):
    chat = call.from_user.id
    data = await state.get_data()
    mess_to_delete = data['mess_tmp']
    try:
        await bot.delete_message(chat, mess_to_delete)
    except Exception as ex:
        logging.error(f'Не удалось удалить сообщение ГОД {ex}')
    button = call.data
    await state.update_data(year_here=button)
    data = await bot.send_message(chat, "🔘 Выбери месяц", reply_markup=i_month)
    mess_tmp = data.message_id
    await state.update_data(mess_tmp=mess_tmp)
    await state.set_state(States.get_day)


async def get_day(call: CallbackQuery, state: FSMContext, bot: Bot):
    await cbqa(call, bot)
    chat = call.from_user.id
    data = await state.get_data()
    mess_to_delete = data['mess_tmp']
    await bot.delete_message(chat, mess_to_delete)
    button = call.data
    data = await state.get_data()
    year_here = int(data['year_here'])
    monthrange = calendar.monthrange(year_here, get_month_number(button))[1]
    await state.update_data(month_here=button)
    data = await bot.send_message(chat, "🔘 Выбери день", reply_markup=get_keyboard_days(monthrange))
    mess_tmp = data.message_id
    await state.update_data(mess_tmp=mess_tmp)
    await state.set_state(States.get_hour)


async def get_hour(call: CallbackQuery, state: FSMContext, bot: Bot):
    await cbqa(call, bot)
    chat = call.from_user.id
    data = await state.get_data()
    mess_to_delete = data['mess_tmp']
    await bot.delete_message(chat, mess_to_delete)
    button = call.data
    await state.update_data(day_here=button)
    data = await bot.send_message(chat, "🔘 Выбери час", reply_markup=get_keyboard_hour)
    mess_tmp = data.message_id
    await state.update_data(mess_tmp=mess_tmp)
    await state.set_state(States.get_minutes)


async def get_minutes(call: CallbackQuery, state: FSMContext, bot: Bot):
    await cbqa(call, bot)
    chat = call.from_user.id
    data = await state.get_data()
    mess_to_delete = data['mess_tmp']
    await bot.delete_message(chat, mess_to_delete)
    button = call.data
    await state.update_data(hour_here=button)
    data = await bot.send_message(chat, "🔘 Выбери минуты", reply_markup=get_keyboard_minutes)
    mess_tmp = data.message_id
    await state.update_data(mess_tmp=mess_tmp)
    await state.set_state(States.get_check)


async def get_check(call: CallbackQuery, state: FSMContext, bot: Bot):
    await cbqa(call, bot)
    chat = call.from_user.id
    data = await state.get_data()
    mess_to_delete = data['mess_tmp']
    await bot.delete_message(chat, mess_to_delete)
    button = call.data
    await state.update_data(minutes_here=button)

    data = await state.get_data()
    year = data['year_here']
    month = get_month_number(data['month_here'])
    month_human_read = data['month_here']
    day = data['day_here']
    hour = data['hour_here']
    minute = data['minutes_here']
    if len(minute) == 1:
        minute_human_read = f'0{minute}'
    else:
        minute_human_read = minute

    try:
        datetime_here = datetime(int(year), int(month), int(day), int(hour), int(minute))
        if datetime_here <= datetime.now():
            await bot.send_message(chat, '🟠 Введённые дата и время уже прошли. Начнём заново')
            data = await bot.send_message(chat, 'Выбери год', reply_markup=get_keyboard_year(datetime.now().year))
            mess_tmp = data.message_id
            await state.update_data(mess_tmp=mess_tmp)
            await state.set_state(States.get_month)
        else:
            await state.update_data(datetime_here=datetime_here)
            await bot.send_message(chat,
                                   f'🔘 Давай проверим введённые дату и время\n{day} {month_human_read} {year} год\n'
                                   f'Время: {hour}:{minute_human_read}', reply_markup=i_kb_9)
            await state.set_state(States.confirm_date)
    except Exception as ex:
        logging.error(f'Обработка времени: {ex}')


async def confirm_date(call: CallbackQuery, state: FSMContext, bot: Bot):
    await cbqa(call, bot)
    activ = call.data
    if activ == 'right':
        data = await state.get_data()
        date_to_base = data['datetime_here']

        list_values_of_DB = f"watch_on='off'," \
                            f"scheduler_on='on'," \
                            f"scheduler_time='{date_to_base}'"
        update_values_db_two(list_values_of_DB, 'user_channel', data['work_channel'])

        channel_id_here = data['work_channel']
        run_scheduler(date_to_base, channel_id_here)

        await bot.send_message(call.message.chat.id,
                               '🔘 Хорошо, запуск запланирован!\n\n🔘 Для изменения закреплённого '
                               'сообщения или проверки его состояния нажми кнопку СТАТУС '
                               'внизу экрана\n\n🔘 Если нужно закрепить новое сообщение нажми '
                               'кнопку НОВЫЙ ПОСТ (Внимание: текущий пост перестанет перемещаться '
                               'и будет заменён на новый в назначенное время)', reply_markup=r_kb_2)
        await state.update_data(corrections='no')
        await state.update_data(mogify_post='no')

    elif activ == 'wrong':
        await bot.send_message(call.message.chat.id, '🔘 Давай введём дату и время снова')
        data = await bot.send_message(call.message.chat.id, 'Выбери год',
                                      reply_markup=get_keyboard_year(datetime.now().year))
        mess_tmp = data.message_id
        await state.update_data(mess_tmp=mess_tmp)
        await state.set_state(States.get_month)


async def get_corrections(call: CallbackQuery, state: FSMContext, bot: Bot):
    await cbqa(call, bot)
    activ = call.data
    if activ == 'change_picture':
        await state.update_data(corrections='yes')
        await state.update_data(picture='yes_picture')
        await bot.send_message(call.message.chat.id, "🔘 Пришли мне картинку без подписи")
        await state.set_state(States.get_picture)
    elif activ == 'change_text':
        await state.update_data(corrections='yes')
        await state.update_data(text='yes_text')
        await bot.send_message(call.message.chat.id, "🔘 Пришли мне текст поста")
        await state.set_state(States.get_text)
    elif activ == 'change_button':
        await state.update_data(corrections='yes')
        await state.update_data(button='yes_button')
        await bot.send_message(call.message.chat.id, '🔘 Пришли текст на кнопке')
        await state.set_state(States.set_button_text)


async def get_status(message: Message, state: FSMContext):
    user_id_here = message.from_user.id

    data = await state.get_data()
    work_channel = data['work_channel']

    list_of_request = "watch_on, scheduler_on, scheduler_time, post_id_archive, button_text, button_link, is_payed, p, t, b"
    sss = list(request_to_db_multi(list_of_request, 'user_channel', work_channel)[0])
    watch_on = sss[0]
    scheduler_on = sss[1]
    scheduler_time = sss[2]
    post_id_archive = sss[3]
    button_text = sss[4]
    button_link = sss[5]
    is_payed = sss[6]
    is_picture = sss[7]
    is_text = sss[8]
    is_button = sss[9]

    # Проверка чтобы бот не падал при нажатии кнопки Статус при неразмещённом ни разу посте
    if is_picture != 'none' and is_text != 'none' and is_button != 'none':

        await state.update_data(watch_on=watch_on)
        await state.set_state(States.status_buttons)

        if watch_on == 'on':
            service_message = f'🔘 Наблюдение за каналом и перемещение закреплённого поста *активны*'
        else:
            if scheduler_on == 'on':
                t = str(scheduler_time)
                service_message = f'🔘 Запланировано включение по расписанию\n\n Время запуска: {t}'
            else:
                service_message = f'🔘 Наблюдение за каналом и перемещение закреплённого поста *выключены*\n\n' \
                                  f'🔘 Время отложенного запуска *не указано*'

        if is_payed in LISTOFUSERPAY:
            if post_id_archive is not None:
                if is_button == 'yes_button':  # Пост с кнопкой
                    take = await bot.forward_message(user_id_here, ARCHIVE, post_id_archive)

                    entities_tmp = take.entities
                    caption_entities_tmp = take.caption_entities

                    if entities_tmp is not None and caption_entities_tmp is None:
                        entities = entities_tmp
                    elif entities_tmp is None and caption_entities_tmp is not None:
                        entities = caption_entities_tmp
                    else:
                        entities = 'none'
                    await state.update_data(entities=entities)

                    await message.answer(service_message, parse_mode='Markdown', reply_markup=i_kb_14)

                else:  # Пост без кнопки
                    take = await bot.forward_message(user_id_here, ARCHIVE, post_id_archive)

                    entities_tmp = take.entities
                    caption_entities_tmp = take.caption_entities

                    if entities_tmp is not None and caption_entities_tmp is None:
                        entities = entities_tmp
                    elif entities_tmp is None and caption_entities_tmp is not None:
                        entities = caption_entities_tmp
                    else:
                        entities = 'none'
                    await state.update_data(entities=entities)

                    await message.answer(service_message, parse_mode='Markdown', reply_markup=i_kb_14)

            else:
                service_message = f'🔘 Пост для публикации *отсутствует*\n\n' \
                                  f'🔘 Наблюдение за каналом и перемещение закреплённого поста *выключены*\n\n' \
                                  f'🔘 Время отложенного запуска *не указано*'
                await message.answer(service_message, parse_mode='Markdown', reply_markup=r_kb_2)

        else:  # if is_payed == 'trial' or is_payed == 'payed':
            await message.answer('🟠 У Вас нет доступа к статистике бота, обратитесь в техподдержку, пожалуйста!',
                                 reply_markup=r_kb_3)

    else:
        service_message = f'🔘 Пост для публикации *отсутствует*\n\n' \
                          f'🔘 Нажми кнопку "Новый пост" внизу экрана'
        await message.answer(service_message, parse_mode='Markdown', reply_markup=r_kb_2)


async def status_buttons(call: CallbackQuery, state: FSMContext, bot: Bot):
    await cbqa(call, bot)
    button = call.data
    if button == 'modify':  # Изменить пост
        await bot.send_message(call.message.chat.id, '🔘 Что нужно изменить?', reply_markup=i_kb_6)

        data = await state.get_data()
        work_channel = data['work_channel']

        list_of_request = "p, t, b, picture_id, post_text, button_text, button_link"
        sss = list(request_to_db_multi(list_of_request, 'user_channel', work_channel)[0])
        p = sss[0]
        t = sss[1]
        b = sss[2]
        picture_id = sss[3]
        post_text = sss[4]
        button_text = sss[5]
        button_link = sss[6]

        await state.update_data(modify_post='yes')
        await state.update_data(picture=p)
        await state.update_data(text=t)
        await state.update_data(button=b)
        await state.update_data(picture_id=picture_id)
        await state.update_data(post_text=post_text)
        await state.update_data(button_text=button_text)
        await state.update_data(button_link=button_link)

        await state.set_state(States.corrections)

    elif button == 'change_time':  # Изменить время
        data = await state.get_data()
        watch_on = data['watch_on']
        work_channel = data['work_channel']
        user_here = request_to_db_single_two('user_id', 'user_channel', work_channel)
        if watch_on == 'on':
            await bot.send_message(call.message.chat.id,
                                   '🔘 Включено отслеживание постов на твоём канала.\nЕсли ты установишь новое время запуска,'
                                   ' то отслеживание будет приостановлено до наступления нового времени',
                                   reply_markup=i_kb_15)
        else:
            try:
                stop_scheduler_2(user_here, work_channel)
            except Exception as ex:
                logging.error(f"[Change time deleting scheduler] - {ex}", exc_info=True)

            await bot.send_message(call.message.chat.id, '🔘 Давай установим новое время запуска')
            data = await bot.send_message(call.message.chat.id, 'Выбери год',
                                          reply_markup=get_keyboard_year(datetime.now().year))
            mess_tmp = data.message_id
            await state.update_data(mess_tmp=mess_tmp)
            await state.set_state(States.get_month)

    elif button == 'yes_change_time':  # Подтверждение изменения времени
        data = await state.get_data()
        work_channel = data['work_channel']
        user_here = request_to_db_single_two('user_id', 'user_channel', work_channel)
        try:
            stop_scheduler_2(user_here, work_channel)
        except Exception as ex:
            logging.error(f"[Change time deleting scheduler] - {ex}", exc_info=True)

        await bot.send_message(call.message.chat.id, '🔘 Давай установим новое время запуска')
        data = await bot.send_message(call.message.chat.id, 'Выбери год',
                                      reply_markup=get_keyboard_year(datetime.now().year))
        mess_tmp = data.message_id
        await state.update_data(mess_tmp=mess_tmp)
        await state.set_state(States.get_date_time)

    elif button == 'switch_off':  # Выключить
        data = await state.get_data()
        work_channel = data['work_channel']
        user_here = request_to_db_single_two('user_id', 'user_channel', work_channel)
        try:
            stop_scheduler_2(user_here, work_channel)
        except Exception as ex:
            logging.error(f"[Change time deleting scheduler] - {ex}", exc_info=True)
        await bot.send_message(call.message.chat.id,
                               '🔘 Работа PINbot остановлена,\n\n🔘 Чтобы снова включить или изменить закреплённое ранее '
                               'сообщение нажми кнопку СТАТУС\n\n'
                               '🔘 Если нужно закрепить новое сообщение нажми кнопку НОВЫЙ ПОСТ '
                               '(Внимание: текущий пост перестанет перемещаться и будет заменён на новый в '
                               'назначенное время)', reply_markup=r_kb_2)

    elif button == 'status_cancel':  # Отменить действия
        await bot.send_message(call.message.chat.id,
                               '🔘 Хорошо, всё остаётся без изменений.\n\n🔘 Для изменения закреплённого сообщения или '
                               'проверки его состояния нажми кнопку СТАТУС внизу экрана\n\n'
                               '🔘 Если нужно закрепить новое сообщение нажми кнопку НОВЫЙ ПОСТ '
                               '(Внимание: текущий пост перестанет перемещаться и будет заменён на новый '
                               'в назначенное время)', reply_markup=r_kb_2)
        await state.set_state(States.status_buttons)
