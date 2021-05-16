import { Route } from '@angular/compiler/src/core';
import { Component, OnDestroy, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { ActivatedRoute, Router } from '@angular/router';
import { Subscription } from 'rxjs';
import { Class, Dungeon, Player, Race, Room } from 'Testfiles/models für Schnittstellen';
import { CreateCharacterComponent } from '../create-character/create-character.component';
import { DungeonService } from '../services/dungeon.service';
import { HttpService } from '../services/http.service';
import { WebsocketService } from '../services/websocket.service';

@Component({
  selector: 'app-play',
  templateUrl: './play.component.html',
  styleUrls: ['./play.component.scss']
})
export class PlayComponent implements OnInit, OnDestroy {

  sub1: Subscription;
  sub2: Subscription;
  sub3: Subscription;
  sub4: Subscription;
  sub5: Subscription;
  
  world: Dungeon = {};
  loading;
  rooms: Room[];
  currentRoom: Room;
  player: Player = {
    name: '',
    dungeonID: '1',
    race: {
      name: '',
      description: '',
    },
    class: {
      name: '',
      description: '',
      equipment: null
    },
    userID: '1',
    health: 100,
    inventory: []
  };

  constructor(public dialog: MatDialog,
    private route: ActivatedRoute,
    private router: Router,
    private DungeonService: DungeonService,
    private httpService: HttpService,
    private socketService: WebsocketService) { }

    //auf privat prüfen -> Request

  ngOnInit(): void {
    this.sub4 = this.socketService.getCurrentRoom().subscribe((res: string) => {
      console.log("currentRoom", res);
      this.currentRoom = JSON.parse(res);
    })
    this.sub5 = this.socketService.kickOut().subscribe((res: string) => {
      console.log("kick Out", res);
      window.alert(res);
      this.router.navigate['/'];
    })
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.world['dungeonID'] = id;
      this.checkCharakter(id);
    }
    this.currentRoom = {
      name: "loading Room...",
      x: 0,
      y: 0,
      north: true,
      south: true,
      east: true,
      west: true,
      item: null,
      npc: null,
      players: [],
      isStartRoom: true,
      isActive: true,
      description: "loading Room Description..."
    }
  }

  openDialog() {
    const dialogRef = this.dialog.open(CreateCharacterComponent, {
      disableClose: true,
      data: this.world,
    });

    dialogRef.afterClosed().subscribe(result => {
      this.player = result;
      console.log("player created:",this.player)
      this.socketService.sendCharacter(this.player);
      this.getDiscoveredRooms()
    });
  }

  getDiscoveredRooms() {
    console.log("requesting room data...")
    this.sub2 = this.socketService.getDiscoveredMap(this.world.dungeonID, JSON.parse(localStorage.getItem('currentUser')).userID).subscribe((res: string) => {
      console.log("rooms res", res)
      this.rooms = JSON.parse(res)
      this.rooms.forEach(r => r['isActive'] = true);
      console.log("rooms variable", this.rooms)
    })
  }


  checkCharakter(dID) {
    this.loading = true;
    console.log("checking Char...")
    let check = this.socketService.getCharacter(dID, JSON.parse(localStorage.getItem('currentUser')).userID).subscribe((res) => {
      console.log("get Char Response", res);
      if (res != "false") {
        this.loading = false;
        this.player = JSON.parse(res as string);
        this.player['dungeonID'] = this.world.dungeonID;
        
      } else {
        this.socketService.getCharConfig(dID).subscribe((res: string) => {
          console.log("get CharConf", res)
          if (res != null) {
            this.loading = false;
            const k = JSON.parse(res)
            console.log(k[0]);
            console.log(k[1]);
            this.world['classes'] = [];
            this.world['races'] = [];
            k[0].forEach(element => {
              this.world.classes.push({
                classID: element['classID'],
                name: element['name'],
                description: element['description'],
                equipment: element['equipment']
              })
            });
            k[1].forEach(element => {
              console.log(element);
              this.world['races'].push({
                raceID: element['raceID'],
                name: element['name'],
                description: element['description'],
              })
            });
            console.log(this.world)
            this.openDialog();

          }
        })
      }
      this.getDiscoveredRooms();
    });
  }

  ngOnDestroy(){
    if (this.sub1) {
      this.sub1.unsubscribe();
    }
    if (this.sub2) {
      this.sub2.unsubscribe();
    }
  }
}




