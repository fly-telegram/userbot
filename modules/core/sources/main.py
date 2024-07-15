# Fly-telegram UserBot
# this code is licensed by cc-by-nc (https://creativecommons.org/share-your-work/cclicenses)

from pyrogram import Client, filters
from pyrogram.types import Message

from git import GitCommandError
import sys
import os

from utils.git import repo, origin
from .utils import prefixes, db


@Client.on_message(filters.command("restart", prefixes=prefixes) & filters.me)
async def restart_cmd(Client, message: Message):
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
async def update_cmd(Client, message: Message):
    await message.edit("🕊 <b>Updating...</b>")

    try:
        origin.pull()
    except GitCommandError:
        repo.git.reset("--hard")

    db.set(
        "restart_info",
        {
            "chat_id": message.chat.id,
            "message_id": message.id,
            "text": "🕊 <b>Updated!</b>",
        },
    )
    db.save()

    os.execl(sys.executable, sys.executable, "main.py")


@Client.on_message(
    filters.command(["addprefix", "addpref"],
                    prefixes=prefixes) & filters.me
)
async def add_prefix_cmd(Client, message: Message):
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