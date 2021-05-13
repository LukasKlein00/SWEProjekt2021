import { AfterViewChecked, ChangeDetectorRef, Component, OnDestroy, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';
import { AuthentificationService } from './services/authentification.service';
import { WebsocketService } from './services/websocket.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements AfterViewChecked, OnInit, OnDestroy{
  title = 'Client';
  currentUser = this.authentificationService.currentUserValue
  sub1: Subscription;

  constructor(
    private authentificationService: AuthentificationService,
    private cdRef:ChangeDetectorRef,
    private websocketService: WebsocketService,
    ){}
  ngAfterViewChecked(): void {
    this.currentUser = this.authentificationService.currentUserValue;
    this.cdRef.detectChanges();
  }
  
  ngOnInit() {
    if (this.currentUser) {
      this.websocketService.sendUserID(this.currentUser);
      this.sub1 = this.authentificationService.check().subscribe(response => {
      },
      error => {
        this.logout();
      });
    }
  }

  logout() {
    this.authentificationService.logout();
  }

  ngOnDestroy(){
    this.sub1.unsubscribe();
  }
}
