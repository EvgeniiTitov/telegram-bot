from aiogram import types


__all__ = ("send_welcome", "echo")


async def send_welcome(message: types.Message):
    await message.reply("Hi! I am EchoBot!")


async def echo(message: types.Message):
    await message.answer(message.text)
