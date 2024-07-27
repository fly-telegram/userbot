# Fly-telegram UserBot
# this code is licensed by cc-by-nc (https://creativecommons.org/share-your-work/cclicenses)

from database.types import account
from utils.misc import Builder

prefixes = account.get("prefixes")
help_manager = Builder()

DRAGON_EMOJI = "🐉"
EMOJI = "📦"
HIDDEN_EMOJI = "🕶️"