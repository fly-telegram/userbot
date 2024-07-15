# Fly-telegram UserBot
# this code is licensed by cc-by-nc (https://creativecommons.org/share-your-work/cclicenses)

from database.db import Database

from utils.config import account

prefixes = account.get("prefixes")
db = Database("./database/data.json")
