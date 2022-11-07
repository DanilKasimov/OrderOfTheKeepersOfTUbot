from aiogram import types
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


def get_note(ticket):
    req = requests.get(
        'https://ticket.ertelecom.ru/rest/api/latest/issue/' + ticket,
        auth=(config.JIRA_LOGIN, config.JIRA_PASSWORD)
    )
    ticket_name = req.json()["fields"]["summary"]

    if req.json()["fields"]["description"] is None:
        desc = req.json()["fields"]["creator"]["displayName"] + 'хуйло не сделал описание'
    else:
        desc = req.json()["fields"]["description"].replace("*", "").replace("#", "").replace("{", "").replace("}", "")
    return f'Описание задачи {ticket} ({ticket_name}):\n{desc}'

async def get_fura(bot, message: types.Message):
    await bot.send_voice(
        message.chat.id,
        voice=types.InputFile(media_file_path + 'easter.mp3')
    )


async def registration_user(bot, callback_query: types.CallbackQuery):
    db.insert_user(
        callback_query.from_user.id,
        callback_query.from_user.username,
        callback_query.from_user.full_name
    )
    await callback_query.message.answer(f'Вы успешно зарегистрированы как {callback_query.from_user.full_name}')
    await pr_del_msg(bot, callback_query)


async def callback_handler(bot, callback_query: types.CallbackQuery):
    global bot_state
    if callback_query.data == 'statistic':
        await pr_get_statistic(bot, callback_query)
    else:
        bot_state = callback_query.data
        users = db.get_all_users()
        buttons = []
        for i in users:
            buttons.append(types.InlineKeyboardButton(i[2], callback_data=i[1]))
        buttons.append(types.InlineKeyboardButton('Бухгалтерия', callback_data='Бухгалтерия'))
        buttons.append(types.InlineKeyboardButton('Аудиторы', callback_data='Аудиторы'))
        buttons.append(types.InlineKeyboardButton('Мониторинг', callback_data='Мониторинг'))
        buttons.append(types.InlineKeyboardButton('Бит', callback_data='Бит'))
        buttons.append(types.InlineKeyboardButton('Миша', callback_data='Миша'))
        buttons.append(types.InlineKeyboardButton('Вонючая магистраль', callback_data='Вонючая магистраль'))
        buttons.append(types.InlineKeyboardButton('BPMS', callback_data='BPMS'))
        buttons.append(types.InlineKeyboardButton('Инвентаризация', callback_data='Инвентаризация'))
        buttons.append(types.InlineKeyboardButton('Бабка уборщица', callback_data='Бабка уборщица'))
        buttons.append(types.InlineKeyboardButton('Пиошники', callback_data='Пиошники'))
        buttons.append(types.InlineKeyboardButton('SAP', callback_data='SAP'))
        fuck_keyboard = types.InlineKeyboardMarkup()
        b = 0
        while b < len(buttons) - 1:
            fuck_keyboard.row(buttons[b], buttons[b + 1])
            b += 2
        if len(buttons) % 2 != 0:
            fuck_keyboard.add(buttons[len(buttons) - 1])
        await callback_query.message.answer('Выберите пользователя', reply_markup=fuck_keyboard)
        await pr_del_msg(bot, callback_query)


async def horoscope_zz_handler(bot, callback_query: types.CallbackQuery):
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
    await pr_del_msg(bot, callback_query)


async def horoscope_year_handler(bot, callback_query: types.CallbackQuery):
    global bot_state
    bot_state = callback_query.data
    names = config.ZODIACS_YEAR.keys()
    buttons = []
    for i in names:
        buttons.append(types.InlineKeyboardButton(i, callback_data=config.ZODIACS_YEAR[i]))
    fuck_keyboard = types.InlineKeyboardMarkup()
    for b in buttons:
        fuck_keyboard.add(b)
    await callback_query.message.answer('Выберите годовое животное', reply_markup=fuck_keyboard)
    await pr_del_msg(bot, callback_query)


