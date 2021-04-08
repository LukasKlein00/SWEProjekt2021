import { Component, OnInit } from '@angular/core';
import { Dungeon } from 'Testfiles/models für Schnittstellen';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  availableMUDs: Dungeon[] = [{
    dungeonName: 'Dummydungeon',
    dungeonDescription: 'Explore the amazing World of Suburbia',
    dungeonID: "1",
    maxPlayers: 10,
    currentPlayers: 2,
    dungeonMasterID: "3",
    private: true,
  },
  {
    dungeonName: 'TESTosterondungeon',
    dungeonDescription: 'Feel the Power',
    dungeonID: "2",
    maxPlayers: 10,
    currentPlayers: 5,
    dungeonMasterID: "3",
  },
  {
    dungeonName: 'Dummydungeon',
    dungeonDescription: 'Explore the amazing World of Suburbia',
    dungeonID: "1",
    maxPlayers: 10,
    currentPlayers: 2,
    dungeonMasterID: "3",
    private: true,
  },
  {
    dungeonName: 'TESTosterondungeon',
    dungeonDescription: 'Feel the Power',
    dungeonID: "2",
    maxPlayers: 10,
    currentPlayers: 5,
    dungeonMasterID: "3",
  },
  {
    dungeonName: 'Dummydungeon',
    dungeonDescription: 'Explore the amazing World of Suburbia',
    dungeonID: "1",
    maxPlayers: 10,
    currentPlayers: 2,
    dungeonMasterID: "3",
  },
  {
    dungeonName: 'TESTosterondungeon',
    dungeonDescription: 'Feel the Power',
    dungeonID: "2",
    maxPlayers: 10,
    currentPlayers: 5,
    dungeonMasterID: "3",
  }]
  myMUDs: Dungeon[] = [
  {
    dungeonName: 'TESTosterondungeon',
    dungeonDescription: 'Feel the Power',
    dungeonID: "2",
    maxPlayers: 10,
    currentPlayers: 5,
    dungeonMasterID: "3",
  },]

  filters = ['all','public','private'];
  selectedFilter = this.filters[0];

  constructor() { }

  ngOnInit(): void {

  }

  copyDungeon(d: Dungeon) {
    const myClonedObject = Object.assign({}, d);
    myClonedObject.dungeonName = d.dungeonName + 'Copy';
    this.myMUDs.push(myClonedObject);
  }

}
