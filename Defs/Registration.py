import asyncio

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile

from Config.config import BOTUSERNAME
from DB.DB_utils import update_values_db_two, get_max_id_two
from Keyboards.Inline import i_kb_10, i_kb_11, i_kb_13, i_kb_12
from Keyboards.Reply import r_kb_1
from Utils.CallBackQueryAnswer import cbqa
from Utils.Check_is_bot_userbot_allowed import is_bot_and_userbot_allowed
from Utils.State_Machine import States


async def greeting(message: Message, state: FSMContext, bot: Bot):
    await message.answer("🔘 Привет!", reply_markup=r_kb_1)
    await message.answer('🔘 Для начала моей работы выполни несколько действий - без них никак не получится.\n\n'
                         'Сначала зарегистрируем твой канал.\nПерешли мне любой пост, который в нём уже опубликован, с помощью функции "Переслать" или "Поделиться".', reply_markup=r_kb_1)
    await state.set_state(States.get_channel)


async def get_channel(message: Message, state: FSMContext, bot: Bot):
    mess = message
    user_channel = mess.forward_from_chat.id
    channel_title = mess.forward_from_chat.title
    await state.update_data(user_channel=user_channel)
    await state.update_data(channel_title=channel_title)
    print(user_channel, channel_title)

    if get_max_id_two('user_channel', user_channel) is not None:
        await message.answer(f'🔘 Похоже на ошибку.\n\nТы не можешь подключить канал "{channel_title}",\nID {user_channel},\n\n🔘 Перешли мне сообщение из своего канала.')
    else:
        await message.answer(f'🔘 Твой канал "{channel_title}",\nID твоего канала {user_channel},\nверно?', reply_markup=i_kb_10)
        await state.set_state(States.set_channel)


async def set_channel(call: CallbackQuery, state: FSMContext, bot: Bot):
    await cbqa(call, bot)
    button = call.data
    if button == 'right':
        data = await state.get_data()
        user_id_here = data['user_id']
        user_channel = data['user_channel']
        channel_title = data['channel_title']
        list_values_of_DB = f"user_channel='{user_channel}', channel_title='{channel_title}'"
        update_values_db_two(list_values_of_DB, 'user_id', user_id_here)

        await bot.send_message(call.message.chat.id, f'🔘 Хорошо, я запомнил твой канал.')
        await bot.send_message(call.message.chat.id, f'🔘 Теперь добавь меня {BOTUSERNAME} в администраторы своего канала.\n'
                                                     f'Затем нажми кнопку "Готово"', reply_markup=i_kb_11)
        await state.set_state(States.check_admins)

    elif button == 'wrong':
        await bot.send_message(call.message.chat.id, '🔘 Перешли мне любое сообщение из своего канала')
        await state.set_state(States.get_channel)

    elif button == 'back':
        await bot.send_message(call.message.chat.id, f'🔘 Добавь меня {BOTUSERNAME} в администраторы своего канала.\n'
                                                     f'Затем нажми кнопку "Готово"', reply_markup=i_kb_11)
        await state.set_state(States.check_admins)


async def check_admins(call: CallbackQuery, state: FSMContext, bot: Bot):
    await cbqa(call, bot)
    button = call.data
    if button == 'done':
        await bot.send_message(call.message.chat.id, '🔘 Подожди несколько секунд, я подключаюсь')
        data = await state.get_data()
        user_id_here = data['user_id']
        user_channel = data['user_channel']

        # Проверяем есть ли бот и юзербот в админах
        if await is_bot_and_userbot_allowed(user_channel):
            list_values_of_DB = f"user_bot_allowed='yes', user_channel_allowed='yes', reg_done='yes'"
            update_values_db_two(list_values_of_DB, 'user_id', user_id_here)

            await state.update_data(work_user_for_base=user_id_here)
            await state.update_data(work_channel=user_channel)

            await bot.send_message(call.message.chat.id, '🔘 Отлично! Всё получилось!\nПродолжаем?', reply_markup=i_kb_13)
            await state.set_state(States.select_getting_post_0)

        else:
            await bot.send_message(call.message.chat.id, '🔘 Пока я не добавлен в администраторы твоего канала.\n'
                                                         'Попробуй ещё раз и нажми "Готово"', reply_markup=i_kb_11)

    elif button == 'how':
        await bot.send_message(call.message.chat.id, f'🔘 Как добавить администратора в канал на компьютере:\n'
                                                     f'1. Скопируй ссылку: {BOTUSERNAME}\n'
                                                     f'2. Открой свой канал')
        await bot.send_message(call.message.chat.id, f'3. Нажми три точки в верхнем углу')
        await bot.send_photo(call.message.chat.id, FSInputFile("Media/1.png"))
        await asyncio.sleep(2)
        await bot.send_message(call.message.chat.id, f'4. Выбери "Управление каналом"')
        await bot.send_photo(call.message.chat.id, FSInputFile("Media/2.png"))
        await asyncio.sleep(2)
        await bot.send_message(call.message.chat.id, f'5. Нажми "Администраторы"')
        await bot.send_photo(call.message.chat.id, FSInputFile("Media/3.png"))
        await asyncio.sleep(2)
        await bot.send_message(call.message.chat.id, f'6. Выбери "Добавить администратора"')
        await bot.send_photo(call.message.chat.id, FSInputFile("Media/4.png"))
        await asyncio.sleep(2)
        await bot.send_message(call.message.chat.id, f'7. В строке поиска вставь скопированную ссылку: https://t.me/pinanybot', disable_web_page_preview=True)
        await bot.send_photo(call.message.chat.id, FSInputFile("Media/5.png"))
        await asyncio.sleep(2)
        await bot.send_message(call.message.chat.id, f'8. Нажми на появившийся профиль PINbot')
        await bot.send_photo(call.message.chat.id, FSInputFile("Media/6.png"))
        await asyncio.sleep(2)
        await bot.send_message(call.message.chat.id, f'9. Ты увидишь сообщение:"Пользователь не подписан на этот канал. Пригласить его и назначить администратором?"\n'
                                                     f'10. Нажми "ОК"\n')
        await bot.send_photo(call.message.chat.id, FSInputFile("Media/7.png"))
        await asyncio.sleep(2)
        await bot.send_message(call.message.chat.id, f'11. Нажми "Сохранить"')
        await bot.send_photo(call.message.chat.id, FSInputFile("Media/8.png"))
        await asyncio.sleep(2)
        await bot.send_message(call.message.chat.id, f'12. Нажми "Закрыть"')
        await bot.send_photo(call.message.chat.id, FSInputFile("Media/9.png"))
        await asyncio.sleep(2)
        await bot.send_message(call.message.chat.id, f'13. Нажми "Сохранить"')
        await bot.send_photo(call.message.chat.id, FSInputFile("Media/10.png"), reply_markup=i_kb_12)

        await state.set_state(States.set_channel)
