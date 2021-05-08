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
  
}


