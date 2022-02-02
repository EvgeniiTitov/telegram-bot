from aiogram import types, Bot

from bot.utils import make_request
from bot.handlers._logger import logger
from config import Config


__all__ = ("get_crypto_prices", "get_crypto_prices_scheduled")


_URL = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin"


"""
TODO:
1. Ability to specify which crypto price to get?
2. Scheduled: ADA, BTC, DOT (add more cryptos)

2. Meaningful logging
"""


async def get_crypto_prices(message: types.Message) -> None:
    logger.info("Doing API call for crypto prices")
    session = await message.bot.get_session()
    result = await make_request(session, _URL, return_type="json")
    if not result:
        await message.answer("Crypto API call returned nothing")

    logger.info("Crypto API call was successful")
    try:
        reply = "BTC price: $" + str(result[0]["current_price"])
    except Exception as e:
        logger.exception(
            f"Failed to extract price from API response. Error: {e}"
        )
        await message.answer("Error - Failed to extra price from API response")
    else:
        await message.answer(reply)


async def get_crypto_prices_scheduled(bot: Bot) -> None:
    logger.info("Automatic crypto price check triggered. Checking the price")
    session = await bot.get_session()
    result = await make_request(session, _URL, return_type="json")
    if not result:
        await _send_message(bot, "Auto crypto API call returned nothing")
    logger.info("Automatic crypto API call was successful")
    try:
        reply = "BTC price: $" + str(result[0]["current_price"])
    except Exception as e:
        logger.exception(
            f"Failed to extract price from API response. Error: {e}"
        )
        await _send_message(
            bot, "Error - Failed to extra price from API response"
        )
    else:
        await _send_message(bot, reply)


async def _send_message(bot: Bot, message: str) -> None:
    await bot.send_message(chat_id=Config.EUGENE_CHAT_ID, text=message)
