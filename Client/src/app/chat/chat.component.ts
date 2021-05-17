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
  loadingReq = false;
  messageBody;

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
    this.messageBody = document.querySelector('#messageBody');
    this.sub1 = this.socket.getChat().subscribe((msg: string) => {
      
      const m = JSON.parse(msg)
      if (m.dmRequest) {
        this.loadingReq = false;
      }
      this.chatMessages.push(m);
      this.inscreaseChatNumber();
      this.autoScroll();
    });
  }

  inscreaseChatNumber() {
    this.ChatMessageEvent.emit(this.unreadMessages + 1);
  }

  autoScroll(){
    setTimeout(()=>{                        
      this.messageBody.scroll({
        top: this.messageBody.scrollHeight,
        left: 0,
        behavior: 'smooth'
      });
 }, 100);
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
    this.autoScroll();
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
    let orignalMsg = this.text.slice(1);
    let entry = this.text.slice(1).toLowerCase();
    

    if (entry.startsWith("whisper ")) {
      entry = orignalMsg.slice(8);
      
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
    let orignalMsg = this.text.slice(1);
    let entry = this.text.slice(1).toLowerCase()
    
    if (entry.startsWith("dm ")) {
      entry = orignalMsg.slice(3);
      
      this.socket.sendMessageToMaster(this.dungeonID, this.userName, entry);
    } else if (entry.startsWith("whisper ")) {
      entry = orignalMsg.slice(8);
      
      this.socket.sendWhisperToRoom(this.dungeonID, this.userName, entry);
    } else if (entry == "help" || entry == "h") {
      this.writeHelp();
    } else {
      if (!this.loadingReq) {
        switch (entry) {
          case "north":
          case "n":
            
            this.socket.sendDirection(this.dungeonID, this.userID, "north");
            break;
          case "south":
          case "s":
            
            this.socket.sendDirection(this.dungeonID, this.userID, "south");
            break;
          case "west":
          case "w":
            
            this.socket.sendDirection(this.dungeonID, this.userID, "west");
            break;
          case "east":
          case "e":
            
            this.socket.sendDirection(this.dungeonID, this.userID, "east");
            break;
          default:
            
            this.socket.sendMasterRequest(this.dungeonID, this.userName, entry);
            this.loadingReq = true;
        }
      } else {
        this.chatMessages.push({
          msg: "Cannot Perform Actions during a DM Request",
          color: "red"
        })
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
        );
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
      )
    }
  }

  roomChat() {
    this.socket.sendMessageToRoom(this.dungeonID, this.userID, this.roomID, this.text)
  }

  allChat() {
    
    this.socket.sendMessageToAll(this.dungeonID, this.text)
  }

  ngOnDestroy() {
    this.sub1.unsubscribe();
  }
}

