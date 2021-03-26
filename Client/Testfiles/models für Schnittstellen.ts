export class Map {
    mapName: string;
    mapDescription: string;
    mapID?: number;
    maxPlayers: number;
    currentPlayers?: number;
    mapMasterID?: number;
    map?: Room[][];
    races?: Race[];
    classes?: Class[];
    items?: Item[];
    npcs?: Npc[];
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
    players: Player[];
    isStartRoom: boolean;
    isActive: boolean;
    description: string;
}

export class Race {
    name: string;
    description: string;
}

export class Class {
    name: string;
    description: string;
    equipment: Item;
}

export class Item {
    name: string;
    description: string;
}

export class Npc {
    name: string;
    equipment: Item;
    description: string;
}

export class Player {
    name: string;
    userID: number;
    health: number;
    inventar: Item[];
    equipment: Item;
    race: Race;
    class: Class;
    mapID: number;
}

export class Message {
    content: string;
    playerName: string;
    mapID: number;
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

export class ParticipateMap {
    userID: number;
    mapID: number;
}

export class JoinPlayer {
    ownPlayer: Player;
    map: Map;
    isMapMaster: boolean;
}

export class PlayerJoinInfos {
    mapID: number;
    playerName: string;
}

export class WebsocketObject {
    method: 'chat' | 'mapUpdate' | 'playerAction' | 'playerJoin';
    content: Message | PlayerAction | Map | PlayerJoinInfos;
}

export class PlayerAction {
    userID: number;
    mapID: number;
    action: 'goNorth' | 'goSouth' | 'goEast' | 'goWest' | 'battlePlayer' | 'battleNpc';
    enemyUserID?: number;
    enemyNpcID?: number;
}

export class requestForMaster {
    request: string;
    requester: Player;
    answer: string;
}


//objekte nicht benutzt, nur das man weiß, dass diese Requests kommen :)

export class MapRequest {
    mapID: number;
}

export class AuthorisationWithToken {
    token: string;
}


