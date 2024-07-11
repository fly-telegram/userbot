# Fly-telegram UserBot
# this code is licensed by cc-by-nc (https://creativecommons.org/share-your-work/cclicenses)

from aiogram import Bot
from aiogram import types, Router
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()


@router.message()
async def main_handler(message: types.Message) -> types.Message:
    builder = InlineKeyboardBuilder()

    builder.row(types.InlineKeyboardButton(
        text="💻 GitHub", url="https://github.com/fly-telegram")
    )
    builder.row(types.InlineKeyboardButton(
        text="🕊 Updates",
        url="https://t.me/flyTG_UB")
    )

    await message.reply("🕊 <b>Hi! this is fly-telegram's inline userbot!</b>",
                        reply_markup=builder.as_markup())
