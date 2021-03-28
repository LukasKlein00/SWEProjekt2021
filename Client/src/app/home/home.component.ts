import { Component, OnInit } from '@angular/core';
import { Map } from 'Testfiles/models für Schnittstellen';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  availableMUDs: Map[] = [{
    mapName: 'DummyMap',
    mapDescription: 'Explore the amazing World of Suburbia',
    mapID: 1,
    maxPlayers: 10,
    currentPlayers: 2,
    mapMasterID: 3,
    private: true,
  },
  {
    mapName: 'TESTosteronMap',
    mapDescription: 'Feel the Power',
    mapID: 2,
    maxPlayers: 10,
    currentPlayers: 5,
    mapMasterID: 3,
  },
  {
    mapName: 'DummyMap',
    mapDescription: 'Explore the amazing World of Suburbia',
    mapID: 1,
    maxPlayers: 10,
    currentPlayers: 2,
    mapMasterID: 3,
    private: true,
  },
  {
    mapName: 'TESTosteronMap',
    mapDescription: 'Feel the Power',
    mapID: 2,
    maxPlayers: 10,
    currentPlayers: 5,
    mapMasterID: 3,
  },
  {
    mapName: 'DummyMap',
    mapDescription: 'Explore the amazing World of Suburbia',
    mapID: 1,
    maxPlayers: 10,
    currentPlayers: 2,
    mapMasterID: 3,
  },
  {
    mapName: 'TESTosteronMap',
    mapDescription: 'Feel the Power',
    mapID: 2,
    maxPlayers: 10,
    currentPlayers: 5,
    mapMasterID: 3,
  }]
  myMUDs: Map[] = [{
    mapName: 'DummyMap',
    mapDescription: 'Explore the amazing World of Suburbia',
    mapID: 1,
    maxPlayers: 10,
    currentPlayers: 2,
    mapMasterID: 3,
  },
  {
    mapName: 'TESTosteronMap',
    mapDescription: 'Feel the Power',
    mapID: 2,
    maxPlayers: 10,
    currentPlayers: 5,
    mapMasterID: 3,
  },]

  filters = ['all','public','private'];
  selectedFilter = this.filters[0];

  constructor() { }

  ngOnInit(): void {

  }

}
