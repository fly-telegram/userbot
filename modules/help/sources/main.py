# Fly-telegram UserBot
# this code is licensed by cc-by-nc (https://creativecommons.org/share-your-work/cclicenses)

from pyrogram import Client, filters
from pyrogram.types import Message

from utils import loader
from .utils import (
    help_manager, prefixes,
    DRAGON_EMOJI, EMOJI
)


@loader.command(Client, "help")
async def help_cmd(Client, message: Message):
    items = sorted(help_manager.get_items(),
                   key=lambda x: (len(x[1]['commands']), x[0]))

    all_commands = "\n".join(
        f"├─ {EMOJI if not data['is.dragon'] else DRAGON_EMOJI} <b>{module}</b>: [ <code>{', '.join(data['commands'])}</code> ]" if i < len(items) - 1 else
        f"└─ {EMOJI if not data['is.dragon'] else DRAGON_EMOJI} <b>{module}</b>: [ <code>{', '.join(data['commands'])}</code> ]"
        for i, (module, data) in enumerate(items)
    )
    await message.edit("🕊 <b>All commands</b>\n" f"{all_commands}")
