import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthentificationService } from '../services/authentification.service';
import { HttpService } from '../services/http.service';

@Component({
  selector: 'app-profil',
  templateUrl: './profil.component.html',
  styleUrls: ['./profil.component.scss']
})
export class ProfilComponent implements OnInit {

  user;
  constructor(
    private authentificationService: AuthentificationService,
    private httpService: HttpService,
    ) { }

  ngOnInit(): void {
    if (this.authentificationService.currentUserValue) {
      this.user = this.authentificationService.currentUserValue
    } else {
      this.user = "unknown"
    }
    
  }

  deleteUser(){
    this.httpService.deleteUser(this.user.userID).subscribe((response) => {
      localStorage.removeItem('currentUser');
      window.location.reload()
    });;
  }

}
