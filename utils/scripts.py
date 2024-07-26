# Fly-telegram UserBot
# this code is licensed by cc-by-nc (https://creativecommons.org/share-your-work/cclicenses)

import traceback
import importlib
import subprocess
import sys


def format_exc(e: Exception) -> str:
    """
    Formats an exception into a string.

    Args:
        e (Exception): The exception to format.

    Returns:
        str: A string representation of the exception.
    """
    return traceback.format_exception(*sys.exc_info())


def import_library(library_name: str, package_name: str = None):
    """
    Imports a library and installs it if it's not already installed.

    Args:
        library_name (str): The name of the library to import.
        package_name (str, optional): The name of the package to install. Defaults to None.

    Returns:
        module: The imported library module.

    Raises:
        ImportError: If the library cannot be imported.
    """
    try:
        module = importlib.import_module(library_name)
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", package_name])

    return module