async def get_menu(bot, message: types.Message):
    if check_ban(message.from_user.id):
        buttons = []
        if db.check_user(message.from_user.id):
            buttons.append(types.InlineKeyboardButton('Гороскоп по ЗЗ', callback_data='horoscope_zz'))
            #buttons.append(types.InlineKeyboardButton('Гороскоп по животному года', callback_data='horoscope_year'))
            buttons.append(types.InlineKeyboardButton('Послать нахуй', callback_data='fuck_you'))
            buttons.append(types.InlineKeyboardButton('Объявить мышью', callback_data='set_mouse'))
            buttons.append(types.InlineKeyboardButton('Сделать комплимент', callback_data='complement'))
            buttons.append(types.InlineKeyboardButton('Дать леща', callback_data='lesh'))
            buttons.append(types.InlineKeyboardButton('Статистика', callback_data='statistic'))
            buttons.append(types.InlineKeyboardButton('Пожелать здоровья', callback_data='pain'))
            buttons.append(types.InlineKeyboardButton('Порча на понос', callback_data='porch'))
            if message.from_user.id == 386629136:
                buttons.append(types.InlineKeyboardButton('Забанить пользователя на 10 минут', callback_data='ban'))
            buttons.append(types.InlineKeyboardButton('Пользователь заебал', callback_data='zaeb'))
        else:
            buttons.append(types.InlineKeyboardButton('Регистрация', callback_data='registration'))
        main_keyboard = types.InlineKeyboardMarkup()
        b = 0
        while b < len(buttons) - 1:
            main_keyboard.row(buttons[b], buttons[b + 1])
            b += 2
        if len(buttons) % 2 != 0:
            main_keyboard.add(buttons[len(buttons) - 1])
        await message.answer('Привет, шо нада?', reply_markup=main_keyboard)
        await bot.delete_message(message.chat.id, message.message_id)
    else:
        await bot.delete_message(message.chat.id, message.message_id)


async def get_start(bot, message: types.Message):
    if message.from_user.id == 386629136:
        await message.answer('Меню', reply_markup=start_keyboard)
        await pr_del_msg(bot, callback_query)


async def pr_fuck_you(bot, callback_query: types.CallbackQuery):
    if callback_query.data == 'OrderOfTheKeeperOfTUbot':
        login = db.get_user_login(callback_query.from_user.id)
        await callback_query.message.answer(f'@{login} сам пошёл нахуй')
        db.insert_log(login, 'hui')
    else:
        await callback_query.message.answer(f'@{callback_query.data} получает путёвку нахуй')
        db.insert_log(callback_query.data, 'hui')
    await bot.send_voice(
        callback_query.message.chat.id,
        voice=types.InputFile(media_file_path + 'fuck-you.mp3')
    )
    await pr_del_msg(bot, callback_query)


async def pr_set_mouse(bot, callback_query: types.CallbackQuery):
    number = random.randint(1, 26)
    if os.path.isfile(media_file_path + 'mouse_' + str(number) + '.jpg'):
        file = types.InputFile(media_file_path + 'mouse_' + str(number) + '.jpg')
    else:
        file = types.InputFile(media_file_path + 'мышь.jpg')
    if callback_query.data == 'OrderOfTheKeeperOfTUbot':
        login = db.get_user_login(callback_query.from_user.id)
        await bot.send_photo(
            callback_query.message.chat.id,
            file,
            caption=f'@{login} сам мышь'
        )
        db.insert_log(login, 'mouse')
    else:
        await bot.send_photo(
            callback_query.message.chat.id,
            file,
            caption=f'@{callback_query.data} с этого момента официально считается мышью'
        )
        db.insert_log(callback_query.data, 'mouse')
    await bot.send_voice(
        callback_query.message.chat.id,
        voice=types.InputFile(media_file_path + 'mouse-voice.mp3')
    )
    await pr_del_msg(bot, callback_query)


