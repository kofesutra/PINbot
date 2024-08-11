from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def build_inline(text, link):
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=text,
                url=link
            )
        ]
    ])
    return inline_keyboard


def build_inline_pay(link):
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Оплатить',
                url=link
            ),
            InlineKeyboardButton(
                text='Готово',
                callback_data='check_payment'
            )
        ]
    ])
    return inline_keyboard
