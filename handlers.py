from aiogram import types
import os
import DataBaseUtils
import datetime
import random
import config
import requests
from bs4 import BeautifulSoup

db = DataBaseUtils.DbConnection('OrderBot.db')
banned_users = {}
bot_state = 'Simple'
media_file_path = str(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'media')) + '\\'
start_button = types.KeyboardButton('/Старт')
start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(start_button)


async def registration_user(bot, callback_query: types.CallbackQuery):
    db.insert_user(
        callback_query.from_user.id,
        callback_query.from_user.username,
        callback_query.from_user.full_name
    )
    await callback_query.message.answer(f'Вы успешно зарегистрированы как {callback_query.from_user.full_name}')
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)


async def callback_handler(bot, callback_query: types.CallbackQuery):
    global bot_state
    bot_state = callback_query.data
    users = db.get_all_users()
    buttons = []
    for i in users:
        buttons.append(types.InlineKeyboardButton(i[2], callback_data=i[1]))
    fuck_keyboard = types.InlineKeyboardMarkup()
    for b in buttons:
        fuck_keyboard.add(b)
    await callback_query.message.answer('Выберите пользователя', reply_markup=fuck_keyboard)
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)


async def horoscope_handler(bot, callback_query: types.CallbackQuery):
    global bot_state
    bot_state = callback_query.data
    names = config.ZODIACS.keys()
    buttons = []
    for i in names:
        buttons.append(types.InlineKeyboardButton(i, callback_data=config.ZODIACS[i]))
    fuck_keyboard = types.InlineKeyboardMarkup()
    for b in buttons:
        fuck_keyboard.add(b)
    await callback_query.message.answer('Выберите знак зодиака', reply_markup=fuck_keyboard)
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)


async def get_menu(bot, message: types.Message):
    buttons = []
    if db.check_user(message.from_user.id):
        buttons.append(types.InlineKeyboardButton('Гороскоп', callback_data='horoscope'))
        buttons.append(types.InlineKeyboardButton('Послать нахуй', callback_data='fuck_you'))
        buttons.append(types.InlineKeyboardButton('Объявить мышью', callback_data='set_mouse'))
        buttons.append(types.InlineKeyboardButton('Сделать комплимент', callback_data='complement'))
        buttons.append(types.InlineKeyboardButton('Дать леща', callback_data='lesh'))
    else:
        buttons.append(types.InlineKeyboardButton('Регистрация', callback_data='registration'))
    main_keyboard = types.InlineKeyboardMarkup()
    for b in buttons:
        main_keyboard.add(b)
    await message.answer('Привет, шо нада?', reply_markup=main_keyboard)
    await bot.delete_message(message.chat.id, message.message_id)


async def get_start(bot, message: types.Message):
    if message.from_user.id == 386629136:
        await message.answer('Меню', reply_markup=start_keyboard)
        await bot.delete_message(message.chat.id, message.message_id)


async def pr_fuck_you(bot, callback_query: types.CallbackQuery):
    if callback_query.data == 'OrderOfTheKeeperOfTUbot':
        login = db.get_user_login(callback_query.from_user.id)
        await callback_query.message.answer(f'@{login} сам пошёл нахуй')
    else:
        await callback_query.message.answer(f'@{callback_query.data} получает путёвку нахуй')
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)


async def pr_set_mouse(bot, callback_query: types.CallbackQuery):
    number = random.randint(1, 26)
    if os.path.isfile(media_file_path + 'mouse_' + str(number) + '.jpg'):
        file = types.InputFile(media_file_path + 'mouse_' + str(number) + '.jpg')
    else:
        file = types.InputFile(media_file_path + 'мышь.jpg')
    await bot.send_photo(
        callback_query.message.chat.id,
        file,
        caption=f'@{callback_query.data} с этого момента официально считается мышью'
    )
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)


async def pr_get_complement(bot, callback_query: types.CallbackQuery):
    file = types.InputFile(media_file_path + 'cat.png')
    await bot.send_photo(
        callback_query.message.chat.id,
        file,
        caption=f'@{callback_query.data} ну просто волшебная булочка с корицей'
    )
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)


