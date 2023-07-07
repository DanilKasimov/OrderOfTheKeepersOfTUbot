from aiogram import Bot, Dispatcher, executor, types
import config
import handlers as hand

bot = Bot(token=config.BOT_API_TOKEN)
dp = Dispatcher(bot)


@dp.callback_query_handler()
async def callback_handler(callback_query: types.CallbackQuery):
    await hand.callback_query_handler(bot, callback_query)

@dp.message_handler(content_types=types.ContentType.all())
async def mess_handler(message: types.Message):
    await hand.message_handler(bot, message)

if __name__ == '__main__':
    executor.start_polling(dp)
