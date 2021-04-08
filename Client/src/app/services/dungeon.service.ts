import { Injectable } from '@angular/core';
import { Class, Dungeon, Item, Npc, Race, Room } from 'Testfiles/models für Schnittstellen';
import * as uuid from 'uuid';

@Injectable({
  providedIn: 'root'
})
export class DungeonService {


  constructor() { }

  createNewClass(): Class {
    const x: Class = {
      name: 'newClass',
      description: 'newClassDescription',
      equipment: null
    }
    return x
  }

  createNewRace(): Race {
    const x: Race = {
      name: 'newRace',
      description: 'newRaceDescription',
    }
    return x
  }

  createNewItem(): Item {
    const x: Item = {
      name: 'newItem',
      description: 'newItemDescription',
    }
    return x
  }

  createNewNpc(): Npc {
    const x: Npc = {
      name: 'newNpc',
      description: 'newDescription',
      equipment: null,
    }
    return x
  }

  createNewDungeon(dungeonSize: number): Dungeon {

    //erstellt Räumematrix
    let rooms: Room[][] = [];
    for (let row = 0; row < dungeonSize; row++) {
      let rowElement: Room[] = []
      for (let col = 0; col < dungeonSize; col++) {
        const room: Room = this.createNewRoom(col, row);
        rowElement.push(room)
      }
      rooms.push(rowElement);
    }

    //erstellt Dungeon
    let dungeon: Dungeon = {
      dungeonID: uuid.v4(),
      dungeonMasterID: uuid.v4(),                   //id des Masters dann
      dungeonName: 'Newdungeon',
      dungeonDescription: 'Newdungeon Description',
      maxPlayers: 10,
      rooms: rooms,
      races: [],
      classes: [],
      items: [],
      npcs: [],
      private: false,
      whiteList: [],
      blackList: [],
    }

    

    return dungeon;
  }

  createNewRoom(x,y): Room {
    return {
      name: `NewRoom ${x} ${y}`,
      x: x,
      y: y,
      north: true,
      south: true,
      east: true,
      west: true,
      item: null,
      npc: null,
      players: [],
      isStartRoom: false,
      isActive: false,
      description: `NewRoom ${x} ${y} Description`,
    }
  }
}
