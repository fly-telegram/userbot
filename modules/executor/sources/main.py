import traceback
from meval import meval
from pyrogram import Client, filters
from pyrogram.types import Message

from .utils import (
    help_manager, prefixes,
    localenv, ERROR_EMOJI,
    DONE_EMOJI, SECRET_TEXT,
    AsyncTerminal
)

command_processes = {}  # {"chatID": {"messageID": "PROC"}}


@Client.on_message(filters.command(["eval", "e", "python"], prefixes) & filters.me)
async def eval(Client, message: Message):
    if len(message.command) == 1:
        await message.edit("❌ <b>The code has to be entered!</b>")
        return

    code = message.text.split(maxsplit=1)[1].strip()
    error = False

    try:
        result = str(await meval(code, globals(), **localenv(message, Client)))
    except Exception as e:
        error = True
        result = traceback.format_exc()

    phone = message.from_user.phone_number
    result = result.replace(phone, SECRET_TEXT)

    await message.edit(
        f"<b>🐍 Python code:</b>\n"
        f"<pre language='python'>{code}</pre>\n"
        f"<b>{DONE_EMOJI if not error else ERROR_EMOJI} Result: </b>\n"
        f"<pre language='python'>{result}</pre>"
    )


@Client.on_message(filters.command(["sh", "bash", "terminal"], prefixes) & filters.me)
async def terminal(Client, message: Message):
    global command_processes

    if len(message.command) == 1:
        await message.edit("❌ Need a command!")

    await message.edit("🕊 <b>Running...</b>")
    command = message.text.split(maxsplit=1)[1].strip()

    text = (
        "📼 <b>Command</b>: \n"
        f"<code>{command}</code>\n"
        "📀 <b>Result</b>: \n"
    )

    try:
        process = AsyncTerminal(message, command, text, 0.25)
        command_processes = process.get_processes()
        await process.run()
    except Exception as error:
        return await message.edit(
            "📼 <b>Command</b>: \n"
            f"<code>{command}</code>\n"
            "❌ <b>Executing error</b>: \n"
            f"<pre language=python>{error}</pre>"
        )


@Client.on_message(filters.command(["terminate", "kill", "pkill"], prefixes) & filters.me)
async def kill(Client, message: Message):
    reply = message.reply_to_message
    if not reply:
        await message.edit("❌ <b>Terminal?</b>")
        return
    if str(reply.chat.id) not in command_processes.keys():
        await message.edit("❌ <b>In this chat is not running a terminal.</b>")
        return

    command_processes[str(reply.chat.id)][str(reply.id)].kill()
    del command_processes[str(reply.chat.id)][str(reply.id)]
    await message.edit("🕊 <b>Terminal killed.</b>")


@Client.on_message(filters.command(["terminals", "processes"], prefixes) & filters.me)
async def terminals(Client, message: Message):
    items = sorted(command_processes.items())
    terminals = "\n".join(
        f"├─ <i><a href='https://t.me/c/{chat_id}/{message_id}'>💻 {i+1} Terminal</a></i>" if i < len(items) - 1 else
        f"└─ <i><a href='https://t.me/c/{chat_id[4:]}/{message_id}'>💻 {i+1} Terminal</a></i>"
        for i, (chat_id, data) in enumerate(items) for message_id in data.keys()
    )
    not_terminals = "└─ 💻 <i>No running terminals.</i>"

    await message.edit(
        "🕊 <b>Terminals</b>\n" f"{terminals if terminals else not_terminals}"
    )

help_manager.add_module("executor", ["eval", "terminal", "kill", "terminals"])
