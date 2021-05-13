import { tokenName } from '@angular/compiler';
import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Subscription } from 'rxjs';
import { AuthentificationService } from '../services/authentification.service';

@Component({
  selector: 'app-confirm',
  templateUrl: './confirm.component.html',
  styleUrls: ['./confirm.component.scss']
})
export class ConfirmComponent implements OnInit, OnDestroy {

  token: string;
  confirmed;
  sub1 : Subscription

  constructor(
    private route: ActivatedRoute,
    private authentificationService: AuthentificationService,
  ) { }

  ngOnInit(): void {
    this.sub1 = this.route.queryParams.subscribe(p => {
      this.token = p['token'];
      if (this.token){
        setTimeout(()=>{                         
          this.confirm()
     }, 3000);
      }
    })
  }

  confirm(){
    this.authentificationService.confirm(this.token).subscribe(
      data => {
        this.confirmed = true;
      },
      error => {
        this.confirmed = false;
      });
  }

  ngOnDestroy() {
    this.sub1.unsubscribe();
  }
}
