from aiogram import types


__all__ = ("send_welcome", "echo")


async def send_welcome(message: types.Message):
    response = [
        "Hi! Here are your details for integration:",
        f"\nChat id: {message.chat.id}; \nUsername: {message.chat.username}",
    ]
    await message.reply(" ".join(response))


async def echo(message: types.Message):
    await message.answer(message.text)
