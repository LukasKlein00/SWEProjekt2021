import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Dungeon } from 'Testfiles/models für Schnittstellen';

@Injectable({
  providedIn: 'root'
})
export class HttpService {

  //private readonly apiUrl = 'http://193.196.53.67:1188'
  private readonly apiUrl = 'http://localhost:1188'


  constructor(private http: HttpClient) { }

  saveOrUpdateDungeon(dungeon: Dungeon) {
    return this.http.post(`${this.apiUrl}/saveDungeon`, dungeon);
  }
}