async def pr_get_complement(bot, callback_query: types.CallbackQuery):
    file = types.InputFile(media_file_path + 'cat.png')
    await bot.send_photo(
        callback_query.message.chat.id,
        file,
        caption=f'@{callback_query.data} ну просто волшебная булочка с корицей'
    )
    db.insert_log(callback_query.data, 'cool')
    if callback_query.data == 'OrderOfTheKeeperOfTUbot':
        await bot.send_voice(
            callback_query.message.chat.id,
            voice=types.InputFile(media_file_path + 'kudasai.mp3')
        )
    else:
        await bot.send_voice(
            callback_query.message.chat.id,
            voice=types.InputFile(media_file_path + 'uwu-voice.mp3')
        )
    await pr_del_msg(bot, callback_query)


async def pr_get_virus(bot, message: types.Message):
    if random.randint(0, 1) == 1:
        file = types.InputFile(media_file_path + 'avast.mp3')
    else:
        file = types.InputFile(media_file_path + 'kasper.mp3')
    await bot.send_voice(
        message.chat.id,
        voice=file
    )


async def pr_get_horoscope_zz(bot, callback_query: types.CallbackQuery):
    file = types.InputFile(media_file_path + callback_query.data + '.png')
    req = requests.get(config.HOROSCOPE_URL + callback_query.data)
    soup = BeautifulSoup(req.text, features="html.parser")
    await bot.send_photo(
        callback_query.message.chat.id,
        file,
        caption=soup.find_all(id="eje_text")[0].findNext().findNext().findNext().findNext().findNext().findNext().text
    )
    await pr_del_msg(bot, callback_query)


async def pr_get_horoscope_year(bot, callback_query: types.CallbackQuery):
    file = types.InputFile(media_file_path + callback_query.data + '.png')
    req = requests.get(config.HOROSCOPE_URL + callback_query.data + '/')
    soup = BeautifulSoup(req.text, features="html.parser")
    capt = ''
    for i in soup.find_all('p'):
        capt += str(i).replace('<p>', '').replace('</p>', '') + '\n'
    await bot.send_photo(
        callback_query.message.chat.id,
        file,
        caption=capt
    )
    await pr_del_msg(bot, callback_query)


def check_ban(id):
    try:
        if (datetime.datetime.now() - banned_users[id]).total_seconds() > 600:
            return True
        else:
            return False
    except:
        return True


