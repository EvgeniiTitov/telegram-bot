import asyncio
import typing as t

import aiohttp
from aiogram import types

from bot.utils import make_request
from bot.handlers._logger import logger


__all__ = "get_info_by_name"


_URLS = [
    "https://api.agify.io?name={name}",
    "https://api.genderize.io?name={name}",
    "https://api.nationalize.io?name={name}",
]


"""
Thats for test I dont care
"""


async def _make_requests(
    session: aiohttp.ClientSession, query_params: t.MutableMapping[str, str]
) -> t.Any:
    requests_coro = asyncio.gather(
        *(
            make_request(
                session, url.format(**query_params), return_type="json"
            )
            for url in _URLS
        ),
        return_exceptions=True,
    )
    try:
        responses = await asyncio.wait_for(requests_coro, timeout=5.0)
    except asyncio.TimeoutError:
        print("Timed-out")
        return None
    return responses


def _construct_response_from_json(api_response: t.Sequence[dict]) -> dict:
    resp_1 = api_response[0]
    resp_2 = api_response[1]
    resp_3 = api_response[2]
    return {
        "name": resp_1["name"],
        "age": resp_1["age"],
        "gender": resp_2["gender"],
        "country": resp_3["country"][0]["country_id"],
    }


async def get_info_by_name(message: types.Message) -> None:
    name = message.text.split(" ")[-1]
    logger.info(f"Get info by name called with name {name}")
    if not name:
        await message.answer("No name provided")
    session = await message.bot.get_session()
    logger.info("Calling info by name APIs")
    response_raw = await _make_requests(session, query_params={"name": name})
    response = _construct_response_from_json(response_raw)
    logger.info(f"Info by name API result: {response}")
    await message.answer(str(response))
