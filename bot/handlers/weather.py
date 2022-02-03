import json
import typing as t

from aiogram import Bot

from bot.utils import make_get_request
from bot.handlers._logger import logger
from config import Config


__all__ = "get_current_weather_scheduled"


API_KEY = Config.weather_api_key()
URL = Config.WEATHER_URL.format(key=API_KEY, loc="Sydney")
CHAT_ID = Config.EUGENE_CHAT_ID


async def get_current_weather_scheduled(bot: Bot) -> None:
    logger.info(">> Scheduled weather check triggered <<")
    session = await bot.get_session()
    response = await make_get_request(session, URL)
    if not response:
        await _send_message(bot, "Scheduled weather API call returned nothing")
        return
    logger.info("Scheduled weather API call was successful")
    try:
        weather_info = _parse_api_response(response)
    except Exception:
        logger.exception("Failed while parsing weather API response")
        await _send_message(bot, "Error: Failed while parsing API response")
    else:
        await _send_message(bot, "Weather: " + str(weather_info))


async def _send_message(bot: Bot, message: str) -> None:
    await bot.send_message(chat_id=CHAT_ID, text=message)


def _parse_api_response(api_response: t.Union[str, dict]) -> dict:
    api_response = json.loads(api_response)
    return {
        "Location:": api_response["location"]["name"],
        "Time:": api_response["location"]["localtime"],
        "Temp:": api_response["current"]["temp_c"],
        "Condition": api_response["current"]["condition"]["text"],
        "Wind": api_response["current"]["wind_kph"],
        "Humidity": api_response["current"]["humidity"],
        "UV": api_response["current"]["uv"]
    }


# async def test():
#     async with aiohttp.ClientSession() as session:
#         response = await session.get(
#             url=URL.format(key=API_KEY, loc="Sydney")
#         )
#         text = await response.text()
#         result = json.loads(text)
#         print(json.dumps(result, indent=3))
#
#         answer = {
#             "Location:": result["location"]["name"],
#             "Time:": result["location"]["localtime"],
#             "Temp:": result["current"]["temp_c"],
#             "Condition": result["current"]["condition"]["text"],
#             "Wind": result["current"]["wind_kph"],
#             "Humidity": result["current"]["humidity"],
#             "UV": result["current"]["uv"]
#         }
#         print("\n\n", answer)
#
#
# if __name__ == '__main__':
#     asyncio.run(test())
