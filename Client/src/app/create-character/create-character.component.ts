import { Component, OnInit } from '@angular/core';
import {MAT_DIALOG_DATA} from '@angular/material/dialog';
import { Inject } from '@angular/core';
import { Map, Player, SubmitPlayer } from 'Testfiles/models für Schnittstellen';

@Component({
  selector: 'app-create-character',
  templateUrl: './create-character.component.html',
  styleUrls: ['./create-character.component.scss']
})
export class CreateCharacterComponent implements OnInit {

  player: Player = {
    name: '',
    equipment: null,
    mapID: 1,
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

  constructor(@Inject(MAT_DIALOG_DATA) public World: Map) { }

  ngOnInit(): void {
  }

}
