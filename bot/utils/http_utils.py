import asyncio
import typing as t

import aiohttp

from bot.utils.logger import Logger


__all__ = ("make_get_request", "make_get_requests")


"""
TODO:
1. Implement retrying
"""

logger = Logger("http_utils_logger")


async def _make_get_request(
    session: aiohttp.ClientSession, url: str, return_type="text", **kwargs
) -> t.Union[str, dict]:
    response = await session.get(url, **kwargs)
    response.raise_for_status()
    return (
        await response.text()
        if return_type == "text"
        else await response.json()
    )


async def make_get_request(
    session: aiohttp.ClientSession,
    url: str,
    timeout: float = 30.0,
    return_type: str = "text",
    **kwargs,
) -> t.Optional[t.Union[str, dict]]:
    if return_type not in ["text", "json"]:
        raise ValueError("Return type must be either text or json")
    logger.info(f"Calling url {url}")
    try:
        result = await asyncio.wait_for(
            _make_get_request(session, url, return_type, **kwargs),
            timeout=timeout,
        )
    except asyncio.TimeoutError:
        logger.exception(f"Timed-out while calling {url}")
        return None
    except aiohttp.ClientError as e:
        logger.exception(f"Request to {url} failed with error: {e}")
        return None
    logger.info(f"Call to {url} was successful")
    return result


async def make_get_requests(
    session: aiohttp.ClientSession,
    urls: t.Sequence[str],
    url_params: t.Optional[t.MutableMapping[str, str]] = None,
    timeout: float = 30,
    return_type: str = "text",
    **kwargs,
) -> t.Any:
    if return_type not in ["text", "json"]:
        raise ValueError("Return type must be either text or json")
    if not url_params:
        url_params = dict()
    coros = [
        _make_get_request(
            session, url.format(**url_params), return_type, **kwargs
        )
        for url in urls
    ]
    gathered_coro = asyncio.gather(*coros, return_exceptions=True)
    try:
        results = await asyncio.wait_for(gathered_coro, timeout=timeout)
    except asyncio.TimeoutError:
        logger.exception(f"Timed-out while concurrently calling URLS: {urls}")
        return None
    return results


# async def _test():
#     async with aiohttp.ClientSession() as session:
#         response = await make_request(
#             session,
#             url="https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin",
#             return_type="text"
#         )
#         print("Response:", response)
#
#         responses = await make_requests(
#             session,
#             urls=[
#                 "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin",
#                 "https://api.coingecko.com/api/v3/coins/markets?vs_currency=aud&ids=bitcoin",
#                 "https://api.coingecko.com/api/v3/coins/markets?vs_currency=rub&ids=bitcoin"
#             ],
#             return_type="json"
#         )
#         print("Result:")
#         for response in responses:
#             print(response)
#
#
# if __name__ == '__main__':
#     asyncio.run(_test())
