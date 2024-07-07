import contextlib
import threading
import logging
import asyncio

from pyrogram import Client
from pyrogram.errors import exceptions
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from inline.types import inline


def fix_task_error(task: asyncio.Task):
    def no_error(task: asyncio.Task):
        try:
            task.cancel()
        except Exception:
            pass

    task.add_done_callback(functools.partial(no_error))


class UserbotHandler(logging.StreamHandler):
    def __init__(self, client: Client):
        self.buffer = []

        self.filters = []
        self.lock = threading.RLock()

        self.client = client
        super().__init__()

    def emit(self, record: logging.LogRecord):
        super().emit(record)
        with contextlib.suppress(Exception):
            task = asyncio.ensure_future(self.inlinelog(record))

    async def inlinelog(self, record: logging.LogRecord):
        if record.levelname == "ERROR" and inline.bot:
            builder = InlineKeyboardBuilder()

            builder.row(types.InlineKeyboardButton(
                text="⚠️ Issues", url="https://github.com/fly-telegram/userbot/issues"))

            try:
                me = await self.client.get_me()
            except exceptions.flood_420.FloodWait:
                return self.buffer.append(self.format(record))

            text = f"<code>{self.format(record)}</code>\n"
            if self.buffer:
                for x in self.buffer:
                    text += f"<code>{x}</code>\n"

            await inline.bot.send_message(me.id, text,
                                          reply_markup=builder.as_markup())


def load(client: Client):
    format = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(funcName)s: %(lineno)d - %(message)s",
        "%m-%d %H:%M:%S")

    logger = logging.getLogger()
    logger.handlers = []
    logger.setLevel(logging.INFO)

    telegram_handler = UserbotHandler(client)
    logger.addHandler(telegram_handler)
    telegram_handler.setFormatter(format)

    logging.getLogger("pyrogram").setLevel(logging.WARNING)
    logging.getLogger("aiogram").setLevel(logging.WARNING)
    logging.getLogger("aiohttp").setLevel(logging.WARNING)

    return logger
