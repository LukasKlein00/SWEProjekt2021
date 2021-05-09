import { Route } from '@angular/compiler/src/core';
import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { ActivatedRoute } from '@angular/router';
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
export class PlayComponent implements OnInit {

  world: Dungeon;
  loading;
  rooms: Room[];
  currentRoom: Room;
  player: Player = {
    name: '',
    equipment: null,
    dungeonID: 1,
    race: {
      name: '',
      description: '',
    },
    class: {
      name: '',
      description: '',
      equipment: null
    },
    userID: 1,
    health: 100,
    inventar: []
  };

  constructor(public dialog: MatDialog,
    private route: ActivatedRoute,
    private DungeonService: DungeonService,
    private httpService: HttpService,
    private socketService: WebsocketService) { }

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    console.log("id",id)
    if (id) {
      if (this.checkCharakter(id)) {

      } else {
        this.getCharakterCreationData(id);
        this.openDialog();

      }
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

    });
  }

  getCharakterCreationData(dID) {
    this.loading = true;
    
this.socketService.getClasses(dID).subscribe((res) => {
  console.log("classes",res);
  if (res) {
    
    this.world['class'] = res as Class[];
  }
})
this.socketService.getRaces(dID).subscribe((res) => {
  console.log("races",res)
  this.loading = false;
  if (res) {
    
    this.world['races'] = res as Race[];
  }
})
  }

  checkCharakter(dID) {
    this.loading = true;
    console.log("checking Char...")
    let check = this.socketService.getCharacter(dID, JSON.parse(localStorage.getItem('currentUser')).userID).subscribe( (res) => {
      console.log("GETcHAR",res);
      this.loading = false
      if (res) {
        return true 
      } else {
        return false
      }
    })

    return check
  }
  
    

}
