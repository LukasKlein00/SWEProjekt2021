class fileReader:
    def __init__(self, name: str):
        self.name = name

    def read(self):
        with open(self.name) as file:
            return file.read()

    def overwriteName(self, name: str):
        self.name = name
        return self
