# Fly-telegram UserBot
# this code is licensed by cc-by-nc (https://creativecommons.org/share-your-work/cclicenses)

from pyrogram import Client, idle

from inline.types import inline
from utils.loader import Loader
from utils.parse_arguments import parse
from database.types import db
from utils.git import check_update
from utils.misc import init_time

import time
import log
import os

logo = """
      :::::::::: :::     :::   :::             ::::::::::: :::::::: 
     :+:        :+:     :+:   :+:                 :+:    :+:    :+: 
    +:+        +:+      +:+ +:+                  +:+    +:+         
   :#::+::#   +#+       +#++:  +#++:++#++:++    +#+    :#:          
  +#+        +#+        +#+                    +#+    +#+   +#+#    
 #+#        #+#        #+#                    #+#    #+#    #+#     
###        ########## ###                    ###     ########       
"""

parser = parse()
loader = Loader()


async def main(client: Client):
    if not parser.no_logo:
        print(logo)

    await client.start()
    await inline.load(client)

    logger = log.load(client)

    update = "Update available!" if check_update() else "Up-To-Date"
    logger.info(f"Userbot is started! ({update})")

    success_modules = 0
    failed_modules = 0

    if not os.path.isdir('./dragon_modules'):
        os.makedirs("dragon_modules")

    for module in os.listdir("./dragon_modules"):
        if os.path.isfile(os.path.join("./dragon_modules", module)):
            try:
                name = module.split(".py")[0]
                await loader.load_dragon(name, client)
                logger.info(f"[LOADER] Dragon module '{name}' loaded")
                success_modules += 1
            except Exception as error:
                logger.error(
                    f"[LOADER] Failed load '{name}' dragon module: {error}")
                failed_modules += 1

    for module in os.listdir("./modules"):
        if os.path.isdir(os.path.join("./modules", module)):
            try:
                await loader.load(module, client)
                logger.info(f"[LOADER] Module '{module}' loaded")
                success_modules += 1
            except Exception as error:
                logger.error(
                    f"[LOADER] Failed load '{module}' module: {error}")
                failed_modules += 1

    logger.info(
        f"[LOADER] Successfully imported modules: {success_modules}, with errors: {failed_modules}."
    )

    if db.get("restart_info"):
        await client.edit_message_text(
            db.get("restart_info", "chat_id"),
            db.get("restart_info", "message_id"),
            db.get("restart_info", "text"),
        )
        db.set("restart_info", None)
        db.save()

    await idle()
    await client.stop()
