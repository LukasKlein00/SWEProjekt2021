export class Dungeon {
    dungeonName?: string;
    dungeonDescription?: string;
    dungeonID?: string;
    maxPlayers?: number;
    currentPlayers?: number;
    dungeonMasterID?: string;
    rooms?: Room[];
    races?: Race[];
    classes?: Class[];
    items?: Item[];
    npcs?: Npc[];
    private?: boolean;
    accessList?: Access[];
}

export class Access {
    name: string;
    isAllowed: boolean;
}

export class Room {
    name: string;
    x: number;
    y: number;
    north: boolean;
    south: boolean;
    east: boolean;
    west: boolean;
    item: Item;
    npc: Npc;
    players?: Player[];
    isStartRoom: boolean;
    isActive?: boolean;
    isViewed?: boolean;
    description: string;
}

export class Race {
    raceID?: string;
    name: string;
    description: string;
}

export class Class {
    classID?: string;
    name: string;
    description: string;
    equipment: Item;
}

export class Item {
    itemID?: string;
    name: string;
    description: string;
}

export class Npc {
    npcID?: string;
    name: string;
    equipment: Item;
    description: string;
}

export class Player {
    name: string;
    description?: string;
    userID: string;
    health?: number;
    inventar?: Item[];
    equipment?: Item;
    race: Race;
    class: Class;
    dungeonID: string;
}

export class SubmitPlayer {
    name: string;
    race: Race;
    class: Class;
    dungeonID: number;
    equipment: Item[];
    userID: number;
}

export class Message {
    content: string;
    playerName: string;
    dungeonID: number;
    receiver: 'dungeonchat' | 'roomchat' | string;
}

export class Register {
    username: string;
    name: string;
    surname: string;
    email: string;
    password: string;
}

export class Login {
    username: string;
    password: string;
}

export class LoginData {
    token: string;
    username: string;
    userid: number;
}

export class User {
    username: string;
    name?: string;
    surname?: string;
    email?: string;
    passwort?: string;
    characters: Player[];
}

export class ParticipateDungeon {
    userID: number;
    dungeonID: number;
}

export class JoinPlayer {
    ownPlayer: Player;
    dungeon: Dungeon;
    isDungeonMaster: boolean;
}

export class PlayerJoinInfos {
    dungeonID: number;
    playerName: string;
}

export class WebsocketObject {
    method: 'chat' | 'dungeonUpdate' | 'playerAction' | 'playerJoin';
    content: Message | PlayerAction | Dungeon | PlayerJoinInfos;
}

export class PlayerAction {
    userID: number;
    dungeonID: number;
    action: 'goNorth' | 'goSouth' | 'goEast' | 'goWest' | 'battlePlayer' | 'battleNpc';
    enemyUserID?: number;
    enemyNpcID?: number;
}

export class requestForMaster {
    request: string;
    requester: Player;
    answer: string;
    x: number;
    y: number;
}


//objekte nicht benutzt, nur das man weiß, dass diese Requests kommen :)

export class DungeonRequest {
    dungeonID: number;
}

export class AuthorisationWithToken {
    token: string;
}


