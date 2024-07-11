# Fly-telegram UserBot
# this code is licensed by cc-by-nc (https://creativecommons.org/share-your-work/cclicenses)

import importlib
import shutil
import sys
import os

from typing import Set

import pyrogram

from .misc import Builder, modules_help

MODULES_DIR = "modules"
DRAGON_MODULES_DIR = "dragon_modules"

class CodeAnalysis:
    def __init__(self):
        self.fucntions = (
            "eval",
           "exec",
           "pyrogram.raw.functions.account.DeleteAccount",
        )
        self.items = []

    def analyze(self, path: str) -> Set[str]:
        with open(path, 'r') as file:
            code = file.read()
            
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    if '.'.join(reversed([node.func.attr] + [n.attr for n in reversed(node.func.value)])) in self.fuctions:
                        self.items.append('.'.join(reversed([node.func.attr] + [n.attr for n in reversed(node.func.value)])))
                elif isinstance(node.func, ast.Name):
                    if node.func.id in self.functions:
                        self.items.append(node.func.id)
        
        return self.items

class Loader:
    def __init__(self):
        self.help_manager = Builder()

        self.core_modules = (
            "help",
            "loader",
            "core",
            "executor",
        )

    async def unload(self, name: str, client: pyrogram.Client, remove: bool = True) -> bool:
        """Unload a module"""
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

        if remove:
            shutil.rmtree(os.path.join(MODULES_DIR, name))

        return True

    async def load(self, name: str, client: pyrogram.Client) -> bool:
        """Load a module"""
        path = os.path.join(MODULES_DIR, name)
        
        if name not in os.listdir(MODULES_DIR):
            raise NameError(f"Module '{name}' is not found!")
        elif "module.json" not in os.listdir(path):
            raise ValueError(
                f"Module '{name}' is out of date or does not have a module information file."
            )

        for file in os.listdir(path):
            if file.endswith('.py'):
                founded_items = CodeAnalysis.analyze(path)
                if founded_items:
                    raise Exception(f"Malicious code was found in '{name}' dragon module: ", ",".join(founded_items))

        module = importlib.import_module(
            f"{MODULES_DIR}.{name}.sources.main"
        )  # load module

        for obj_name, obj in vars(module).items():
            handlers = getattr(obj, "handlers", [])
            if not isinstance(handlers, list):
                continue

            for handler, group in handlers:
                client.add_handler(handler, group)  # add handler

        return True

    async def load_dragon(self, name: str, client: pyrogram.Client):
        """"Load dragon module"""
        if f"{name}.py" not in os.listdir(DRAGON_MODULES_DIR):
            raise NameError(f"Dragon module '{name}' is not found!")
       founded_items = CodeAnalysis.analyze(path)
        if founded_items:
            raise Exception(f"malicious code was found in '{name}' dragon module: ", ",".join(founded_items))
            
        module = importlib.import_module(f"{DRAGON_MODULES_DIR}.{name}")

        # convert "modules_help" to "modules"
        for module_name, commands in modules_help.items():
            self.help_manager.add_module(
                module_name,
                [
                    command.split()[0]
                    for command in commands.keys()
                ], True)

        for obj_name, obj in vars(module).items():
            handlers = getattr(obj, "handlers", [])
            if not isinstance(handlers, list):
                continue

            for handler, group in handlers:
                client.add_handler(handler, group)  # add handler

    async def unload_dragon(self, name: str, client: pyrogram.Client, remove: bool = True
                            ) -> bool:
        """"Unload dragon modules"""
        if f"{name}.py" not in os.listdir(DRAGON_MODULES_DIR):
            raise NameError(f"Dragon module '{name}' is not found!")

        module = importlib.import_module(f"{DRAGON_MODULES_DIR}.{name}")
        self.help_manager.remove_module(name)

        if name in sys.modules:
            del sys.modules[name]

        if remove:
            os.remove(os.path.join(DRAGON_MODULES_DIR, f"{name}.py"))

        return True
