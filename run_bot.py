import logging

from aiogram import Bot, Dispatcher, executor, types

from bot.command_handlers import get_crypto_prices, get_info_by_name
from config import Config


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


TOKEN = Config().token
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

dp.register_message_handler(get_crypto_prices, commands=["cryptoprice"])
dp.register_message_handler(get_info_by_name, commands=["infoaboutme"])


@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    await message.reply("Hi! I am EchoBot!")


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
