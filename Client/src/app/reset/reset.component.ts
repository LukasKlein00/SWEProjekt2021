import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthentificationService } from '../services/authentification.service';

@Component({
  selector: 'app-reset',
  templateUrl: './reset.component.html',
  styleUrls: ['./reset.component.scss']
})
export class ResetComponent implements OnInit {
  

  constructor(
    private route: ActivatedRoute,
    private authentificationService: AuthentificationService,
    private router: Router,
  ) { }

  token: string;
  psw: string;
  error;


  ngOnInit(): void {
    
    this.route.queryParams.subscribe(p => {
      this.token = p['token'];
      console.log(p)
    })
  }

  reset() {
    if (this.psw && this.psw.length >= 6) {
      this.authentificationService.confirm(this.token).subscribe(res => {
        this.router.navigateByUrl('');
      });
    } else {
      this.error = "Password is too short"
    }
  }

}
