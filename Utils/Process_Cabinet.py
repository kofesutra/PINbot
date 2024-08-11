import os
from _csv import writer
from datetime import datetime

from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, CallbackQuery

from Config.config import CSV_FILE_2, LIST_DATA_REF_VIP, LIST_SUBJECTS_REF_VIP, LIST_DATA_REF, \
    LIST_SUBJECTS_REF, LINKTOBOT
from DB.DB_Refs_Utils import db_export_ref, request_to_db_distinct_refs, request_to_db_sum_refs, \
    request_to_db_sum_multi_refs, db_export_ref_vip
from DB.DB_utils import request_to_db_multi
from Keyboards.Inline import i_kb_payments
from Keyboards.Inline_Cabinet import i_kb_cabinet_vip, i_kb_cabinet_lead_1_full, i_kb_cabinet_lead_1_not_full, \
    i_kb_cabinet_lead_2, i_kb_cabinet_others
from Utils.Bot import bot
from Utils.Process_Employee import employee, remove_employee
from Utils.State_Machine import States


async def get_cabinet(call: CallbackQuery, state: FSMContext):
    user_id_here = call.from_user.id

    # Запрос из базы статуса юзера
    list_of_request = "user_status, paid_month_count, date_of_end"
    sss = list(request_to_db_multi(list_of_request, 'user_id', user_id_here)[0])
    user_status = sss[0]
    paid_month_count = sss[1]
    date_of_end = sss[2]

    await state.update_data(user_status=user_status)

    if date_of_end is None:
        paid_mess_here = f'🔘 Сведений об окончании доступа нет.'
    else:
        paid_mess_here = f'🔘 Доступ оплачен до: {date_of_end}'

    if user_status == 'vip':
        await bot.send_message(user_id_here, f'🔘Это твой личный кабинет.\n\n'
                                             f'Ты можешь получить свою инвайт-ссылку,\n'
                                             f'посмотреть краткую статистику регистраций по ней,\n'
                                             f'скачать подробную статистику,\n'
                                             f'Назначить и удалить работника', reply_markup=i_kb_cabinet_vip)

    elif user_status == 'lead_1_full':
        await bot.send_message(user_id_here, f'🔘 Это твой личный кабинет.\n\n'
                                             f'Ты можешь получить свою инвайт-ссылку,\n'
                                             f'посмотреть краткую статистику регистраций по ней,\n'
                                             f'скачать подробную статистику,\n'
                                             f'Назначить и удалить работника\n\n'
                                             f'{paid_mess_here}', reply_markup=i_kb_cabinet_lead_1_full)

    elif user_status == 'lead_1':
        await bot.send_message(user_id_here, f'🔘 Это твой личный кабинет.\n\n'
                                             f'Инвайт-ссылка пока недоступна.\n'
                                             f'Ты можешь ознакомиться с тарифами и условиями получения инвайт-ссылки,\n'
                                             f'оплатить доступ,\n'
                                             f'скачать подробную статистику,\n'
                                             f'Назначить и удалить работника\n\n'
                                             f'{paid_mess_here}', reply_markup=i_kb_cabinet_lead_1_not_full)

    elif user_status == 'lead_2':
        await bot.send_message(user_id_here, f'🔘 Это твой личный кабинет.\n\n'
                                             f'Инвайт-ссылка пока недоступна.\n'
                                             f'Ты можешь ознакомиться с тарифами и условиями получения инвайт-ссылки,\n'
                                             f'оплатить доступ\n\n'
                                             f'{paid_mess_here}', reply_markup=i_kb_cabinet_lead_2)

    elif user_status == 'employee':
        await bot.send_message(user_id_here, f'🔘 Личный кабинет недоступен.')

    else:
        await bot.send_message(user_id_here, f'🔘 Это твой личный кабинет.\n\n'
                                             f'Инвайт-ссылка пока недоступна.\n'
                                             f'Ты можешь ознакомиться с тарифами и условиями получения инвайт-ссылки,\n'
                                             f'оплатить доступ\n\n'
                                             f'{paid_mess_here}', reply_markup=i_kb_cabinet_others)


