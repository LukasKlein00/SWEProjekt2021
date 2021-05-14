import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';
import { Access, Class, Dungeon, Item, Npc, Race, Room } from 'Testfiles/models für Schnittstellen';

@Injectable({
  providedIn: 'root'
})
export class HttpService {

  private readonly apiUrl = environment.httpUrl;


  constructor(private http: HttpClient) { }

  saveOrUpdateDungeon(dungeon: Dungeon) {
    console.log(dungeon)
    return this.http.post(`${this.apiUrl}/saveDungeon`, dungeon);
  }

  getCreatedDungeons() {
    return this.http.post(`${this.apiUrl}/getMyDungeons`,JSON.stringify(JSON.parse(localStorage.getItem('currentUser')).userID));
  }

  deleteDungeon(id) {
    return this.http.post(`${this.apiUrl}/deleteDungeon`, JSON.stringify(id));
  }

  deleteUser(id) {
    return this.http.post(`${this.apiUrl}/deleteUser`, JSON.stringify(id));
  }

  copyDungeon(id) {
    return this.http.post(`${this.apiUrl}/copyDungeon`, JSON.stringify(id));
  }

  getDungeon(id) {
    return this.http.post(`${this.apiUrl}/getDungeon`, JSON.stringify(id));
  }

  getRooms(id) {
    return this.http.post<Room[]>(`${this.apiUrl}/getRooms`, JSON.stringify(id));
  }

  getClasses(id) {
    return this.http.post<Class[]>(`${this.apiUrl}/getClasses`, JSON.stringify(id));
  }

  getRaces(id) {
    return this.http.post<Race[]>(`${this.apiUrl}/getRaces`, JSON.stringify(id));
  }

  getItems(id) {
    return this.http.post<Item[]>(`${this.apiUrl}/getItems`, JSON.stringify(id));
  }

  getNpcs(id) {
    return this.http.post<Npc[]>(`${this.apiUrl}/getNpcs`, JSON.stringify(id));
  }

  getAccessList(id) {
    return this.http.post<Access[]>(`${this.apiUrl}/getAccessList`, JSON.stringify(id));
  }

  deleteAccess(userName, dungeonID){
    console.log("deleAccess entered")
    return this.http.post(`${this.apiUrl}/deleteAccess`, {userName, dungeonID});
  }

}