async def pr_get_horoscope(bot, callback_query: types.CallbackQuery):
    file = types.InputFile(media_file_path + callback_query.data + '.png')
    req = requests.get(config.HOROSCOPE_URL + callback_query.data)
    soup = BeautifulSoup(req.text, features="html.parser")
    await bot.send_photo(
        callback_query.message.chat.id,
        file,
        caption=soup.find_all(id="eje_text")[0].findNext().findNext().findNext().findNext().findNext().findNext().text
    )
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)


async def get_message_answer(bot, message: types.Message):
    if message.text.lower().find('ахах') != -1:
        await message.answer_sticker(config.FUNY_STICKERS[random.randint(0, 18)])
    elif message.text.lower().find('пиздец') != -1:
        await message.answer_sticker(config.SHOCK_STICKERS[random.randint(0, 16)])
    elif message.text.lower().find('хорош') != -1:
        await message.answer_sticker(config.GOODMAN_STICKERS[random.randint(0, 6)])
    elif message.text.lower().find('спать') != -1:
        await message.answer_sticker(config.SLEEP_STICKERS[random.randint(0, 15)])
    elif message.text == '+':
        await message.answer('+')
    elif message.text.lower().find('поедем') != -1 and message.text.lower().find('кушать') != -1:
        await message.answer(config.EAT_PLACES[random.randint(0, 3)])
    elif check_fix(message.text):
        await pr_fix(bot, message)
    elif message.text.lower().find('где') != -1 and message.text.lower().find('?') != -1:
        await pr_search(bot, message)
    elif message.text.lower().find('переиграл') != -1:
        await pr_replay(bot, message)
    elif message.text.lower().find('бубу') != -1:
        await message.answer_sticker(config.BUBU_STICKERS[random.randint(0, 5)])
    elif message.text.find('👉👈') != -1:
        await pr_fingers(bot, message)
    elif message.text.lower().find('пидарас') != -1:
        await pr_pidor(bot, message)


async def pr_pidor(bot, message: types.Message):
    file = types.InputFile(media_file_path + 'pidor.jpg')
    await bot.send_photo(
        message.chat.id,
        file
    )


async def pr_fingers(bot, message: types.Message):
    file = types.InputFile(media_file_path + 'fingers.jpg')
    await bot.send_photo(
        message.chat.id,
        file
    )

async def pr_replay(bot, message: types.Message):
    file = types.InputFile(media_file_path + 'replay.jpg')
    login = db.get_user_login(message.from_user.id)
    await bot.send_photo(
        message.chat.id,
        file,
        caption=f'@{login} красава'
    )

async def pr_search(bot, message: types.Message):
    file = types.InputFile(media_file_path + 'search.jpg')
    login = db.get_user_login(message.from_user.id)
    await bot.send_photo(
        message.chat.id,
        file,
        caption=f'Давайте поможем @{login} найти то, что нужно'
    )

def check_fix(text):
    if text.lower().find('правь') != -1:
        return True
    elif text.lower().find('правит') != -1:
        return True
    elif text.lower().find('правте') != -1:
        return True
    elif text.lower().find('правишь') != -1:
        return True
    elif text.lower().find('чини') != -1:
        return True
    else:
        return False

async def pr_fix(bot, message: types.Message):
    file = types.InputFile(media_file_path + 'fix.jpg')
    await bot.send_photo(
        message.chat.id,
        file,
        caption='Ща починим'
    )


async def pr_get_lesh(bot, callback_query: types.CallbackQuery):
    file = types.InputFile(media_file_path + 'lesh.png')
    await bot.send_photo(
        callback_query.message.chat.id,
        file,
        caption=f'@{callback_query.data} получает леща'
    )
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)


async def command_handler(bot, callback_query: types.CallbackQuery):
    global bot_state
    if bot_state == 'fuck_you':
        bot_state = 'Simple'
        await pr_fuck_you(bot, callback_query)
    elif bot_state == 'set_mouse':
        bot_state = 'Simple'
        await pr_set_mouse(bot, callback_query)
    elif bot_state == 'complement':
        bot_state = 'Simple'
        await pr_get_complement(bot, callback_query)
    elif bot_state == 'horoscope':
        bot_state = 'Simple'
        await pr_get_horoscope(bot, callback_query)
    elif bot_state == 'lesh':
        bot_state = 'Simple'
        await pr_get_lesh(bot, callback_query)