from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import ContentTypes
from telegram_bot.handlers import main


def setup(dp: Dispatcher):
    dp.register_message_handler(main.start, CommandStart())
    dp.register_message_handler(main.get_url, content_types=ContentTypes.TEXT)
    dp.register_message_handler(
        main.delete_wrong_messages, content_types=ContentTypes.all()
    )