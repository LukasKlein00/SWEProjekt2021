import { tokenName } from '@angular/compiler';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { AuthentificationService } from '../services/authentification.service';

@Component({
  selector: 'app-confirm',
  templateUrl: './confirm.component.html',
  styleUrls: ['./confirm.component.scss']
})
export class ConfirmComponent implements OnInit {

  token: string;

  constructor(
    private route: ActivatedRoute,
    private authentificationService: AuthentificationService,
  ) { }

  ngOnInit(): void {
    this.route.queryParams.subscribe(p => {
      this.token = p['token'];
      if (this.token){
        confirm()
      }
      console.log(p)
    })
  }

  confirm(){
    this.authentificationService.confirm(this.token).subscribe(res => {
      console.log(res);
    });
  }
}
