from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

i_kb_admin_1 = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Да, отправить',
            callback_data='yes_right'
        ),
        InlineKeyboardButton(
            text='Нет',
            callback_data='no_wrong'
        ),
        InlineKeyboardButton(
            text='Отмена',
            callback_data='cancel'
        )
    ]
])
