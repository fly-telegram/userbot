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
        value: Union[str, int, bool, float],
        validator
    ):
        self.key = key
        self.value = value
        self.validator = validator

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
        for value in self.values:
            self.module_data["__config__"][value.key] = value.value
        
        db.set(self.module, self.module_data)
    
    def __repr__(self):
        """
        Returns a string representation of the Config object.
        Returns:
            str: A string representation of the Config object.
        """
        return str(self.module_data.get("__config__"))
    
    def __getitem__(self, key):
        """
        Returns the value associated with the given key.
        Args:
            key (str): The key of the configuration value.
        Returns:
            Union[str, int, bool, float]: The value associated with the given key.
        """
        return self.module_data["__config__"].get(key)
    
    def __setitem__(self, key, value):
        """
        Sets the value associated with the given key.
        Args:
            key (str): The key of the configuration value.
            value (Union[str, int, bool, float]): The new value.
        """
        for config_value in self.values:
            if config_value.key == key:
                if not config_value.validator(value):
                    raise ValueError(f"Invalid value for key '{key}'.")
                self.module_data["__config__"][key] = value
                db.set(self.module, self.module_data)