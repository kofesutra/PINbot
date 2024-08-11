import datetime
import logging
import random
import string

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from Config.config import ADMIN_ID
from DB.DB_utils import request_to_db_multi
from Keyboards.Inline_Builder import build_inline_pay
from Keyboards.Reply import r_kb_2
from Utils import Bot
from Utils.Bot import get_future_date
from Utils.Process_Pay_to_base import insert_payment_to_base
from Utils.Process_Yoomoney import yoo_receive_pay_link, yoo_check_payment
from Utils.State_Machine import States


async def start_payment(call: CallbackQuery, state: FSMContext, bot: Bot):
    user_id_here = call.from_user.id
    pay_description = '1 месяц'
    amount = 1020

    button = call.data
    if button == 'month_1':
        pay_description = '1 месяц'
        amount = 1020
    elif button == 'month_3':
        pay_description = '3 месяца'
        amount = 3060
    elif button == 'month_6':
        pay_description = '6 месяцев'
        amount = 5508
    elif button == 'month_12':
        pay_description = '12 месяцев'
        amount = 9792

    # Генерим метку оплаты: id юзера + рандомная буква + дата
    # Запоминаем её
    # Обращаемся к юмани и получаем ссылку на оплату
        date = datetime.date.today()
    rand = random.choice(string.ascii_lowercase)
    label = f'{user_id_here}{rand}{date}'
    await state.update_data(label=label)
    await state.update_data(tarif=button)

    try:
        link = await yoo_receive_pay_link(pay_description, amount, label)
        await bot.send_message(user_id_here,
                               f'🔘 Выбран тариф {pay_description} доступа\nстоимость: {amount}р\n\nНажми кнопку '
                               f'"Оплатить"\nзатем вернись сюда и нажми кнопку "Готово"',
                               reply_markup=build_inline_pay(link))
        await state.set_state(States.check_payment)
    except Exception as ex:
        logging.error(f'Юмани ссылка не получена: {ex}')
        await bot.send_message(ADMIN_ID, f'АХТУНГ! Юмани не даёт ссылку на оплату')
        await bot.send_message(user_id_here,
                               f'🔘 Какие-то неполадки.\nПопробуй ещё раз через минуту. Если ошибка повторится напиши в техподдержку',
                               reply_markup=r_kb_2)


async def check_payment(call: CallbackQuery, state: FSMContext, bot: Bot):
    user_id_here = call.from_user.id
    await bot.send_message(user_id_here, f'🔘 Я проверяю твой платёж, пожалуйста, подожди немного')

    data = await state.get_data()
    label = str(data['label'])
    is_paid = data['tarif']

    status, pay_datetime, amount = await yoo_check_payment(label)

    if status == 'none':
        await bot.send_message(user_id_here, f'🔘 Платёжная система сообщила мне, что платёж не обнаружен')
    elif status == 'success':
        await bot.send_message(user_id_here, f'🔘 Платёж осуществлен успешно!')

        # TODO Записать в базу все необходимые данные:
        # TODO В основную базу:
        # Отметка об оплате, дата платежа, сумма платежа, дата окончания оплаченного периода, label платежа (для просмотра в истории юмани)

        # Если платёж не первый, и если срок ещё не вышел
        # то получить из базы дату окончания оплаченного срока
        # и прибавить к ней дополнительный срок

        list_of_request = "date_of_end, paid_month_count"
        sss = list(request_to_db_multi(list_of_request, 'user_id', user_id_here)[0])
        date_of_old_end = sss[0]
        paid_month_count = sss[1]
        date_time_2 = datetime.datetime.now()

        if date_of_old_end >= date_time_2:
            pay_datetime = date_of_old_end
        end_date = '2000-01-01 23:59:59'

        if is_paid == 'month_1':
            end_date = get_future_date(pay_datetime, 31)
            paid_month_count = paid_month_count + 1
        elif is_paid == 'month_3':
            end_date = get_future_date(pay_datetime, 92)
            paid_month_count = paid_month_count + 3
        elif is_paid == 'month_6':
            end_date = get_future_date(pay_datetime, 184)
            paid_month_count = paid_month_count + 6
        elif is_paid == 'month_12':
            end_date = get_future_date(pay_datetime, 365)
            paid_month_count = paid_month_count + 12

        await insert_payment_to_base(user_id_here, is_paid, pay_datetime, end_date, amount, label, paid_month_count, state, bot)

    elif status == 'refused':
        await bot.send_message(user_id_here,
                               f'🔘 Платёжная система отказала в проведении платежа.\n\nПроверь свои данные карты или кошелька и доступные средства')
    elif status == 'in_progress':
        await bot.send_message(user_id_here,
                               f'🔘 Платёжная система сообщила мне, что платёж в процессе проведения. Подожди немного и снова нажми кнопку "Готово" для повторной проверки')
