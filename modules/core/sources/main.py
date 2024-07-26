# Fly-telegram UserBot
# this code is licensed by cc-by-nc (https://creativecommons.org/share-your-work/cclicenses)

from pyrogram import Client, filters
from pyrogram.types import Message

from git import GitCommandError
import sys
import os

from utils import loader
from utils.git import repo, origin, version, check_update
from utils.misc import uptime, ram
from .utils import prefixes, db, text


@Client.on_message(filters.command("restart", prefixes=prefixes) & loader.owner)
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


@Client.on_message(filters.command("update", prefixes=prefixes) & loader.owner)
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
                    prefixes=prefixes) & loader.owner
)
async def addprefix_cmd(Client, message: Message):
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


@Client.on_message(
    filters.command(["userbot", "info", "fly-telegram", "flytg"],
                    prefixes=prefixes) & loader.owner
)
async def info_cmd(client: Client, message: Message):
    update = "Update available!" if check_update() else "Up-To-Date"
    me = await client.get_me()
    github_url = db.get("core", "update", "GIT_ORIGIN")

    userbot_version = ".".join(map(str, version))

    owner = '<a href="tg://user?id={}">{}</a>'.format(
            me.id,
            me.username
    )

    await message.delete()
    await client.send_photo(
        chat_id=message.chat.id,
        photo="./assets/logo.gif",
        caption=text.format(
            owner=owner,
            version=userbot_version,
            update=update,
            uptime=uptime(),
            ram=ram(),
            github_url=github_url
        )
    )
