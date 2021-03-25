import { Component, OnInit } from '@angular/core';
import { Map, Room } from 'Testfiles/models für Schnittstellen';

@Component({
  selector: 'app-play',
  templateUrl: './play.component.html',
  styleUrls: ['./play.component.scss']
})
export class PlayComponent implements OnInit {

  Rooms: Room[][];
  currentRoom: Room;

  constructor() { }

  ngOnInit(): void {
    let world: Map = JSON.parse(localStorage.getItem('blub'));
    this.Rooms = world.map;
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

  
    

}
