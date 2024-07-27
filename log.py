# Fly-telegram UserBot
# this code is licensed by cc-by-nc (https://creativecommons.org/share-your-work/cclicenses)

import contextlib
import threading
import logging
import asyncio
import functools

from pyrogram import Client
from pyrogram.errors import exceptions
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from inline.types import inline

def fix_task_error(task: asyncio.Task):
    """
    Fixes task errors by canceling the task and ignoring any exceptions.

    Args:
        task (asyncio.Task): The task to fix.
    """
    def no_error(task: asyncio.Task):
        try:
            task.cancel()
        except Exception:
            pass

    task.add_done_callback(functools.partial(no_error))

class UserbotHandler(logging.StreamHandler):
    """
    A custom logging handler for the userbot.

    Args:
        client (Client): The Telegram client instance.
    """

    def __init__(self, client: Client):
        """
        Initializes the handler.

        Args:
            client (Client): The Telegram client instance.
        """
        self.buffer = []

        self.filters = []
        self.lock = threading.RLock()

        self.client = client
        super().__init__()

    def emit(self, record: logging.LogRecord):
        """
        Emits a log record.

        Args:
            record (logging.LogRecord): The log record.
        """
        super().emit(record)
        with contextlib.suppress(Exception):
            task = asyncio.ensure_future(self.inlinelog(record))

    async def inlinelog(self, record: logging.LogRecord):
        """
        Logs an error message to the Telegram bot.

        Args:
            record (logging.LogRecord): The log record.
        """
        if record.levelname == "ERROR" and inline.bot:
            builder = InlineKeyboardBuilder()

            builder.row(types.InlineKeyboardButton(
                text=" Issues", url="https://github.com/fly-telegram/userbot/issues"))

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

def load(client: Client) -> logging.Logger:
    """
    Loads the logging configuration for the userbot.

    Args:
        client (Client): The Telegram client instance.

    Returns:
        logging.Logger: The logger instance.
    """

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