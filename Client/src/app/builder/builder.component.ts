import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Subscription } from 'rxjs';
import { first } from 'rxjs/operators';
import { Class, Item, Dungeon, Npc, Race, requestForMaster, Room, Access } from 'Testfiles/models für Schnittstellen';
import { DungeonService } from '../services/dungeon.service';
import { HttpService } from '../services/http.service';
import { ToastService } from '../services/toast.service';
import { WebsocketService } from '../services/websocket.service';

@Component({
  selector: 'app-builder',
  templateUrl: './builder.component.html',
  styleUrls: ['./builder.component.scss']
})
export class BuilderComponent implements OnInit, OnDestroy {

  chatMessages = 0;
  loading = false;
  sub1: Subscription;
  sub2: Subscription;
  sub3: Subscription;  

  currentPlayers;

  viewedRoom;
  requests: requestForMaster[] = []
  insertedUsername;
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
    private websocketService: WebsocketService,
  ) { }

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    this.dungeon = this.DungeonService.createNewDungeon(this.dungeonSize);
    
    this.rooms = this.dungeon.rooms;
    if (id) {
      this.getDungeon(id);
      this.getRooms(id);
    }
    this.sub1 = this.websocketService.getJoinRequests().subscribe((res: string) => {
      res = JSON.parse(res);
      this.toastService.show(`${res[1]} wants to join`, {
        classname: 'toast',
        delay: 20000, 
        autohide: true,
        userID: res[0]
      });
    }
    );
    this.sub1 = this.websocketService.getDMRequests().subscribe((res: string) => {
      let req: requestForMaster = JSON.parse(res);
      
      
      this.requests.push(req);
      });
  }

  receiveMessage(e){
    
    
    if (document.querySelector('#nav-chat-tab').getAttribute('aria-selected') == 'false') {
      this.chatMessages = e
    }
  }


  newClass() {
    return this.DungeonService.createNewClass();
  }

  addClass() {
    this.dungeon.classes.push(this.selectedClass);
    this.selectedClass = this.newClass()
    this.saveDungeon();
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
    this.saveDungeon();
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
    this.saveDungeon();
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
    this.saveDungeon();
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

  saveDungeon(publish = false) {
    this.loading = true;


    const safeDungeon: Dungeon = JSON.parse(JSON.stringify(this.dungeon))
    const deletedRooms = [];
    safeDungeon.rooms.filter(room => !room.isActive && room.roomID).forEach(r => deletedRooms.push(r.roomID));
    
    safeDungeon.rooms = safeDungeon.rooms.filter(room => room.isActive == true);   //speichert nur die Räume ab, die aktiviert wurden

    safeDungeon['deletedRooms'] = deletedRooms;
    localStorage.setItem('blub', JSON.stringify(safeDungeon));
    
    //sende dungeon an Server!
    this.httpService.saveOrUpdateDungeon(safeDungeon).pipe(first())
      .subscribe(response => {
        
        
        if (response) {
          this.dungeon.dungeonID = response.toString();
          this.getRooms(this.dungeon.dungeonID) //setzt die von Backend erstellte DungeonID
        }
        if (publish) {
          let hasStartRoom = false;
          this.sub3 = this.websocketService.getPlayersInMyDungeon().subscribe((res) => {
            this.currentPlayers = res;
          })
          this.rooms.forEach(room => {
            if (room.isStartRoom) {
              hasStartRoom = true;
            }
          })
          if (hasStartRoom) {
            
            this.websocketService.sendPublish(this.dungeon.dungeonID);
          } else {
            window.alert("You Need To Add At Least 1 Start Room Before Publishing")
          }
          
        }
        //fixing bug with Duplicate cause of NONE id
        this.httpService.getRaces(this.dungeon.dungeonID).pipe(first()).subscribe(res => {
          if (res) {
            this.dungeon.races = res
          }
        })
        this.httpService.getClasses(this.dungeon.dungeonID).pipe(first()).subscribe(res => {
          if (res) {
            this.dungeon.classes = res
          }
        })
        this.httpService.getNpcs(this.dungeon.dungeonID).pipe(first()).subscribe(res => {
          if (res) {
            this.dungeon.npcs = res
          }
        });
        this.httpService.getItems(this.dungeon.dungeonID).pipe(first()).subscribe(res => {
          if (res) {
            this.dungeon.items = res
          }
        })
        this.httpService.getAccessList(this.dungeon.dungeonID).pipe(first()).subscribe(res => {
          if (res) {
            this.dungeon.accessList = res
          }
        })
        this.loading = false;
      });

  }

  publishDungeon() {
    this.saveDungeon(true);
  }

  selectRoom(r: Room) {
    this.selectedRoom = r;
    document.getElementById('nav-room-tab').click();
  }

  submitRequest(req: requestForMaster) {
    
    this.websocketService.sendAnsweredDMRequest(req);
    this.requests.splice(this.requests.indexOf(req), 1);
  }
  onItemSelect(item: any) {
    
  }
  onSelectAll(items: any) {
    
  }

  getRooms(id) {
    this.httpService.getRooms(id).pipe(first()).subscribe(res => {
      
      res.map(r => {
        const index = this.dungeon.rooms.findIndex(oldRoom => oldRoom.x == r.x && oldRoom.y == r.y);
        r['isActive'] = true;
        this.dungeon.rooms[index] = r;
      });
      this.loading = false;
    });
    console.log("räume", this.dungeon.rooms);
  }

  getRaces() {
    if (this.dungeon.races.length == 0) {
      this.httpService.getRaces(this.dungeon.dungeonID).pipe(first()).subscribe(res => this.dungeon.races = res)
    }
  }

  getClasses() {
    if (this.dungeon.classes.length == 0) {
      this.httpService.getClasses(this.dungeon.dungeonID).pipe(first()).subscribe(res => this.dungeon.classes = res)
    }
  }

  getItems() {
    if (this.dungeon.items.length == 0) {
      
      this.httpService.getItems(this.dungeon.dungeonID).pipe(first()).subscribe(res => this.dungeon.items = res)
    }
  }

  getNpcs() {
    if (this.dungeon.npcs.length == 0) {
      
      this.httpService.getNpcs(this.dungeon.dungeonID).pipe(first()).subscribe(res => this.dungeon.npcs = res);
    }
  }

  getAccessList() {
    if (this.dungeon.accessList.length == 0) {
      this.httpService.getAccessList(this.dungeon.dungeonID).pipe(first()).subscribe(res => {
        
        if (res) {
          this.dungeon.accessList = res
        }
      }
      )
    }
  }

  getDungeon(id) {
    this.loading = true;
    this.httpService.getDungeon(id).pipe(first()).subscribe(res => {
      this.dungeon.dungeonID = res[0][0];
      this.dungeon.dungeonMasterID = res[0][1];
      this.dungeon.dungeonName = res[0][2];
      this.dungeon.dungeonDescription = res[0][3];
      this.dungeon.private = Boolean(res[0][4]).valueOf();
      this.dungeon.maxPlayers = res[0][5];

      
    })
  }

  submitAccess() {
    if (this.insertedUsername.length != 0) {
      if (!this.dungeon.accessList.find(x => x.name == this.insertedUsername)) {
        this.dungeon.accessList.push({
          name: this.insertedUsername,
          isAllowed: true,
        });
        this.insertedUsername = null;
      }
    }
  }

  removeFromAccess(user) {
    this.httpService.deleteAccess(user.name, this.dungeon.dungeonID).pipe(first()).subscribe();
    const index = this.dungeon.accessList.indexOf(user, 0);
    if (index > -1) {
      this.dungeon.accessList.splice(index, 1);
    }
  }

  enterRequest(req){
    this.viewedRoom = this.rooms.find(r => r.x == req.x && r.y == req.y);
  }

  leaveRequest(){
    this.viewedRoom = null;
  }

  ngOnDestroy() {
    this.saveDungeon();
    if (this.sub1) {
      this.sub1.unsubscribe()
    }
    if (this.sub2) {
      this.sub2.unsubscribe()
    }
    if (this.sub3) {
      this.sub3.unsubscribe()
    }
  }
}

