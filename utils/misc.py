# core help and Dragon-Userbot

from typing import List, Optional
from utils.config import account
from utils.git import version

prefix = account.get("prefixes")

modules_help = {}

modules = {}


class Builder:
    def add_module(
        self,
        name: str,
        commands: List[str],
        is_dragon: Optional[bool] = False,
    ) -> None:
        modules[name] = {
            "commands": commands,
            "is.dragon": is_dragon
        }

    def get_modules(self) -> List[str]:
        return modules.keys()

    def get_items(self):
        return modules.items()

    def get_module(self, name: str) -> dict:
        return modules[name]

    def remove_module(self, name: str) -> dict:
        del modules[name]
        return modules


userbot_version = ".".join(map(str, version))
