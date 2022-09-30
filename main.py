from aiogram import Bot, Dispatcher, executor, types
import config
import handlers as hand

bot = Bot(token=config.BOT_API_TOKEN)
dp = Dispatcher(bot)


@dp.callback_query_handler(lambda c: c.data == 'horoscope')
async def callback_horoscope(callback_query: types.CallbackQuery):
    await hand.horoscope_handler(bot, callback_query)


@dp.callback_query_handler(lambda c: c.data == 'registration')
async def callback_registration(callback_query: types.CallbackQuery):
    await hand.registration_user(bot, callback_query)


@dp.callback_query_handler(lambda c: c.data in ['fuck_you', 'set_mouse', 'complement'])
async def callback_handler(callback_query: types.CallbackQuery):
    await hand.callback_handler(bot, callback_query)


@dp.message_handler(commands=['Старт'])
async def get_menu(message: types.Message):
    await hand.get_menu(bot, message)


@dp.message_handler(commands=['Меню'])
async def get_menu(message: types.Message):
    await hand.get_start(bot, message)


@dp.callback_query_handler()
async def fuck_you(callback_query: types.CallbackQuery):
    await hand.command_handler(bot, callback_query)


if __name__ == '__main__':
    executor.start_polling(dp)
