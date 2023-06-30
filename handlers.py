from aiogram import types, Bot
import os
import DataBaseUtils
import random
import config
import requests
from bs4 import BeautifulSoup
import datetime



db = DataBaseUtils.DbConnection('OrderBot.db')
banned_users = {}
bot_state = 'Simple'
media_file_path = str(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'media')) + '\\'
start_button = types.KeyboardButton('/Старт')
start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(start_button)
main_menu_buttons = {
    'Гороскоп по ЗЗ': 'horoscope',
    'Послать нахуй': 'fuck_you',
    'Объявить мышью': 'set_mouse',
    'Сделать комплимент': 'complement',
    'Дать леща': 'lesh',
    'Статистика': 'statistic',
    'Пожелать здоровья': 'pain',
    'Порча на понос': 'porch',
    'Пользователь заебал': 'zaeb',
}
users_dop = [
    'Бухгалтерия', 
    'Аудиторы',
    'Мониторинг',
    'Бит',
    'Миша',
    'Вонючая магистраль',
    'BPMS',
    'Инвентаризация',
    'Бабка уборщица',
    'Пиошники',
    'SAP',
    'Олег',
]

def check_ban(id):
    try:
        if (datetime.datetime.now() - banned_users[id]).total_seconds() > 600:
            return True
        else:
            return False
    except:
        return True

def get_main_keyboard(user_id):
    buttons = []
    if db.check_user(user_id):
        for key in list(main_menu_buttons.keys()):
            buttons.append(types.InlineKeyboardButton(key, callback_data=main_menu_buttons[key]))
        if user_id == 386629136:
            buttons.append(types.InlineKeyboardButton('Забанить пользователя', callback_data='ban'))
    else:
        buttons.append(types.InlineKeyboardButton('Регистрация', callback_data='registration'))
    main_keyboard = types.InlineKeyboardMarkup()
    b = 0
    while b < len(buttons) - 1:
        main_keyboard.row(buttons[b], buttons[b + 1])
        b += 2
    if len(buttons) % 2 != 0:
        main_keyboard.add(buttons[len(buttons) - 1])
    return main_keyboard

async def pr_del_msg(bot : Bot, chat_id, message_id):
    try:
        await bot.delete_message(chat_id, message_id)
    except:
        print('Message deleted early')

async def command_handler(bot : Bot, message : types.Message):
    if message.get_command() == '/Старт':
        await message.answer('Привет, шо нада?', reply_markup=get_main_keyboard(message.from_user.id))
        await pr_del_msg(bot, message.chat.id, message.message_id)
    elif message.get_command() == '/Меню':
        if message.from_user.id == 386629136:
            await message.answer('Меню', reply_markup=start_keyboard)
            await pr_del_msg(bot, message.chat.id, message.message_id)

async def text_handler(bot : Bot, message : types.Message):
    pass


async def message_handler(bot : Bot, message : types.Message):
    if check_ban(message.from_user.id):
        if message.is_command():
            await command_handler(bot, message)
        else:
            await text_handler(bot, message)
    else:
        await pr_del_msg(bot, message.chat.id, message.message_id)

async def get_horoscope_keyboard(bot : Bot, callback_query: types.CallbackQuery):
    global bot_state
    bot_state = callback_query.data
    keyboard = types.InlineKeyboardMarkup()
    for name in list(config.ZODIACS.keys()):
        keyboard.add(types.InlineKeyboardButton(name, callback_data=config.ZODIACS[name])) 
    await callback_query.message.answer('Выберите знак зодиака', reply_markup=keyboard)
    await pr_del_msg(bot, callback_query.message.chat.id, callback_query.message.message_id)

async def get_horoscope(bot : Bot, callback_query: types.CallbackQuery):
    file = types.InputFile(media_file_path + callback_query.data + '.png')
    req = requests.get(config.HOROSCOPE_URL + callback_query.data)
    soup = BeautifulSoup(req.text, features="html.parser")
    await bot.send_photo(
        callback_query.message.chat.id,
        file,
        caption=soup.find_all(id="eje_text")[0].findNext().findNext().findNext().findNext().findNext().findNext().text
    )
    await pr_del_msg(bot, callback_query.message.chat.id, callback_query.message.message_id)

async def registr_user(bot : Bot, callback_query: types.CallbackQuery):
    db.insert_user(
        callback_query.from_user.id,
        callback_query.from_user.username,
        callback_query.from_user.full_name
    )
    await callback_query.message.answer(f'Вы успешно зарегистрированы как {callback_query.from_user.full_name}')
    await pr_del_msg(bot, callback_query.message.chat.id, callback_query.message.message_id)

