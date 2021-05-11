import { Injectable } from '@angular/core';
import { Socket } from 'ngx-socket-io';
import { map } from 'rxjs/operators';
import { Class, Race } from 'Testfiles/models für Schnittstellen';


@Injectable({
  providedIn: 'root'
})
export class WebsocketService {


  constructor(
    private socket: Socket
  ) {}

  sendUserID(id) {
    console.log("sending UserID to connect")
    this.socket.emit('on_login',id);
  }

  sendPublish(id) {
    this.socket.emit('publish',id)
  }

  sendPublishedDungeonRequest() {
    this.socket.emit('on_home')
  }

  getMessage() {
    return this.socket.fromEvent('message').pipe(map((data) => data))
  }

  getPublishedDungeons(){
    return this.socket.fromEvent('make_dungeon_available').pipe(map((data) => data))
  }

  getCharConfig(dungeonID){
    this.socket.emit('get_character_config',{dungeonID})
    return this.socket.fromEvent('get_character_config').pipe(map((data) => {return data}))
  }

  getRooms(){
    return this.socket.fromEvent('get_rooms').pipe(map((data) => data))
  }

  getCharacter(dungeonID, userID){
    this.socket.emit('get_character_in_dungeon',{dungeonID, userID})
    return this.socket.fromEvent('get_character_in_dungeon').pipe(map((data) => {
      return data}))
  }
}


