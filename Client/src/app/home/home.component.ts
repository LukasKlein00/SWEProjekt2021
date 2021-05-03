import { Component, OnInit } from '@angular/core';
import { Dungeon } from 'Testfiles/models für Schnittstellen';
import { HttpService } from '../services/http.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  loading = false;
  availableMUDs: Dungeon[] = [{
    dungeonName: "Jack's mega cooler TestDungeon",
    dungeonDescription: 'Es war einmal vor langer Zeit ein nettes SWE Projekt, welches dafür sorgt, das mal ganz viel Erfahrung sammelt und sein Leben einfach genießt',
    dungeonID: "1",
    maxPlayers: 10,
    currentPlayers: 5,
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
  myMUDs: Dungeon[] = []

  filters = ['all','public','private'];
  selectedFilter = this.filters[0];

  constructor(
    private httpService: HttpService
  ) { }

  ngOnInit(): void {
    this.getCreatedDungeons()
  }
  
  getCreatedDungeons(){
    this.myMUDs = [];
    if (localStorage.getItem('currentUser')) {
      this.httpService.getCreatedDungeons()
      .subscribe((response) => {
          Object.keys(response).forEach( key => {this.myMUDs.push( {
            dungeonID: response[key][0],
            dungeonName: response[key][1],
            dungeonDescription: response[key][2]
          });});
          this.myMUDs.sort((a,b) => a.dungeonName.localeCompare(b.dungeonName));
          this.loading = false
        });
    }
  }

  copyDungeon(d: Dungeon) {
    this.loading = true;
    this.httpService.copyDungeon(d.dungeonID).subscribe((response) => {
      this.getCreatedDungeons();  
    });;
  }

  deleteDungeon(d: Dungeon){
    this.loading = true;
    this.httpService.deleteDungeon(d.dungeonID).subscribe((response) => {
      this.getCreatedDungeons()
      
    });;
  }
}
