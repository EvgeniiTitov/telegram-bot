import typing as t

from aiogram import types

from bot.utils import make_requests
from bot.handlers._logger import logger


__all__ = "get_info_by_name"


_URLS = [
    "https://api.agify.io?name={name}",
    "https://api.genderize.io?name={name}",
    "https://api.nationalize.io?name={name}",
]


"""
That's for test I don't care
"""


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
    response_raw = await make_requests(
        session, _URLS, url_params={"name": name}, return_type="json"
    )
    response = _construct_response_from_json(response_raw)
    logger.info(f"Info by name API result: {response}")
    await message.answer(str(response))
