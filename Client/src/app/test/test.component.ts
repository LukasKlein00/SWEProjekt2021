import { Component, OnInit } from '@angular/core';
import { WebsocketBuilder } from 'websocket-ts';
import { AuthentificationService } from '../services/authentification.service';

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
  readonly uri = 'ws://193.196.53.67:1187';
  //readonly uri = 'ws://localhost:1187';
  text = '';
  chat = [];
  action = [];
  status = 'unknown';
  currentUser = this.authentificationService.currentUserValue ?? { username: 'UNKNOWN'};

  constructor(private authentificationService: AuthentificationService) {
    this.socket = new WebsocketBuilder(this.uri)
      .onOpen((i, ev) => { console.log('opened'); this.status = 'Online'; })
      .onClose((i, ev) => { console.log('closed'); this.status = 'Offline (closed)'; })
      .onError((i, ev) => { console.log('error'); this.status = 'Offline (error)'; })
      .onMessage((i, ev) => { this.unloadData(ev.data); console.log(i)})
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
          id: this.currentUser.username,
          msg: this.text,
          method: 'allchat'
        }));
        this.text = '';
      }
    }
  }

  b2click() {
    this.socket.send(JSON.stringify({
      id: this.currentUser.username,
      msg: 'action zum Server',
      method: 'action'
    }));
  }

}
