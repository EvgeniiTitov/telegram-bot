import asyncio

import aiohttp
from aiogram import types

from bot.utils import make_request
from bot.handlers._logger import logger


__all__ = "get_crypto_prices"


_URL = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin"


"""
TODO:
1. Ability to specify which crypto price to get?
2. Meaningful logging
"""


async def get_crypto_prices(message: types.Message) -> None:
    session = await message.bot.get_session()
    logger.info("Doing API call for crypto prices")
    try:
        response = await asyncio.wait_for(
            make_request(session=session, url=_URL, return_type="json"),
            timeout=5.0,
        )
    except asyncio.TimeoutError:
        logger.exception(f"Timed-out while calling {_URL}")
        return None
    except aiohttp.ClientError as e:
        logger.exception(f"Request to {_URL} failed with error: {e}")
        return None
    logger.info("Crypto API call was successful")
    reply = (
        response[0]["current_price"]
        if response
        else "API call returned nothing"
    )
    await message.answer(reply)