async def cabinet_buttons(call: CallbackQuery, state: FSMContext):
    button = call.data
    user_id_here = call.from_user.id
    data = await state.get_data()
    user_status = data['user_status']

    if button == 'invitelink':
        if user_status == 'vip' or user_status == 'lead_1_full':
            # Cообщение со сгенерированной ссылкой
            await bot.send_message(user_id_here, f'🔘 Твоя инвайт-ссылка на PINbot:\n'
                                                 f'{LINKTOBOT}{user_id_here}\n\n'
                                                 f'🔘 Ссылка на демо PINbot (показывает как он работает, используй для объяснения принципа и механики работы PINbot):\n'
                                                 f'https://t.me/pinanydemobot', disable_web_page_preview=True)
        else:
            # Cообщение о возможности стать участником
            await bot.send_message(user_id_here, '🔘 Ты тоже можешь стать участником реферальной программы\n\n'
                                                 'Посмотри раздел "Тарифы')

    elif button == 'statistics':
        if user_status == 'vip':
            await run_db_statistics_vip(user_id_here)
        elif user_status == 'lead_1_full':
            await run_db_statistics(user_id_here)
        else:
            await bot.send_message(user_id_here, '🔘 Ты тоже можешь стать участником реферальной программы\n\n'
                                                 'Посмотри раздел "Тарифы')

    elif button == 'download_statistics':
        if user_status == 'vip':
            await run_db_export_vip(user_id_here)
        elif user_status == 'lead_1_full':
            await run_db_export(user_id_here)
        else:
            await bot.send_message(user_id_here, '🔘 Ты тоже можешь стать участником реферальной программы\n\n'
                                                 'Посмотри раздел "Тарифы')

    elif button == 'payment':
        await bot.send_message(user_id_here, f'🔘 Выбери свой тариф', reply_markup=i_kb_payments)
        await state.set_state(States.payment)

    elif button == 'tarifs':
        await bot.send_message(user_id_here, '🟢 Как получить доступ к сервису PINbota?\n'
                                             'Доступ к сервису осуществляется через платную подписку по реферальным ссылкам партнерской программы\n\n'
                                             '🟠 Сколько стоит подписка?\n'
                                             'Стоимость подписки со скидкой в 40% по реферальной партнерской ссылке - 1020 рублей в месяц\n\n'
                                             '🟣 Как стать партнером?\n'
                                             'При оплате доступа на 3 месяца в сумме 3060 рублей пользователь Сервиса PINbot автоматически становится ПАРТНЕРОМ и будет получать вознаграждение в размере 15% от платежей новых подписчиков пришедших по его реферальной ссылке\n\n'
                                             '🔴 Бонусы для пользователей Сервиса PINbot\n'
                                             '- Ознакомительная бесплатная подписка на PINbot на 7 дней\n'
                                             '- При  оплате подписки на 6 мес дополнительная скидка 10% - 5508 рублей (918 руб/мес)\n'
                                             '- При оплате годовой подписки (12 мес) дополнительная скидка 20% - 9792 (816 руб/мес)\n\n'
                                             '🟢 Итого:\n'
                                             '1 месяц - 1020р.\n'
                                             '3 месяца - 3060р.\n'
                                             '6 месяцев - 5508р.\n'
                                             '12 месяцев - 9792р.\n\n')

    elif button == 'set_employee':
        await state.set_state(States.employee)
        await employee(call, state, bot)

    elif button == 'remove_employee':
        await state.set_state(States.remove_employee)
        await remove_employee(call, state, bot)

    elif button == 'howto_employee':
        await bot.send_message(user_id_here, '🔘Ты можешь делегировать управление моей работой другому человеку.\n'
                                             'Для этого нажми кнопку "Назначить работника" и следуй подсказкам.\n'
                                             'Важно: сначала добавь работника в список и только потом отправь ему ссылку для входа\n\n'
                                             '🔘Если ты пожелаешь убрать работника из списка доверенных лиц нажми кнопку "Убрать работника"\n\n'
                                             'Важно: назначенный работник не будет иметь доступа к реферальной программе и твоей статистике, '
                                             'он сможет только менять пост и время для моей работы')


