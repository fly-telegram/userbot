# Fly-telegram UserBot
# this code is licensed by cc-by-nc (https://creativecommons.org/share-your-work/cclicenses)

from database.types import account
from utils.loader import Loader
from utils.misc import Builder

prefixes = account.get("prefixes")
loader = Loader()
help_manager = Builder()
