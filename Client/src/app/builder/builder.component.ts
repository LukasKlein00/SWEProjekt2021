import { Component, Directive, OnInit } from '@angular/core';
import { Class, Item, Map, Npc, Race, requestForMaster, Room } from 'Testfiles/models für Schnittstellen';
import { ToastService } from '../services/toast.service';

@Component({
  selector: 'app-builder',
  templateUrl: './builder.component.html',
  styleUrls: ['./builder.component.scss']
})
export class BuilderComponent implements OnInit {

  privateSlider = false;
  maxPlayerOptions = [3,4,5,6,7,8,9,10]
  requests: requestForMaster[] = [
    {
      request: 'kill Spider',
      requester: {
        name: 'Tom',
        userID: 1,
        health: 79,
        inventar: [{
          name: 'gold nugget',
          description: '',
        },
        {
          name: 'salty Potatos',
          description: '',
        }],
        equipment: {
          name: 'damaged sword',
          description: '',
        },
        race: null,
        class: null,
        mapID: null,
      },
      answer: '',
      x: 1,
      y: 4,
    },
    {
      request: 'eat Apple',
      requester: {
        name: 'Sibille',
        userID: 3,
        health: 40,
        inventar: [
          {
            name: 'rotten Apple',
            description: '',
          }
        ],
        equipment: {
          name: null,
          description: null,
        },
        race: null,
        class: null,
        mapID: null,
      },
      answer: '',
      x: 3,
      y: 4,
    },
    {
      request: 'trade with Robert and run away after a short amount of time',
      requester: {
        name: 'Tim',
        userID: 1,
        health: 20,
        inventar: [],
        equipment: {
          name: null,
          description: null,
        },
        race: null,
        class: null,
        mapID: null,
      },
      answer: '',
      x: 5,
      y: 5,
    }
  ]
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

  constructor(
    public toastService: ToastService
  ) { }

  ngOnInit(): void {
    this.toastService.show('John wants to join', {
      classname: 'toast',
      delay: 7000,
      autohide: true
    });
    this.toastService.show('Elli wants to join', {
      classname: 'toast',
      delay: 5000,
      autohide: true
    });
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
      items: [{
        name: 'blubstrahler',
        description: 'shoots bubbles',
      },
      {
        name: 'blubstrahler2.0',
        description: 'shoots bubbles',
      },
      ],
      npcs: [],
    }
  }
  newClass() {
    const x: Class = {
      name: 'testClass',
      description: 'newClassDescription',
      equipment: null
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
      description: 'newRaceDescription',
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
      description: 'newItemDescription',
    }
    return x
  }

  addItem() {
    this.Map.items = [...this.Map.items, this.selectedItem];
    this.selectedItem = this.newItem()
  }

  editItem(i: Item) {
    this.selectedItem = i;
    this.Map.items.splice(this.Map.items.indexOf(i),1);
  }

  newNpc() {
    const x: Npc = {
      name: 'newNpc',
      description: 'newDescription',
      equipment: null,
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

  selectRoom(r: Room){
    this.selectedRoom = r;
    document.getElementById('nav-room-tab').click();
  }

  submitRequest(req: requestForMaster){
    this.Map.map[req.y][req.x]['isViewed'] = false;
    this.requests.splice(this.requests.indexOf(req),1);
  }
  onItemSelect(item: any) {
    console.log(item);
  }
  onSelectAll(items: any) {
    console.log(items);
  }

  moveOverRequest(request: requestForMaster) {
    this.Map.map[request.y][request.x]['isViewed'] = true;
  }

  moveOutRequest(request: requestForMaster) {
    this.Map.map[request.y][request.x]['isViewed'] = false;
  }
  
}

