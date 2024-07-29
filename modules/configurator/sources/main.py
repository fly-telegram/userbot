# Fly-telegram UserBot
# this code is licensed by cc-by-nc (https://creativecommons.org/share-your-work/cclicenses)

from pyrogram import Client, filters
from pyrogram.types import Message

from utils import loader, config
from .utils import prefixes, db, EMOJI


@Client.on_message(filters.command(["config", "cfg"], prefixes) & loader.owner)
async def config_cmd(Client, message: Message):
    modules = {
        key: value["__config__"]
        for key, value in db.items()
        if isinstance(value, dict) and "__config__" in value
        and bool(value["__config__"])
    }
    if len(message.command) <= 1:
        all_modules = "\n".join(
            f"├─ {EMOJI} <b>{module}</b>\n" + "\n".join(
                f"│  ├─ <b>{key}</b>" if i < len(config_keys) - 1 else
                f"│  └─ <b>{key}</b>"
                for i, key in enumerate(config_keys)
            ) if i < len(modules) - 1 else
            f"└─ {EMOJI} <b>{module}</b>\n" + "\n".join(
                f"    ├─ <b>{key}</b>" if i < len(config_keys) - 1 else
                f"    └─ <b>{key}</b>"
                for i, key in enumerate(config_keys)
            )
            for i, (module, config_keys) in enumerate(modules.items())
        )
        await message.edit("🕊️ <b>Modules and values editable:</b>\n" f"{all_modules}")
    elif len(message.command) == 2:
        module_name = message.command[1]
        if module_name in modules:
            config_keys = "\n".join(
                f"├─ <b>{key}</b>" if i < len(modules[module_name]) - 1 else
                f"└─ <b>{key}</b>"
                for i, key in enumerate(modules[module_name])
            )
            await message.edit(f"🕊️ <b>{module_name}</b>\n" f"{config_keys}")
        else:
            await message.edit("❌ <b>Module not found.</b>")
    elif len(message.command) == 4:
        module_name = message.command[1]
        key = message.command[2]
        value = message.command[3]
        module = db.get(module_name)
        if module_name in modules:
            if key in modules[module_name]:
                for config_value in self.values:
                    if config_value.key == key:
                        if not config_value.validator(value):
                            await message.edit("❌ <b>Invalid value.</b>")
                            return
                        module["__config__"][key] = value
                        db.set(module_name, module)
                        await message.edit(f"🕊️ <b>{module_name}</b>\n"
                                           f"<code>Value is set to {value}!</code>")
                        return
                await message.edit("❌ <b>Key is not found.</b>")