# Fly-telegram UserBot
# this code is licensed by cc-by-nc (https://creativecommons.org/share-your-work/cclicenses)

from pyrogram import Client
from pyrogram.enums.parse_mode import ParseMode

from utils.parse_arguments import parse
from database.types import account
from utils.core import main
from utils.git import *

import logging

try:
    import uvloop

    uvloop.install()
except ModuleNotFoundError:
    pass

parser = parse()

client = Client(
    "./account/telegram",
    api_id=account.get("id"),
    api_hash=account.get("hash"),
    app_version=".".join(map(str, version)),
    device_model="Fly Telegram",
    parse_mode=ParseMode.HTML,
    session_string=parser.session_string if parser.session_string else None,
    test_mode=parser.test if parser.test else False
)

try:
    client.run(main(client))
except RuntimeError as e:
    logging.error(f"Connection failed! {e}")
