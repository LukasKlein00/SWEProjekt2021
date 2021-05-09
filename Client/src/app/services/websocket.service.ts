import { Injectable } from '@angular/core';
import { Socket } from 'ngx-socket-io';
import { map } from 'rxjs/operators';


@Injectable({
  providedIn: 'root'
})
export class WebsocketService {


  constructor(
    private socket: Socket
  ) {}

  sendMessage(msg: string) {
    this.socket.emit('message',msg);
  }

  sendPublish(id) {
    this.socket.emit('publish',id)
  }

  getMessage() {
    return this.socket.fromEvent('message').pipe(map((data) => data))
  }

  getPublishedDungeons(){
    return this.socket.fromEvent('make_dungeon_available').pipe(map((data) => data))
  }

  getRaces(dungeonID){
    this.socket.emit('get_races',dungeonID)
    return this.socket.fromEvent('get_races').pipe(map((data) => data))
  }

  getClasses(dungeonID){
    this.socket.emit('get_classes',dungeonID)
    return this.socket.fromEvent('get_classes').pipe(map((data) => data))
  }

  getRooms(){
    
    return this.socket.fromEvent('get_rooms').pipe(map((data) => data))
  }

  getCharacter(dungeonID, userID){
    this.socket.emit('get_character_config',{dungeonID, userID})
    return this.socket.fromEvent('get_character_config').pipe(map((data) => data))
  }
  
}


