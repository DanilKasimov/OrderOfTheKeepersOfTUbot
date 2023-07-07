from aiogram import types, Bot
import random
import config
import DataBaseUtils
import os

media_file_path = str(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'media')) + '\\'

db = DataBaseUtils.DbConnection('OrderBot.db')

async def print_ahah(bot : Bot, message : types.Message):
    await message.answer_sticker(config.FUNY_STICKERS[random.randint(0, len(config.FUNY_STICKERS) - 1)]) 

async def print_pizd(bot : Bot, message : types.Message):
    await message.answer_sticker(config.SHOCK_STICKERS[random.randint(0, len(config.SHOCK_STICKERS) - 1)])

async def print_good(bot : Bot, message : types.Message):
    await message.answer_sticker(config.GOODMAN_STICKERS[random.randint(0, len(config.GOODMAN_STICKERS) - 1)])

async def print_sleep(bot : Bot, message : types.Message):
    await message.answer_sticker(config.SLEEP_STICKERS[random.randint(0, len(config.SLEEP_STICKERS) - 1)])

async def print_plus(bot : Bot, message : types.Message):
    if message.text == '+':
        await message.answer('+')

async def print_minus(bot : Bot, message : types.Message):
    if message.text == '-':
        await message.answer('-')

async def print_go_eat(bot : Bot, message : types.Message):
    if message.text.lower().find('кушать') != -1 and message.text.lower().find('поедем') != -1:
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

async def print_repare(bot : Bot, message : types.Message):
    file = types.InputFile(media_file_path + 'fix.jpg')
    await bot.send_photo(
        message.chat.id,
        file,
        caption='Ща починим'
    )

async def print_search(bot : Bot, message : types.Message):
    if message.text.lower().find('где') != -1 and message.text.lower().find('?') != -1:
        file = types.InputFile(media_file_path + 'search.jpg')
        login = db.get_user_login(message.from_user.id)
        await bot.send_photo(
            message.chat.id,
            file,
            caption=f'Давайте поможем @{login} найти то, что нужно'
        )

async def print_replay(bot : Bot, message : types.Message):
    file = types.InputFile(media_file_path + 'replay.jpg')
    login = db.get_user_login(message.from_user.id)
    await bot.send_photo(
        message.chat.id,
        file,
        caption=f'@{login} красава'
    )

async def print_bubu(bot: Bot, message : types.Message):
    await message.answer_sticker(config.BUBU_STICKERS[random.randint(0, len(config.BUBU_STICKERS) - 1)])

async def print_fingers(bot: Bot, message : types.Message):
    file = types.InputFile(media_file_path + 'fingers.jpg')
    await bot.send_photo(
        message.chat.id,
        file
    )

async def print_pidr(bot: Bot, message : types.Message):
    file = types.InputFile(media_file_path + 'pidor.jpg')
    await bot.send_photo(
        message.chat.id,
        file
    )

async def print_fura(bot: Bot, message : types.Message):
    await bot.send_voice(
        message.chat.id,
        voice=types.InputFile(media_file_path + 'easter.mp3')
    )

async def print_sad(bot: Bot, message : types.Message):
    await message.answer_sticker(config.CRY_STICKERS[random.randint(0, len(config.CRY_STICKERS) - 1)])

async def print_pohui(bot: Bot, message : types.Message):
    await message.answer_sticker(config.POHUI_STICKERS[random.randint(0, len(config.POHUI_STICKERS) - 1)])

async def print_virus(bot: Bot, message : types.Message):
    if random.randint(0, 1) == 1:
        file = types.InputFile(media_file_path + 'avast.mp3')
    else:
        file = types.InputFile(media_file_path + 'kasper.mp3')
    await bot.send_voice(
        message.chat.id,
        voice=file
    )

async def print_sprav(bot: Bot, message : types.Message):
    await message.answer_sticker('CAACAgIAAxkBAAEGSxtjY0JDVWilZ_UZndYPkDo2SNiyTgACVAADuRtZC2dCUqTSakgJKgQ')

async def print_misha_zaeb(bot: Bot, message : types.Message):
    await message.answer_sticker('CAACAgIAAxkBAAEGSx1jY0LJbBYBHWeKjzukEemjCNxViAACWgADuRtZC1fMhgYQTAjPKgQ')
    await message.answer_sticker('CAACAgIAAxkBAAEGSx9jY0LLH0u2SEqZnzGYbA3qZPNpVgACdQADuRtZCwrzLOB1qOVZKgQ')
    await message.answer_sticker('CAACAgIAAxkBAAEGSx9jY0LLH0u2SEqZnzGYbA3qZPNpVgACdQADuRtZCwrzLOB1qOVZKgQ')
    await message.answer_sticker('CAACAgIAAxkBAAEGSyFjY0LNUmrLHxVU5bHow9Ebkms54wACWwADuRtZC8HaaJQtmnPkKgQ')

text_messages = {
    'ахах' : print_ahah,
    'пиздец' : print_pizd,
    'хорош' : print_good,
    'спать' : print_sleep,
    '+' : print_plus,
    '-' : print_minus,
    'поедем' : print_go_eat,
    'кушать' : print_go_eat,
    'правь' : print_repare,
    'правит' : print_repare,
    'правте' : print_repare,
    'правишь' : print_repare,
    'чини' : print_repare,
    'где' : print_search,
    '?' : print_search,
    'переиграл' : print_replay,
    'бубу' : print_bubu,
    '👉👈' : print_fingers,
    'пидор' : print_pidr,
    'пидар' : print_pidr,
    'шок' : print_fura,
    '((' : print_sad,
    'грусть' : print_sad,
    'плак' : print_sad,
    'похуй' : print_pohui,
    'поебать' : print_pohui,
    'плевать' : print_pohui,
    'без разницы' : print_pohui,
    'болел' : print_virus,
    'болею' : print_virus,
    'справедливо' : print_sprav,
    'миша заебал' : print_misha_zaeb,
}