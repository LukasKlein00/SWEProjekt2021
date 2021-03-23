import { Component, OnInit } from '@angular/core';
import { Class, Item, Map, Npc, Race, Room } from 'Testfiles/models für Schnittstellen';

@Component({
  selector: 'app-builder',
  templateUrl: './builder.component.html',
  styleUrls: ['./builder.component.scss']
})
export class BuilderComponent implements OnInit {

  mapSize = 11;
  Map: Map;
  Rooms: Room[][] = [];
  selectedRoom: Room;
  selectedRace: Race = this.newRace();
  selectedClass: Class = this.newClass();
  selectedItem: Item = this.newItem();
  selectedNpc: Npc = this.newNpc();
  behaviors = ['passive','neutral','aggressive'];
  damageTypes = ['normal','magic'];
  blub;

  constructor() { }

  ngOnInit(): void {
    for (let row = 0; row < this.mapSize; row++) {
      let rowElement = []
      for (let col = 0; col < this.mapSize; col++) {
        const r: Room = this.newRoom(col, row);
        rowElement.push(r)
      }
      this.Rooms.push(rowElement);
    }
    const sRoom: Room = this.Rooms[Math.floor(this.mapSize / 2)][Math.floor(this.mapSize / 2)]
    sRoom.isStartRoom = true;
    sRoom.description = 'Starting Room Description';
    sRoom.isActive = true;
    this.selectedRoom = sRoom;

    this.Map = {
      mapName: 'NewMap',
      mapDescription: 'NewMap Description',
      maxPlayers: 10,
      map: this.Rooms,
      races: [],
      classes: [],
      items: [],
      npcs: [],
    }
  }
  newClass() {
    const x: Class = {
      name: 'testClass',
      bonusstats: {
        maxHealth: 100,
        maxMana: 100,
        dodgeChance: 0,
        armor: 0,
        intelligence: 10,
        strength: 10,
      },
      equipment: {
        name: 'newWeapon',
        damageTyp: 'normal',
        baseDamage: 10,
        value: 10,
    }
    }
    return x
  }

  addClass() {
    this.Map.classes.push(this.selectedClass);
    this.selectedClass = this.newClass()
  }

  editClass(c: Class) {
    this.selectedClass = c;
    this.Map.classes.splice(this.Map.classes.indexOf(c),1);
  }

  newRace() {
    const x: Race = {
      name: 'testRace',
      bonusstats: {
        maxHealth: 100,
        maxMana: 100,
        dodgeChance: 0,
        armor: 0,
        intelligence: 10,
        strength: 10,
      }
    }
    return x
  }

  addRace() {
    this.Map.races.push(this.selectedRace);
    this.selectedRace = this.newRace()
  }

  editRace(r: Race) {
    this.selectedRace = r;
    this.Map.races.splice(this.Map.races.indexOf(r),1);
  }

  newItem() {
    const x: Item = {
      name: 'newItem',
      damageTyp: 'normal',
      baseDamage: 10,
      value: 10,
    }
    return x
  }

  addItem() {
    this.Map.items.push(this.selectedItem);
    this.selectedItem = this.newItem()
  }

  editItem(i: Item) {
    this.selectedItem = i;
    this.Map.items.splice(this.Map.items.indexOf(i),1);
  }

  newNpc() {
    const x: Npc = {
      name: 'newNpc',
      stats: {
        maxHealth: 100,
        maxMana: 100,
        dodgeChance: 10,
        armor: 0,
        intelligence: 10,
        strength: 10,
        experience: 100,
        dropExperience: 10,
      },
      equipment: null,
      behavoir: 'neutral',
    }
    return x
  }

  addNpc() {
    this.Map.npcs.push(this.selectedNpc);
    this.selectedNpc = this.newNpc()
  }

  editNpc(n: Npc) {
    this.selectedNpc = n;
    this.Map.npcs.splice(this.Map.npcs.indexOf(n),1);
  }


  toggleRoom(r: Room) {
    r.isActive = !r.isActive;
  }

  increaseMap() {
    let newRow = []
    for (let row = 0; row < this.mapSize; row++) {
      this.Rooms[row].push(this.newRoom(row, this.mapSize));
      newRow.push(this.newRoom(this.mapSize, row));
    }
    newRow.push(this.newRoom(this.mapSize, this.mapSize));
    this.Rooms.push(newRow);
    this.mapSize += 1;
  }

  decreaseMap() {
    if (this.mapSize>10) {
      this.Rooms.pop()
      for (let row of this.Rooms) {
        row.pop();
      }
      this.mapSize -= 1;
    }
  }

  newRoom(x, y) {
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

  saveMap(){
    localStorage.setItem('blub',JSON.stringify(this.Map));
    //sende Map an Server!
  }

  publishMap(){
    this.saveMap();
    //sende MUD an joinable Lobbies
  }
}

