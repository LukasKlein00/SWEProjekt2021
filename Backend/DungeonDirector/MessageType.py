from enum import Enum


class MessageType(Enum):
    whisper = 0
    room = 1
    broadcast = 2
    dungeon_master = 3
