class Character:
    def __init__(self, characterID: int, classID: int, raceID: int, discoveredMap: [int], userID: str, name: str,
                 description: str, health: int):
        self.characterID = characterID
        self.classID = classID
        self.raceID = raceID
        self.discoveredMap = discoveredMap
        self.userID = userID
        self.name = name
        self.description = description
        self.health = health
