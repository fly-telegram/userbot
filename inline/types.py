# Fly-telegram UserBot
# this code is licensed by cc-by-nc (https://creativecommons.org/share-your-work/cclicenses)

__all__ = ["Message", "CallbackQuery", "InlineQuery", "inline"]

from .core import Inline
from aiogram.types import Message, CallbackQuery, InlineQuery

inline = Inline()
