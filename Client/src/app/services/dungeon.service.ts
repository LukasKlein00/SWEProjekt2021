import { Injectable } from '@angular/core';
import { Class, Dungeon, Item, Npc, Race, Room } from 'Testfiles/models für Schnittstellen';
import * as uuid from 'uuid';
import { jsonSchema } from 'uuidv4';

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

    if (JSON.parse(localStorage.getItem('currentUser'))) {
      //erstellt Räumematrix
    let rooms: Room[] = [];
    for (let row = 1; row <= dungeonSize; row++) {
      for (let col = 1; col <= dungeonSize; col++) {
        const room: Room = this.createNewRoom(col, row);
        rooms.push(room)
      }
    }

    //erstellt Dungeon
    
    let dungeon: Dungeon = {
      dungeonID: null,
      dungeonMasterID: JSON.parse(localStorage.getItem('currentUser')).userID,            
      dungeonName: 'Newdungeon',
      dungeonDescription: 'Newdungeon Description',
      maxPlayers: 10,
      rooms: rooms,
      races: [],
      classes: [],
      items: [],
      npcs: [],
      private: false,
      accessList: [],
    }
    return dungeon; 
    } else {
      let dungeon: Dungeon = {         
        dungeonName: 'Newdungeon',
        dungeonDescription: 'Newdungeon Description',
        maxPlayers: 10,
        rooms: [],
        races: [],
        classes: [],
        items: [],
        npcs: [],
        private: false,
        accessList: [],
      }
      return dungeon;
    }
  }

  createNewRoom(x,y): Room {
    return {
      x: x,
      y: y,
    }
  }
}
