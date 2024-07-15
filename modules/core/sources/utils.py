# Fly-telegram UserBot
# this code is licensed by cc-by-nc (https://creativecommons.org/share-your-work/cclicenses)

from database.db import Database

from utils.config import account

prefixes = account.get("prefixes")
db = Database("./database/data.json")

text = """
<b>🕊️ fly telegram userbot</b>
├─ <i><b>Owner</b></i>: {owner}
├─ <i><b>Version</b></i>: <code>{version} ({update})</code>
├─ <i><b>Uptime</b></i>: <code>{uptime}</code>
├─<i><b>RAM</b></i>: </code>{ram}</code>
└─ <i><b>Repository</b></i>: <a href="{github_url}">GitHub</a>
"""