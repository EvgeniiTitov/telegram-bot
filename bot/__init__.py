import logging

from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from bot.handlers import (
    get_crypto_prices,
    get_crypto_prices_scheduled,
    get_info_by_name,
    echo,
    send_welcome,
)
from config import Config


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


TOKEN = Config().token


def register_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(send_welcome, commands=["start", "hello"])
    dp.register_message_handler(get_crypto_prices, commands=["cryptoprice"])
    dp.register_message_handler(get_info_by_name, commands=["infoaboutme"])
    dp.register_message_handler(echo)


def register_scheduler_handlers(scheduler: AsyncIOScheduler, bot: Bot) -> None:
    scheduler.add_job(
        func=get_crypto_prices_scheduled,
        trigger=IntervalTrigger(minutes=5),
        args=(bot,),
        kwargs={},
        name="Test",
    )


async def run_bot() -> None:
    bot = Bot(token=TOKEN)
    scheduler = AsyncIOScheduler()
    logger.info("Bot and Scheduler created")
    register_scheduler_handlers(scheduler, bot)
    logger.info("Registered automatic handlers with the Scheduler")
    try:
        scheduler.start()
        dp = Dispatcher(bot)
        register_handlers(dp)
        logger.info("Registered user triggered handlers with the Dispatcher")
        await dp.start_polling()
    finally:
        await bot.session.close()
