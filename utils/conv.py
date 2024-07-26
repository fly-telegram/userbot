# Fly-telegram UserBot
# this code is licensed by cc-by-nc (https://creativecommons.org/share-your-work/cclicenses)

import asyncio
import logging
from typing import List, Union

from pyrogram import Client, types

class Conversation:
    """
    A context manager for a conversation with a Telegram chat.

    Args:
        client (Client): The Telegram client instance.
        chat (Union[str, int]): The chat ID or username.
        clear (bool, optional): Whether to clear the conversation messages when exiting. Defaults to False.

    Attributes:
        client (Client): The Telegram client instance.
        chat (Union[str, int]): The chat ID or username.
        clear (bool): Whether to clear the conversation messages when exiting.
        messages (List[types.Message]): A list of sent and received messages in the conversation.
    """

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
        """
        Enters the conversation context.
        """
        return self

    async def __aexit__(
        self,
        exc_type: type,
        exc_value: Exception,
        exc_traceback
    ) -> bool:
        """
        Exits the conversation context.

        If an exception occurs, logs the exception. If `clear` is True, clears the conversation messages.
        """
        if all(
            [exc_type, exc_value, exc_traceback]
        ):
            logging.exception(exc_value)
        else:
            if self.clear:
                await self.clear_messages()

        return True

    async def send(self, text: str, *args, **kwargs) -> types.Message:
        """
        Sends a message to the chat.

        Args:
            text (str): The message text.
            *args: Additional arguments for the `send_message` method.
            **kwargs: Additional keyword arguments for the `send_message` method.

        Returns:
            types.Message: The sent message.
        """
        message = await self.client.send_message(
            self.chat, text, *args, **kwargs)

        self.messages.append(message)
        return message

    async def response(self, timeout: int = 30, limit: int = 1) -> types.Message:
        """
        Waits for a response from the chat.

        Args:
            timeout (int, optional): The timeout in seconds. Defaults to 30.
            limit (int, optional): The maximum number of messages to retrieve. Defaults to 1.

        Returns:
            types.Message: The received response message.

        Raises:
            RuntimeError: If the timeout is reached.
        """
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
        """
        Clears the conversation messages.
        """
        for message in self.messages:
            await message.delete()