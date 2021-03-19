import { Component } from '@angular/core';
import { AuthentificationService } from './services/authentification.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'Client';
  currentUser = this.authentificationService.currentUserValue

  constructor(private authentificationService: AuthentificationService){}

  logout() {
    console.log("#");
    this.authentificationService.logout();
  }
}
