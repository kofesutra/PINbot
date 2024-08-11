from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

r_kb_admin = ReplyKeyboardMarkup(resize_keyboard=True,
                                 keyboard=[
                                     [
                                         KeyboardButton(text='Ping'),
                                         KeyboardButton(text='База'),
                                         KeyboardButton(text='Логи'),
                                         KeyboardButton(text='Письмо'),
                                         KeyboardButton(text='Рассылка')
                                     ]
                                 ]
                                 )
