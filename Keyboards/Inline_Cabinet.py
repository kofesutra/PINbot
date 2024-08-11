from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

i_kb_cabinet_vip = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Инвайт-ссылка',
            callback_data='invitelink'
        ),
        InlineKeyboardButton(
            text='Статистика',
            callback_data='statistics'
        ),
        InlineKeyboardButton(
            text='Скачать',
            callback_data='download_statistics'
        )
    ],
    [
        InlineKeyboardButton(
            text='Назначить работника',
            callback_data='set_employee'
        ),
        InlineKeyboardButton(
            text='Убрать работника',
            callback_data='remove_employee'
        ),
        InlineKeyboardButton(
            text='Как назначить',
            callback_data='howto_employee'
        )
    ],
    [
        InlineKeyboardButton(
            text='Оплата',
            callback_data='payment'
        ),
        InlineKeyboardButton(
            text='Тарифы',
            callback_data='tarifs'
        )
    ]
])


i_kb_cabinet_lead_1_full = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Инвайт-ссылка',
            callback_data='invitelink'
        ),
        InlineKeyboardButton(
            text='Статистика',
            callback_data='statistics'
        ),
        InlineKeyboardButton(
            text='Скачать',
            callback_data='download_statistics'
        )
    ],
    [
        InlineKeyboardButton(
            text='Назначить работника',
            callback_data='set_employee'
        ),
        InlineKeyboardButton(
            text='Убрать работника',
            callback_data='remove_employee'
        ),
        InlineKeyboardButton(
            text='Как назначить',
            callback_data='howto_employee'
        )
    ],
    [
        InlineKeyboardButton(
            text='Оплата',
            callback_data='payment'
        ),
        InlineKeyboardButton(
            text='Тарифы',
            callback_data='tarifs'
        )
    ]
])


i_kb_cabinet_lead_1_not_full = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Оплата',
            callback_data='payment'
        ),
        InlineKeyboardButton(
            text='Тарифы',
            callback_data='tarifs'
        )
    ],
    [
        InlineKeyboardButton(
            text='Назначить работника',
            callback_data='set_employee'
        ),
        InlineKeyboardButton(
            text='Убрать работника',
            callback_data='remove_employee'
        ),
        InlineKeyboardButton(
            text='Как назначить',
            callback_data='howto_employee'
        )
    ]
])


i_kb_cabinet_lead_2 = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Оплата',
            callback_data='payment'
        ),
        InlineKeyboardButton(
            text='Тарифы',
            callback_data='tarifs'
        )
    ]
])

i_kb_cabinet_others = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Оплата',
            callback_data='payment'
        ),
        InlineKeyboardButton(
            text='Тарифы',
            callback_data='tarifs'
        )
    ]
])

