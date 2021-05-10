import { utf8Encode } from "@angular/compiler/src/util";
import { Component, OnInit } from "@angular/core";
import { Dungeon } from "Testfiles/models für Schnittstellen";
import { HttpService } from "../services/http.service";
import { WebsocketService } from "../services/websocket.service";

@Component({
  selector: "app-home",
  templateUrl: "./home.component.html",
  styleUrls: ["./home.component.scss"],
})
export class HomeComponent implements OnInit {
  loading = false;
  availableMUDs: Dungeon[];
  myMUDs: Dungeon[];

  filters = ["all", "public", "private"];
  selectedFilter = this.filters[0];

  constructor(
    private httpService: HttpService,
    private WebSocketService: WebsocketService
  ) {}

  ngOnInit(): void {
    this.getCreatedDungeons();
    this.WebSocketService.getMessage().subscribe((r) =>
      console.log("socketservice", r)
    );
    this.WebSocketService.getPublishedDungeons().subscribe((r: string) => {
      this.availableMUDs = JSON.parse(r);
      console.log("avDungeons", r);
    });
  }

  getCreatedDungeons() {
    this.myMUDs = [];
    if (localStorage.getItem("currentUser")) {
      this.httpService.getCreatedDungeons().subscribe((response) => {
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
    this.httpService.copyDungeon(d.dungeonID).subscribe((response) => {
      this.getCreatedDungeons();
    });
  }

  deleteDungeon(d: Dungeon) {
    this.loading = true;
    this.httpService.deleteDungeon(d.dungeonID).subscribe((response) => {
      this.getCreatedDungeons();
    });
  }
}
