from DB.DB_Refs_Utils import request_to_db_single_refs, add_all_to_db_refs
from DB.DB_utils import update_values_db_two


async def process_invite_link(user_id_inviter, state, bot):
    # ID из ссылки (приглашающий) и текущего юзера не совпадают
    data = await state.get_data()
    user_id_here = data['user_id']
    username = data['username']
    if user_id_inviter != user_id_here:
        # Первый вход лида

        # Проверить нет ли юзера в базе по трём столбцам: вип, лид_1 и лид_2
        is_referal = request_to_db_single_refs('id', 'referal', user_id_here)
        is_lead_1 = request_to_db_single_refs('id', 'lead_1', user_id_here)
        is_lead_2 = request_to_db_single_refs('id', 'lead_2', user_id_here)
        # Проверить наличие ВИПА и Лида_1 по инвайт-номеру
        referal_0 = request_to_db_single_refs('id', 'referal', user_id_inviter)
        referal_1 = request_to_db_single_refs('id', 'lead_1', user_id_inviter)

        if is_referal is None and is_lead_1 is None and is_lead_2 is None:
            # Если инвайт от ВИПА
            if referal_0 is not None and referal_1 is None:
                # Вносим юзера в базу рефов как Лид_1
                username_inviter = request_to_db_single_refs('referal_username', 'referal', user_id_inviter)
                list_subjects_of_DB = "referal, lead_1, referal_username, lead_1_username"
                list_data_of_DB = f"{user_id_inviter}, '{user_id_here}', '{username_inviter}', '{username}'"
                add_all_to_db_refs(list_subjects_of_DB, list_data_of_DB)

                # Вносим юзера в основную базу как Лид_1
                list_values_of_DB = f"user_status='lead_1'"
                update_values_db_two(list_values_of_DB, 'user_id', user_id_here)

            # Если инвайт от Лида_1
            elif referal_0 is None and referal_1 is not None:
                # Вносим юзера в базу рефов как Лид_2
                referal_0_here = request_to_db_single_refs('referal', 'lead_1', user_id_inviter)
                referal_username_0_here = request_to_db_single_refs('referal_username', 'referal', referal_0_here)
                username_inviter = request_to_db_single_refs('lead_1_username', 'lead_1', user_id_inviter)
                list_subjects_of_DB = "referal, lead_1, lead_2, referal_username, lead_1_username, lead_2_username"
                list_data_of_DB = f"{referal_0_here}, '{user_id_inviter}', '{user_id_here}', '{referal_username_0_here}', '{username_inviter}', '{username}'"
                add_all_to_db_refs(list_subjects_of_DB, list_data_of_DB)

                # Вносим юзера в основную базу как Лид_2
                list_values_of_DB = f"user_status='lead_2'"
                update_values_db_two(list_values_of_DB, 'user_id', user_id_here)

            else:
                # Вносим юзера как лид_1 для рефа 1000
                list_subjects_of_DB = "referal, lead_1, referal_username, lead_1_username"
                list_data_of_DB = f"1000, '{user_id_here}', '1000', '{username}'"
                add_all_to_db_refs(list_subjects_of_DB, list_data_of_DB)

                # Вносим юзера в основную базу как Лид_1 от 1000
                list_values_of_DB = f"user_status='lead_1'"
                update_values_db_two(list_values_of_DB, 'user_id', user_id_here)
        else:
            return

    else:  # if user_id_inviter != user_id_here:
        return
