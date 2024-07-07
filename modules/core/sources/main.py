from pyrogram import Client, filters
from pyrogram.types import Message

import sys
import os

from utils.git import origin
from .utils import prefixes, db, help_manager


@Client.on_message(filters.command("restart", prefixes=prefixes) & filters.me)
async def restart(Client, message: Message):
    db.set(
        "restart_info",
        {
            "chat_id": message.chat.id,
            "message_id": message.id,
            "text": "🕊 <b>Restarted!</b>",
        },
    )
    db.save()

    await message.edit("🕊 <b>Restarting...</b>")
    os.execl(sys.executable, sys.executable, "main.py")


@Client.on_message(filters.command("update", prefixes=prefixes) & filters.me)
async def update(Client, message: Message):
    await message.edit("🕊 <b>Updating...</b>")
    pull = origin.pull()
    if not pull:
        await message.edit("🕊 <b>your userbot is the latest version!</b>")
        return
    
    db.set(
        "restart_info",
        {
            "chat_id": message.chat.id,
            "message_id": message.id,
            "text": "🕊 <b>Updated!</b>",
        },
    )
    os.execl(sys.executable, sys.executable, "main.py")

@Client.on_message(
    filters.command(["addprefix", "addpref"],
                    prefixes=prefixes) & filters.me
)
async def add_prefix(Client, message: Message):
    if len(message.command) <= 1:
        await message.edit("🕊 <b>The prefix must be entered.</b>")
        return

    prefix = message.command[1].lower()
    prefixes.append(prefix)
    account.set("prefixes", prefixes)
    account.save()

    await message.edit(
        f"🕊 <b>added new prefix: {prefix}</b>\n"
        f"<code>prefixes: {' | '.join(prefixes)}</code>"
    )

help_manager.add_module("core", ["addprefix", "restart"])
