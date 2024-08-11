from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_keyboard_year(year):
    year_2 = year + 1
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=f'{year}',
                callback_data=f'{year}'
            ),
            InlineKeyboardButton(
                text=f'{year_2}',
                callback_data=f'{year_2}'
            )
        ]
    ])
    return kb


i_month = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='ЯНВ',
            callback_data='январь'
        ),
        InlineKeyboardButton(
            text='ФЕВ',
            callback_data='февраль'
        ),
        InlineKeyboardButton(
            text='МАР',
            callback_data='март'
        ),
        InlineKeyboardButton(
            text='АПР',
            callback_data='апрель'
        )
    ],
    [
        InlineKeyboardButton(
            text='МАЙ',
            callback_data='май'
        ),
        InlineKeyboardButton(
            text='ИЮН',
            callback_data='июнь'
        ),
        InlineKeyboardButton(
            text='ИЮЛ',
            callback_data='июль'
        ),
        InlineKeyboardButton(
            text='АВГ',
            callback_data='август'
        )
    ],
    [
        InlineKeyboardButton(
            text='СЕН',
            callback_data='сентябрь'
        ),
        InlineKeyboardButton(
            text='ОКТ',
            callback_data='октябрь'
        ),
        InlineKeyboardButton(
            text='НОЯ',
            callback_data='ноябрь'
        ),
        InlineKeyboardButton(
            text='ДЕК',
            callback_data='декабрь'
        )
    ]
])


def get_month_number(input):
    if input == 'январь':
        return 1
    elif input == 'февраль':
        return 2
    elif input == 'март':
        return 3
    elif input == 'апрель':
        return 4
    elif input == 'май':
        return 5
    elif input == 'июнь':
        return 6
    elif input == 'июль':
        return 7
    elif input == 'август':
        return 8
    elif input == 'сентябрь':
        return 9
    elif input == 'октябрь':
        return 10
    elif input == 'ноябрь':
        return 11
    elif input == 'декабрь':
        return 12


