import { Component, OnInit } from '@angular/core';
import { WebsocketBuilder } from 'websocket-ts';
import { v4 as uuidv4 } from 'uuid';

export class PythonJSON {
  id: string;
  msg: string;
  typ: string;
}

@Component({
  selector: 'app-test',
  templateUrl: './test.component.html',
  styleUrls: ['./test.component.scss']
})
export class TestComponent implements OnInit {
  socket: any;
  readonly uri = 'ws://193.196.53.67:80';
  // readonly uri = 'ws://localhost:80';
  clientID = uuidv4();
  text = 'test';
  chat = [{
    id: 'TestUser',
    msg: 'Test'
  }];
  action = ['testaction'];
  status = 'unknown';

  constructor() {
    this.socket = new WebsocketBuilder(this.uri)
      .onOpen((i, ev) => { console.log('opened'); this.status = 'Online'; })
      .onClose((i, ev) => { console.log('closed'); this.status = 'Offline (closed)'; })
      .onError((i, ev) => { console.log('error'); this.status = 'Offline (error)'; })
      .onMessage((i, ev) => { this.unloadData(ev.data); })
      .onRetry((i, ev) => { console.log('retry'); })
      .build();
  }

  ngOnInit(): void {
  }

  unloadData(d) {
    const data: PythonJSON = JSON.parse(d);
    if (data.typ === 'chat') {
      this.chat.push({
        id: data.id,
        msg: data.msg
      });
    }
    if (data.typ === 'action') {
      this.action.push(data.msg);
    }
  }


  allchat(event) {
    if (event && event.key === 'Enter') {
      console.log('allchat');
      if (this.text) {
        this.socket.send(JSON.stringify({
          id: this.clientID,
          msg: this.text,
          method: 'allchat'
        }));
        this.text = '';
      }
    }
  }

  b2click() {
    this.socket.send(JSON.stringify({
      id: this.clientID,
      msg: 'action zum Server',
      method: 'action'
    }));
  }

}
