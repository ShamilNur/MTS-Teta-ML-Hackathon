from aiogram.types import Message

from telegram_bot.config.config import URL_RE
from telegram_bot.config.loader import bot
from telegram_bot.services.url_worker import url_worker


async def start(message: Message):
    await bot.send_message(
        message.from_user.id, "Привет! Отправь мне URL, чтобы я распознал его"
    )


async def get_url(message: Message):
    if URL_RE.match(message.text):
        answer = await url_worker(message.text)
        await bot.send_message(
            message.from_user.id,
            answer,
        )
        return
    await bot.send_message(
        message.from_user.id, "Это не похоже на URL, отправьте что-нибудь ещё"
    )


async def delete_wrong_messages(message: Message):
    await bot.delete_message(message.from_user.id, message.message_id)
