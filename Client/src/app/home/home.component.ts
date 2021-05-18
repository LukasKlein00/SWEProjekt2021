import { utf8Encode } from "@angular/compiler/src/util";
import { Component, OnDestroy, OnInit } from "@angular/core";
import { Router } from "@angular/router";
import { Subscription } from "rxjs";
import { first } from "rxjs/operators";
import { Dungeon } from "Testfiles/models für Schnittstellen";
import { HttpService } from "../services/http.service";
import { WebsocketService } from "../services/websocket.service";

@Component({
  selector: "app-home",
  templateUrl: "./home.component.html",
  styleUrls: ["./home.component.scss"],
})
export class HomeComponent implements OnInit, OnDestroy {
  loading = false;
  joinLoad = false;
  availableMUDs: Dungeon[];
  myMUDs: Dungeon[];
  sub1: Subscription;

  filters = ["all", "public", "private"];
  selectedFilter = this.filters[0];
  

  constructor(
    private httpService: HttpService,
    private WebSocketService: WebsocketService,
    private router: Router,
  ) {}

  ngOnInit(): void {
    this.getCreatedDungeons();
    this.WebSocketService.sendPublishedDungeonRequest();
    this.sub1 = this.WebSocketService.getPublishedDungeons().subscribe((r: string) => {
      this.availableMUDs = JSON.parse(r);
      
    });
  }

  getCreatedDungeons() {
    this.myMUDs = [];
    if (localStorage.getItem("currentUser")) {
      this.httpService.getCreatedDungeons().pipe(first()).subscribe((response) => {
        Object.keys(response).forEach((key) => {
          this.myMUDs.push({
            dungeonID: response[key][0],
            dungeonName: response[key][1],
            dungeonDescription: response[key][2],
          });
        });
        this.myMUDs.sort((a, b) => a.dungeonName.localeCompare(b.dungeonName));
        this.loading = false;
      });
    }
  }

  copyDungeon(d: Dungeon) {
    this.loading = true;
    this.httpService.copyDungeon(d.dungeonID).pipe(first()).subscribe((response) => {
      this.getCreatedDungeons();
    });
  }

  deleteDungeon(d: Dungeon) {
    this.loading = true;
    this.httpService.deleteDungeon(d.dungeonID).pipe(first()).subscribe((response) => {
      this.getCreatedDungeons();
    });
    this.WebSocketService.deleteDungeon(d.dungeonID);
  }

  joinDungeon(dungeon) {
    if (localStorage.getItem('currentUser')) {
      if (dungeon.private) {
        this.joinLoad = true;
        this.WebSocketService.sendJoinRequest(dungeon.dungeonID, JSON.parse(localStorage.getItem('currentUser')).userID );
        this.WebSocketService.getJoinRequestAnswer().pipe(first()).subscribe( (res: string) => {
          
          let check: boolean = JSON.parse(res)
          
          if (check == false){
            
          }
          if (check == true) {
            
            this.router.navigate(['/play',{id: dungeon.dungeonID}])
          } 
          this.joinLoad = false;
        });
      } else {
        this.router.navigate(['/play',{id: dungeon.dungeonID}])
      }
    } else {
      this.router.navigate(['/login'])
    }
  }

  ngOnDestroy() {
    this.sub1.unsubscribe();
  }
}
