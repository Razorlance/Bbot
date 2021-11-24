from aiogram import types, bot
import asyncio
import operator
from config import *
from Filters import filters_list
from aiogram.dispatcher import FSMContext
from Keyboards.inline import regular_keyboard, admin_keyboard, inline_kb1, cancel_markup
from Utils.states_list import States

mailing_messages = {}
event_messages = {}


@dp.message_handler(state="*", commands=['remove_keyboard'])
async def remove_keyboard(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply('Клавиатура скрыта, чтобы с вернуть напишить /start', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(commands=['make_admin'])
async def myrights(message: types.Message):
    await bot.send_message(admins[0],
                           "".join([str(message.chat.id) + "\n", "@" + str(message.from_user.username) + "\n",
                                    str(message.from_user.first_name) + " " + str(message.from_user.last_name)]))
    await message.answer("Запрос отправлен")


@dp.message_handler(commands=['info'])
@dp.message_handler(regexp="Ссылки")
async def send_info(message: types.Message):
    await message.answer(messages_text["info"], parse_mode="HTML", disable_web_page_preview=True)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    user_name = str(message.from_user.first_name) + " " + str(message.from_user.last_name)
    if message.from_user.id not in members:
        users['members'].append(message.from_user.id)
        users['member_bans']["@" + message.from_user.username] = 0
        users['member_names']["@" + message.from_user.username] = user_name
        users['member_bans'] = dict(sorted(users['member_bans'].items(), key=lambda item: item[1], reverse=True))
    await message.answer("Привет, я бот, созданный специально для ботария. Люби меня. Или бан.",
                         reply_markup=regular_keyboard)


@dp.message_handler(commands=["admin_panel"], is_admin=True)
async def send_admin_panel(message: types.Message):
    await message.answer("Вот админ панель:", reply_markup=admin_keyboard)


@dp.message_handler(commands=["ban"])
async def ban_user(message: types.Message):
    await message.answer("Админа забанил Амазон поэтому функция оффлайн. Пока...", reply_markup=regular_keyboard)    #
    # m = message.get_args().split(" ")
    # banned_members = list(users['member_bans'])
    # try:
    #     await dp.throttle('ban', rate=1800)
    #     if len(m) == 1 and m[0] in banned_members and m[0] != '':
    #         if "@" + message.from_user.username != m[0]:
    #             users['member_bans'][m[0]] += 1
    #             await message.answer("Пользователь с именем {} был забанен".format(m[0]), reply_markup=regular_keyboard)
    #         else:
    #             users['member_bans'][m[0]] -= 1
    #             await message.answer("Пользователь с именем {} был разбанен".format(m[0]),
    #                                  reply_markup=regular_keyboard)
    #         users['member_bans'] = dict(sorted(users['member_bans'].items(), key=lambda item: item[1], reverse=True))
    #         client.put_object(
    #             Body=json.dumps(users),
    #             Bucket=BUCKET,
    #             Key=FILE_TO_READ,
    #         )
    #
    # except:
    #     await message.answer("Ты в бане. Жди❤")


@dp.message_handler(regexp="Топ банов")
@dp.message_handler(commands=["ban_list"])
async def show_ban_list(message: types.Message):
    top = ""
    for k, v in users['member_bans'].items():
        top += users['member_names'][k] + ": " + str(v) + "\n"
    await message.answer("<b>🛑Tоп забаненных пользователей🛑</b>\n" + top, parse_mode="HTML",
                         reply_markup=regular_keyboard)


@dp.message_handler(regexp="Создать рассылку", is_admin=True, state='*')
async def process_setstate_command(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(States.all()[1])
    await message.answer("Введите текст рассылки:", reply_markup=cancel_markup)


@dp.message_handler(state=States.CREATE_MAILING, regexp="Отмена", is_admin=True)
async def first_test_state_case_met(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.reset_state()
    await message.answer('Отмена...', reply_markup=admin_keyboard)


@dp.message_handler(state=States.CREATE_MAILING, is_admin=True)
async def first_test_state_case_met(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    mailing_messages[str(message.from_user.id)] = message
    await state.set_state(States.all()[3])
    await message.reply('Вы уверены, что хотите отправить сообщение?', reply_markup=inline_kb1)


@dp.message_handler(regexp="Да", state=States.SEND_MAILING, is_admin=True)
async def first_test_state_case_met(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    mail = mailing_messages[str(message.from_user.id)]
    num = 0
    for member in members:
        num += 1
        a = await bot.send_message(member, mail.text)
        await bot.pin_chat_message(member, a.message_id)
    await state.reset_state()
    await message.answer('Сообщение отправленно {} пользователям'.format(num), reply_markup=admin_keyboard)


@dp.message_handler(regexp="Нет", state=States.SEND_MAILING, is_admin=True)
async def first_test_state_case_met(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.reset_state()
    await message.reply('Отмена...', reply_markup=admin_keyboard)


@dp.message_handler(regexp="Создать событие", state='*')
async def process_setstate_command(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(States.all()[0])
    await message.answer("Введите название событие:", reply_markup=cancel_markup)


@dp.message_handler(state=States.CREATE_EVENT, regexp="Отмена", is_admin=True)
async def process_setstate_command(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.reset_state()
    await message.answer('Отмена...', reply_markup=regular_keyboard)


@dp.message_handler(state=States.CREATE_EVENT)
async def process_setstate_command(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(States.all()[2])
    event_messages[str(message.from_user.id)] = message
    await message.answer("Вы уверены, что хотите создать событие?", reply_markup=inline_kb1)


@dp.message_handler(regexp="Да", state=States.SEND_EVENT)
async def process_setstate_command(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    m = (
        await bot.send_poll(message.from_user.id, event_messages[str(message.from_user.id)].text,
                            ['Пойду', 'Возможно', 'Точно нет'], correct_option_id=0, is_anonymous=False))
    await bot.pin_chat_message(message.from_user.id, m.message_id)
    people = 0
    for member in members:
        if member != message.from_user.id:
            people += 1
            a = await bot.forward_message(chat_id=member, from_chat_id=message.chat.id, message_id=m.message_id)
            await bot.pin_chat_message(member, a.message_id)

    await state.reset_state()
    await message.answer('Сообытие создано и отправленно {} пользователям'.format(people),
                         reply_markup=regular_keyboard)


@dp.message_handler(regexp="Нет", state=States.SEND_EVENT)
async def process_setstate_command(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.reset_state()
    await message.answer("Отмена...", reply_markup=regular_keyboard)
