import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { Dungeon, Player, Room } from 'Testfiles/models für Schnittstellen';
import { CreateCharacterComponent } from '../create-character/create-character.component';

@Component({
  selector: 'app-play',
  templateUrl: './play.component.html',
  styleUrls: ['./play.component.scss']
})
export class PlayComponent implements OnInit {

  World: Dungeon;
  Rooms: Room[][];
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

  constructor(public dialog: MatDialog) { }

  ngOnInit(): void {
    this.World = JSON.parse(localStorage.getItem('blub'));
    this.Rooms = this.World.dungeon;
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
    this.openDialog();
  }

  openDialog() {
    const dialogRef = this.dialog.open(CreateCharacterComponent, {
      disableClose: true,
      data: this.World,
    });

    dialogRef.afterClosed().subscribe(result => {
      this.player = result;

    });
  }
  
    

}
