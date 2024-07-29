# Fly-telegram UserBot
# this code is licensed by cc-by-nc (https://creativecommons.org/share-your-work/cclicenses)

from database.types import db
from typing import Union

class Validators:
    @staticmethod
    def Float(value):
        try:
            return float(value)
        except ValueError:
            return False

    @staticmethod
    def Integer(value):
        try:
            return int(value)
        except ValueError:
            return False

    @staticmethod
    def Boolean(value):
        true = ["true", "t", "1", "yes", "y"]
        false = ["false", "f", "0", "no", "n"]
        
        value = value.lower()
        
        if value in true:
            return True
        return False

    @staticmethod
    def String(value):
        return True