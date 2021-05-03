import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';
import { Dungeon } from 'Testfiles/models für Schnittstellen';

@Injectable({
  providedIn: 'root'
})
export class HttpService {

  private readonly apiUrl = environment.httpUrl;


  constructor(private http: HttpClient) { }

  saveOrUpdateDungeon(dungeon: Dungeon) {
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
    return this.http.post(`${this.apiUrl}/getRooms`, JSON.stringify(id));
  }

  getClasses(id) {
    return this.http.post(`${this.apiUrl}/getClasses`, JSON.stringify(id));
  }

  getRaces(id) {
    return this.http.post(`${this.apiUrl}/getRaces`, JSON.stringify(id));
  }

  getItems(id) {
    return this.http.post(`${this.apiUrl}/getItems`, JSON.stringify(id));
  }

  getNpcs(id) {
    return this.http.post(`${this.apiUrl}/getNpcs`, JSON.stringify(id));
  }

  getAccessList(id) {
    return this.http.post(`${this.apiUrl}/getAccessList`, JSON.stringify(id));
  }

}
