from datetime import datetime

from aiogram.fsm.context import FSMContext

from DB.DB_utils import request_to_db_multi, update_values_db_two
from Utils import Bot
from Utils.State_Machine import States


async def process_worker_link(user_id_inviter, state, bot):
    # Запрашиваем в базе имеется ли запись от инвайтера для этого юзера
    data = await state.get_data()
    user_id_here = data['user_id']
    username = data['username']
    if user_id_inviter != user_id_here:
        list_of_request = "employee_of, user_status, id"
        try:
            sss = list(request_to_db_multi(list_of_request, 'username', f"'{username}'")[0])
            employee_of = sss[0]
            user_status = sss[1]
            id_here = sss[2]

            # Если пригласитель и id из инвайт ссылки совпадают и статус юзера = employee
            if employee_of == int(user_id_inviter) and user_status == 'employee':
                date_time_2 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                list_values_of_DB = f"user_id = '{data['user_id']}'," \
                                    f"first_name = '{data['first_name']}'," \
                                    f"last_name = '{data['last_name']}'," \
                                    f"date_of_use = '{date_time_2}'," \
                                    f"come_from = '{data['come_from']}'"
                update_values_db_two(list_values_of_DB, 'id', id_here)

                list_of_request = "reg_done, user_channel"
                sss = list(request_to_db_multi(list_of_request, 'user_id', employee_of)[0])
                reg_done = 'yes'
                work_channel = sss[1]  # Получаем id канала, в котором будет вестись работа
                work_user_for_base = employee_of  # И в строку какого юзера (владельца) будем вносить изменения
                await state.update_data(work_user_for_base=work_user_for_base)
                await state.update_data(work_channel=work_channel)

                await state.update_data(worker='worker')  # Сделано для остановки регистрации
                await bot.send_message(user_id_here, '🔘 Мои поздравления!\n\n'
                                                     'Твоя регистрация прошла успешно')

            else:
                await bot.send_message(user_id_here, '🔘 В моей базе нет записей о твоём приглашении\n\n'
                                                     'Это может означать, что тот, кто прислал тебе инвайт-ссылку ещё не внёс нужные данные\n\n'
                                                     'Если что-то не так, пожалуйста, обратись в техподдержку')
                await state.set_state(States.stop)
                await stop_registration(user_id_here, state, bot)
        except Exception as ex:
            await bot.send_message(user_id_here, '🔘 В моей базе нет записей о твоём приглашении\n\n'
                                                 'Это может означать, что тот, кто прислал тебе инвайт-ссылку ещё не внёс нужные данные\n\n'
                                                 'Если что-то не так, пожалуйста, обратись в техподдержку')
            await state.set_state(States.stop)
            await stop_registration(user_id_here, state, bot)
    else:
        await bot.send_message(user_id_here, '🔘 Ты не можешь назначить себя работником')
        return


async def stop_registration(user_id_here, state: FSMContext, bot: Bot):
    await bot.send_message(user_id_here, f'🔘 Работа завершена')
    await state.update_data(user_id=88888888)  # Сделано для остановки регистрации
