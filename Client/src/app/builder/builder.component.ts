import { Component, OnInit } from '@angular/core';
import { Map, Room } from 'Testfiles/models für Schnittstellen';

@Component({
  selector: 'app-builder',
  templateUrl: './builder.component.html',
  styleUrls: ['./builder.component.scss']
})
export class BuilderComponent implements OnInit {

  mapSize = 11;
  Map: Map;
  Rooms: Room[][] = [];
  selectedRoom: Room;;

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
    }
  }

  activateRoom(r: Room) {
    r.isActive = true;
  }

  deactivateRoom(r: Room) {
    r.isActive = false;
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
      name: `NewRoom ${x} + ${y}`,
      x: x,
      y: y,
      north: true,
      south: true,
      east: true,
      west: true,
      items: [],
      npc: [],
      players: [],
      isStartRoom: false,
      isActive: false,
      description: `NewRoom ${x} + ${y} Description`,
    }
  }
}

