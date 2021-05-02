import { AfterViewChecked, ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { AuthentificationService } from './services/authentification.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements AfterViewChecked, OnInit{
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
  
  ngOnInit() {
    if (this.currentUser) {
      console.log("check");
      this.authentificationService.check().subscribe(response => {
        console.log("user checked")
      },
      error => {
        console.log("logging out..")
        this.logout();
      });
    }
  }

  logout() {
    this.authentificationService.logout();
  }
}
