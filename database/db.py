import ujson


class Database(dict):
    def __init__(self, location: str):
        self.data = ujson.load(open(location, "rb"))
        self.location = location

    def save(self):
        with open(self.location, "w") as file:
            ujson.dump(self.data, file, indent=2)
        self.data = ujson.load(open(self.location, "rb"))

    def get(self, *keys):
        self.data = ujson.load(open(self.location, "rb"))
        data = self.data

        for key in keys:
            if key in data:
                data = data[key]
            else:
                return None
        return data

    def set(self, key: str, value: str):
        self.data = ujson.load(open(self.location, "rb"))
        self.data[key] = value
