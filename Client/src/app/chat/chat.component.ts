import { Component, Input, OnDestroy, OnInit, Output, EventEmitter } from '@angular/core';
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
  @Input() isDungeonMaster: boolean = false;

  @Input() unreadMessages: number = 0;
  @Output() ChatMessageEvent = new EventEmitter<number>();

  userID = JSON.parse(localStorage.getItem("currentUser")).userID;
  userName = JSON.parse(localStorage.getItem("currentUser")).username;

  sub1: Subscription;

  constructor(
    private socket: WebsocketService,
  ) { }

  ngOnInit(): void {
    this.sub1 = this.socket.getChat().subscribe((msg: string) => {
      console.log("received msg: ", msg)
      this.chatMessages.push(JSON.parse(msg));
      this.inscreaseChatNumber();
      const messageBody = document.querySelector('#messageBody');
      messageBody.scrollTop = messageBody.scrollHeight - messageBody.clientHeight;
    });
  }

  inscreaseChatNumber() {
    this.ChatMessageEvent.emit(this.unreadMessages + 1);
  }

  chat(event) {

    if (event && event.key === 'Enter' && this.text != '') {
      if (!this.isDungeonMaster) {
        this.checkChatEvent()
      } else {
        this.checkDungeonMasterEvent();
      }
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

  checkDungeonMasterEvent() {
    if (this.text[0] == '/') {
      this.checkDungeonMasterAction()
    } else {
      this.allChat()
    }
  }

  checkDungeonMasterAction() {
    let entry = this.text.slice(1).toLowerCase()
    console.log("DMcommand", entry)

    if (entry.startsWith("whisper ")) {
      entry = entry.slice(8);
      console.log("whisper:", entry);
      this.socket.sendWhisperToPlayer(this.dungeonID, entry);
    } else if (entry == "help" || entry == "h") {
      this.writeHelp(true);
    } else {
      this.chatMessages.push({
        msg: "Unknown Command",
        color: "red"
      })
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
  writeHelp(isDM = false) {
    if (isDM) {
      this.chatMessages.push({ msg: "<<< HELP MENU >>>", color: "yellow" },
        { msg: "use '/' followed by text to execute a command" },
        {},
        { msg: "help | h: return the HELP menu" },
        {},
        { msg: 'whisper "name" <message>: chat with <name> in the same room' },
        { msg: "<<< HELP MENU >>>", color: "yellow" });
    } else {
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
        { msg: 'whisper "name" <message>: chat with <name> in the same room' },
        {},
        { msg: "<your action>: sends <your action> as an action request to the Dungeon Master" },
        { msg: "<<< HELP MENU >>>", color: "yellow" },
      )
    }
  }

  roomChat() {
    this.socket.sendMessageToRoom(this.dungeonID, this.userID, this.roomID, this.text)
  }

  allChat() {
    console.log("send to all: ", this.text)
    this.socket.sendMessageToAll(this.dungeonID, this.text)
  }

  ngOnDestroy() {
    this.sub1.unsubscribe();
  }
}

