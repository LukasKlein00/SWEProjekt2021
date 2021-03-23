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
}

export class Room {
    name: string;
    x: number;
    y: number;
    north: boolean;
    south: boolean;
    east: boolean;
    west: boolean;
    items: Item[];
    npc: Npc[];
    players: Player[];
    isStartRoom: boolean;
    isActive: boolean;
    description: string;
}

export class Race {
    name: string;
    bonusstats: Stats;
}

export class Class {
    name: string;
    bonusstats: Stats;
    equipment: Item;
}

export class Item {
    name: string;
    damageTyp: 'normal' | 'magic';
    baseDamage: number;
    value: number;
}

export class Npc {
    name: string;
    stats: Stats;
    equipment: Item;
    behavoir: 'aggressive' | 'neutral' | 'passive';
}

export class Player {
    name: string;
    userID: number;
    stats: Stats;
    inventar: Item[];
    equipment: Item;
    balance: number;
    race: Race;
    class: Class;
    mapID: number;
}

export class Stats {
    maxHealth: number;
    currentHealth: number;
    maxMana: number;
    currentMana: number;
    dodgeChance: number;
    armor: number;
    intelligence: number;
    strength: number;
    experience: number;
    dropExperience: number;
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


//objekte nicht benutzt, nur das man weiß, dass diese Requests kommen :)

export class MapRequest {
    mapID: number;
}

export class AuthorisationWithToken {
    token: string;
}


