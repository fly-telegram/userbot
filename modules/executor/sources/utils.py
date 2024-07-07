from utils.config import account, database
from utils.misc import Builder

from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import exceptions

import asyncio
import logging
import sys

prefixes = account.get("prefixes")
help_manager = Builder()

ERROR_EMOJI = "❌"
DONE_EMOJI = "✅"

SECRET_TEXT = "🔐 secret"


def localenv(message: Message,
             client: Client):
    return {
        "message": message,
        "msg": message,
        "m": message,
        "client": client,
        "app": client,
        "c": client,
        "builder": Builder,
        "database": database,
        "db": database
    }


class Stream:
    def __init__(self, stream: asyncio.StreamReader, message: Message, text: str, sleep: int):
        self.stream = stream
        self.message = message
        self.sleep = sleep
        self.text = text

    async def process(self):
        while True:
            line = await self.stream.readline()
            if line:
                self.text += f"<code>{line.decode().strip()}</code>\n"
                try:
                    await self.message.edit(self.text)
                except (exceptions.bad_request_400.MessageNotModified, exceptions.flood_420.FloodWait):
                    pass
                await asyncio.sleep(self.sleep)
            else:
                break


class AsyncTerminal:
    def __init__(self, message: Message, command: str, text: str, sleep: int):
        self.command = command
        self.message = message
        self.text = text
        self.sleep = sleep
        self.command_processes = {}

    async def run(self) -> int:
        process = await asyncio.create_subprocess_shell(self.command,
                                                        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)

        self.command_processes[str(self.message.chat.id)] = {
            str(self.message.id): process}

        stdout_processor = Stream(
            process.stdout, self.message, self.text, self.sleep)
        stderr_processor = Stream(
            process.stderr, self.message, self.text, self.sleep)

        await asyncio.gather(
            stdout_processor.process(),
            stderr_processor.process()
        )

        code = await process.wait()
        del self.command_processes[str(
            self.message.chat.id)][str(self.message.id)]
        return code

    def get_processes(self):
        return self.command_processes
