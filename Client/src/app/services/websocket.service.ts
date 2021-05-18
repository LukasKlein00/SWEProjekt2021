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
  ) { }

  sendUserID(user) {
    
    this.socket.emit('on_login', user);
    
  }

  sendPublish(id) {
    this.socket.emit('publish', id)
  }

  sendRequestAnswer(userID, isAllowed) {
    this.socket.emit('send_join_request_answer', { userID, isAllowed })
  }

  sendPublishedDungeonRequest() {
    this.socket.emit('on_home')
  }

  sendJoinRequest(dungeonID, userID) {
    
    this.socket.emit('join_dungeon', { dungeonID, userID });
  }

  sendCharacter(player) {
    this.socket.emit('send_character_config', player)
    return this.socket.fromEvent('send_character_config').pipe(map((data) => data))
  }

  getJoinRequests() {
    return this.socket.fromEvent('JoinRequest').pipe(map((data) => data))
  }

  getJoinRequestAnswer() {
    return this.socket.fromEvent('on_join_request_answer').pipe(map((data) => {
      return data
    }))
  }

  getPublishedDungeons() {
    return this.socket.fromEvent('make_dungeon_available').pipe(map((data) => data))
  }

  getCharConfig(dungeonID) {
    this.socket.emit('get_character_config', { dungeonID })
    return this.socket.fromEvent('get_character_config').pipe(map((data) => { return data }))
  }

  getRooms() {
    return this.socket.fromEvent('get_rooms').pipe(map((data) => data))
  }

  getCharacter(dungeonID, userID) {
    this.socket.emit('get_character_in_dungeon', { dungeonID, userID })
    return this.socket.fromEvent('get_character_in_dungeon').pipe(map((data) => {
      
      return data
    }))
  }

  getDiscoveredMap(dungeonID, userID) {
    this.socket.emit('character_joined_room', { dungeonID, userID })
    return this.socket.fromEvent('character_joined_room').pipe(map((data) => {
      
      return data
    }))
  }

  sendDirection(dungeonID, userID, direction) {
    this.socket.emit('move_to_room', { dungeonID, userID, direction })
  }

  sendMasterRequest(dungeonID, userID, message) {
    this.socket.emit('dungeon_master_request', { dungeonID, userID, message })
  }

  sendMessageToRoom(dungeonID, userName, roomID, message) {
    this.socket.emit('send_message_to_room', { dungeonID, userName, roomID, message })
  }

  sendMessageToAll(dungeonID, message) {
    this.socket.emit('send_message_to_all', { dungeonID, message })
  }

  sendMessageToMaster(dungeonID, userName, message) {
    this.socket.emit('send_message_to_master', { dungeonID, userName, message })
  }

  sendWhisperToRoom(dungeonID, userName, message) {
    this.socket.emit('send_whisper_to_room', { dungeonID, userName, message })
  }

  sendWhisperToPlayer(dungeonID, message) {
    this.socket.emit('send_whisper_to_player', { dungeonID, message })
  }

  getChat() {
    return this.socket.fromEvent('get_chat').pipe(map((data) => {
      return data
    }))
  }

  getCurrentRoom() {
    return this.socket.fromEvent('current_room').pipe(map((data) => {
      return data
    }))
  }

  kickOut() {
    return this.socket.fromEvent('kick_out').pipe(map((data) => {
      return data
    }))
  }

  getDMRequests(){
    return this.socket.fromEvent('send_request_to_dm').pipe(map((data) => {
      return data
    }))
  }

  getPlayersInMyDungeon() {
    return this.socket.fromEvent('players_in_my_dungeon').pipe(map((data) => {
      
      return data
    }))
  }

  getIsActive() {
    return this.socket.fromEvent('dungeon_is_active').pipe(map((data) => {
      return data
    }))
  }

  sendAnsweredDMRequest(req) {
    this.socket.emit('dungeon_master_request_answer_to_user', req)
  }

  deleteDungeon(dungeonID) {
    this.socket.emit('delete_dungeon', {dungeonID})
  }

}




