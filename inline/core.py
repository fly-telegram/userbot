# Fly-telegram UserBot
# this code is licensed by cc-by-nc (https://creativecommons.org/share-your-work/cclicenses)

from pyrogram import errors, Client
from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramUnauthorizedError
from aiogram.enums import ParseMode

from . import events
from utils.conv import Conversation
from database.types import db

import random
import re
import string
import asyncio


class Inline:
    def __init__(self):
        """
        Initializes the inline bot manager.
        """
        self.bot = None
        self.dispatcher = None
        self.errors_text = ["Sorry.", "That I cannot do.", "too many attempts"]

    async def create(self, client: Client, botfather: str = "@BotFather") -> str:
        """
        Creates a new inline bot.

        Args:
            client (Client): The Telegram client instance.
            botfather (str, optional): The BotFather username. Defaults to "@BotFather".

        Returns:
            str: The bot token.
        """
        id = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(5))
        me = await client.get_me()
        username = f"flyTG_{id}_bot"
        display_name = f"🕊 Fly-telegram of {me.first_name}"

        messages = [
            "/cancel",
            "/newbot",
            display_name,
            username,
            "/setinline",
            f"@{username}",
            "🕊 fly-telegram: ",
        ]

        pattern = r"Use this token to access the HTTP API:\n([0-9]+:[A-Za-z0-9_]+)"
        token = None

        async with Conversation(client, botfather, True) as conv:
            for message in messages:
                try:
                    await conv.send(message)
                    response = await conv.response(limit=2)
                    match = re.search(pattern, response.text)
                    if match:
                        token = match.group(1)
                    if any(error in response.text for error in self.errors_text):
                        return False
                except errors.UserIsBlocked:
                    await client.unblock_user(botfather)

            async with Conversation(client, f"@{username}", True) as conv:
                await conv.send("/start")

        return token

    async def load(self, client: Client):
        """
        Loads the inline bot.

        Args:
            client (pyrogram.Client): The Telegram client instance.
        """
        token = db.get("inline_token")
        if not token:
            token = await self.create(client)
            db.set("inline_token", token)
            db.save()

        try:
            self.bot = Bot(token=token, default=Bot.Default.parse_mode(ParseMode.HTML))
        except TelegramUnauthorizedError:
            db.set("inline_token", "")
            db.save()
            return

        self.dispatcher = Dispatcher()
        self.dispatcher.include_router(events.router)

        me = await client.get_me()
        await self.bot.send_message(me.id, "🕊 <b>Fly-telegram userbot is loaded!</b>")

        asyncio.ensure_future(self.dispatcher.start_polling(self.bot, skip_updates=True, handle_signals=False))