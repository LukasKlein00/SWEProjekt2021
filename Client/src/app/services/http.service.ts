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

  getDungeon(id) {
    return this.http.post(`${this.apiUrl}/getDungeon`, JSON.stringify(id));
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

}