async def get_users(bot : Bot, callback_query: types.CallbackQuery):
    users = db.get_all_users()
    buttons = []
    for i in users:
        buttons.append(types.InlineKeyboardButton(i[2], callback_data=f'$@{i[1]}*{callback_query.data}'))
    for i in users_dop:
        buttons.append(types.InlineKeyboardButton(i, callback_data=f'${i}*{callback_query.data}'))
    fuck_keyboard = types.InlineKeyboardMarkup()
    b = 0
    while b < len(buttons) - 1:
        fuck_keyboard.row(buttons[b], buttons[b + 1])
        b += 2
    if len(buttons) % 2 != 0:
        fuck_keyboard.add(buttons[len(buttons) - 1])
    await callback_query.message.answer('Выберите пользователя', reply_markup=fuck_keyboard)
    await pr_del_msg(bot, callback_query.message.chat.id, callback_query.message.message_id)

def get_fuck_message(from_user_id, user_str):
    if user_str[1:] == '@OrderOfTheKeeperOfTUbot':
        login = db.get_user_login(from_user_id)
        db.insert_log(login, 'hui')
        return f'@{login} сам пошёл нахуй' 
    else:
        db.insert_log(user_str[2:], 'hui')
        return f'{user_str[1:]} получает путёвку нахуй'
    
def get_mouse_message(from_user_id, user_str):
    if user_str[1:] == '@OrderOfTheKeeperOfTUbot':
        login = db.get_user_login(from_user_id)
        db.insert_log(login, 'mouse')
        return f'@{login} с этого момента официально считается мышью' 
    else:
        db.insert_log(user_str[2:], 'mouse')
        return f'{user_str[1:]} с этого момента официально считается мышью'

async def send_fuck(bot: Bot, callback_query: types.CallbackQuery, user_str):
    await callback_query.message.answer(get_fuck_message(callback_query.from_user.id, user_str))
    await bot.send_voice(
        callback_query.message.chat.id,
        voice=types.InputFile(media_file_path + 'fuck-you.mp3')
    )

async def send_mouse(bot: Bot, callback_query: types.CallbackQuery, user_str):
    number = random.randint(1, 26)
    if os.path.isfile(media_file_path + 'mouse_' + str(number) + '.jpg'):
        file = types.InputFile(media_file_path + 'mouse_' + str(number) + '.jpg')
    else:
        file = types.InputFile(media_file_path + 'мышь.jpg')
    await bot.send_photo(
        callback_query.message.chat.id,
        file,
        caption=get_mouse_message(callback_query.from_user.id, user_str)
    )
    await bot.send_voice(
        callback_query.message.chat.id,
        voice=types.InputFile(media_file_path + 'mouse-voice.mp3')
    )

async def send_compliment(bot: Bot, callback_query: types.CallbackQuery, user_str):
    file = types.InputFile(media_file_path + 'cat.png')
    await bot.send_photo(
        callback_query.message.chat.id,
        file,
        caption=f'{user_str[1:]} ну просто волшебная булочка с корицей'
    )
    if random.randint(1, 2) == 1:
        file = 'kudasai.mp3'
    else:
        file = 'uwu-voice.mp3'
    await bot.send_voice(
        callback_query.message.chat.id,
        voice=types.InputFile(media_file_path + file)
    )
    db.insert_log(callback_query.data, 'cool')

def get_lash_message(from_user_id, user_str):
    if user_str[1:] == '@OrderOfTheKeeperOfTUbot':
        login = db.get_user_login(from_user_id)
        db.insert_log(login, 'lesh')
        return f'@{login} получает леща' 
    else:
        db.insert_log(user_str[2:], 'lesh')
        return f'{user_str[1:]} получает леща'
    
async def send_lesh(bot: Bot, callback_query: types.CallbackQuery, user_str):
    file = types.InputFile(media_file_path + 'lesh.png')
    login = db.get_user_login(callback_query.from_user.id)
    await bot.send_photo(
        callback_query.message.chat.id,
        file,
        caption=get_lash_message(callback_query.from_user.id, user_str)
    )
    db.insert_log(login, 'lesh')

async def send_pain(bot: Bot, callback_query: types.CallbackQuery, user_str):
    await bot.send_photo(
        callback_query.message.chat.id,
        types.InputFile(media_file_path + 'pain.jpg'),
        caption=f'Желаем нашей любимой мыши {user_str[1:]} скорейшего выздоровления'
    )
    db.insert_log(user_str[2:], 'pain')

def get_porch_message(from_user_id, user_str):
    if user_str[1:] == '@OrderOfTheKeeperOfTUbot':
        login = db.get_user_login(from_user_id)
        db.insert_log(login, 'porch')
        return f'@{login} словил порчу на понос' 
    else:
        db.insert_log(user_str[2:], 'porch')
        return f'{user_str[1:]} словил порчу на понос'
    
async def send_porch(bot: Bot, callback_query: types.CallbackQuery, user_str):
    await bot.send_photo(
        callback_query.message.chat.id,
        types.InputFile(media_file_path + 'porch.jpg'),
        caption=get_porch_message(callback_query.from_user.id, user_str)
    )   

