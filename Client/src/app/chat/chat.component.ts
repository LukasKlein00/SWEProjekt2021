import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';
import { WebsocketService } from '../services/websocket.service';

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.scss']
})
export class ChatComponent implements OnInit, OnDestroy {

  text = '';
  chatMessages = [];

  @Input() styles: any = {};

  @Input() dungeonID: any;
  @Input() roomID: any;

  userID = JSON.parse(localStorage.getItem("currentUser")).userID;
  userName = JSON.parse(localStorage.getItem("currentUser")).username;

  sub1: Subscription;

  constructor(
    private socket: WebsocketService,
  ) { }

  ngOnInit(): void {
    this.sub1 = this.socket.getChat().subscribe(msg => {
      this.chatMessages.push(msg);
      const messageBody = document.querySelector('#messageBody');
      messageBody.scrollTop = messageBody.scrollHeight - messageBody.clientHeight;
    });
  }

  chat(event) {
    
    if (event && event.key === 'Enter' && this.text != '') {
      this.checkChatEvent()
      this.text = '';
    }
    const messageBody = document.querySelector('#messageBody');
    messageBody.scrollTop = messageBody.scrollHeight - messageBody.clientHeight;
  }

  checkChatEvent() {
    if (this.text[0] == '/') {
      this.checkAction()
    } else {
      this.roomChat()
    }
  }

  checkAction() {
    let entry = this.text.slice(1).toLowerCase()
    console.log("command", entry)

    if (entry.startsWith("dm ")) {
      entry = entry.slice(3);
      console.log("dm:", entry);
      this.socket.sendMessageToMaster(this.dungeonID, this.userName, entry);
    } else if (entry.startsWith("whisper ")) {
      entry = entry.slice(8);
      console.log("whisper:", entry);
      this.socket.sendWhisperToRoom(this.dungeonID, this.userName, entry);
    } else {
      switch (entry) {
        case "north":
        case "n":
          console.log("go north")
          this.socket.sendDirection(this.dungeonID, this.userID, "north");
          break;
        case "south":
        case "s":
          console.log("go south")
          this.socket.sendDirection(this.dungeonID, this.userID, "south");
          break;
        case "west":
        case "w":
          console.log("go west")
          this.socket.sendDirection(this.dungeonID, this.userID, "west");
          break;
        case "east":
        case "e":
          console.log("go east")
          this.socket.sendDirection(this.dungeonID, this.userID, "east");
          break;
        case "help":
        case "h":
          this.writeHelp();
          break;
        default:
          console.log("request to master")
          this.socket.sendMasterRequest(this.dungeonID, this.userName, entry);
      }
    }


  }
  writeHelp() {
    this.chatMessages.push({ msg: "<<< HELP MENU >>>", color: "yellow" },
      { msg: "use '/' followed by text to execute a command" },
      {},
      { msg: "help | h: return the HELP menu" },
      {},
      { msg: "north | n: tries to enter the room to the north" },
      { msg: "east | e: tries to enter the room to the east" },
      { msg: "south | s: tries to enter the room to the south" },
      { msg: "west | w: tries to enter the room to the west" },
      {},
      { msg: "dm: chat directly with the Dungeon Master" },
      { msg: "whisper <name>: chat with <name> in the same room" },
      {},
      { msg: "<your action>: sends <your action> as an action request to the Dungeon Master" },
      { msg: "<<< HELP MENU >>>", color: "yellow" },
    )
  }

  roomChat() {
    this.socket.sendMessageToRoom(this.dungeonID, this.userID, this.roomID, this.text)
    //zum Testen
    this.chatMessages.push({
      pre: this.userName + " :",
      msg: this.text,
    });
  }

  ngOnDestroy() {
    this.sub1.unsubscribe();
  }
}

