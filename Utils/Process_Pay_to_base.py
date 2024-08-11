from datetime import datetime

from DB.DB_Refs_Utils import request_to_db_single_refs, get_max_id_refs, update_values_db_refs, add_all_to_db_refs
from DB.DB_utils import update_values_db_two


async def insert_payment_to_base(user_id_here, is_paid, pay_date, end_date, summ, label, paid_month_count, state, bot):
    # Найти в базе кто есть юзер: лид_1 или лид_2
    # и внести запись об оплатах по ранжиру

    # Внос в основную базу
    list_values_of_DB = f"is_payed='{is_paid}'," \
                        f"date_of_pay='{pay_date}'," \
                        f"date_of_end='{end_date}'," \
                        f"sum_of_pay='{summ}'," \
                        f"pay_label='{label}'," \
                        f"paid_month_count='{paid_month_count}'"
    update_values_db_two(list_values_of_DB, 'user_id', user_id_here)

    # Внос в базу refs
    # Проверить нет ли юзера в базе по трём столбцам: вип, лид_1 и лид_2
    is_referal = request_to_db_single_refs('id', 'referal', user_id_here)
    is_lead_1 = request_to_db_single_refs('id', 'lead_1', user_id_here)
    is_lead_2 = request_to_db_single_refs('id', 'lead_2', user_id_here)

    # Если юзер Лид_1
    if is_lead_1 is not None and is_lead_2 is None:

        # Изменение статуса lead_1 на lead_1_full если оплата 3 месяца и более
        if paid_month_count >= 3:
            list_values_of_DB = f"user_status='lead_1_full'"
            update_values_db_two(list_values_of_DB, 'user_id', user_id_here)

        ref_id_0 = request_to_db_single_refs('referal', 'lead_1', user_id_here)
        ref_username_0 = request_to_db_single_refs('referal_username', 'referal', ref_id_0)
        username_here = request_to_db_single_refs('lead_1_username', 'lead_1', user_id_here)

        if type(summ) != int:
            summ = int(summ)
        sum_to_ref_0 = round(summ - summ / 100 * 80, 2)

        # Получаем из базы последнюю строку id юзера
        id_here = get_max_id_refs('lead_1', user_id_here)
        sum_of_pay_here = request_to_db_single_refs('sum_of_pay_lead_1', 'id', id_here)
        datetime_here = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Сумма оплаты не указана (платежа не было)
        if sum_of_pay_here is None:
            # Вносим изменения в базу
            list_values_of_DB = f"paid_by_lead_1='True'," \
                                f"date_of_pay_lead_1='{datetime_here}'," \
                                f"sum_of_pay_lead_1='{summ}',"\
                                f"sum_to_ref_0='{sum_to_ref_0}'"
            update_values_db_refs(list_values_of_DB, 'id', id_here)

        else:
            # Добавляем новую строку
            list_subjects_of_DB = "referal, lead_1, referal_username, lead_1_username, paid_by_lead_1, date_of_pay_lead_1, sum_of_pay_lead_1, sum_to_ref_0"
            list_data_of_DB = f"{ref_id_0}, '{user_id_here}', '{ref_username_0}', '{username_here}', 'True', '{datetime_here}', '{summ}', '{sum_to_ref_0}'"
            add_all_to_db_refs(list_subjects_of_DB, list_data_of_DB)

    # Если юзер Лид_2
    elif is_lead_1 is None and is_lead_2 is not None:
        # TODO Если оплачены 3 месяца и более, то учитывать Лида_2 как Лида_1 под 1000
        #  но проверить согласование выплат им Лиду_1 и ВИПу

        # Изменение статуса lead_2 на lead_1_full если оплата 3 месяца и более
        # if paid_month_count >= 3:
        #     list_values_of_DB = f"user_status='lead_1_full'"
        #     update_values_db_two(list_values_of_DB, 'user_id', user_id_here)

        lead_id_1 = request_to_db_single_refs('lead_1', 'lead_2', user_id_here)  # Получение id Лида_1
        ref_id_0 = request_to_db_single_refs('referal', 'lead_1', lead_id_1)  # Получение id Рефа
        lead_username_1 = request_to_db_single_refs('lead_1_username', 'lead_1', lead_id_1)
        ref_username_0 = request_to_db_single_refs('referal_username', 'referal', ref_id_0)
        username_here = request_to_db_single_refs('lead_2_username', 'lead_2', user_id_here)

        if type(summ) != int:
            summ = int(summ)
        sum_to_ref_0 = round(summ - summ / 100 * 95, 2)
        sum_to_lead_1 = round(summ - summ / 100 * 85, 2)

        # Получаем из базы последнюю строку id юзера
        id_here = get_max_id_refs('lead_2', user_id_here)
        sum_of_pay_here = request_to_db_single_refs('sum_of_pay_lead_2', 'id', id_here)
        datetime_here = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Сумма оплаты не указана (платежа не было)
        if sum_of_pay_here is None:
            # Вносим изменения в базу
            list_values_of_DB = f"paid_by_lead_2='True'," \
                                f"date_of_pay_lead_2='{datetime_here}'," \
                                f"sum_of_pay_lead_2='{summ}',"\
                                f"sum_to_ref_lead_2_to_0='{sum_to_ref_0}'," \
                                f"sum_to_ref_lead_2_to_1='{sum_to_lead_1}'"
            update_values_db_refs(list_values_of_DB, 'id', id_here)

        else:
            # Добавляем новую строку
            list_subjects_of_DB = "referal, lead_1, lead_2, referal_username, lead_1_username, lead_2_username, " \
                                  "paid_by_lead_2, date_of_pay_lead_2, sum_of_pay_lead_2, sum_to_ref_lead_2_to_0, sum_to_ref_lead_2_to_1"
            list_data_of_DB = f"{ref_id_0}, '{lead_id_1}', '{user_id_here}', '{ref_username_0}', '{lead_username_1}', '{username_here}', " \
                              f"'True', '{datetime_here}', '{summ}', '{sum_to_ref_0}', '{sum_to_lead_1}'"
            add_all_to_db_refs(list_subjects_of_DB, list_data_of_DB)
