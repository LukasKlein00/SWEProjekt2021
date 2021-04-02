import { Component, OnInit } from '@angular/core';
import { Class, Item, Dungeon, Npc, Race, requestForMaster, Room } from 'Testfiles/models für Schnittstellen';
import { DungeonService } from '../services/dungeon.service';
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
        dungeonID: null,
      },
      answer: '',
      x: 1,
      y: 4,
    },
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
        dungeonID: null,
      },
      answer: '',
      x: 1,
      y: 4,
    },
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
        dungeonID: null,
      },
      answer: '',
      x: 1,
      y: 4,
    },
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
        dungeonID: null,
      },
      answer: '',
      x: 1,
      y: 4,
    }]
  dungeonSize = 11;
  dungeon: Dungeon;
  rooms: Room[][] = [];
  selectedRoom: Room;
  selectedRace: Race = this.newRace();
  selectedClass: Class = this.newClass();
  selectedItem: Item = this.newItem();
  selectedNpc: Npc = this.newNpc();
  blub;

  constructor(
    public toastService: ToastService,
    private DungeonService: DungeonService
  ) { }

  ngOnInit(): void {
    this.dungeon = this.DungeonService.createNewDungeon(this.dungeonSize);
    this.rooms = this.dungeon.rooms;
    console.log(this.rooms);
    this.selectedRoom = this.rooms[5][5];
    /* this.toastService.show('John wants to join', {
      classname: 'toast',
      delay: 7000,
      autohide: true
    });
    this.toastService.show('Elli wants to join', {
      classname: 'toast',
      delay: 5000,
      autohide: true
    }); */
  }
  newClass() {
    return this.DungeonService.createNewClass();
  }

  addClass() {
    this.dungeon.classes.push(this.selectedClass);
    this.selectedClass = this.newClass()
  }

  editClass(c: Class) {
    this.selectedClass = c;
    this.dungeon.classes.splice(this.dungeon.classes.indexOf(c),1);
  }

  newRace() {
    return this.DungeonService.createNewRace();
  }

  addRace() {
    this.dungeon.races.push(this.selectedRace);
    this.selectedRace = this.newRace()
  }

  editRace(r: Race) {
    this.selectedRace = r;
    this.dungeon.races.splice(this.dungeon.races.indexOf(r),1);
  }

  newItem() {
    return this.DungeonService.createNewItem();
  }

  addItem() {
    this.dungeon.items = [...this.dungeon.items, this.selectedItem];
    this.selectedItem = this.newItem()
  }

  editItem(i: Item) {
    this.selectedItem = i;
    this.dungeon.items.splice(this.dungeon.items.indexOf(i),1);
  }

  newNpc() {
    return this.DungeonService.createNewNpc();
  }

  addNpc() {
    this.dungeon.npcs.push(this.selectedNpc);
    this.selectedNpc = this.newNpc()
  }

  editNpc(n: Npc) {
    this.selectedNpc = n;
    this.dungeon.npcs.splice(this.dungeon.npcs.indexOf(n),1);
  }


  toggleRoom(r: Room) {
    r.isActive = !r.isActive;
  }

  increaseDungeon() {
    let newRow = []
    for (let row = 0; row < this.dungeonSize; row++) {
      this.rooms[row].push(this.DungeonService.createNewRoom(row, this.dungeonSize));
      newRow.push(this.DungeonService.createNewRoom(this.dungeonSize, row));
    }
    newRow.push(this.DungeonService.createNewRoom(this.dungeonSize, this.dungeonSize));
    this.rooms.push(newRow);
    this.dungeonSize += 1;
  }

  decreaseDungeon() {
    if (this.dungeonSize>10) {
      this.rooms.pop()
      for (let row of this.rooms) {
        row.pop();
      }
      this.dungeonSize -= 1;
    }
  }

  saveDungeon(){
    localStorage.setItem('blub',JSON.stringify(this.dungeon));
    //sende dungeon an Server!
  }

  publishDungeon(){
    this.saveDungeon();
    //sende MUD an joinable Lobbies
  }

  selectRoom(r: Room){
    this.selectedRoom = r;
    document.getElementById('nav-room-tab').click();
  }

  submitRequest(req: requestForMaster){
    this.dungeon.rooms[req.y][req.x]['isViewed'] = false;
    this.requests.splice(this.requests.indexOf(req),1);
  }
  onItemSelect(item: any) {
    console.log(item);
  }
  onSelectAll(items: any) {
    console.log(items);
  }

  moveOverRequest(request: requestForMaster) {
    this.dungeon.rooms[request.y][request.x]['isViewed'] = true;
  }

  moveOutRequest(request: requestForMaster) {
    this.dungeon.rooms[request.y][request.x]['isViewed'] = false;
  }
  
}

