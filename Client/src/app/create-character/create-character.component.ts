import { AfterViewChecked, Component, OnInit } from '@angular/core';
import {MAT_DIALOG_DATA} from '@angular/material/dialog';
import { Inject } from '@angular/core';
import { Dungeon, Player} from 'Testfiles/models für Schnittstellen';

@Component({
  selector: 'app-create-character',
  templateUrl: './create-character.component.html',
  styleUrls: ['./create-character.component.scss']
})
export class CreateCharacterComponent implements OnInit, AfterViewChecked {


  formisinvalid = true;
  player: Player = {
    name: '',
    equipment: null,
    description: '',
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

  constructor(@Inject(MAT_DIALOG_DATA) public World: Dungeon) { }

  ngOnInit(): void {
  }

  ngAfterViewChecked() {
    if (this.player.name && this.player.race.name && this.player.class.name && this.player.description) {
      this.formisinvalid= false;
    } else {
      this.formisinvalid = true;
    }
  }

}
