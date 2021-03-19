import { AfterViewChecked, ChangeDetectorRef, Component } from '@angular/core';
import { AuthentificationService } from './services/authentification.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements AfterViewChecked{
  title = 'Client';
  currentUser = this.authentificationService.currentUserValue

  constructor(
    private authentificationService: AuthentificationService,
    private cdRef:ChangeDetectorRef
    ){}
  ngAfterViewChecked(): void {
    this.currentUser = this.authentificationService.currentUserValue;
    this.cdRef.detectChanges();
  }

  logout() {
    this.authentificationService.logout();
  }
}
