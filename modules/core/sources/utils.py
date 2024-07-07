from database.db import Database

from utils.config import account
from utils.misc import Builder

prefixes = account.get("prefixes")
db = Database("./database/data.json")
help_manager = Builder()
