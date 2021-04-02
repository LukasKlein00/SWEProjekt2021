import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.scss']
})
export class ChatComponent implements OnInit {

  text = '';
  chatMessages = [];

  constructor() { }

  ngOnInit(): void {
  }

  chat(event) {
    if (event && event.key === 'Enter') {
        this.chatMessages.push({
          id: "testUser",
          msg: this.text
        });
        this.text = '';
      }
      const messageBody = document.querySelector('#messageBody');
      messageBody.scrollTop = messageBody.scrollHeight - messageBody.clientHeight;
  }
}

