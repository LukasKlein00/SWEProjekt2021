class Räume:

    def __init__(self, userIDs: [int], koordinaten: [int, int], raumID: int, dungeonID: int, npcID: int, itemID: int,
                 raumbeschreibung: str, raumname: str, isStartraum: bool, norden: bool, süden: bool, westen: bool,
                 osten: bool):
        self.userIDs = userIDs
        self.koordinaten = koordinaten
        self.raumID = raumID
        self.dungeonID = dungeonID
        self.npcID = npcID
        self.itemID = itemID
        self.raumbeschreibung = raumbeschreibung
        self.raumname = raumname