async def get_message_answer(bot, message: types.Message):
    if check_ban(message.from_user.id):
        if message.text is not None:
            if message.text.lower().find('ахах') != -1:
                await message.answer_sticker(config.FUNY_STICKERS[random.randint(0, len(config.FUNY_STICKERS) - 1)])
            if message.text.lower().find('пиздец') != -1:
                await message.answer_sticker(config.SHOCK_STICKERS[random.randint(0, len(config.SHOCK_STICKERS) - 1)])
            if message.text.lower().find('хорош') != -1:
                await message.answer_sticker(config.GOODMAN_STICKERS[random.randint(0, len(config.GOODMAN_STICKERS) - 1)])
            if message.text.lower().find('спать') != -1:
                await message.answer_sticker(config.SLEEP_STICKERS[random.randint(0, len(config.SLEEP_STICKERS) - 1)])
            if message.text == '+':
                await message.answer('+')
            if message.text.lower().find('поедем') != -1 and message.text.lower().find('кушать') != -1:
                ver = random.randint(0, 100)
                if 0 <= ver < 22:
                    await message.answer('Едем в аймолл')
                elif 22 <= ver < 44:
                    await message.answer('Едем в планету')
                elif 44 <= ver < 66:
                    await message.answer('Идём в шаву')
                elif 66 <= ver < 88:
                    await message.answer('Идём в столовку')
                elif 88 <= ver < 90:
                    await message.answer('Едим раков')
                elif 90 <= ver < 92:
                    await message.answer('Едим роллы')
                elif 92 <= ver < 94:
                    await message.answer('Едим смузи')
                elif 94 <= ver < 96:
                    await message.answer('Не едим сегодня')
                elif 96 <= ver < 98:
                    await message.answer('Едим пиццамен')
                else:
                    await message.answer('Шашлыкофф')
            if check_fix(message.text):
                await pr_fix(bot, message)
            if message.text.lower().find('где') != -1 and message.text.lower().find('?') != -1:
                await pr_search(bot, message)
            if message.text.lower().find('переиграл') != -1:
                await pr_replay(bot, message)
            if message.text.lower().find('бубу') != -1:
                await message.answer_sticker(config.BUBU_STICKERS[random.randint(0, len(config.BUBU_STICKERS) - 1)])
            if message.text.find('👉👈') != -1:
                await pr_fingers(bot, message)
            if message.text.lower().find('пидор') != -1:
                await pr_pidor(bot, message)
            if message.text.lower().find('пидар') != -1:
                await pr_pidor(bot, message)
            if message.text.lower().find('шок') != -1:
                await get_fura(bot, message)
            if message.text.lower().find('((') != -1:
                await message.answer_sticker(config.CRY_STICKERS[random.randint(0, len(config.CRY_STICKERS) - 1)])
            if message.text.lower().find('грусть') != -1:
                await message.answer_sticker(config.CRY_STICKERS[random.randint(0, len(config.CRY_STICKERS) - 1)])
            if message.text.lower().find('плак') != -1:
                await message.answer_sticker(config.CRY_STICKERS[random.randint(0, len(config.CRY_STICKERS) - 1)])
            if message.text.lower().find('похуй') != -1:
                await message.answer_sticker(config.POHUI_STICKERS[random.randint(0, len(config.POHUI_STICKERS) - 1)])
            if message.text.lower().find('поебать') != -1:
                await message.answer_sticker(config.POHUI_STICKERS[random.randint(0, len(config.POHUI_STICKERS) - 1)])
            if message.text.lower().find('плевать') != -1:
                await message.answer_sticker(config.POHUI_STICKERS[random.randint(0, len(config.POHUI_STICKERS) - 1)])
            if message.text.lower().find('без разницы') != -1:
                await message.answer_sticker(config.POHUI_STICKERS[random.randint(0, len(config.POHUI_STICKERS) - 1)])
            if message.text.lower().find('когди') != -1:
                await pr_cogdis(bot, message)
            if message.text.lower().find('заболел') != -1:
                await pr_get_virus(bot, message)
            if message.text.lower().find('болею') != -1:
                await pr_get_virus(bot, message)
            if message.text.find('https://ticket.ertelecom.ru/browse/') != -1:
                if message.text.find(' ', message.text.find('browse/')) != -1:
                    await message.answer(get_note(message.text[message.text.find('browse/') + 7:message.text.find(' ', message.text.find('browse/'))]))
                else:
                    await message.answer(get_note(message.text[message.text.find('browse/') + 7:]))
            if message.text.lower().find('справедливо') != -1:
                await message.answer_sticker('CAACAgIAAxkBAAEGSxtjY0JDVWilZ_UZndYPkDo2SNiyTgACVAADuRtZC2dCUqTSakgJKgQ')
            if message.text.lower().find('миша заебал') != -1:
                await message.answer_sticker('CAACAgIAAxkBAAEGSx1jY0LJbBYBHWeKjzukEemjCNxViAACWgADuRtZC1fMhgYQTAjPKgQ')
                await message.answer_sticker('CAACAgIAAxkBAAEGSx9jY0LLH0u2SEqZnzGYbA3qZPNpVgACdQADuRtZCwrzLOB1qOVZKgQ')
                await message.answer_sticker('CAACAgIAAxkBAAEGSx9jY0LLH0u2SEqZnzGYbA3qZPNpVgACdQADuRtZCwrzLOB1qOVZKgQ')
                await message.answer_sticker('CAACAgIAAxkBAAEGSyFjY0LNUmrLHxVU5bHow9Ebkms54wACWwADuRtZC8HaaJQtmnPkKgQ')
    else:
        await bot.delete_message(message.chat.id, message.message_id)

