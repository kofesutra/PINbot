from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

r_kb_1 = ReplyKeyboardMarkup(resize_keyboard=True,
                             keyboard=[
                                 [
                                     KeyboardButton(text='Начать заново'),
                                     KeyboardButton(text='Техподдержка')
                                 ]
                             ]
                             )

# r_kb_2 = ReplyKeyboardMarkup(resize_keyboard=True,
#                              keyboard=[
#                                  [
#                                      KeyboardButton(text='Начать заново'),
#                                      KeyboardButton(text='Статус бота'),
#                                      KeyboardButton(text='Техподдержка')
#                                  ],
#                                  [
#                                      KeyboardButton(text='Остановить бота'),
#                                      KeyboardButton(text='Запустить бота'),
#                                      # KeyboardButton(text='Изменить время отложки'),
#                                      KeyboardButton(text='Удалить время отложки')
#                                  ]
#                              ]
#                              )

r_kb_2 = ReplyKeyboardMarkup(resize_keyboard=True,
                             keyboard=[
                                 [
                                     KeyboardButton(text='Новый пост'),
                                     KeyboardButton(text='Статус'),
                                     KeyboardButton(text='Кабинет'),
                                     KeyboardButton(text='Техподдержка')
                                 ]
                             ]
                             )

r_kb_3 = ReplyKeyboardMarkup(resize_keyboard=True,
                             keyboard=[
                                 [
                                     KeyboardButton(text='Новый пост'),
                                     KeyboardButton(text='Техподдержка')
                                 ]
                             ]
                             )
