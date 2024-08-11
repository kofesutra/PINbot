from datetime import datetime

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from Config.config import LINKTOBOTFORWORKER
from DB.DB_utils import add_all_to_db, request_to_db_column, delete_from_db, get_max_id_two
from Keyboards.Inline_Employee import i_kb_emp_1, i_kb_list_for_remove
from Keyboards.Reply import r_kb_2
from Utils import Bot
from Utils.State_Machine import States


async def employee(call: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    user_id_here = data['user_id']
    await bot.send_message(user_id_here, f'🔘 Для того, чтобы назначить работника пришли мне его юзернейм '
                                         f'(@username) или ссылку на его профиль (https://t.me/username)',
                           disable_web_page_preview=True)
    await state.set_state(States.get_employee)


async def get_employee(message: Message, state: FSMContext, bot: Bot):
    if message.text:
        data = message.text
        # Преобразовать в юзернейм без @ и https://t.me/
        user_check = is_username(data)
        if user_check != 'error':
            await message.answer(f'🔘 Внимательно проверь юзернейм: @{user_check}', reply_markup=i_kb_emp_1)
            await state.update_data(user_check=user_check)
            await state.set_state(States.check_employee)
        else:
            await message.answer(
                f'🔘 Какая-то ошибка. Пришли текстовое сообщение, в котором только юзернейм или ссылка на профиль')
    else:
        await message.answer(f'🔘 Пришли текстовое сообщение, в котором только юзернейм или ссылка')


def is_username(text):
    if ' ' in text:
        return 'error'
    elif 'none' in text:
        return 'error'
    elif 'None' in text:
        return 'error'
    elif '@' in text:
        srez = text[1:]  # Обрезаем первый символ
        return srez
    elif 'https://t.me/' in text:
        srez = text[13:]  # Обрезаем https://t.me/
        return srez
    else:
        return 'error'


async def check_employee(call: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    user_id_here = data['user_id']
    user_check = data['user_check']
    button = call.data
    if button == 'yes':
        # Проверить, нет ли этого юзера в базе
        if get_max_id_two('username', f"'{user_check}'") is not None:
            # Работник есть в базе
            await bot.send_message(user_id_here,
                                       f'🔘 Ошибка: твой работник уже зарегистрирован в моей базе. Если что-то неверно, пожалуйста, обратись в техподдержку', reply_markup=r_kb_2)
        else:  # Работника нет в базе
            await bot.send_message(user_id_here, f'🔘 Хорошо, вношу твоего работника в базу данных')
            # Bнести запись в новую строку
            date_time_2 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            list_subjects_of_DB = "username, date_of_start, reg_done, user_status, employee_of"
            list_data_of_DB = f"'{data['user_check']}', '{date_time_2}', 'yes', " \
                              f"'employee', '{user_id_here}'"
            add_all_to_db(list_subjects_of_DB, list_data_of_DB)
            await bot.send_message(user_id_here, f'🔘Теперь отправь работнику ссылку для входа\n\n'
                                             f'Важно: он должен зайти именно по этой ссылке\n\n'
                                             f'{LINKTOBOTFORWORKER}{user_id_here}', disable_web_page_preview=True, reply_markup=r_kb_2)
    elif button == 'no':
        await bot.send_message(user_id_here, f'🔘 Пришли юзернейм работника ещё раз')
        await state.set_state(States.get_employee)


async def remove_employee(call: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    user_id_here = data['user_id']
    # Запросить в базе данные о работниках для user_id_here
    try:
        list_of_request = "id, username, first_name, last_name, user_id"
        list_of_employees = request_to_db_column(list_of_request, 'employee_of', user_id_here)
        count_of_emp = len(list_of_employees)
        count = 0
        if count_of_emp != 0:
            await bot.send_message(user_id_here, f'🔘Вот список твоих работников:\n\n')
            for emp in list_of_employees:
                count = count + 1
                await bot.send_message(user_id_here,
                                       f'Номер {count}:\nюзернейм: {emp[1]}, имя: {emp[2]}, фамилия: {emp[3]}, id: {emp[4]}')

            await bot.send_message(user_id_here,
                                   f'🔘 Выбери работника запись которого следует удалить из базы и нажми соответствующую цифру\n\n'
                                   f'', reply_markup=i_kb_list_for_remove(count_of_emp))
            await state.update_data(list_of_employees=list_of_employees)
            await state.set_state(States.confirm_remove_employee)
        else:
            await bot.send_message(user_id_here, f'🔘 Работники не найдены в моей базе')

    except Exception as ex:
        await bot.send_message(user_id_here, f'🔘 Работники не найдены в моей базе')


async def confirm_remove_employee(call: CallbackQuery, state: FSMContext, bot: Bot):
    button = call.data
    data = await state.get_data()
    user_id_here = data['user_id']
    list_of_employees = data['list_of_employees']
    if button == '1':
        id_here = list_of_employees[0][0]  # id строки (индекс записи в списке и индекс поля в строке)
        delete_from_db('id', id_here)
    elif button == '2':
        id_here = list_of_employees[1][0]
        delete_from_db('id', id_here)
    elif button == '3':
        id_here = list_of_employees[2][0]
        delete_from_db('id', id_here)
    elif button == '4':
        id_here = list_of_employees[3][0]
        delete_from_db('id', id_here)
    elif button == '5':
        id_here = list_of_employees[4][0]
        delete_from_db('id', id_here)

    await bot.send_message(user_id_here,
                           f'🔘 Готово! Запись о работнике удалена из моей базы.\n\nЕсли нужно, ты можешь добавить другого работника')
