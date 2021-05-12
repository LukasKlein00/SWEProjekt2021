import { Injectable, TemplateRef } from '@angular/core';
import { WebsocketService } from './websocket.service';

@Injectable({
  providedIn: 'root'
})
export class ToastService {

  constructor(
    private socket: WebsocketService
  ){

  }

  toasts: any[] = [];

  // Push new Toasts to array with content and options
  show(textOrTpl: string | TemplateRef<any>, options: any = {}) {
    this.toasts.push({ textOrTpl, ...options });
  }

  // Callback method to remove Toast DOM element from view
  remove(toast, isAllowed: boolean) {
    this.toasts = this.toasts.filter(t => t !== toast);
    this.socket.sendRequestAnswer(toast.userID, isAllowed);
  }
}
