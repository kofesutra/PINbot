from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

i_kb_emp_1 = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Да, правильно',
            callback_data='yes'
        ),
        InlineKeyboardButton(
            text='Нет, ошибочка',
            callback_data='no'
        )
    ]
])


def i_kb_list_for_remove(count):
    if count == 1:
        i_kb_lfr = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='1',
                    callback_data='1'
                )
            ]
        ])
        return i_kb_lfr
    elif count == 2:
        i_kb_lfr = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='1',
                    callback_data='1'
                ),
                InlineKeyboardButton(
                    text='2',
                    callback_data='2'
                )
            ]
        ])
        return i_kb_lfr
    elif count == 3:
        i_kb_lfr = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='1',
                    callback_data='1'
                ),
                InlineKeyboardButton(
                    text='2',
                    callback_data='2'
                ),
                InlineKeyboardButton(
                    text='3',
                    callback_data='3'
                )
            ]
        ])
        return i_kb_lfr
    elif count == 4:
        i_kb_lfr = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='1',
                    callback_data='1'
                ),
                InlineKeyboardButton(
                    text='2',
                    callback_data='2'
                ),
                InlineKeyboardButton(
                    text='3',
                    callback_data='3'
                ),
                InlineKeyboardButton(
                    text='4',
                    callback_data='4'
                )
            ]
        ])
        return i_kb_lfr
    elif count == 5:
        i_kb_lfr = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='1',
                    callback_data='1'
                ),
                InlineKeyboardButton(
                    text='2',
                    callback_data='2'
                ),
                InlineKeyboardButton(
                    text='3',
                    callback_data='3'
                ),
                InlineKeyboardButton(
                    text='4',
                    callback_data='4'
                ),
                InlineKeyboardButton(
                    text='5',
                    callback_data='5'
                )
            ]
        ])
        return i_kb_lfr


i_kb_worker_reg = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Хорошо!',
            callback_data='registration_ok'
        )
    ]
])
