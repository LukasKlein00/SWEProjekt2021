import { AfterViewChecked, ChangeDetectorRef, Component, OnInit } from '@angular/core';
import {MAT_DIALOG_DATA} from '@angular/material/dialog';
import { Inject } from '@angular/core';
import { Dungeon, Item, Player} from 'Testfiles/models für Schnittstellen';

@Component({
  selector: 'app-create-character',
  templateUrl: './create-character.component.html',
  styleUrls: ['./create-character.component.scss']
})
export class CreateCharacterComponent implements OnInit, AfterViewChecked {


  formisinvalid = true;
  player: Player = {
    name: '',
    description: '',
    dungeonID: '',
    race: {
      name: '',
      description: ''
    },
    class: {
      name: '',
      description: '',
      equipment: null,
    },
    userID: '',
    health: 100,
  };

  constructor(
    @Inject(MAT_DIALOG_DATA) public World: Dungeon,
    private cdRef:ChangeDetectorRef) { }

  ngOnInit(): void {
    this.player.dungeonID = this.World.dungeonID;
    if (JSON.parse(localStorage.getItem('currentUser'))) {
      this.player.userID = JSON.parse(localStorage.getItem('currentUser')).userID;
    }
  }

  ngAfterViewChecked() {
    if (this.player.name && this.player.race.name && this.player.class.name && this.player.description) {
      this.formisinvalid= false;
    } else {
      this.formisinvalid = true;
    }
    this.cdRef.detectChanges();
  }

}
