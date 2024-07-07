import asyncio
import logging
from typing import List, Union

from pyrogram import Client, types


class Conversation:
    def __init__(
        self,
        client: Client,
        chat: Union[str, int],
        clear: bool = False
    ) -> None:
        self.client = client
        self.chat = chat
        self.clear = clear

        self.messages: List[types.Message] = []

    async def __aenter__(self) -> "Conversation":
        return self

    async def __aexit__(
        self,
        exc_type: type,
        exc_value: Exception,
        exc_traceback
    ) -> bool:
        if all(
            [exc_type, exc_value, exc_traceback]
        ):
            logging.exception(exc_value)
        else:
            if self.clear:
                await self.clear_messages()

        return True

    async def send(self, text: str, *args, **kwargs) -> types.Message:
        message = await self.client.send_message(
            self.chat, text, *args, **kwargs)

        self.messages.append(message)
        return message

    async def response(self, timeout: int = 30, limit: int = 1) -> types.Message:
        responses = self.client.get_chat_history(self.chat, limit=limit)
        async for response in responses:
            if response.from_user.is_self:
                timeout -= 1
                if timeout == 0:
                    raise RuntimeError("Timeout error")

                await asyncio.sleep(1)
                responses = self.client.get_chat_history(
                    self.chat, limit=limit)

        self.messages.append(response)
        return response

    async def clear_messages(self) -> None:
        for message in self.messages:
            await message.delete()
