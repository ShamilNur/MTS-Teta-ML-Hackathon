import re

import aiogram

import handlers
from telegram_bot.config.loader import dp


async def on_startup(*args, **kwargs):
    handlers.setup(dp)
    print("Bot started")


if __name__ == "__main__":

    def start():
        aiogram.executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

    start()