async def run_db_statistics(user_id_here):
    # Количество лидов
    count_leads_2 = len(request_to_db_distinct_refs('lead_2', 'lead_1', user_id_here))
    # Накопленная сумма (1 и 2 уровни вместе)
    sum_leads_2 = request_to_db_sum_refs('sum_to_ref_lead_2_to_1', 'lead_1', user_id_here)
    if sum_leads_2 is None:
        sum_leads_2 = 0
    # Выплаченная сумма
    sum_pay_leads_2 = request_to_db_sum_multi_refs('sum_to_ref_lead_2_to_1', 'lead_1', user_id_here, 'payout_lead_2_to_1', True)
    if sum_pay_leads_2 is None:
        sum_pay_leads_2 = 0
    sum_unpayed = sum_leads_2 - sum_pay_leads_2

    await bot.send_message(user_id_here, f'🟣 Статистика на настоящее время:\n\n🟠 Зарегистрированных по реферальной ссылке всего: {count_leads_2}\n\n'
                         f'🟢 Сумма реф. выплат всего: {sum_leads_2}\nВыплаченная сумма: {sum_pay_leads_2}\nНевыплаченная сумма: {sum_unpayed}')


async def run_db_statistics_vip(user_id_here):
    # Количество лидов
    count_leads_1 = len(request_to_db_distinct_refs('lead_1', 'referal', user_id_here))
    count_leads_2 = len(request_to_db_distinct_refs('lead_2', 'referal', user_id_here))
    count_leads_all = count_leads_1 + count_leads_2
    # Накопленная сумма (1 и 2 уровни вместе)
    sum_leads_1 = request_to_db_sum_refs('sum_to_ref_0', 'referal', user_id_here)
    sum_leads_2 = request_to_db_sum_refs('sum_to_ref_lead_2_to_0', 'referal', user_id_here)
    if sum_leads_1 is None:
        sum_leads_1 = 0
    if sum_leads_2 is None:
        sum_leads_2 = 0
    sum_total = sum_leads_1 + sum_leads_2
    # Выплаченная сумма
    sum_pay_leads_1 = request_to_db_sum_multi_refs('sum_to_ref_0', 'referal', user_id_here, 'payout_lead_1_to_0', True)
    sum_pay_leads_2 = request_to_db_sum_multi_refs('sum_to_ref_lead_2_to_0', 'referal', user_id_here, 'payout_lead_2_to_0', True)
    if sum_pay_leads_1 is None:
        sum_pay_leads_1 = 0
    if sum_pay_leads_2 is None:
        sum_pay_leads_2 = 0
    sum_pay_total = sum_pay_leads_1 + sum_pay_leads_2
    sum_unpayed = sum_total - sum_pay_total

    await bot.send_message(user_id_here, f'🟣 Статистика на настоящее время:\n\n🟠 Зарегистрированных по реферальной ссылке всего: {count_leads_all}\n'
                         f'Их них\nПервого уровня: {count_leads_1}\nВторого уровня: {count_leads_2}\n\n'
                         f'🟢 Сумма реф. выплат всего: {sum_total}\nВыплаченная сумма: {sum_pay_total}\nНевыплаченная сумма: {sum_unpayed}')


async def run_db_export(user_id_here):
    await bot.send_message(user_id_here, 'Экспорт БД')
    zzz = db_export_ref(LIST_DATA_REF, 'lead_1', user_id_here)

    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_time_2 = str(date_time)
    csv_here = CSV_FILE_2 + date_time_2 + '.csv'

    with open(csv_here, mode='a', encoding='utf-8', newline='') as file:
        writer_object = writer(file)
        writer_object.writerow(LIST_SUBJECTS_REF)  # Заголовки в csv
        writer_object.writerows(zzz)
        file.close()

    await bot.send_document(user_id_here, FSInputFile(f"{csv_here}"))

    os.remove(csv_here)


async def run_db_export_vip(user_id_here):
    await bot.send_message(user_id_here, 'Экспорт БД')
    zzz = db_export_ref_vip(LIST_DATA_REF_VIP, 'referal', user_id_here)

    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_time_2 = str(date_time)
    csv_here = CSV_FILE_2 + date_time_2 + '.csv'

    with open(csv_here, mode='a', encoding='utf-8', newline='') as file:
        writer_object = writer(file)
        writer_object.writerow(LIST_SUBJECTS_REF_VIP)  # Заголовки в csv
        writer_object.writerows(zzz)
        file.close()

    await bot.send_document(user_id_here, FSInputFile(f"{csv_here}"))

    os.remove(csv_here)
