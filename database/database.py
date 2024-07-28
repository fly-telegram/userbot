# Fly-telegram UserBot
# this code is licensed by cc-by-nc (https://creativecommons.org/share-your-work/cclicenses)

import ujson
from pathlib import Path
from typing import Any, Dict


class Database(dict):
    def __init__(self, location: str = "db.json"):
        """
        Initializes the database.

        Args:
            location (str): The location of the JSON file.
        """
        self.location = Path(location)
        self.update(**self.load(self.location))

    def load(self, location: Path) -> Dict[str, Any]:
        """
        Loads the database from the JSON file.

        Args:
            location (Path): The location of the JSON file.

        Returns:
            Dict[str, Any]: The loaded database.
        """
        if not location.exists():
            return {}
        with location.open("rb") as file:
            return ujson.load(file)

    def save(self) -> None:
        """
        Saves the database to the JSON file.
        """
        with self.location.open("w") as file:
            ujson.dump(self, file, indent=2)

        self.update(**self.load(self.location))

    def get(self, *keys):
        """
        Gets a value from the database.

        Args:
            *keys: The keys to access the value.

        Returns:
            Any: The value.
        """
        self.update(**self.load(self.location))

        data = self
        for key in keys:
            if key in data:
                data = data[key]
            else:
                return None
        return data

    def set(self, key: str, value: Any):
        """
        Sets a value in the database.

        Args:
            key (str): The key to set the value.
            value (Any): The value to set.
        """
        self.update(**self.load(self.location))

        self[key] = value
        self.save()
