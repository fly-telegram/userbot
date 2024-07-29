# Fly-telegram UserBot
# this code is licensed by cc-by-nc (https://creativecommons.org/share-your-work/cclicenses)

from database.types import db, account
from utils.misc import Builder

from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import exceptions

import asyncio

from utils.config import Config, ConfigValue
from utils.validators import Validators

config_module = Config(
    "executor",
    ConfigValue(
        "terminal.speed",
        0.25,
        Validators.Float
    ),
    
)

prefixes = account.get("prefixes")

ERROR_EMOJI = "❌"
DONE_EMOJI = "✅"

SECRET_TEXT = "🔐 secret"


def localenv(message: Message, client: Client) -> dict:
    """
    Returns a dictionary of local environment variables.

    Args:
        message (Message): The message instance.
        client (Client): The client instance.

    Returns:
        dict: A dictionary of local environment variables.
    """
    return {
        "message": message,
        "msg": message,
        "m": message,
        "client": client,
        "app": client,
        "c": client,
        "builder": Builder,
        "database": db,
        "db": db,
    }


class BufferedStream:
    def __init__(self, stream: asyncio.StreamReader, buffer_size: int):
        """
        Initializes a buffered stream.

        Args:
            stream (asyncio.StreamReader): The stream reader instance.
            buffer_size (int): The buffer size.
        """
        self.stream = stream
        self.buffer = bytearray()
        self.buffer_size = buffer_size

    async def read(self) -> bytes:
        """
        Reads data from the stream.

        Returns:
            bytes: The read data.
        """
        chunk = await self.stream.read(self.buffer_size)
        if not chunk:
            return None

        self.buffer.extend(chunk)
        data = bytes(self.buffer)

        self.buffer.clear()
        return data


class Stream:
    def __init__(
        self,
        stream: asyncio.StreamReader,
        message: Message,
        text: str,
        sleep: int,
        buffer_size: int = 8192,
    ):
        """
        Initializes a stream.

        Args:
            stream (asyncio.StreamReader): The stream reader instance.
            message (Message): The message instance.
            text (str): The text to be processed.
            sleep (int): The sleep time.
            buffer_size (int, optional): The buffer size. Defaults to 8192.
        """
        self.stream = BufferedStream(stream, buffer_size)
        self.message = message
        self.sleep = sleep
        self.text = text
        self.last_chunk = b""

    async def process(self):
        """
        Processes the stream.
        """
        while True:
            chunk = await self.stream.read()
            if chunk:
                if chunk != self.last_chunk:
                    self.last_chunk = chunk
                    self.text += f"<code>{chunk.decode().strip()}</code>\n"
                    try:
                        await self.message.edit(self.text)
                    except (
                        exceptions.bad_request_400.MessageNotModified,
                        exceptions.flood_420.FloodWait,
                    ):
                        pass
                    await asyncio.sleep(self.sleep)
            else:
                break


class AsyncTerminal:
    def __init__(
        self,
        message: Message,
        command: str,
        text: str,
        sleep: int,
        buffer_size: int = 4096,
    ):
        """
        Initializes an async terminal.

        Args:
            message (Message): The message instance.
            command (str): The command to be executed.
            text (str): The text to be processed.
            sleep (int): The sleep time.
            buffer_size (int, optional): The buffer size. Defaults to 4096.
        """
        self.command = command
        self.message = message
        self.text = text
        self.sleep = sleep
        self.buffer_size = buffer_size
        self.command_processes = {}

    async def run(self) -> int:
        """
        Runs the async terminal.

        Returns:
            int: The exit code.
        """
        process = await asyncio.create_subprocess_shell(
            self.command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )

        self.command_processes[str(self.message.chat.id)] = {
            str(self.message.id): process
        }

        stdout_processor = Stream(
            process.stdout, self.message, self.text, self.sleep, self.buffer_size
        )
        stderr_processor = Stream(
            process.stderr, self.message, self.text, self.sleep, self.buffer_size
        )

        await asyncio.gather(stdout_processor.process(), stderr_processor.process())

        code = await process.wait()
        del self.command_processes[str(
            self.message.chat.id)][str(self.message.id)]
        return code

    def get_processes(self) -> dict:
        """
        Returns the command processes.

        Returns:
            dict: A dictionary of command processes.
        """
        return self.command_processes
