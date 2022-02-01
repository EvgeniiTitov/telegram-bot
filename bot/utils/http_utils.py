import typing as t

import aiohttp


__all__ = "make_request"


"""
TODO:
1. Add a wrapper on top of make_request catching .raise_for_status()
2. Implement retrying
3. Timeouting with asyncio.wait_for()
4. Multiple requests with asyncio.gather()
etc etc etc
"""


async def make_request(
    session: aiohttp.ClientSession, url: str, return_type="text", **kwargs
) -> t.Union[str, t.Dict]:
    if return_type not in ["text", "json"]:
        raise ValueError("Return type must be either text or json")
    response = await session.get(url, **kwargs)
    response.raise_for_status()
    return (
        await response.text()
        if return_type == "text"
        else await response.json()
    )
