# Fly-telegram UserBot
# this code is licensed by cc-by-nc (https://creativecommons.org/share-your-work/cclicenses)

from pyrogram import Client, filters
from pyrogram.types import Message

from utils import loader, misc
from .utils import (
    help_manager, prefixes, db,
    DRAGON_EMOJI, EMOJI,
    HIDDEN_EMOJI
)


@Client.on_message(filters.command(["help"], prefixes) & loader.owner)
async def help_cmd(Client, message: Message):
    items = sorted([item for item in help_manager.get_items() if not db.get(str(item[1]), "__hidden__")],
               key=lambda x: (len(x[1]['commands']), x[0]))

    all_commands = "\n".join(
        f"├─ {EMOJI if not data['is.dragon'] else DRAGON_EMOJI} <b>{module}</b>: [ <code>{', '.join(data['commands'])}</code> ]" if i < len(items) - 1 else
        f"└─ {EMOJI if not data['is.dragon'] else DRAGON_EMOJI} <b>{module}</b>: [ <code>{', '.join(data['commands'])}</code> ]"
        for i, (module, data) in enumerate(items)
    )
    await message.edit("🕊 <b>All commands</b>\n" f"{all_commands}")

@Client.on_message(filters.command(["hide", "hidemodule", "hidemod"], prefixes) & loader.owner)
async def hide_cmd(Client, message: Message):
    if len(message.command) <= 1:
        await message.edit("❌ <b>Module?</b>")
        return
    
    module = message.command[1].lower()
    if module not in misc.modules.keys():
        await message.edit("❌ <b>Module not found.</b>")
        return
        
    config = db.get(module)
    config["__hidden__"] = True
    db.set(module, config)
    db.save()
    
    await message.edit(f"🕊️ <b>Module '{module}' is hidden!</b>")
    
@Client.on_message(filters.command(["unhide", "unhidemodule", "unhidemod"], prefixes) & loader.owner)
async def unhide_cmd(Client, message: Message):
    if len(message.command) <= 1:
        await message.edit("❌ <b>Module?</b>")
        return
    
    module = message.command[1].lower()
    if module not in misc.modules.keys():
        await message.edit("❌ <b>Module not found.</b>")
        return
        
    config = db.get(module)
    config["__hidden__"] = False
    db.set(module, config)
    db.save()
    
    await message.edit(f"🕊️ <b>Module '{module}' is not hidden!</b>")
    
@Client.on_message(filters.command(["hidehelp"], prefixes) & loader.owner)
async def hidehelp_cmd(Client, message: Message):
    items = sorted([item for item in help_manager.get_items() if db.get(str(item[1]), "__hidden__")],
               key=lambda x: (len(x[1]['commands']), x[0]))

    all_commands = "\n".join(
        f"├─ {HIDDEN_EMOJI if not data['is.dragon'] else DRAGON_EMOJI} <b>{module}</b>: [ <code>{', '.join(data['commands'])}</code> ]" if i < len(items) - 1 else
        f"└─ {HIDDEN_EMOJI if not data['is.dragon'] else DRAGON_EMOJI} <b>{module}</b>: [ <code>{', '.join(data['commands'])}</code> ]"
        for i, (module, data) in enumerate(items)
    )
    await message.edit("🕊 <b>All hidden commands</b>\n" f"{all_commands}")