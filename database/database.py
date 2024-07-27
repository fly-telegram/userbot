# Fly-telegram UserBot
# this code is licensed by cc-by-nc (https://creativecommons.org/share-your-work/cclicenses)

import ujson


class Database(dict):
    """
    A custom dictionary class for managing a JSON file.

    Attributes:
        data (dict): The dictionary data.
        location (str): The location of the JSON file.
    """

    def __init__(self, location: str):
        """
        Initializes the database.

        Args:
            location (str): The location of the JSON file.
        """
        self.data = ujson.load(open(location, "rb"))
        self.location = location

    def save(self):
        """
        Saves the database to the JSON file.
        """
        with open(self.location, "w") as file:
            ujson.dump(self.data, file, indent=2)
        self.data = ujson.load(open(self.location, "rb"))

    def get(self, *keys):
        """
        Gets a value from the database.

        Args:
            *keys: The keys to access the value.

        Returns:
            Any: The value.
        """
        self.data = ujson.load(open(self.location, "rb"))
        data = self.data

        for key in keys:
            if key in data:
                data = data[key]
            else:
                return None
        return data

    def set(self, key: str, value: str):
        """
        Sets a value in the database.

        Args:
            key (str): The key to set the value.
            value (str): The value to set.
        """
        self.data = ujson.load(open(self.location, "rb"))
        self.data[key] = value
