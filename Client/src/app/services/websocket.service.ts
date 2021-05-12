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

  sendUserID(user) {
    console.log("sending UserID to connect")
    this.socket.emit('on_login',user);
    console.log("sending User", user);
  }

  sendPublish(id) {
    this.socket.emit('publish',id)
  }

  sendRequestAnswer(userID, isAllowed) {
    this.socket.emit('send_join_request_answer', {userID, isAllowed})
  }

  sendPublishedDungeonRequest() {
    this.socket.emit('on_home')
  }

  sendJoinRequest(dungeonID, userID) {
    console.log("sending Request")
    this.socket.emit('join_dungeon',{dungeonID, userID});
  }

  sendCharacter(player) {
    this.socket.emit('send_character_config',player)
  }

  getJoinRequests() {
    return this.socket.fromEvent('JoinRequest').pipe(map((data) => data))
  }

  getJoinRequestAnswer(){
    return this.socket.fromEvent('on_join_request_answer').pipe(map((data) => {
      return data}))
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


