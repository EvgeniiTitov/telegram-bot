import logging
import asyncio

from aiogram import Bot, Dispatcher

from bot.handlers import (
    get_crypto_prices,
    get_info_by_name,
    echo,
    send_welcome,
)
from config import Config


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


TOKEN = Config().token


def register_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(send_welcome, commands=["start", "hello"])
    dp.register_message_handler(get_crypto_prices, commands=["cryptoprice"])
    dp.register_message_handler(get_info_by_name, commands=["infoaboutme"])
    dp.register_message_handler(echo)


async def main() -> None:
    bot = Bot(token=TOKEN)
    logger.info("Created bot")
    try:
        dp = Dispatcher(bot)
        register_handlers(dp)
        logger.info("Registered handlers with the Dispatcher")
        await dp.start_polling()
    finally:
        await bot.close()


if __name__ == "__main__":
    asyncio.run(main())
