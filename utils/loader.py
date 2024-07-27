# Fly-telegram UserBot
# this code is licensed by cc-by-nc (https://creativecommons.org/share-your-work/cclicenses)

import importlib
import inspect
import shutil
import ast
import sys
import os

from typing import Set

from pyrogram import Client, filters
from pyrogram.types import Message

from .misc import Builder, modules_help
from database.types import account

MODULES_DIR = "modules"
DRAGON_MODULES_DIR = "dragon_modules"
loaded_modules: Set[object] = set()


class Filters:
    def owner_filter(_, __, message: Message) -> bool:
        """
        Check if the message sender is an owner or the bot itself.

        Args:
            _ (any): Unused argument.
            __ (any): Unused argument.
            message (Message): The message to check.

        Returns:
            bool: True if the message sender is an owner or the bot itself, False otherwise.
        """
        return bool(
            message.from_user.id in account.get(
                "owners") or message.from_user.is_self
        )


owner = filters.create(Filters.owner_filter)


class CodeAnalysis:
    def __init__(self):
        """
        Initialize the CodeAnalysis class.

        The class is used to analyze Python code and detect the use of certain functions and modules.
        """
        self.functions = (
            "eval",
            "exec",
            "DeleteAccount",
        )
        self.allowed: Set[str] = set()  # Initialize allowed set
        self.items: Set[str] = set()  # Initialize items set

    def analyze(self, path: str) -> Set[str]:
        """
        Analyze the Python code in the given file.

        Args:
            path (str): The path to the Python file to analyze.

        Returns:
            Set[str]: A set of detected function and module names.
        """
        with open(path, "r") as file:
            code = file.read()

        tree = ast.parse(code)

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):

                if isinstance(node.func, ast.Attribute):
                    if (
                        isinstance(node.func.value, ast.Call)
                        and isinstance(node.func.value.func, ast.Name)
                        and node.func.value.func.id == "__import__"
                    ):
                        module_name = node.func.value.args[0].s
                        if module_name in self.allowed:
                            self.items.add(module_name)

                elif isinstance(node.func, ast.Name) and node.func.id in self.functions:
                    self.items.add(node.func.id)

        return self.items


class Loader:
    def __init__(self):
        """
        Initializes the Loader instance.

        Creates a new instance of the `Builder` class and sets the core modules.
        """
        self.help_manager = Builder()

        self.core_modules = (
            "help",
            "loader",
            "core",
            "executor",
        )

    async def unload(self, name: str, client: Client, remove: bool = True) -> bool:
        """
        Unloads a module.

        Args:
            name (str): The name of the module to unload.
            client (Client): The client instance.
            remove (bool, optional): Whether to remove the module's files. Defaults to True.

        Returns:
            bool: True if the module was unloaded successfully, False otherwise.

        Raises:
            NameError: If the module is not found.
            PermissionError: If the module is a system module.
        """
        if name not in os.listdir(MODULES_DIR):
            raise NameError(f"Module '{name}' is not found!")
        if name in self.core_modules:
            raise PermissionError("Cannot unload system modules!")

        module = importlib.import_module(
            f"modules.{name}.sources.main")  # load module

        for obj_name, obj in vars(module).items():
            handlers = getattr(obj, "handlers", [])
            if not isinstance(handlers, list):
                continue

            for handler, group in handlers:
                client.remove_handler(handler, group)  # remove handler

        self.help_manager.remove_module(name)  # remove from help

        if name in sys.modules:
            del sys.modules[name]  # remove from sys modules

        if module in loaded_modules:
            loaded_modules.remove(module)

        if remove:
            shutil.rmtree(os.path.join(MODULES_DIR, name))

        return True

    async def load(self, name: str, client: Client,
                   check_code: bool = True) -> bool:
        """
        Loads a module.

        Args:
            name (str): The name of the module to load.
            client (Client): The client instance.
            check_code (bool, optional): Whether to check the module's code for malicious content. Defaults to True.

        Returns:
            bool: True if the module was loaded successfully, False otherwise.

        Raises:
            NameError: If the module is not found.
            ValueError: If the module is out of date or does not have a module information file.
            Exception: If malicious code is found in the module.
        """
        path = os.path.join(MODULES_DIR, name)

        if name not in os.listdir(MODULES_DIR):
            raise NameError(f"Module '{name}' is not found!")
        elif "module.json" not in os.listdir(path):
            raise ValueError(
                f"Module '{name}' is out of date or does not have a module information file."
            )

        if check_code:
            for file in os.listdir(path):
                if file.endswith(".py"):
                    path = os.path.join(MODULES_DIR, name, file)
                    founded_items = CodeAnalysis().analyze(path)
                    if founded_items:
                        raise Exception(
                            f"Malicious code was found in '{name}' module: ",
                            ",".join(founded_items),
                        )

        module = importlib.import_module(
            f"modules.{name}.sources.main")  # load module
        loaded_modules.add(module)

        # add to help
        commands = [
            func[:-4]
            for func, _ in inspect.getmembers(module, inspect.isfunction)
            if func.endswith("_cmd")
        ]
        self.help_manager.add_module(name, commands)

        for obj_name, obj in vars(module).items():
            handlers = getattr(obj, "handlers", [])
            if not isinstance(handlers, list):
                continue

            for handler, group in handlers:
                client.add_handler(handler, group)  # add handler

        return True

    async def load_dragon(self, name: str, client: Client,
                          check_code: bool = True) -> bool:
        """
        Loads a dragon module.

        Args:
            name (str): The name of the dragon module to load.
            client (Client): The client instance.
            check_code (bool, optional): Whether to check the module's code for malicious content. Defaults to True.

        Returns:
            bool: True if the module was loaded successfully, False otherwise.

        Raises:
            NameError: If the dragon module is not found.
            Exception: If malicious code is found in the module.
        """
        path = os.path.join(DRAGON_MODULES_DIR, f"{name}.py")
        if not os.path.exists(path):
            raise NameError(f"Dragon module '{name}' is not found!")

        if check_code:
            founded_items = CodeAnalysis().analyze(path)
            if founded_items:
                raise Exception(
                    f"Malicious code was found in '{name}' dragon module: ",
                    ",".join(founded_items),
                )

        module = importlib.import_module(f"dragon_modules.{name}")
        loaded_modules.add(module)

        # convert "modules_help" to "modules"
        for module_name, commands in modules_help.items():
            self.help_manager.add_module(
                module_name, [command.split()[0]
                              for command in commands.keys()], True
            )

        for obj_name, obj in vars(module).items():
            handlers = getattr(obj, "handlers", [])
            if not isinstance(handlers, list):
                continue

            for handler, group in handlers:
                client.add_handler(handler, group)  # add handler

        return True

    async def unload_dragon(
        self, name: str, client: Client, remove: bool = True
    ) -> bool:
        """
        Unloads a dragon module.

        Args:
            name (str): The name of the dragon module to unload.
            client (Client): The client instance.
            remove (bool, optional): Whether to remove the module's files. Defaults to True.

        Returns:
            bool: True if the module was unloaded successfully, False otherwise.

        Raises:
            NameError: If the dragon module is not found.
        """
        path = os.path.join(DRAGON_MODULES_DIR, f"{name}.py")
        if not os.path.exists(path):
            raise NameError(f"Dragon module '{name}' is not found!")

        module = importlib.import_module(f"dragon_modules.{name}")
        self.help_manager.remove_module(name)

        if name in sys.modules:
            del sys.modules[name]

        if module in loaded_modules:
            loaded_modules.remove(module)

        if remove:
            os.remove(path)

        return True
