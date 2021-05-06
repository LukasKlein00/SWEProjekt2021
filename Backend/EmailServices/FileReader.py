class FileReader:
    def __init__(self, name: str):
        self.name = name

    def read(self):
        with open(self.name) as file:
            return file.read()

    def overwrite_name(self, name: str):
        self.name = name
        return self