def get_keyboard_days(days):
    if days == 28:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text='1', callback_data='1'),
                InlineKeyboardButton(text='2', callback_data='2'),
                InlineKeyboardButton(text='3', callback_data='3'),
                InlineKeyboardButton(text='4', callback_data='4'),
                InlineKeyboardButton(text='5', callback_data='5'),
                InlineKeyboardButton(text='6', callback_data='6'),
                InlineKeyboardButton(text='7', callback_data='7')
            ],
            [
                InlineKeyboardButton(text='8', callback_data='8'),
                InlineKeyboardButton(text='9', callback_data='9'),
                InlineKeyboardButton(text='10', callback_data='10'),
                InlineKeyboardButton(text='11', callback_data='11'),
                InlineKeyboardButton(text='12', callback_data='12'),
                InlineKeyboardButton(text='13', callback_data='13'),
                InlineKeyboardButton(text='14', callback_data='14')
            ],
            [
                InlineKeyboardButton(text='15', callback_data='15'),
                InlineKeyboardButton(text='16', callback_data='16'),
                InlineKeyboardButton(text='17', callback_data='17'),
                InlineKeyboardButton(text='18', callback_data='18'),
                InlineKeyboardButton(text='19', callback_data='19'),
                InlineKeyboardButton(text='20', callback_data='20'),
                InlineKeyboardButton(text='21', callback_data='21')
            ],
            [
                InlineKeyboardButton(text='22', callback_data='22'),
                InlineKeyboardButton(text='23', callback_data='23'),
                InlineKeyboardButton(text='24', callback_data='24'),
                InlineKeyboardButton(text='25', callback_data='25'),
                InlineKeyboardButton(text='26', callback_data='26'),
                InlineKeyboardButton(text='27', callback_data='27'),
                InlineKeyboardButton(text='28', callback_data='28')
            ]
        ])
        return kb

    elif days == 29:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text='1', callback_data='1'),
                InlineKeyboardButton(text='2', callback_data='2'),
                InlineKeyboardButton(text='3', callback_data='3'),
                InlineKeyboardButton(text='4', callback_data='4'),
                InlineKeyboardButton(text='5', callback_data='5'),
                InlineKeyboardButton(text='6', callback_data='6'),
                InlineKeyboardButton(text='7', callback_data='7')
            ],
            [
                InlineKeyboardButton(text='8', callback_data='8'),
                InlineKeyboardButton(text='9', callback_data='9'),
                InlineKeyboardButton(text='10', callback_data='10'),
                InlineKeyboardButton(text='11', callback_data='11'),
                InlineKeyboardButton(text='12', callback_data='12'),
                InlineKeyboardButton(text='13', callback_data='13'),
                InlineKeyboardButton(text='14', callback_data='14')
            ],
            [
                InlineKeyboardButton(text='15', callback_data='15'),
                InlineKeyboardButton(text='16', callback_data='16'),
                InlineKeyboardButton(text='17', callback_data='17'),
                InlineKeyboardButton(text='18', callback_data='18'),
                InlineKeyboardButton(text='19', callback_data='19'),
                InlineKeyboardButton(text='20', callback_data='20'),
                InlineKeyboardButton(text='21', callback_data='21')
            ],
            [
                InlineKeyboardButton(text='22', callback_data='22'),
                InlineKeyboardButton(text='23', callback_data='23'),
                InlineKeyboardButton(text='24', callback_data='24'),
                InlineKeyboardButton(text='25', callback_data='25'),
                InlineKeyboardButton(text='26', callback_data='26'),
                InlineKeyboardButton(text='27', callback_data='27'),
                InlineKeyboardButton(text='28', callback_data='28')
            ],
            [
                InlineKeyboardButton(text='29', callback_data='29')
            ]
        ])
        return kb

    elif days == 30:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text='1', callback_data='1'),
                InlineKeyboardButton(text='2', callback_data='2'),
                InlineKeyboardButton(text='3', callback_data='3'),
                InlineKeyboardButton(text='4', callback_data='4'),
                InlineKeyboardButton(text='5', callback_data='5'),
                InlineKeyboardButton(text='6', callback_data='6'),
                InlineKeyboardButton(text='7', callback_data='7')
            ],
            [
                InlineKeyboardButton(text='8', callback_data='8'),
                InlineKeyboardButton(text='9', callback_data='9'),
                InlineKeyboardButton(text='10', callback_data='10'),
                InlineKeyboardButton(text='11', callback_data='11'),
                InlineKeyboardButton(text='12', callback_data='12'),
                InlineKeyboardButton(text='13', callback_data='13'),
                InlineKeyboardButton(text='14', callback_data='14')
            ],
            [
                InlineKeyboardButton(text='15', callback_data='15'),
                InlineKeyboardButton(text='16', callback_data='16'),
                InlineKeyboardButton(text='17', callback_data='17'),
                InlineKeyboardButton(text='18', callback_data='18'),
                InlineKeyboardButton(text='19', callback_data='19'),
                InlineKeyboardButton(text='20', callback_data='20'),
                InlineKeyboardButton(text='21', callback_data='21')
            ],
            [
                InlineKeyboardButton(text='22', callback_data='22'),
                InlineKeyboardButton(text='23', callback_data='23'),
                InlineKeyboardButton(text='24', callback_data='24'),
                InlineKeyboardButton(text='25', callback_data='25'),
                InlineKeyboardButton(text='26', callback_data='26'),
                InlineKeyboardButton(text='27', callback_data='27'),
                InlineKeyboardButton(text='28', callback_data='28')
            ],
            [
                InlineKeyboardButton(text='29', callback_data='29'),
                InlineKeyboardButton(text='30', callback_data='30')
            ]
        ])
        return kb

    else:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text='1', callback_data='1'),
                InlineKeyboardButton(text='2', callback_data='2'),
                InlineKeyboardButton(text='3', callback_data='3'),
                InlineKeyboardButton(text='4', callback_data='4'),
                InlineKeyboardButton(text='5', callback_data='5'),
                InlineKeyboardButton(text='6', callback_data='6'),
                InlineKeyboardButton(text='7', callback_data='7')
            ],
            [
                InlineKeyboardButton(text='8', callback_data='8'),
                InlineKeyboardButton(text='9', callback_data='9'),
                InlineKeyboardButton(text='10', callback_data='10'),
                InlineKeyboardButton(text='11', callback_data='11'),
                InlineKeyboardButton(text='12', callback_data='12'),
                InlineKeyboardButton(text='13', callback_data='13'),
                InlineKeyboardButton(text='14', callback_data='14')
            ],
            [
                InlineKeyboardButton(text='15', callback_data='15'),
                InlineKeyboardButton(text='16', callback_data='16'),
                InlineKeyboardButton(text='17', callback_data='17'),
                InlineKeyboardButton(text='18', callback_data='18'),
                InlineKeyboardButton(text='19', callback_data='19'),
                InlineKeyboardButton(text='20', callback_data='20'),
                InlineKeyboardButton(text='21', callback_data='21')
            ],
            [
                InlineKeyboardButton(text='22', callback_data='22'),
                InlineKeyboardButton(text='23', callback_data='23'),
                InlineKeyboardButton(text='24', callback_data='24'),
                InlineKeyboardButton(text='25', callback_data='25'),
                InlineKeyboardButton(text='26', callback_data='26'),
                InlineKeyboardButton(text='27', callback_data='27'),
                InlineKeyboardButton(text='28', callback_data='28')
            ],
            [
                InlineKeyboardButton(text='29', callback_data='29'),
                InlineKeyboardButton(text='30', callback_data='30'),
                InlineKeyboardButton(text='31', callback_data='31')
            ]
        ])
        return kb

