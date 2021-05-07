import { Injectable } from '@angular/core';
import { Socket } from 'ngx-socket-io';
import { map } from 'rxjs/operators';
import { environment } from 'src/environments/environment';


@Injectable({
  providedIn: 'root'
})
export class WebsocketService extends Socket {


  constructor(
    private socket: Socket
  ) {
    super({ url: environment.websocketUrl, options: {} });
  }

  sendMessage(msg: string) {
    this.socket.emit('message',msg);
  }

  getMessage() {
    return this.socket.fromEvent('message').pipe(map((data) => data)) //data.msg
  }
}


