# Fly-telegram UserBot
# this code is licensed by cc-by-nc (https://creativecommons.org/share-your-work/cclicenses)

from typing import List, Optional

from database.types import account, db
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
        hidden: Optional[bool] = False
    ) -> None:
        """
        Add module to help

        Args:
            name (str): Module name.
            commands (list): List of module commands.
            is_dragon (bool): Dragon module or not. (optional)
            hidden (bool): is the module hidden? (optional)
        """

        if not name in db.keys():
            db.set(
                name,
                {
                    "__config__": {},
                    "__hidden__": hidden
                }
            )

        modules[name] = {
            "commands": commands,
            "is.dragon": is_dragon
        }

    def get_modules(self) -> List[str]:
        """
        Get all modules keys.

        Returns:
            list: Modules keys 
        """
        return modules.keys()

    def get_items(self):
        """
        Get all modules items.

        Returns:
            items: Modules items.
        """
        return modules.items()

    def remove_module(self, name: str) -> dict:
        """
        Remove module from help.

        Args:
            name (str): Module name.

        Returns:
            list: All modules.
        """
        del modules[name]
        return modules


userbot_version = ".".join(map(str, version))

init_time = time.perf_counter()


def uptime() -> str:
    """
    Get the uptime of the program since it was initialized.

    Returns:
        str: The uptime as a string in the format days, hours, minutes, and seconds.
    """

    return str(
        datetime.timedelta(
            seconds=round(
                time.perf_counter() - init_time
            )
        )
    )


def ram() -> float:
    """
    Get the total memory usage of the current process and its children in megabytes.

    Returns:
        float: The total memory usage in megabytes, rounded to one decimal place. Returns 0 if an error occurs.
    """
    try:
        import psutil

        process = psutil.Process(os.getpid())
        mem = process.memory_info()[0] / 2.0**20
        for child in process.children(recursive=True):
            mem += child.memory_info()[0] / 2.0**20

        return round(mem, 1)
    except Exception:
        return 0
