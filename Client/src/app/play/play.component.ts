import { Route } from '@angular/compiler/src/core';
import { Component, OnDestroy, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { ActivatedRoute } from '@angular/router';
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
    inventar: []
  };

  constructor(public dialog: MatDialog,
    private route: ActivatedRoute,
    private DungeonService: DungeonService,
    private httpService: HttpService,
    private socketService: WebsocketService) { }

    //auf privat prüfen -> Request

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.world['dungeonID'] = id;
      this.checkCharakter(id);
    }
    this.currentRoom = {
      name: "NewRoom 5 5",
      x: 5,
      y: 5,
      north: true,
      south: true,
      east: true,
      west: true,
      item: null,
      npc: null,
      players: [],
      isStartRoom: true,
      isActive: true,
      description: "Starting Room Description"
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

    });
  }

  getCharacterOverwiew() {
    console.log("requesting char data...")
    this.sub1 = this.socketService.getCharacterData(this.world.dungeonID, JSON.parse(localStorage.getItem('currentUser')).userID).subscribe(res => console.log("character overview", res))
  }

  getDiscoveredRooms() {
    console.log("requesting room data...")
    this.sub2 = this.socketService.getDiscoveredMap(this.world.dungeonID, JSON.parse(localStorage.getItem('currentUser')).userID).subscribe(res => console.log("character overview", res))
  }


  checkCharakter(dID) {
    this.loading = true;
    console.log("checking Char...")
    let check = this.socketService.getCharacter(dID, JSON.parse(localStorage.getItem('currentUser')).userID).subscribe((res) => {
      console.log("get Char Response", res);
      if (res != "false") {
        this.loading = false;
        this.player = JSON.parse(res as string);
        
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
      this.getCharacterOverwiew();
      this.getDiscoveredRooms();
    });
  }

  ngOnDestroy(){
    this.sub1.unsubscribe();
    this.sub2.unsubscribe();
  }
}




