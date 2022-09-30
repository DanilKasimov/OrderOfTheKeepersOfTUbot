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


async def get_sticker(bot, message: types.Message):
    if message.text.find('ахах') != -1:
        await message.answer_sticker(config.STICKERS[random.randint(0, 18)])


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