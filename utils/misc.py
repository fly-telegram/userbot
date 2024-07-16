# Fly-telegram UserBot
# this code is licensed by cc-by-nc (https://creativecommons.org/share-your-work/cclicenses)

from typing import List, Optional

from utils.config import account
from utils.git import version

import datetime
import time
import os

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

    def remove_module(self, name: str) -> dict:
        del modules[name]
        return modules


userbot_version = ".".join(map(str, version))

init_time = time.perf_counter()


def uptime() -> str:
    return str(
        datetime.timedelta(
            seconds=round(
                time.perf_counter() - init_time
            )
        )
    )


def ram() -> float:
    try:
        import psutil

        process = psutil.Process(os.getpid())
        mem = process.memory_info()[0] / 2.0**20
        for child in process.children(recursive=True):
            mem += child.memory_info()[0] / 2.0**20

        return round(mem, 1)
    except Exception:
        return 0