get_keyboard_hour = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='0', callback_data='0'),
            InlineKeyboardButton(text='1', callback_data='1'),
            InlineKeyboardButton(text='2', callback_data='2'),
            InlineKeyboardButton(text='3', callback_data='3'),
            InlineKeyboardButton(text='4', callback_data='4'),
            InlineKeyboardButton(text='5', callback_data='5')
        ],
        [
            InlineKeyboardButton(text='6', callback_data='6'),
            InlineKeyboardButton(text='7', callback_data='7'),
            InlineKeyboardButton(text='8', callback_data='8'),
            InlineKeyboardButton(text='9', callback_data='9'),
            InlineKeyboardButton(text='10', callback_data='10'),
            InlineKeyboardButton(text='11', callback_data='11')
        ],
        [
            InlineKeyboardButton(text='12', callback_data='12'),
            InlineKeyboardButton(text='13', callback_data='13'),
            InlineKeyboardButton(text='14', callback_data='14'),
            InlineKeyboardButton(text='15', callback_data='15'),
            InlineKeyboardButton(text='16', callback_data='16'),
            InlineKeyboardButton(text='17', callback_data='17')
        ],
        [
            InlineKeyboardButton(text='18', callback_data='18'),
            InlineKeyboardButton(text='19', callback_data='19'),
            InlineKeyboardButton(text='20', callback_data='20'),
            InlineKeyboardButton(text='21', callback_data='21'),
            InlineKeyboardButton(text='22', callback_data='22'),
            InlineKeyboardButton(text='23', callback_data='23')
        ]
    ])

get_keyboard_minutes = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='00', callback_data='0'),
            InlineKeyboardButton(text='05', callback_data='5'),
            InlineKeyboardButton(text='10', callback_data='10'),
            InlineKeyboardButton(text='15', callback_data='15')
        ],
        [
            InlineKeyboardButton(text='20', callback_data='20'),
            InlineKeyboardButton(text='25', callback_data='25'),
            InlineKeyboardButton(text='30', callback_data='30'),
            InlineKeyboardButton(text='35', callback_data='35')
        ],
        [
            InlineKeyboardButton(text='40', callback_data='40'),
            InlineKeyboardButton(text='45', callback_data='45'),
            InlineKeyboardButton(text='50', callback_data='50'),
            InlineKeyboardButton(text='55', callback_data='55')
        ]
    ])
