from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

kb_1 = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='УЗНАТЬ ПОДРОБНЕЕ',
            url='https://t.me/detox_dieta/22'
        )
    ]
])

kb_2 = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='УЗНАТЬ ПОДРОБНЕЕ О FMD ДЕТОКС',
            url='https://t.me/detox_dieta/22'
        )
    ],
    [
        InlineKeyboardButton(
            text='В ГОСТИ К УМКЕ_Боту',
            url='https://t.me/u_m_k_a_bot'
        )
    ]
])

kb_3 = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='ПЕРЕЙТИ к УМКЕ_Боту',
            url='https://t.me/u_m_k_a_bot'
        )
    ]
])

i_kb_1 = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='ДА',
            callback_data='yes_picture'
        ),
        InlineKeyboardButton(
            text='НЕТ',
            callback_data='no_picture'
        )
    ]
])

i_kb_2 = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='ДА',
            callback_data='yes_button'
        ),
        InlineKeyboardButton(
            text='НЕТ',
            callback_data='no_button'
        )
    ]
])

i_kb_3 = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Давай',
            callback_data='yes_check'
        )
    ]
])

i_kb_4 = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='ДА',
            callback_data='yes_text'
        ),
        InlineKeyboardButton(
            text='НЕТ',
            callback_data='no_text'
        )
    ]
])

i_kb_5 = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='ДА',
            callback_data='yes_post'
        ),
        InlineKeyboardButton(
            text='НЕТ',
            callback_data='no_post'
        )
    ]
])

i_kb_6 = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Картинку',
            callback_data='change_picture'
        ),
        InlineKeyboardButton(
            text='Текст',
            callback_data='change_text'
        ),
        InlineKeyboardButton(
            text='Кнопку',
            callback_data='change_button'
        )
    ]
])

i_kb_7 = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Прислать готовый',
            callback_data='send_ready'
        ),
        InlineKeyboardButton(
            text='Оформить здесь',
            callback_data='make_here'
        )
    ]
])

i_kb_8 = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Сейчас',
            callback_data='now'
        ),
        InlineKeyboardButton(
            text='Отложить',
            callback_data='later'
        )
    ]
])

i_kb_9 = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Всё верно',
            callback_data='right'
        ),
        InlineKeyboardButton(
            text='Нет, ошибочка',
            callback_data='wrong'
        )
    ]
])

i_kb_10 = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Да, верно',
            callback_data='right'
        ),
        InlineKeyboardButton(
            text='Нет, ошибочка',
            callback_data='wrong'
        )
    ]
])

i_kb_11 = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Готово',
            callback_data='done'
        ),
        InlineKeyboardButton(
            text='Как добавить?',
            callback_data='how'
        )
    ]
])

i_kb_12 = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Вернуться назад и проверить',
            callback_data='back'
        )
    ]
])

i_kb_12_2 = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Готово',
            callback_data='done'
        ),
        InlineKeyboardButton(
            text='Вернуться назад',
            callback_data='back'
        )
    ]
])

i_kb_13 = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Далее',
            callback_data='next'
        )
    ]
])

i_kb_14 = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Редактировать пост',
            callback_data='modify'
        ),
        InlineKeyboardButton(
            text='Изменить время',
            callback_data='change_time'
        )
    ],
    [
        InlineKeyboardButton(
            text='Отключить',
            callback_data='switch_off'
        ),
        InlineKeyboardButton(
            text='Назад',
            callback_data='status_cancel'
        )
    ]
])

i_kb_15 = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Изменить время',
            callback_data='yes_change_time'
        ),
        InlineKeyboardButton(
            text='Не изменять',
            callback_data='status_cancel'
        )
    ]
])


i_kb_payments = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='1 месяц: 1020р.',
            callback_data='month_1'
        ),
        InlineKeyboardButton(
            text='3 месяца: 3060р.',
            callback_data='month_3'
        )
    ],
    [
        InlineKeyboardButton(
        text='6 месяцев: 5508р.',
        callback_data='month_6'
    ),
        InlineKeyboardButton(
            text='12 месяцев: 9792р.',
            callback_data='month_12'
        )
    ]
])