def get_zaeb_message(from_user_id, user_str):
    if user_str[1:] == '@OrderOfTheKeeperOfTUbot':
        login = db.get_user_login(from_user_id)
        db.insert_log(login, 'zaeb')
        return f'@{login} уже просто заебал' 
    else:
        db.insert_log(user_str[2:], 'zaeb')
        return f'{user_str[1:]} уже просто заебал'

async def send_zaeb(bot: Bot, callback_query: types.CallbackQuery, user_str):
    await callback_query.message.answer(get_zaeb_message(callback_query.from_user.id, user_str))
    await send_fuck(bot, callback_query, user_str)
    await send_mouse(bot, callback_query, user_str)
    await send_lesh(bot, callback_query, user_str)
    await send_porch(bot, callback_query, user_str)

async def send_ban(bot: Bot, callback_query: types.CallbackQuery, user_str):
    banned_users[db.get_user_id(user_str[2:])] = datetime.datetime.now()
    db.insert_log(user_str[2:], 'ban')
    await bot.send_photo(
        callback_query.message.chat.id,
        types.InputFile(media_file_path + 'ban.jpg'),
        caption=f'{user_str[1:]} получает бан на 10 минут'
    )

async def user_handler(bot : Bot, callback_query: types.CallbackQuery):
    data = callback_query.data.split('*')
    if data[1] == 'fuck_you':
        await send_fuck(bot, callback_query, data[0])
    if data[1] == 'set_mouse':
        await send_mouse(bot, callback_query, data[0])
    if data[1] == 'complement':
        await send_compliment(bot, callback_query, data[0])
    if data[1] == 'lesh':
        await send_lesh(bot, callback_query, data[0])
    if data[1] == 'pain':
        await send_pain(bot, callback_query, data[0])
    if data[1] == 'porch':
        await send_porch(bot, callback_query, data[0])
    if data[1] == 'zaeb':
        await send_zaeb(bot, callback_query, data[0])
    if data[1] == 'ban':
        await send_ban(bot, callback_query, data[0])
    await pr_del_msg(bot, callback_query.message.chat.id, callback_query.message.message_id)

async def get_statistic(bot : Bot, callback_query: types.CallbackQuery):
    users = db.get_all_users()
    for user in users:
        result = ''
        stats = db.get_statistic(user[1])
        cnt_hui = 0
        cnt_mouse = 0
        cnt_cool = 0
        cnt_lesh = 0
        cnt_ban = 0
        cnt_porch = 0
        cnt_pain = 0
        cnt_zaeb = 0
        for stat in stats:
            if stat[0] == 'hui':
                cnt_hui += 1
            elif stat[0] == 'mouse':
                cnt_mouse += 1
            elif stat[0] == 'cool':
                cnt_cool += 1
            elif stat[0] == 'lesh':
                cnt_lesh += 1
            elif stat[0] == 'ban':
                cnt_ban += 1
            elif stat[0] == 'porch':
                cnt_porch += 1
            elif stat[0] == 'pain':
                cnt_pain += 1
            elif stat[0] == 'zaeb':
                cnt_zaeb += 1
        if cnt_mouse > 0:
            result += f'@{user[1]} был(а) назван(а) мышью {cnt_mouse} раз(а)\n'
        if cnt_cool > 0:
            result += f'@{user[1]} получил(а) комплимент {cnt_cool} раз(а)\n'
        if cnt_hui > 0:
            result += f'@{user[1]} был(а) послан(а) нахуй {cnt_hui} раз(а)\n'
        if cnt_lesh > 0:
            result += f'@{user[1]} получил(а) леща {cnt_lesh} раз(а)\n'
        if cnt_ban > 0:
            result += f'@{user[1]} получил(а) бан {cnt_ban} раз(а)\n'
        if cnt_porch > 0:
            result += f'@{user[1]} словил(а) порчу на понос {cnt_porch} раз(а)\n'
        if cnt_pain > 0:
            result += f'@{user[1]} пожелали здоровья {cnt_porch} раз(а)\n'
        if cnt_zaeb > 0:
            result += f'@{user[1]} заебал {cnt_porch} раз(а)\n'
        if result != '':
            await callback_query.message.answer(result)
    await pr_del_msg(bot, callback_query.message.chat.id, callback_query.message.message_id)

async def callback_query_handler(bot : Bot, callback_query: types.CallbackQuery):
    if check_ban(callback_query.from_user.id):
        if callback_query.data == 'horoscope':
            await get_horoscope_keyboard(bot, callback_query)
        elif callback_query.data in list(config.ZODIACS.values()):
            await get_horoscope(bot, callback_query)
        elif callback_query.data == 'registration':
            await registr_user(bot, callback_query)
        elif callback_query.data in (
            'fuck_you', 
            'set_mouse', 
            'complement', 
            'lesh', 
            'pain', 
            'porch', 
            'zaeb', 
            'ban'
        ):
            await get_users(bot, callback_query)
        elif callback_query.data[0] == '$':
            await user_handler(bot, callback_query)
        elif callback_query.data == 'statistic':
            await get_statistic(bot, callback_query)

