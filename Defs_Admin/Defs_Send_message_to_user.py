import logging

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from DB.DB_utils import update_values_db_two, request_to_db_single_two
from Keyboards.Inline_Admin import i_kb_admin_1
from Keyboards.Reply_Admin import r_kb_admin
from Utils.Bot import bot
from Utils.Check_is_all_digits import is_digits
from Utils.State_Machine import StatesAdmin


async def run_message_to_user(message: Message, state: FSMContext):
    admin_now = message.from_user.id
    await bot.send_message(admin_now, f'Какому юзеру пишем? Дай USER_ID или username')
    await state.set_state(StatesAdmin.user_id_for_letter)


async def get_user_id_for_letter(message: Message, state: FSMContext):
    admin_now = message.from_user.id
    text_here = message.text

    if is_digits(text_here) != 'error':
        # Значит прислан ID, то есть запросить юзернейм
        username_for_letter = request_to_db_single_two('username', 'user_id', text_here)
        user_id_for_Letter = text_here
    else:
        # Запросить id
        user_id_for_Letter = request_to_db_single_two('user_id', 'username', f"'{text_here}'")
        username_for_letter = text_here

    await bot.send_message(admin_now, f'Юзернейм {username_for_letter} ID {user_id_for_Letter}\nНапиши текст письма')
    await state.update_data(user_id_for_Letter=user_id_for_Letter)
    await state.update_data(username_for_letter=username_for_letter)

    await state.set_state(StatesAdmin.letter_to_user)


async def get_text_for_letter(message: Message, state: FSMContext):
    admin_now = message.from_user.id
    text_here = message.text
    entities_here = message.entities

    await bot.send_message(admin_now, f'{text_here}', entities=entities_here, disable_web_page_preview=True)
    await bot.send_message(admin_now, f'Всё правильно?', reply_markup=i_kb_admin_1)
    await state.update_data(text_for_Letter=text_here)
    await state.update_data(entities_for_Letter=entities_here)
    await state.set_state(StatesAdmin.check_letter)


async def check_letter_to_user(call: CallbackQuery, state: FSMContext):
    admin_now = call.from_user.id
    answer_here = call.data

    if answer_here == 'yes_right':
        data = await state.get_data()
        user_id_for_Letter = data['user_id_for_Letter']
        text_for_Letter = data['text_for_Letter']
        entities_for_Letter = data['entities_for_Letter']
        username_for_letter = data['username_for_letter']
        try:
            await bot.send_message(user_id_for_Letter, text_for_Letter, entities=entities_for_Letter,
                                   disable_web_page_preview=True)
        except Exception as ex:
            logging.error(f'Ошибка отправки письма юзеру {username_for_letter} ID {user_id_for_Letter}: {ex}')
            if 'bot was blocked' in str(ex):
                logging.error(f'Юзер {username_for_letter} ID {user_id_for_Letter} заблокировал бот')
                await bot.send_message(admin_now,
                                       f'Юзер {username_for_letter} ID {user_id_for_Letter} заблокировал бот',
                                       reply_markup=r_kb_admin)

                # Внесение метки Blocked в базу (убирать метку при запуске юзером бота снова)
                list_values_of_DB = f"user_bot_session = 'blocked'"
                update_values_db_two(list_values_of_DB, 'user_id', user_id_for_Letter)
        else:
            await bot.send_message(admin_now, f'Письмо юзеру {username_for_letter} ID {user_id_for_Letter} отправлено',
                                   reply_markup=r_kb_admin)

    elif answer_here == 'no_wrong':
        await state.set_state(StatesAdmin.user_id_for_letter)
        await bot.send_message(admin_now, f'Давай заново\nКакому юзеру пишем? Дай USER_ID или username')

    elif answer_here == 'cancel':
        await state.clear()
        await bot.send_message(admin_now, f'Отменено', reply_markup=r_kb_admin)
