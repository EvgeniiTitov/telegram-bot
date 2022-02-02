import typing as t

from aiogram import types

from bot.utils import make_get_request
from bot.handlers._logger import logger


__all__ = "get_word_meaning"


_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/{word}"


def _construct_response_from_json(api_response: t.Sequence[dict]) -> dict:
    api_response = api_response[0]
    return {
        "word": api_response["word"],
        "phonetics": api_response["phonetics"][0]["text"],
        "meaning": api_response["meanings"][0]["definitions"]
    }


async def get_word_meaning(message: types.Message) -> None:
    word = message.text.split(" ")[-1].strip()
    logger.info(f"<< GET_WORD_MEANING >> called with word: {word}")
    if not word:
        await message.answer("No word provided")
    session = await message.bot.get_session()
    response_raw = await make_get_request(
        session, _URL.format(word=word), return_type="json"
    )
    if not response_raw:
        await message.answer(f"API call returned no results for word: {word}")
        return
    try:
        response = _construct_response_from_json(response_raw)
    except Exception as e:
        logger.exception(f"Failed to process API response. Error: {e}")
        await message.answer("Bot failed to process API response")
        return
    await message.answer(str(response))
