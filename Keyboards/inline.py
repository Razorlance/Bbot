from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

mailing_answer = CallbackData("pref", "name", "action")

btn_1 = KeyboardButton('Да')
btn_2 = KeyboardButton('Нет')
inline_kb1 = ReplyKeyboardMarkup(resize_keyboard=True)
inline_kb1.add(btn_1).add(btn_2)

button1 = KeyboardButton('Ссылки')
button2 = KeyboardButton('Топ банов')
cancel_button = KeyboardButton('Отмена')

cancel_markup = ReplyKeyboardMarkup(resize_keyboard=True).add(cancel_button)

markup4 = ReplyKeyboardMarkup().row(
    button1, button2,
)

regular_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).row(
    button1, button2
).add(KeyboardButton('Создать событие'))

admin_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).row(
    button1, button2
).add(KeyboardButton('Создать событие')).add(KeyboardButton('Создать рассылку'))

# markup5.insert(button6)
