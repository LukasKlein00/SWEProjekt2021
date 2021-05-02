import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Class, Item, Dungeon, Npc, Race, requestForMaster, Room } from 'Testfiles/models für Schnittstellen';
import { DungeonService } from '../services/dungeon.service';
import { HttpService } from '../services/http.service';
import { ToastService } from '../services/toast.service';

@Component({
  selector: 'app-builder',
  templateUrl: './builder.component.html',
  styleUrls: ['./builder.component.scss']
})
export class BuilderComponent implements OnInit {

  privateSlider = false;
  maxPlayerOptions = [3, 4, 5, 6, 7, 8, 9, 10]
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
  dungeonSize = 13;
  dungeon: Dungeon;
  rooms: Room[] = []
  selectedRoom: Room;
  selectedRace: Race = this.newRace();
  selectedClass: Class = this.newClass();
  selectedItem: Item = this.newItem();
  selectedNpc: Npc = this.newNpc();

  constructor(
    public toastService: ToastService,
    private DungeonService: DungeonService,
    private httpService: HttpService,
    private route: ActivatedRoute,
  ) { }

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    console.log(id);
    this.dungeon = this.DungeonService.createNewDungeon(this.dungeonSize);
    this.rooms = this.dungeon.rooms;
    if (id) {
      this.httpService.getDungeon(id)
        .subscribe((res) => {
          this.dungeon.dungeonID = res[0];
          this.dungeon.dungeonName = res[1];
          this.dungeon.dungeonDescription = res[2];
          this.dungeon.maxPlayers = res[3];
          this.dungeon.rooms = JSON.parse(res[5]);
          this.dungeon.races = JSON.parse(res[6]);
          this.dungeon.classes = JSON.parse(res[7]);
          this.dungeon.items = JSON.parse(res[8]);
          this.dungeon.npcs = JSON.parse(res[9]);
          this.dungeon.private = res[10];
        });
    }
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
    this.dungeon.classes.splice(this.dungeon.classes.indexOf(c), 1);
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
    this.dungeon.races.splice(this.dungeon.races.indexOf(r), 1);
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
    this.dungeon.items.splice(this.dungeon.items.indexOf(i), 1);
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
    this.dungeon.npcs.splice(this.dungeon.npcs.indexOf(n), 1);
  }


  toggleRoom(r: Room) {
    if (r.isActive) {
      delete r.isActive;
      delete r.description;
      delete r.isStartRoom;
      delete r.name;
      delete r.item;
      delete r.npc;
    } else {
      r['isActive'] = true;
    }
  }

  increaseDungeon() {
    this.dungeonSize += 1;
    for (let row = 1; row < this.dungeonSize; row++) {
      this.rooms.push(this.DungeonService.createNewRoom(row, this.dungeonSize));
    }
    for (let col = 1; col <= this.dungeonSize; col++) {
      this.rooms.push(this.DungeonService.createNewRoom(this.dungeonSize, col));
    }

  }

  decreaseDungeon() {
    if (this.dungeonSize > 10) {
      this.dungeonSize--;
      this.rooms = this.rooms.filter(room => room.x <= this.dungeonSize && room.y <= this.dungeonSize)
    }
  }

  saveDungeon() {



    const safeDungeon: Dungeon = Object.assign({},this.dungeon);
    safeDungeon.rooms = safeDungeon.rooms.filter(room => room.isActive == true);   //speichert nur die Räume ab, die aktiviert wurden
    localStorage.setItem('blub', JSON.stringify(safeDungeon));
    //sende dungeon an Server!
    this.httpService.saveOrUpdateDungeon(safeDungeon)
      .subscribe(response => {
        this.dungeon.dungeonID = response.toString(); //setzt die von Backend erstellte DungeonID
      });

  }

  publishDungeon() {
    this.saveDungeon();
    //sende MUD an joinable Lobbies
  }

  selectRoom(r: Room) {
    this.selectedRoom = r;
    document.getElementById('nav-room-tab').click();
  }

  submitRequest(req: requestForMaster) {
    this.dungeon.rooms[req.y][req.x]['isViewed'] = false;
    this.requests.splice(this.requests.indexOf(req), 1);
  }
  onItemSelect(item: any) {
    console.log(item);
  }
  onSelectAll(items: any) {
    console.log(items);
  }
}

