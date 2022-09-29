from aiogram import Bot, Dispatcher, executor, types
import config

bot = Bot(token=config.BOT_API_TOKEN)
dp = Dispatcher(bot)

horoscope_button = types.InlineKeyboardButton('Гороскоп', callback_data='horoscope')
main_keyboard = types.InlineKeyboardMarkup().add(horoscope_button)

start_button = types.KeyboardButton('/Старт')
start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(start_button)


@dp.callback_query_handler(lambda c: c.data == 'horoscope')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.send_message(callback_query.message.chat.id, 'У всех всё будет хорошо')


@dp.message_handler(commands=['Старт'])
async def start(message: types.Message):
    await message.answer('Привет, шо нада?', reply_markup=main_keyboard)
    await bot.delete_message(message.chat.id, message.message_id)


@dp.message_handler(commands=['Меню'])
async def get_menu(message: types.Message):
    if message.from_user.id == 386629136:
        await message.answer('Меню', reply_markup=start_keyboard)
        await bot.delete_message(message.chat.id, message.message_id)


if __name__ == '__main__':
    executor.start_polling(dp)
