# Fly-telegram UserBot
# this code is licensed by cc-by-nc (https://creativecommons.org/share-your-work/cclicenses)

from database.types import db
from typing import Union


class ConfigValue:
    """
    Represents a single configuration value.

    Attributes:
        key (str): The key of the configuration value.
        value (Union[str, int, bool, float]): The value of the configuration value.
    """

    def __init__(
        self,
        key: str,
        value: Union[str, int, bool, float]
    ):
        self.key = key
        self.value = value


class Config:
    def __init__(
        self,
        module: str,
        *values: "ConfigValue"
    ):
        """
        Initializes a new Config object.

        Args:
            module (str): The name of the module.
            *values (ConfigValue): A variable number of configuration values.
        """
        super().__init__()
        self.module = module
        self.values = values
        self.module_data = db.get(module)

        self.save()

    def save(self):
        """
        Saves the configuration values to the database.
        """
        config_data = self.module_data["__config__"]
        for value in self.values:
            config_data[value.key] = value.value
        self.module_data["__config__"] = config_data
        db.set(self.module, self.module_data)

    def __repr__(self):
        """
        Returns a string representation of the Config object.

        Returns:
            str: A string representation of the Config object.
        """
        return str(self.module_data.get("__config__"))
