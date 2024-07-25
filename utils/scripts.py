# Fly-telegram UserBot
# this code is licensed by cc-by-nc (https://creativecommons.org/share-your-work/cclicenses)

import traceback
import importlib
import subprocess
import sys


def format_exc(e: Exception) -> str:
    """Return full exception"""
    return traceback.format_exception(*sys.exc_info())


def import_library(library_name: str, package_name: str = None):
    """
    Load package from PyPi (for Dragon-Userbot modules)
    """

    try:
        module = importlib.import_module(library_name)
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", package_name])

    return module
