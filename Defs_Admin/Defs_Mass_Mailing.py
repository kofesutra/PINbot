import asyncio
import logging
from collections import deque

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from pyrogram.errors import FloodWait

from DB.DB_utils import update_values_db_two, request_to_db_column
from Keyboards.Inline_Admin import i_kb_admin_1
from Keyboards.Reply_Admin import r_kb_admin
from Utils.Bot import bot
from Utils.State_Machine import StatesAdmin


async def run_message_mass(message: Message, state: FSMContext):
    admin_now = message.from_user.id

    await bot.send_message(admin_now, f'Напиши текст письма для массовой рассылки')
    await state.set_state(StatesAdmin.get_text_for_mass)


async def get_text_for_mass(message: Message, state: FSMContext):
    admin_now = message.from_user.id
    text_here = message.text
    entities_here = message.entities

    await bot.send_message(admin_now, f'{text_here}', entities=entities_here, disable_web_page_preview=True)
    await bot.send_message(admin_now, f'Всё правильно?', reply_markup=i_kb_admin_1)
    await state.update_data(text_for_Letter=text_here)
    await state.update_data(entities_for_Letter=entities_here)
    await state.set_state(StatesAdmin.check_letter_for_mass)


async def check_letter_for_mass(call: CallbackQuery, state: FSMContext):
    admin_now = call.from_user.id
    answer_here = call.data

    if answer_here == 'yes_right':

        messages_list = deque()  # Создаём очередь
        # Запрос из базы всех ID которые не Blocked
        sss = request_to_db_column('user_id', 'user_bot_session', "'allowed'")
        print(sss)

        # Разбираем список на кортежи, а их на записи
        for s in sss:
            print(s)
            for z in s:
                print(z)
                messages_list.append(z)  # Добавляем в очередь

        result = await run_mass_mailing(messages_list, state)  # Вызываем обработчик:
        if result == 'OK':
            await bot.send_message(admin_now, f'Рассылка закончена.', reply_markup=r_kb_admin)
        else:
            await bot.send_message(admin_now, f'С рассылкой что-то не так.', reply_markup=r_kb_admin)

    elif answer_here == 'no_wrong':
        await state.set_state(StatesAdmin.get_text_for_mass)
        await bot.send_message(admin_now, f'Давай заново\nНапиши текст письма для массовой рассылки')

    elif answer_here == 'cancel':
        await state.clear()
        await bot.send_message(admin_now, f'Отменено', reply_markup=r_kb_admin)


async def run_mass_mailing(messages_list, state: FSMContext):
    data = await state.get_data()
    text_for_Letter = data['text_for_Letter']
    entities_for_Letter = data['entities_for_Letter']
    for user_id_for_Letter in messages_list:
        print(f'{user_id_for_Letter} OK')
        try:
            await bot.send_message(user_id_for_Letter, text_for_Letter, entities=entities_for_Letter,
                                   disable_web_page_preview=True)
            await asyncio.sleep(1)
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except Exception as ex:
            logging.error(f'Ошибка отправки письма юзеру ID {user_id_for_Letter}: {ex}')
            if 'bot was blocked' in str(ex):
                logging.error(f'Юзер ID {user_id_for_Letter} заблокировал бот')

                # Внесение метки Blocked в базу (убирать метку при запуске юзером бота)
                list_values_of_DB = f"user_bot_session = 'blocked'"
                update_values_db_two(list_values_of_DB, 'user_id', user_id_for_Letter)

    return 'OK'
