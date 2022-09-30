from aiogram import Bot, Dispatcher, executor, types
import config
import datetime
import DataBaseUtils
import os

bot = Bot(token=config.BOT_API_TOKEN)
dp = Dispatcher(bot)
db = DataBaseUtils.DbConnection('OrderBot.db')
start_button = types.KeyboardButton('/Старт')
start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(start_button)
media_file_path = 'C:\\specsoft\\PyCharmProjects\\OrderOfTheKeepersOfTUbot\\media\\'
banned_users = {}

global bot_state
bot_state = 'Simple'

@dp.callback_query_handler(lambda c: c.data == 'horoscope')
async def horoscope_collback(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.send_message(callback_query.message.chat.id, 'У всех всё будет хорошо')


@dp.callback_query_handler(lambda c: c.data == 'registration')
async def registration_collback(callback_query: types.CallbackQuery):
    db.insert_user(
        callback_query.from_user.id,
        callback_query.from_user.username,
        callback_query.from_user.full_name
    )
    await callback_query.message.answer(f'Вы успешно зарегистрированы как {callback_query.from_user.full_name}')
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)


@dp.callback_query_handler(lambda c: c.data == 'fuck_you')
async def fuck_collback(callback_query: types.CallbackQuery):
    global bot_state
    bot_state = 'Fuck'
    users = db.get_all_users()
    buttons = []
    for i in users:
        buttons.append(types.InlineKeyboardButton(i[2], callback_data=i[1]))
    fuck_keyboard = types.InlineKeyboardMarkup()
    for b in buttons:
        fuck_keyboard.add(b)
    await callback_query.message.answer('Выберите пользователя', reply_markup=fuck_keyboard)
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)

@dp.callback_query_handler(lambda c: c.data == 'set_mouse')
async def fuck_collback(callback_query: types.CallbackQuery):
    global bot_state
    bot_state = 'Mouse'
    users = db.get_all_users()
    buttons = []
    for i in users:
        buttons.append(types.InlineKeyboardButton(i[2], callback_data=i[1]))
    fuck_keyboard = types.InlineKeyboardMarkup()
    for b in buttons:
        fuck_keyboard.add(b)
    await callback_query.message.answer('Выберите пользователя', reply_markup=fuck_keyboard)
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)


@dp.message_handler(commands=['Старт'])
async def start(message: types.Message):
    buttons = []
    if db.check_user(message.from_user.id):
        buttons.append(types.InlineKeyboardButton('Гороскоп', callback_data='horoscope'))
        buttons.append(types.InlineKeyboardButton('Послать нахуй', callback_data='fuck_you'))
        buttons.append(types.InlineKeyboardButton('Объявить мышью', callback_data='set_mouse'))
    else:
        buttons.append(types.InlineKeyboardButton('Регистрация', callback_data='registration'))
    main_keyboard = types.InlineKeyboardMarkup()
    for b in buttons:
        main_keyboard.add(b)
    await message.answer('Привет, шо нада?', reply_markup=main_keyboard)
    await bot.delete_message(message.chat.id, message.message_id)


@dp.message_handler(commands=['Меню'])
async def get_menu(message: types.Message):
    if message.from_user.id == 386629136:
        await message.answer('Меню', reply_markup=start_keyboard)
        await bot.delete_message(message.chat.id, message.message_id)

@dp.callback_query_handler()
async def fuck_you(callback_query: types.CallbackQuery):
    global bot_state
    if bot_state == 'Fuck':
        bot_state = 'Simple'
        await callback_query.message.answer(f'@{callback_query.data} Пошёл нахуй')
        await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    elif bot_state == 'Mouse':
        bot_state = 'Simple'
        if os.path.isfile(media_file_path + callback_query.data + '.png'):
            file = types.InputFile(media_file_path + callback_query.data + '.png')
        else:
            file = types.InputFile(media_file_path + 'мышь.jpg')
        await bot.send_photo(
            callback_query.message.chat.id,
            file,
            caption=f'@{callback_query.data} с этого момента официально считается мышью'
        )
        banned_users[db.get_user_id(callback_query.data)] = datetime.datetime.now()
        await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)



if __name__ == '__main__':
    executor.start_polling(dp)
