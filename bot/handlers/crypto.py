from aiogram import types, Bot

from bot.utils import make_get_request
from bot.handlers._logger import logger
from config import Config


__all__ = ("get_crypto_prices", "get_crypto_prices_scheduled")


URL = Config.CRYPTO_URL
CHAT_ID = Config.EUGENE_CHAT_ID


"""
TODO:
1. Ability to specify which crypto price to get?
2. Scheduled: ADA, BTC, DOT (add more cryptos)

2. Meaningful logging
"""


async def get_crypto_prices(message: types.Message) -> None:
    await types.ChatActions.typing()
    coin = message.text.split(" ")[-1].strip().lower()
    logger.info(f"<< GET_CRYPTO_PRICES >> called with coin: {coin}")
    if not coin:
        await message.answer("No coin provided")
        return

    session = await message.bot.get_session()
    result = await make_get_request(
        session, URL.format(currency="usd", coin=coin), return_type="json"
    )
    if not result:
        await message.answer("Crypto API call returned nothing")

    logger.info("Crypto API call was successful")
    try:
        reply = (
            f"{coin.capitalize()}'s price: "
            f"${str(result[0]['current_price'])}"
        )
    except Exception as e:
        logger.exception(
            f"Failed to extract price from API response. Error: {e}"
        )
        await message.answer("Error: Failed while parsing API response")
    else:
        await message.answer(reply)


async def get_crypto_prices_scheduled(bot: Bot) -> None:
    logger.info(">> Scheduled crypto price check triggered <<")
    session = await bot.get_session()
    result = await make_get_request(
        session, URL.format(currency="usd", coin="bitcoin"), return_type="json"
    )
    if not result:
        await _send_message(bot, "Scheduled crypto API call returned nothing")
    logger.info("Scheduled crypto API call was successful")
    try:
        reply = "BTC price: $" + str(result[0]["current_price"])
    except Exception as e:
        logger.exception(
            f"Failed to extract price from API response. Error: {e}"
        )
        await _send_message(bot, "Error: Failed while parsing API response")
    else:
        await _send_message(bot, reply)


async def _send_message(bot: Bot, message: str) -> None:
    await bot.send_message(chat_id=CHAT_ID, text=message)
