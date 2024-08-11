from Utils.Process_Invitelink import process_invite_link
from Utils.Process_Worker import process_worker_link


async def process_deeplinks(link, state, bot):
    result = '_'
    if 'Начать заново' in link:
        result = 'заново'
        await state.update_data(come_from=result)
        return result
    elif 'start' in link:
        srez = link[7:]  # Обрезаем в нём первые символы '/start '
        if not srez:  # Если строка пустая
            user_id_inviter = 1000  # Обрезаем в нём ещё символы 'invitelink' и получаем id юзера из ссылки
            result = '1000'
            await state.update_data(come_from=result)
            await state.update_data(user_id_inviter=user_id_inviter)
            await process_invite_link(user_id_inviter, state, bot)
            return result
        else:
            if 'altenter' in link:
                result = 'альтернативный'
                await state.update_data(come_from=result)
                return result

            elif 'invitelink' in link:
                user_id_inviter = link[17:]  # Обрезаем в нём ещё символы 'invitelink' и получаем id юзера из ссылки
                result = 'invitelink'
                await state.update_data(come_from=user_id_inviter)
                await state.update_data(user_id_inviter=user_id_inviter)
                await process_invite_link(user_id_inviter, state, bot)
                return result
            elif 'worker' in link:
                user_id_inviter = link[13:]  # Обрезаем в нём ещё символы 'invitelink' и получаем id юзера из ссылки
                result = 'worker'
                await state.update_data(come_from=user_id_inviter)
                await state.update_data(user_id_inviter=user_id_inviter)
                await process_worker_link(user_id_inviter, state, bot)
                return result
            else:
                result = srez
                await state.update_data(come_from=result)
                return result
