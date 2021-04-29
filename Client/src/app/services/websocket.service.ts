import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';
import { WebsocketObject } from 'Testfiles/models für Schnittstellen';
import { WebsocketBuilder } from 'websocket-ts/lib';
import { PythonJSON } from '../test/test.component';

@Injectable({
  providedIn: 'root'
})
export class WebsocketService {
  socket: any;
  status = 'unknown';
  readonly uri = environment.websocketUrl;

  constructor() { 
    this.socket = new WebsocketBuilder(this.uri)
    .onOpen(() => { console.log('opened'); this.status = 'Online'; })
    .onClose(() => { console.log('closed'); this.status = 'Offline (closed)'; })
    .onError(() => { console.log('error'); this.status = 'Offline (error)'; })
    .onMessage((i, ev) => { this.unloadData(ev.data);})
    .onRetry(() => { console.log('retry'); })
    .build();
  }

  unloadData(incomingData) {
    const data: PythonJSON = JSON.parse(incomingData);
    console.log(data);
  }

  sendData(methode, content) {
    let outgoingData: WebsocketObject = {
      method: methode,
      content: content,
    }
    this.socket.send(JSON.stringify(outgoingData));
  }
}