async def pr_cogdis(bot, message: types.Message):
    file = types.InputFile(media_file_path + 'cogdish.jpg')
    await bot.send_photo(
        message.chat.id,
        file,
        caption='Когдить'
    )
    file = types.InputFile(media_file_path + 'zrist.jpg')
    await bot.send_photo(
        message.chat.id,
        file,
        caption='По-жристиански'
    )
    file = types.InputFile(media_file_path + 'garold.png')
    await bot.send_photo(
        message.chat.id,
        file,
        caption='Это круто'
    )



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
    if callback_query.data == 'OrderOfTheKeeperOfTUbot':
        login = db.get_user_login(callback_query.from_user.id)
        await bot.send_photo(
            callback_query.message.chat.id,
            file,
            caption=f'@{login} сам получает леща'
        )
        db.insert_log(login, 'lesh')
    else:
        await bot.send_photo(
            callback_query.message.chat.id,
            file,
            caption=f'@{callback_query.data} получает леща'
        )
        db.insert_log(callback_query.data, 'lesh')
    await pr_del_msg(bot, callback_query)

async def pr_get_statistic(bot, callback_query: types.CallbackQuery):
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
        if result != '':
            await callback_query.message.answer(result)
    await pr_del_msg(bot, callback_query)


async def pr_ban_user(bot, callback_query: types.CallbackQuery):
    banned_users[db.get_user_id(callback_query.data)] = datetime.datetime.now()
    db.insert_log(callback_query.data, 'ban')
    await bot.send_photo(
        callback_query.message.chat.id,
        types.InputFile(media_file_path + 'ban.jpg'),
        caption=f'@{callback_query.data} получает бан на 10 минут'
    )
    await pr_del_msg(bot, callback_query)


async def pr_pain_user(bot, callback_query: types.CallbackQuery):
    await bot.send_photo(
        callback_query.message.chat.id,
        types.InputFile(media_file_path + 'pain.jpg'),
        caption=f'Желаем нашей любимой мыши @{callback_query.data} скорейшего выздоровления'
    )
    await pr_del_msg(bot, callback_query)

async def pr_del_msg(bot, callback_query: types.CallbackQuery):
    try:
        await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    except:
        print('Message deleted early')

async def pr_porch(bot, callback_query: types.CallbackQuery):
    db.insert_log(callback_query.data, 'porch')
    await bot.send_photo(
        callback_query.message.chat.id,
        types.InputFile(media_file_path + 'porch.jpg'),
        caption=f'@{callback_query.data} словил порчу на понос'
    )
    await pr_del_msg(bot, callback_query)

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
    elif bot_state == 'horoscope_zz':
        bot_state = 'Simple'
        await pr_get_horoscope_zz(bot, callback_query)
    elif bot_state == 'horoscope_year':
        bot_state = 'Simple'
        await pr_get_horoscope_year(bot, callback_query)
    elif bot_state == 'lesh':
        bot_state = 'Simple'
        await pr_get_lesh(bot, callback_query)
    elif bot_state == 'ban':
        bot_state = 'Simple'
        await pr_ban_user(bot, callback_query)
    elif bot_state == 'pain':
        bot_state = 'Simple'
        await pr_pain_user(bot, callback_query)
    elif bot_state == 'porch':
        bot_state = 'Simple'
        await pr_porch(bot, callback_query)
    elif bot_state == 'zaeb':
        bot_state = 'Simple'
        await callback_query.message.answer(f'@{callback_query.data} уже просто заебал')
        await pr_fuck_you(bot, callback_query)
        await pr_set_mouse(bot, callback_query)
        await pr_get_lesh(bot, callback_query)
        await pr_porch(bot, callback_query)
        if callback_query.from_user.id == 386629136:
            await pr_ban_user(bot, callback_query)