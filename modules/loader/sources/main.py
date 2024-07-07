from pyrogram import Client, filters
from pyrogram.types import Message

import asyncio
import tempfile
import zipfile
import shutil
import sys
import os

from database.db import Database
from utils.git import version

from .utils import prefixes, help_manager, loader


@Client.on_message(
    filters.command(["load", "lm", "loadmod"], prefixes) & filters.me
)
async def load_module(Client, message: Message):
    """
    Load a module from a ZIP file or dragon module
    """
    dragon = False
    reply = message.reply_to_message
    file = message if message.document else reply if reply and reply.document else None

    if not file:
        await message.edit("❌ <b>A reply or a document is needed!</b>")
        return

    if file.document.file_name.endswith(".py") or not file.document.file_name.endswith(".zip"):
        dragon = True

    filename = file.document.file_name
    module_name = filename.split(
        ".py")[0] if dragon else filename.split(".zip")[0]

    await message.edit(f"🕊 <b>{module_name}</b>\n<code>Loading module...</code>")

    if not dragon:
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, filename)
            await file.download(file_path)

            with zipfile.ZipFile(file_path, "r") as archive:
                archive.extractall(os.path.join("modules", module_name))
    else:
        file_path = os.path.join("dragon_modules", filename)
        await file.download(file_path)

    if not dragon:
        info = Database(os.path.join("modules", module_name, "module.json"))

        if info.get("requires"):
            python_min_version = info.get("requires", "python_min")
            if python_min_version and sys.version_info < tuple(python_min_version):
                await message.edit(
                    f"❌ <b>{module_name} installing error</b>\n"
                    f"<code>This module requires a python version greater than {'.'.join(map(str, python_min_version))}</code>"
                )
                shutil.rmtree(os.path.join("modules", module_name))
                return

            version_min = info.get("requires", "version_min")
            if version_min and version < tuple(version_min):
                await message.edit(
                    f"❌ <b>{module_name} installing error</b>\n"
                    f"<code>This module requires a version of fly-telegram higher than {'.'.join(map(str, version_min))}</code>"
                )
                shutil.rmtree(os.path.join("modules", module_name))
                return

            requirements = info.get("requires", "requirements")
            format_requirements = "\n".join(
                f"├─ {requirement}" if i < len(
                    requirements) - 1 else f"└─ {requirement}"
                for i, requirement in enumerate(requirements)
            )

            if requirements:
                await message.edit(
                    f"🕊 <b>{module_name}</b>\n"
                    f"<code>Installing requirements: \n{format_requirements}</code>"
                )

                pip_installer = await asyncio.create_subprocess_exec(
                    sys.executable, "-m", "pip", "install", "-q", *requirements
                )
                output = await pip_installer.wait()

                if output != 0:
                    await message.edit("❌ <b>installing requirements failed!</b>")
                    shutil.rmtree(os.path.join("modules", module_name))
                    return

    try:
        if not dragon:
            await loader.load(module_name, Client)
        else:
            await loader.load_dragon(module_name, Client)
    except Exception as error:
        await message.edit(
            f"❌ <b>{module_name} installing error</b>\n<code>{error}</code>"
        )
        if not dragon:
            shutil.rmtree(os.path.join("modules", module_name))
        else:
            os.remove(os.path.join("dragon_modules", filename))
        return

    if dragon:
        await message.edit(
            f"🕊 <b>{module_name} is loaded!</b>\n"
            "└─ 🐉 <i>Dragon-Userbot module</i>"
        )
        return

    author = info.get("meta", "author")
    description = info.get("meta", "description")
    module_version = "".join(map(str, info.get("meta", "version")))

    await message.edit(
        f"🕊 <b>{module_name} by {author} is loaded!</b>\n"
        f"├─ ℹ️ <i>{description}</i>\n"
        f"└─ 📦 <code>{module_version}</code>"
    )


@Client.on_message(
    filters.command(["unload", "unlm", "unloadmod"],
                    prefixes) & filters.me
)
async def unload_module(Client, message: Message):
    """ "
    Unload module by name.
    """
    if len(message.command) <= 1:
        await message.edit("❌ <b>Module name must be entered.</b>")
        return

    module_name = message.command[1].lower()
    remove = True

    dragon = help_manager.get_module(module_name)["is.dragon"]

    if "--no-remove" in message.command:
        remove = False

    await message.edit(f"🕊 <b>{module_name}</b>\n" "<code>Unloading module...</code>")

    try:
        if not dragon:
            await loader.unload(module_name, Client, remove=remove)
        else:
            await loader.unload_dragon(module_name, Client, remove=remove)
    except Exception as error:
        await message.edit(
            f"❌ <b>{module_name} unloading error</b>\n<code>{error}</code>"
        )
        return

    await message.edit(f"🕊 <b>{module_name}</b>\n" "<code>Module unloaded!</code>")

help_manager.add_module("loader", ["load", "unload"])
